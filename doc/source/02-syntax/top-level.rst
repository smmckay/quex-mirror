.. _sec:top-level:

Main Sections
=============

On the top level, the syntax is concerned with the subjects: 

    * Behavior of the lexical analyzer defined by modes and patterns.
    * Token identifiers and token definitions.
    * Class definition of the lexical analyzer.
    * Class definition of a memento.

A particular type of sections are those that consist of solely of user
code to be pasted into the generated code. Such sections are marked in the
following by::

       section-name {
           (user code)
       }

Where ``section-name`` represent the describe section name.

.. _sec:top-level-configuration:

Behavior
########

The key sections to describe a lexer's behavior are ``start``,  ``mode``, and
``define``. These elements are described below.

.. data:: start = mode_name;

   Defines a mode with name ``mode_name`` as initial mode. Whenever the lexer
   starts the first time, includes another file, or resets, this mode is 
   setup.

.. data:: mode

   This keyword opens a section to define a lexer mode.  The precise syntax of
   a mode is defined in a dedicated chapter (namely :ref:`sec:modes`). The
   following fragment provides a rough impression.

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
   :reg:`sec:regular-expressions`). 

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
   sub-patterns is the basis for a robust lexer construction. Divide and 
   conquer! 

Token
#####

The token, is the essential output of lexical analysis. The following keywords
allow one to model the token class and the token identifiers.

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
   and a numeric value (:ref:`sec:basics-number-format:`) to the token
   definition sets a specific value as token identifier. Token identifiers
   enter the global namespace of the generated code as 'token prefix' + 'name'.
   The default token prefix is ``QUEX_TKN_``.  More on token identifiers is
   delivered in section :ref:`sec:token-id-definition`.

   .. note:: 

      Token identifiers in the ``token`` section are specified without prefix.
      By default the prefix is ``QUEX_TKN_``. It can be adapted with the
      command line option ``--token-id-prefix``.

.. data:: repeated_token

   The ``repeated_token`` section selects some token ids for the usage of
   efficient token repetition.  Instead of multiple token objects being
   produced, the same token object is sent multiple times until the repetition
   count is achieved.  A practical application of this can be considered in
   indentation based lexical analysis :ref:`sec-indentation` (off-side rule).
   There, a single less indented line may cause multiple closing scopes. Each
   closed scope is notified by a ``DEDENT`` token. Instead of putting `n`
   ``DEDENT`` tokens into the queue, a single token can now be prepared with
   the repetition count of `n`. The content of the ``repeated_token`` section
   are the names of token identifiers which are subject to repetition.

   .. code-block:: cpp

         repeated_token {
                  ...
                  TOKEN_NAME;
                  ...
         }

.. data:: token_type

   Quex generates a default token class or struct for the lexical analyzer
   containing a 'text' and a 'number' member. If this is not sufficient,
   customized token classes or structs may be defined in the ``token_type``
   section (chapter :ref:`sec:token`).

Additionally, an external token identifier file can be specified on the 
command line using the option ``--external-token-id-file``. An external
token class can be specified by ``--external-token-class``.


.. _sec:top-level-paste:

Lexer Class
###########

Whatever is contained between the two brackets is pasted in the corresponding location
for the given section-name. The available sections are the following:

.. data:: header { (user code) }

   Content of this section is pasted into the header of the generated files. Here, 
   additional include files or constants may be specified. 

.. data:: body { (user code) }

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

.. data:: constructor { (user code) }

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

.. data:: destructor { (user code) }

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

.. data:: reset { (user code) }

   Section that defines customized behavior upon reset. This fragment is
   executed *after* the reset of the remaining parts of the lexical analyser.
   The analyzer is referred to by ``self``.


Memento Class
#############

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

.. data:: memento { (user code) }

   Content of this section is pasted into the definition of the generated
   memento class. The user may have defined customized extra data in the lexer
   class (in the ``body`` section). If this data shall survive stream inclusion
   and return from stream inclusion, it should be specified accordingly in this
   section.

.. data:: memento_pack { (user code) }

   This section contains code to be executed when the state of a lexical
   analyzer is *stored* in a memento upon inclusion. The code is executed
   *after* the default inclusion handling is performed, right before the
   memento is pushed on the stack.

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

.. data:: memento_unpack { (user code) }

   Code from this section is executed when the state of a lexical analyzer is
   *restored* from a memento. The code is executed *after* the default return
   from inclusion handling is performed, right before the deletion of the
   memento.

   Implicit Variables:

   ``memento``: Pointer to the memento object.

   ``self``: Reference to the lexical analyzer object.

.. rubric:: Footnotes

.. [#f1] Quex's regular expressions extend the POSIX regular expressions by queries 
         for unicode properties :ref:`sec:re-unicode-properties` and regular expression 
         algebra :ref:`sec:pattern`.

