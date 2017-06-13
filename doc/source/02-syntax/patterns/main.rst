Pattern Definition
==================

Patterns are specified by means of regular expressions
:cite:`Friedl2006mastering`.  The syntax follows a scheme that has been
popularized by the tool 'lex' :cite:`Lesk1975lex`, includes elements of
*extended POSIX regular expressions* :cite:`Spencer1994regex` and POSIX bracket
expressions. This facilitates the migration from and to other lexical analyzer
generators and test environments.  Several additional non-standard 'commands'
access the *Unicode Properties* database to define character sets [#f1]_.

.. note::

    The ``define`` section is a great tool to specify clean regular expressions
    out of smaller ones. Further, it helps to keep mode definitions clean, so
    that pattern action pairs may be expressed by the pattern's name and the
    action. An example may be seen below for the patterns ``WHITESPACE`` and
    ``IDENTIFIER``.
         
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
First, syntactic means to specify context free regular expressions are
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
    summary.rst
   

.. rubric:: Footnotes

.. [#f1] The syntax used follows *Unicode Regular Expressions* (Unicode UTR #18) only partly.

