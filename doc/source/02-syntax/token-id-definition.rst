.. _sec:token-id-definition:

Token Identifiers
=================

A token identifier is an integer representing the type of lexeme which is
identified at a specific position in the input stream. Token identifiers may be
referred to by named constants, i.e. 'token-ids', or directly with a number or
a character code (section :ref:`mode-actions`). As mentioned earlier, token
identifiers are specified in a ``token`` section such as the following.

.. code:: cpp

    token {
        OP_PLUS; OP_MINUS; OP_DIVISION; OP_MULTIPLICATION;
    }

All token identifiers must have the same prefix. Token ids mentioned in the
``token`` section receive the token prefix automatically. The default prefix is
``QUEX_TKN_``. A customized token id can be specified via the command line
option ``--token-id-prefix`` followed by the desired prefix. This option also
provides a means to place token ids in a specific (C++-) name space.  For
example

   > quex ... --token-id-prefix example::bison::token::

defines a prefix which consist of a name space reference. A call as::

   > quex ... --token-id-prefix example::bison::token::TK_

specifies further that only tokens in the given name space are considered which
start with ``TK_``. Token identifiers which are specified without a numeric
constant is associated automatically with a distinct integer.

Token identifiers do not need to be specified explicitly. Any identifier which
is used in a place where a token identifier is expected is added to the list of
token identifiers.  This facilitates the quick definition of a lexical
analyzer. However, a warning is issued if an undefined token identifier
is used. This is because such a reliance on implicit definitions is error
prone.  Imagine a typo in the description of pattern-action pairs:

.. code-block:: cpp

    ...
           "key"  => QUEX_TKN_KEV;   // typo: KEV instead of KEY
    ...

Assume that the writer of these lines intended to write ``QUEX_TKN_KEY`` and
his code expects the token id to appear upon the detection of ``key``.  With
the code generated from the above fragment, a compiler would compile without
complaints--everything is properly defined. However, the lexer would send
another token id, namely ``QUEX_TKN_KEV`` (with a capital V). The expected
``QUEX_TKN_KEY`` would not be received open the occurrence of ``key``. The
reported warning in such situations is intended to prevent users from long
exhausting debugging sessions on pattern matching behavior.

Numbers can be explicitly assigned to token ids relying on the number
specification scheme shown in section :ref:`sec:basics-number-format`. This
allows for certain tricks. For example, token id groups may be expressed in
terms of a signalling bit. In the following example, the integers associated
with ``DIV``, ``MULTIPLY``, ``PLUS`` and ``MINUS`` are the only ones with 
bit zero being set.

.. code-block:: cpp

   token { 
        TERMINATION   = 0b0000.0000;
        UNINITIALIZED = 0b1000.0000;
        DIV           = 0b0000.0001;
        MULTIPLY      = 0b0001.0001;
        PLUS          = 0b0011.0001;
        MINUS         = 0b0100.0001;
   }

Based on this setup, it is possible to identify operators quickly, such as in
the following C-code fragment.

.. code-block:: cpp

   if( token->id & 0x1 ) {
       // 'token->id' is either DIV, MULTIPLY, PLUS, or MINUS 
       ...
   }

External Token Identifier Definitions
#####################################

Parser generators such as bison :cite:`donnelly2004bison` and  ANTLR
:cite:`parr2013definitive` may provide token identifier defintions themselves.
Assuming that the files are provided in the target language (C or C++), Quex
may scan those files for token identifier names. This is done with the goal to
supervise the consistency of provided token identifiers and their usage.

Quex is not an interpreter for C or C++. So, it may fail to detect numeric
values precisely. In order to avoid total failure, the consideration of numeric
constants is omitted.  Consequently, the ``token`` section may no longer be
used. *All* token ids must be defined in the external file, somewhere. This
includes the implicit token ids for ``TERMINATION`` and ``UNINITIALIZED``. With
indentation handling activated, the token ids for ``INDENT``, ``DEDENT``, and
``NODENT`` must be defined. All token identifiers provided must contain the
appropriate token prefix.  The consistency of numeric values for token ids
remains completely in the hands of whatsoever or whosoever writes the external
token id file.

.. note::

   Quex does undertand C/C++ only to some extend. It tries, for example, to
   dive into included files since it can detect ``#include`` statements.
   However, it does so without any understanding of circumstances such as
   conditional preprocessor statements.

   If Quex really fails to parse external token identifier definitions, the
   file's content must be translated into the content of a ``token`` section.
   The author of this text has never heard of such necessities, though.

On the command line, the external token id file can be specified by the
``--foreign-token-id-file`` option followed by the name of the file.  For
example, if a parser generator creates a token id file called
``my-token-ids.hpp`` the corespondent command line is

.. code-block:: bash

    > quex ... --foreign-token-id-file my-token-ids.hpp 

If the token ids there are specified in the namespace 'token::' and 
all have the prefix ``TK_`` the ``--token-id-prefix`` option must
be used additionally.

.. code-block:: bash

    > quex ... --foreign-token-id-file my-token-ids.hpp \
               --token-id-prefix       token::TK_

In case that a header contains definitions which may be confused with token id
definitions, the region in the file may be specified. This can be done with 
begin and end triggers as in the following example::

    > quex ... --foreign-token-id-file my-token-ids.hpp  yytokentype  '};' 

Then, the scanning of token ids starts with the line where ``yytokentype``
appears and ends with the next occurrence of '};'. In the following 
code fragment, only ``INTEGER`` and ``STRING`` will be considered.

.. code-block:: cpp

    namespace Example {
        namespace BisonicParser  {
            ...
            struct token
            {
                enum yytokentype {
                    INTEGER = 258
                    STRING  = 259
                };
            ...

The command line option ``--foreign-token-id-file-show`` triggers the display
of all token identifiers that have been detected.  When applied to the
aforementioned file, the corespondent output will be

.. code-block:: bash

    note: Token ids found in file 'my-token-ids.hpp' {
    note:     Example::BisonicParser::token::INTEGER => 'INTEGER'
    note:     Example::BisonicParser::token::STRING  => 'STRING'
    note: }

The name space to which the findings are attributed depends on what 
was passed to the option ``--token-id-prefix``. 

