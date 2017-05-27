.. _sec:top-level:

Top Level
=========

There are two types of top level syntax elements. There are those which
*configure functionality* and others which plainly *paste source code* into
locations of the generated code. 

.. _sec:top-level-configuration:

Configuration
#############

The following item list outlines top-level syntax elements for the configuration
of functionality.

.. data:: mode

   A mode section starts with the keyword ``mode`` and has the following syntax

   .. code-block:: cpp

      mode mode-name : 
           base-mode-1 base-mode-2 ...
           <tag-1> <tag-2> ...
      {
           pattern-1    action-1
           incidence-1  incidence-handler-1
           incidence-2  incidence-handler-2
           ...
           pattern-2    action-2
           pattern-3    action-3
           ...
      }

   The identifier following the ``mode`` keyword names the mode to be
   specified.  Optional base modes and additional options, or 'tags', can be
   specified after a colon. A base mode list consists of a list of one or more
   white space separated names. Optional tags are bracketed in ``<`` and ``>``
   brackets. The section in curly brackets which follows is mandatory. It
   defines pattern-action pairs and incidence handlers. Patterns need to be
   described as regular expressions following the POSIX Standard [#f1] (section
   :reg:`sec:regular-expressions`). Modes in itself are a subject described in
   a dedicated chapter :ref:`sec:modes`.

.. data:: define

   The ``define`` keyword is followed by a section in curly brackets.  In this
   section patterns may be associated with identifiers, i.e. shorthands. Such
   shorthands may then be used to define other patterns.
     

   .. code-block:: cpp

      define {
          ...
          PATTERN_NAME    pattern-definition
          ...
      }

   In ``define`` and ``mode`` sections, specified a pattern defined as ``NAME``
   can be referenced by ``{NAME}``. The pattern names, themselves, do not enter
   any name space of the generated source code.  They are only known inside the
   mode definitions. 

   Regular expressions tend to get lengthy and hard to read. Being able to
   split them into named sub-patterns is *essential* for the readability. As
   any program code, regular expression which are hard to reflect upon are
   likely to show unintended behavior. Thus, defining meaningful sub-patterns
   is the basis for robust lexer construction. 

.. data:: token

   In this section token identifiers can be specified. The definition of token
   identifiers is optional. The fact that Quex warns about undefined token-ids
   helps to avoid dubious effects of typos, where the analyzer sends token ids
   that no one catches.

   The syntax of this section is 

       .. code-block:: cpp

              token {
                  ...
                  TOKEN_NAME_0;
                  TOKEN_NAME_1 = 0x4711;
                  ...
              }
      
      The token identifiers need to be separated by semi-colons. Optional
      assignments may set specific values for tokens. If a token is used but
      not defined in a token section, a warning is issued. 

   .. note:: 

      The token identifier in this section are prefix-less. The token prefix,
      e.g. defined by comand line option ``--token-id-prefix`` is automatically
      pasted in front of the identifier.

.. data:: repeated_token

      Repeated tokens may be send from the lexer efficiently by setting a
      repetion number inside a token, instead of sending a sequence of token
      objects (section :ref:`sec:token-repetition`). The token ids subject
      to this type of repetition must be specified in the ``repeated_token``
      section.

      .. code-block:: cpp

              repeated_token {
                  ...
                  TOKEN_NAME;
                  ...
              }

      Only token identifiers mentioned this section may be sent via implicit
      repetition using ``self_send_n(...)``. That is, inside the token a
      repetition number is stored and the ``receive()`` function keeps
      returning the same token identifier until the repetition number is zero.

.. data:: token_type

      Quex generates a default token class/struct for the lexical analyzer 
      containing a 'text' and a 'number' member. If this is not sufficient,
      customized token classes/structs may be defined in the ``token_type``
      section (chapter :ref:`sec:token`).

.. data:: start

      An initial mode ``START_MODE`` in which the lexical analyzer starts its
      analysis can be specified via 
      
      .. code-block:: cpp
      
         start = START_MODE;

