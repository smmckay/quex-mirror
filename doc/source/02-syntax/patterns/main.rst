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
    identifiers. These identifiers may then be used in other regular
    expressions by embracing them in curly brackets. This way, it becomes
    possible to define larger expressions as a composition of smaller regular
    expressions in a clear fashion. 
    
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

    In general terms, the ``define`` section supports the separation of
    *pattern definitions* and *pattern matching behavior*. 

The following sections describe the formal language used to specify patterns.
First, the syntactic means to specify context free regular expressions are
introduced. Second, two sections elaborate on the specification of character
sets and the use of queries into the Unicode database. Third, a section
elaborates on pre- and post-contexts for regular expressions. Eventually, a
final section introduces *regular expression algebra*. 

.. toctree::
   
    re-context-free.rst
    re-character-sets.rst
    ucs-properties.rst
    re-context-dependent.rst
    re-algebra.rst
    match-filtering.rst
    re-cut.rst
    self-repetitiveness.rst
    anti-pattern.rst
    re-other-operations.rst
    summary.rst
   

.. rubric:: Footnotes

.. [#f1] The syntax used follows *Unicode Regular Expressions* (Unicode UTR #18) 
   only partly.

