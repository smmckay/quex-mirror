.. _sec:top-level:

Top Level
=========

There are two types of top level syntax elements: those which *configure
functionality* and others which plainly *paste source code* into locations of
the generated code. 

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
   :reg:`sec:regular-expressions`). A complete description of modes is
   delivered in a chapter :ref:`sec:modes`.

.. data:: define

   The ``define`` keyword is followed by a section in curly brackets.  In this
   section patterns are associated with identifiers, i.e. shorthands. Such
   shorthands may then be used to define other patterns.
     
   .. code-block:: cpp

      define {
          ...
          PATTERN_NAME    pattern-definition
          ...
      }

   Once defined, a pattern may be referenced in ``define`` and ``mode``
   sections by putting the name in curly brackets, such as ``{PATTERN_NAME}``.
   Pattern names, themselves, do not enter any name space of the generated
   source code.  They are only known inside the mode definitions. 

   Regular expressions tend to get lengthy, complex, and hard to read. Being
   able to split them into named sub-patterns is *essential* for the
   readability.  The limited ability of humans to treat complexity
   :cite:`Marois2005capacity` implies that error susceptibility of regular
   expressions increases with their complexity.  Thus, defining meaningful
   sub-patterns is the basis for a robust lexer construction--divide and 
   conquer. 

.. data:: token

   The keyword ``token`` opens a token identifier definition section. It is
   *optional*.  Nevertheless, Quex warns about undefined token-ids in order to
   help to avoid dubious effects of typos, where the analyzer sends token ids
   that no one catches.  The syntax of this section is 

       .. code-block:: cpp

              token {
                  ...
                  TOKEN_NAME_0;
                  TOKEN_NAME_1 = 0x4711;
                  ...
              }
      
      The token identifiers need to be separated by semi-colons. Adding a ``=``
      and a numeric value to the token definition sets a specific value as
      token identifier.  If a token is used but not defined in a token section,
      a warning is issued. The names of the defined token idenfiers enter the
      global namespace with `token prefix` + `name`.

   .. note:: 

      The token identifiers in the token section are specified without prefix.
      The token prefix, is defined by the comand line option
      ``--token-id-prefix``.

.. data:: repeated_token

      The ``repeated_token`` section selects some token ids for the usage of
      efficient token repetition.  Instead of multiple token objects being
      produced, the same token object is sent multiple times until the
      repetition count is achieved.  A practical application of this can be
      considered in indentation based lexical analysis (off-side rule).  There,
      a single less indented line may cause multiple closing scopes. Each
      closed scope is notified by a ``DEDENT`` token. Instead of putting `n`
      ``DEDENT`` tokens into the queue, a single token can now be prepared with
      the repetition count of `n`. The content of the ``repeated_token``
      section are the names of token identifiers which are subject to
      repetition.

      .. code-block:: cpp

              repeated_token {
                  ...
                  TOKEN_NAME;
                  ...
              }

.. data:: token_type

      Quex generates a default token class/struct for the lexical analyzer
      containing a 'text' and a 'number' member. If this is not sufficient,
      customized token classes (C++) or structs (C) may be defined in the
      ``token_type`` section (chapter :ref:`sec:token`).

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
   additional include files or constants may be specified. 

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

   The constructor may return a ``bool`` value indicating the success
   (``true``) or failure (``false``) of the construction. By default, it
   returns ``true``.

.. data:: destructor

   Extensions to the lexer's destructor. This is the place to free or
   de-initialize customized resources.  Also, it is good practice to *mark the
   absence* of resources. This makes it more stable against unintended double-
   destruction. It is also necessary to safely handle ``reset`` and
   ``include_push`` requests.

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