.. _sec:top-level-paste:

Pasting Source Code
###################

Section which define code to be pasted into generated code follow the pattern::

       section-name {
           ...
           section content
           ...
       }

Whatever is contained between the two brackets is pasted in the corresponding location
for the given section-name. The available sections are the following:

.. data:: header

   Content of this section is pasted into the header of the generated files. Here, 
   additional include files may be specified or constants may be specified. 

.. data:: body

   Extensions to the lexical analyzer class definition. This is useful for 
   adding new class members to the analyzers or declaring ``friend``-ship
   relationships to other classes. For example:

   .. code-block:: cpp

        body {
                int         my_counter;
                friend void some_function(MyLexer&);
        }

   defines an additional variable ``my_counter`` and a friend function inside
   the lexer class' body.

.. data:: constructor

   Extensions to the lexer's  constructor. This is the place to initialize the
   additional members mentioned in the ``body`` section. Note, that as in every
   code fragment, the analyzer itself is referred to via the ``self`` variable.
   For example

   .. code-block:: cpp

        constructor {
                self.my_counter = 4711;
        }

   Initializes a self declared member of the analyzer ``my_counter`` to 4711.

   May return a ``bool`` indicating that the initialization succeeded
   (``true``) or failed (``false``). By default, it returns ``true``.

.. data:: destructor

   Extensions to the lexer's destructor. In there, resources may be freed.
   Also, it is good practice to mark absence of resources. The destructor
   may also be used in places, where it is expected that the lexer is made
   safe againt double destruction.

   .. code-block:: cpp

       destructor {
           if( NULL != self.database_fh ) {  // Only close, if fh != NULL 
               fclose(self.database_fh); 
               self.database_fh = NULL;      // Mark fh as closed.        
           }
       }

.. data:: reset

   Section that defines customized behavior upon reset. This fragment is
   executed *after* the reset of the remaining parts of the lexical analyser.
   The analyzer is referred to by ``self``.

Some pattern may trigger a 'stream inclusion'. Inclusion means that the lexer
interrupts the analysis of the current stream and continues with an 'included'
stream.  Once the analysis of the included stream terminates it continues at
the position where it was interrupted in the including file. The storing and
restoring of a lexer's state follows the 'memento pattern'
:cite:`Gamma1994design`.  Upon inclusion a memento is pushed on the inclusion
stack  and upon return a memento is popped. The sections used to configure
customized memento handling upon inclusion and return from inclusion are the
following. Lexer's which are not user-extended do not require any customized
memento handling.

.. data:: memento

   Mementos are stored in objects of a memento class. Extensions to this
   class may be specified in the ``memento`` section. 

.. data:: memento_pack

   Additional code to be executed when the state of a lexical analyzer is
   *stored* in a memento upon inclusion. The code is executed *after* the
   default inclusion handling is performed, right before the memento is pushed
   on the stack.

   Implicit Variables:

   ``memento``:   Pointer to the memento object.

   ``self``:      Reference to the lexical analyzer object.

   ``InputName``: Name of the new data source to be included. 
   
   The ``InputName`` may be a file name or any artificial identifier passed to one of 
   the include-push functions (:ref:`sec:include-stack`).

   Return value:

   The section may return ``true`` if the constructed memento is functional and
   ``false`` if not.  A ``false`` causes an immediate deletion of the memento.
   Then, nothing will be pushed on the stack and the inclusion is aborted.

.. data:: memento_unpack

   Additional code to be executed when the state of a lexical analyzer is
   *restored* from a memento. The code is executed *after* the default return
   from inclusion handling is performed, right before the deletion of the
   memento.

   Implicit Variables:

   ``memento``: Pointer to the memento object.

   ``self``: Reference to the lexical analyzer object.

.. rubric:: Footnotes

.. [#f1] Quex's regular expressions extend the POSIX regular expressions by queries 
         for unicode properties :ref:`sec:re-unicode-properties` and regular expression 
         algebra :ref:`sec:re-algebra`.

