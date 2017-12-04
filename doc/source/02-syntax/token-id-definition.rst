.. _sec:token-id-definition:

Token Identifiers
=================

A token identifier is an integer representing the type of lexeme which matches
a pattern at a specific position in the input stream. Token identifiers may be
referred to by named constants. In the following, the term token identifier, or
'token-ids', stands for both the integer representing the token type and the
token identifier name. Which one is meant shall be clear from the context.

Named constants to be used as token identifiers are specified in a ``token``
section such as the following. 

.. code:: cpp

    token {
        OP_PLUS; OP_MINUS; OP_DIVISION; OP_MULTIPLICATION;
    }

The above fragment defines the token identifiers `QUEX_TKN_OP_PLUS`,
`QUEX_TKN_OP_MINUS`, `QUEX_TKN_OP_DIVISION`, and `QUEX_TKN_MULTIPLICATION`.
Token ids mentioned in the ``token`` section receive the token prefix
automatically. This ensures consistency in the prefix for all tokens. The
default prefix is ``QUEX_TKN_``. A customized token id can be specified via the
command line option ``--token-id-prefix`` followed by the desired prefix. This
option also provides a means to place token ids in a specific (C++-) name
space.  For example::

   > quex ... --token-id-prefix example::bison::token::

defines a prefix which consist of a name space reference. A call such as::

   > quex ... --token-id-prefix example::bison::token::TK_

specifies further that only tokens in the given name space are considered which
start with ``TK_``. 

Token identifiers do not need to be specified explicitly. Any identifier which
is used in a place where a token identifier is expected is added to the list of
token identifiers (provided it starts with the correct prefix).  This
facilitates the quick definition of a lexical analyzer. Nevertheless, a warning
is issued if an undefined token identifier is used. This is because such a
reliance on implicit definitions is error prone.  Assume a users drops a typo
in a pattern-action pair such as the `V` instead of the `Y` in the following
fragment.

.. code-block:: cpp

    ...
    "key"  => QUEX_TKN_KEV;   // typo: KEV instead of KEY
    ...

Assume it was intended to send ``QUEX_TKN_KEY`` and somewhere in the user's
code something expects that particular token id by name. Since, the generated
lexer sends only ``QUEX_TKN_KEV`` (with a `V` instead of `Y`) that expectation
is always failed.  Quex's warning in such situations is intended to prevent
users from long exhausting debugging sessions on pattern matching behavior.

By default each token identifier name is associated with a unique numeric
constant. It is possible, though, to define numeric constants explicitly.
Relying on the number specification syntax as mentioned in
:ref:`sec:basics-number-format` even allows one to do some tricks. For example,
token id groups may be expressed in terms of a signalling bit. In the following
example, the integers associated with ``DIV``, ``MULTIPLY``, ``PLUS`` and
``MINUS`` are the only ones with bit zero being set.

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
*supervise the consistency* of provided token identifiers and their usage. An
external token-id definition file may be passed on the command line 
following the option ``--foreign-token-id-file``.

The parsing of external files is very rudimental and far from a semantic
interpretation. As a result, Quex does not claim to *understand* the numeric
values which are associated with the identifiers. Consequently, the
functionality to generate unique numeric constants for token identifiers cannot
be provided. Since this is an essential feature of the ``token`` section, the
``token`` section itself becomes impossible. The usage of external token
id definition files and the ``token`` section are *mutually exclusive*.

When token ids are defined externally, *all* token ids must be defined in the
external file, somewhere. This includes the implicit token ids for
``TERMINATION`` and ``UNINITIALIZED``. With indentation handling activated, the
token ids for ``INDENT``, ``DEDENT``, and ``NODENT`` must be defined. All token
identifiers provided must contain the appropriate token prefix.  The
consistency of numeric values for token ids remains completely in the hands of
whatsoever or whosoever writes the external token id file.

.. note::

   Quex does try to parse the external file according to the given language
   (``-language C`` or ``--language C++``). It tries, for example, to dive into
   included files since it can detect ``#include`` statements.  However, it
   does so without any understanding of circumstances such as conditional
   preprocessor statements.

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
appears and ends with the next occurrence of '};'. When the aforementioned
command line is applied to a file containing the following code fragment,
then only the token ids ``INTEGER`` and ``STRING`` will be considered.

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
of all token identifiers that have been detected in the given token-id
specification file.  When applied to the aforementioned file, the corespondent
output will be

.. code-block:: bash

    note: Token ids found in file 'my-token-ids.hpp' {
    note:     Example::BisonicParser::token::INTEGER => 'INTEGER'
    note:     Example::BisonicParser::token::STRING  => 'STRING'
    note: }

The name space to which the findings are attributed depends on what 
was passed to the option ``--token-id-prefix``. 

