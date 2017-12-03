Pattern Definition
==================

Patterns are specified by means of regular expressions
:cite:`Friedl2006mastering`.  The syntax follows a scheme that has been
popularized by the tool 'lex' :cite:`Lesk1975lex`. It includes elements of
*extended POSIX regular expressions* :cite:`Spencer1994regex` and POSIX bracket
expressions. This facilitates the migration from and to other lexical analyzer
generators and test environments.  Additionally, some non-standard commands for
the definition of character sets are provided which access the *Unicode
Properties* database [#f1]_.

.. note::

    In a ``define`` section regular expressions are associated with
    identifiers. These identifiers may then be expanded in other definitions.
    This way, it becomes possible to define larger expressions as a composition
    of smaller regular expressions in a clear fashion. 
    
    The usage of references can be applied to the extend that modes only
    contain references to regular expressions. As a consequence, the
    pattern-action pairs become very readable.  Below, a boxed definition of
    two example patterns ``WHITESPACE`` and ``IDENTIFIER`` displays the idea.
         
    .. code-block:: cpp

        define {
           /* Eating white space                          */
           WHITESPACE    [ \t\n]+
           /* An identifier can never start with a number */
           ID_BEGIN      [_a-zA-Z]
           ID_CONTINUE   [_a-zA-Z0-9]*
           IDENTIFIER    {ID_BEGIN}{ID_CONTINUE}
        }

        mode MINE {
            {WHITESPACE}  { } // do nothing
            {IDENTIFIER}  => QUEX_TKN_IDENTIFIER(Lexeme);
        }

    Following this strict approach supports the separation of *pattern
    definition* and *pattern matching behavior*. 

The following sections describe the syntax for patterns.  First, context free
regular expressions are introduced. Second, two subsequent sections elaborate
on the specification of character sets and the use of queries into the Unicode
database. Third, a section elaborates on pre- and post-contexts for regular
expressions. 

This section purposely excludes the syntax of operations related to *DFA
algebra* and *cut/concatenate arithmetic*. While this chapter focusses on
practical applications the latter two subjects require a broader discussion.
They are separated into a dedicated chapter which sets them into a more
prominent position and facilitates it for the application oriented reader to
skip over them.

.. toctree::
   
    re-context-free.rst
    re-character-sets.rst
    ucs-properties.rst
    re-context-dependent.rst

.. rubric:: Footnotes

.. [#f1] The syntax used follows *Unicode Regular Expressions* (Unicode UTR #18) 
   only partly.

