The Anti-Pattern
================

.. describe:: \\A{P}

    The 'anti-pattern' of a pattern ``P`` is the sanitized complement, i.e.
    the result of ``\Sanitize{\Not{P}}``. 
    
The complement operation alone generates patterns with acceptance on the
zero-length lexeme and iterations on arbitrary lexatoms. The sanitization of
the complement delivers a pattern that behaves as follows.  For a given pattern
`P` that matches a set of lexemes `L`, the anti-pattern ``\A{P}`` matches any
lexeme which is not in `L` but is at most one lexatom longer than any lexeme in
`L`.

 .. _fig-anti-pattern-0:

 .. figure:: ../../figures/anti-pattern-0.png

    DFA for the pattern ``"fun"``.

 .. _fig-anti-pattern-1:

 .. figure:: ../../figures/anti-pattern-1.png

    DFA for the anti-pattern of ``"fun"``, i.e. ``\A{"fun"}``.

Figures :ref:`fig-anti-pattern-0` and :ref:`fig-anti-pattern-1` show the
state machines for matching the pattern ``fun`` and ``\A{fun}``. As can be
seen, the anti-pattern does not match all unmatched lexemes of ``fun``.
The implicit ``\Sanitize`` operation ensures that there is no loop on
``\Any`` at an acceptance state. From the complementary set of `L` the
anti-pattern matches only those lexemes which are not more than one
lexatom longer than a correspondent lexeme in `L`.

The anti-pattern operation generates a pattern that is *admissible* and that
has no intersection with the original pattern. However, admissibility 
should not be imposed to early. For example,::

    \Intersection{\A{print} [a-z]+}

will not match against any identifier except ``print``. It will only match
against those which are not ``print`` and no longer than six lexatoms. To 
achieve the probably desired behavior, the sanitization must be applied
explicitly to the final expression.::

    \Sanitize{\Intersection{\Not{print} [a-z]+}}

The concatenation of pattern and anti pattern detects positions in the data
stream where a sequential pattern changes.  Anti patterns in connection with
post-context can express the following schemes:

.. describe:: match until pattern ``\A{P}+/P``

    In connection with post-contexts, anti patterns may used to *match until* a
    specific pattern arrives.  For example, the following mode reads in
    anything until the C-comment delimiter ``*/`` is found.

    .. code:: cpp

            define { DELIMITER "*/" }

            mode COMMENT {
                {DELIMITER}                  => GOUP();   // Return to caller mode
                \A{{DELIMITER}}+/{DELIMITER} => QUEX_TKN_COMMENT_BODY(Lexeme);
            }

.. describe:: match until not pattern ``P+/\A{P}``

    Example: The following mode skips a semi-colon separated list of numbers.

    .. code:: cpp

            define { NUMBER    [0-9]+;[ \t]+ }

            mode COMMENT {
                {NUMBER}+/\A{{NUMBER}} => QUEX_TKN_NUMBERS(Lexeme);
            }

Notably, ``\A{P}+/P`` is not equivalent to ``\A{P}+``. The former requires that
``P`` occurs at the end while the latter does not. In the example with the
C-style comments a ``COMMENT`` token is only sent if the matching ``*/``
appears in the input stream. Respectively, ``P+/\A{P}`` is not equivalent to
``P+``.  In connection with pre-context the following schemes may be expressed:

.. describe:: match upon first pattern ``\A{P}/P/``

    .. code:: cpp

            define {
                NUMBER    [0-9]+;[ \t]+
            }

            mode COMMENT {
                \A{{NUMBER}}/{NUMBER}/ => QUEX_TKN_FIRST_N(Lexeme);
            }

.. describe:: match upon first not pattern ``P/\A{P}/``

        define {
            NUMBER    [0-9]+;[ \t]+
        }

        mode COMMENT {
            {NUMBER}/\A{{NUMBER}}/     => QUEX_TKN_FIRST_NAN(Lexeme);
        }

With a similar discussion as on post-contexts, ``\A{P}/P/`` is not equivalent
to ``P`` and ``P/\A{P}/`` is not equivalent to ``\A{P}``. The pre-contexted
patterns require a *change* in the input patterns.

