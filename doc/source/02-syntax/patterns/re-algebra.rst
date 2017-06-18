Algebra of DFAs
===============

Quex introduces an 'Algebra of DFAs'. That is, there is a set of operations on
state machines and properties that is equivalent to the algebra of sets.  In
fact, the operations involved are designed to match set operations in the *set
of lexemes*. Each DFA matches a distinct set of lexemes. Operations of union,
intersection, complement, etc. are developed so that the according set
operations in the space of lexemes match. The result is a set of operations
that shows a symmetric structure and enables a calculus on DFAs. The following
shows the example of the union operation.  Let the regular expressions P and
Q be defined as below::

       P    [0-9]
       Q    fred

That is, P matches the lexemes "0", "1", "2", ... "9" and Q matches "fred".  In
the space of lexemes the union between the two sets is::

    "0", "1", "2", ... "9", "fred"

The patterns for 'P' and 'Q' can be combined using the already discussed union
operator ``|`` as ``[0-9]|fred``. However, there is more to come.  All
*fundamental operations* are available via the commands:

.. describe:: \\Union{X0 X1 ... Xn}

   matches the *union* of the what is matched by the regular expressions ``X0``,
   ``X1``, ... ``Xn``.

.. describe:: \\Intersection{X0 X1 ... Xn}

   matches the *intersection* of the what is matched by the regular expressions
   ``X0``, ``X1``, ... ``Xn``.

.. describe:: \\Not{X}

   matches the *complementary* set of lexemes of what is matched by the regular
   expressions ``X``.

For the union operation the according state machines are setup in parallel. The
result of an intersection is a state machine, that contains only those paths to
acceptance which are present in all operands.  The complementary operation 
develops a state machine that matches precisely anything but what is given
as argument. 

The set of all lexemes, the *universal set*, and the *empty set* of lexemes
find the counterpart in the space of DFAs in the *universally matching DFA* and
the *unmatching DFA* given by:

.. '\\Universal': matches any lexatom sequence.

.. '\\Empty': matches no lexeme at all, not even the zero-length lexeme. 

The patterns ``Empty`` and ``Universal`` are symmetric with respect to the 
complement operation, i.e. ``\Not{\Empty}`` is equivalent to ``\Universal``
and vice versa. Both are important elements of the algebraic structure.
Derived from the fundamental operators are the operators for *difference*
and *symmetric difference*, i.e.

.. describe:: \\Diff{A B}

   matches all lexemes matched by 'A' except for those which are matched 
   also by 'B'.

.. describe:: \\SymDiff{A B}

   matches all lexemes that are matched *either* by 'A' or by 'B' but 
   not by both.

The given set of properties and operations constitute a structure that
implements all laws from the algebra of sets, as there are the fundamental
laws:

.. describe:: Communativity
    
    .* \Union{A B}        = \Union{B A}
    .* \Intersection{A B} = \Intersection{B A}

.. describe:: Associativity

    .* \Union{\Union{A B} C}               = \Union{A \Union{B C}}
    .* \Intersection{\Intersection{A B} C} = \Intersection{A \Intersection{B C}}

.. describe:: Distributivity

    .* \Union{A \Intersection{B C}} = \Intersection{\Union{A B} \Union{A C}}
    .* \Intersection{A \Union{B C}} = \Union{\Intersection{A B} \Intersection{A C}}

Union and intersection of a given pattern `A` with 'Empty' and the 'Universal' obey
the *identity* and the *complement laws*:

    .* \Union{A \Empty}            = A
    .* \Intersection{A \Universal} = A
    .* \Union{A \Not{A}}           = \Universal
    .* \Intersection{A \Not{A}}    = \Empty

All of the above laws follow the principle of *symmetric duality*, in that if
``\Union`` and ``\Intersection`` as well as ``\Empty`` and ``\Universal`` are
interchanged, one set of rules translates into another.

The Anti-Pattern
================

.. describe:: \\A{P}

    The 'anti-pattern' of a pattern ``P`` is the sanitized complement, i.e.
    the result of ``\Sanitize{\Not{P}}``. 
    
The complement operation alone generate patterns with acceptance on the
zero-length lexeme and iterations on arbitrary lexatoms. The sanitization of
the complement delivers a pattern that behaves as follows.  For a given pattern
`P` that matches a set of lexemes `L`, the anti-pattern ``\A{P}`` matches any
lexeme which is not in `L` but is at most one lexatom longer than any lexeme in
`L`.

 .. _fig-anti-pattern-0:

 .. figure:: ../../figures/anti-pattern-0.png

    DFA matching the pattern ``for``.

 .. _fig-anti-pattern-1:

 .. figure:: ../../figures/anti-pattern-1.png

    DFA implementing the match of pattern ``\A{for}``.

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

Anti patterns in connection with post-context can express the following
schemes:

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
