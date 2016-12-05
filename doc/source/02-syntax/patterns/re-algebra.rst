Algebra of DFAs
===============

Quex implements an 'Algebra of DFAs'. That is, there is a set of operations on
state machines and properties that is equivalent to th algebra of sets.  In
fact, the operations involved are designed to match set operations in the *set
of lexemes*. Each DFA matches a distinct set of lexemes. Operations of union,
intersection, complement, etc. are developped so that the according set
operations in the space of lexemes match. The result is a set of operations
that shows a symetric structure and allows a calculus on DFAs. The following
shows the example of the 'union' operation.  Let the regular expressions P and
Q be defined as below::

       P    [0-9]
       Q    [a-z]

That is, P matches the lexemes::

    "0", "1", "2", ... "9"

and Q matches lexemes following the pattern::

    "a", "b", "c", ... "z"

In the space of lexemes the union between the two sets is::

    "0", "1", "2", ... "9", "a", "b", "c", ... "z"

The 'union' operator on DFAs delivers a state machine that corresponds to::

    [0-9a-z]

The fundamental operations are available in Quex via the commands:

.. describe:: \\Union{X0 X1 ... Xn}

   matches the *union* of the what is matched by the regular expressions ``X0``,
   ``X1``, ... ``Xn``.

.. describe:: \\Intersection{X0 X1 ... Xn}

   matches the *intersection* of the what is matched by the regular expressions
   ``X0``, ``X1``, ... ``Xn``.

.. describe:: \\Not{X}

   matches the *complementary* set of lexemes of what is matched by the regular
   expressions ``X``.

The union operation is identical to what the ``|`` operator does. The according
state machines are setup in parallel. The result of an intersection is a state
machine, that contains only those paths to acceptance which are present in all
operands.  Resulting configurations may :

The set of all lexemes, the *universal set*, and the *empty set* of lexemes
find the counterpart in the space of DFAs in the *universally matching DFA* and
the *unmatching DFA* given by:

.. '\\Universal': matches any lexatom sequence.

.. '\\Empty': matches no lexeme at all, not even the zero-length lexeme. 

The patterns ``Empty`` and ``Universal`` are symmetric with respect to the 
complement operation, i.e. ``\Not{\Empty}`` is equivalent to ``\Universal``
and vice versa. Both are important elements of the algebraic structure.
Derived from the fundamental operators are the operators for difference
and symmetric difference, i.e.

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
    
    .* \Union{A B} = \Union{B A}
    .* \Intersection{A B} = \Intersection{B A}

.. describe:: Associativity

    .* \Union{\Union{A B} C} = \Union{A \Union{B C}}
    .* \Intersection{\Intersection{A B} C} = \Intersection{A \Intersection{B C}}

.. describe:: Distributivity

    .* \Union{A \Intersection{B C}} = \Intersection{\Union{A B} \Union{A C}}
    .* \Intersection{A \Union{B C}} = \Union{\Intersection{A B} \Intersection{A C}}

Union and intersection with 'Empty' and the 'Universal' DFAs a given DFA obey
the identity and the complement laws:

    .* \Union{A \Empty} = A
    .* \Intersection{A \Universal} = A
    .* \Union{A \Not{A}} = \Universal
    .* \Intersection{A \Not{A}} = \Empty

All of the above laws follow the principle of symmetric duality, in that if
``\Union`` and ``\Intersection`` as well as ``\Empty`` and ``\Universal`` are
interchanged, one set of rules translates into another.

    .* \Intersection{A \Universal} = A

.. describe:: Unary Operations (short 'U').

.. describe:: Binary Operations (short 'B').

Unary operations take only one argument. Binary operations take at least two.
Another categorization is

.. describe:: Set Operations (short 'S').

.. describe:: Transformations (short 'T').

Set operations do not change or modify lexemes in the related lexeme sets.
They can be considered in terms of additions or deletions of complete lexemes.
A Transformations produce regular expressions that match new lexemes.  As
indicated in the descriptions the letters 'U', 'B', 'S' and 'L' shall indicate
the operator categories.  Following are the regular expression operators.

.. describe:: \\R{ P } -- Reverse (UT)

   Matches the reverse of what P matches.  For any lexeme Lp = { x0, x1, ...
   xn } which matches P, there is a reverse lexeme Lrp = { xn, ...  x1, x0 }
   which matches \\R{ P }. Examples:

.. describe:: \\Not{ P } -- Complement (UT)

   Matches anything that P does not match.  Any lexeme Lnp = { x0, x1, ...  xn }
   which is not matched by P is matched by \\Not{ P }.

.. describe:: \\Sequence{ P Q } -- Sequentialize (BT)

   Matches the concatination of P and Q. For any to lexemes Lp = { x0, x1, ... xn }
   matched by P and Lq = { y1, y2, ... ym } matched by Q, any lexeme 
   matched by \\Sequence{ P Q } consists of a lexeme from Lp followed by
   a lexeme from Lq.

   This operator is an explicit implementation of ``PQ`` which does
   exactly the same.

.. describe:: \\CutBegin{ P Q } -- Cut Beginning (BL)

   Prune P in front, so that ``\CutBegin{ P Q }`` starts right after what Q 
   would match. 

   Example::

              \CutBegin{"otto_mueller" "otto"} --> "_mueller"

.. note:: 

     ``\CutBegin`` cuts only *one appearance* of a lexeme from Q *at the
     beginning* of P; but it does not mean that the result cannot match a
     lexeme starting with a lexeme from Q. Let P match Lp = {xx, xy} while Q
     matches Lq = {x}, then ``\CutBegin{P Q}`` only cuts the first appearance
     of 'x' and the resulting set of lexemes is {x, y}. It contains 'x'
     which is a lexeme matched by Q.

.. note::

     When dealing with repeated expressions the rules of ``\CutBegin``
     may surprise at the first glance. Consider for example::

           \CutBegin{[0-9]+ 0}
    
     which only cuts out the first occurence of 0.  There is an infinite number
     of lexemes in ``[0-9]+`` having '0' as second character--which becomes now
     the first. Thus the above expression is equivalent to ``[0-9]+`` itself.  To
     delete ``0`` totally from ``[0-9]+`` it is necessary to write::

           \CutBegin{[0-9]+ 0+}



.. describe:: \\CutEnd{ P Q } -- Cut End (BL)

   Prune P at back, so that \\CutEnd{ P Q } ends right before Q would match. 
   Example::

              \CutEnd{"otto_mueller" "mueller"} --> "otto_"

.. describe:: \\Union{ P Q } -- Union (BS)

   Matches all lexemes which are matched by P and all lexemes which are
   matched by Q.

.. describe:: \\Intersection{ P Q } -- Intersection (BS)

   Matches only those lexemes which are matched by both P and Q.

.. describe:: \\NotBegin{ P Q } -- Complement Begin (BS)

   Matches those lexemes of P which do not start with lexemes that
   match Q.

.. describe:: \\NotEnd{ P Q } -- Complement End (BS)

   Matches those lexemes of P which do not end with lexemes that
   match Q.

.. describe:: \\NotIn{ P Q } -- Complement End (BS)

   Matches those lexemes of P which do not contain lexemes that
   match Q.

-----------------------

.. describe:: \\Sanitize{P}

     Sanitizes a pattern with regards to two issues. First, it removes
     acceptance of the zero-length lexeme. Second, it removes acceptance of
     tails of infinite length and arbirtrary lexatoms. Such patterns may indeed
     be produced by DFA algrebraic expressions--so this command helps to
     sanitize.

     The command line option ``--language dot`` allows to print state machine
     graphs. It is advisable to print graphs for the sanitized state machine
     in order to see whether it conforms the expectations.

     Notably, this command cannot sanitize patterns that do not accept anything
     or accept everything as discussed in the frame of DFA algebra.

.. describe:: \\A{P}

    The 'anti-pattern' is a short form of a sanitized complement, i.e.
    ``\Sanitize{\Not{P}}``. The complement operation on normal may generate
    acceptance on the zero-length lexeme and iterations on arbitrary lexatoms.

    For a given stream of lexatoms the anti-pattern ``\A{P}`` matches the
    shortest lexeme that is longer than the longest lexeme matched by ``P``.

      .# The 


    the shortest lexeme that does not match ``P`` but which is longer than any matched lexeme of ``P`` but
    is not matched

    anti-pattern of a pattern ``P`` matches all lexemes which are caught by a
    match failure of ``P``. 

     Let `L` be the set of lexemes that matches `P`. Let s(L) be a
     transformation which extracts out 'shortest' alternatives.  Let Lx be the
     set of *x* from L for which there is a second lexeme *y* in L that starts
     with *x*. Then,::

                                 s(L) := L - Lx 
     
     As a result it is safe to assume that in s(L) there are no two lexemes
     *x* and *y* so that *x* is the start of *y*. For example, the pattern 
     '(ab)|(abc)' is matched by "ab" and "abc". The latter starts with the
     former. The transformation s((ab)|(abc)) takes out the longest 
     and matches therefore only "ab".

     Anti-Pattern
        Let Q be the set of all lexemes which are not matched by P. Let
        s(R) be the pattern that matches shortest alternatives in R. Then, the
        anti-pattern of P is the pattern which matches the set of lexemes
        given by 's(Q)'.

     .. _fig-anti-pattern-0:
 
     .. figure:: ../../figures/anti-pattern-0.png
 
        State machine matching the pattern ``for``.
 
     .. _fig-anti-pattern-1:
 
     .. figure:: ../../figures/anti-pattern-1.png
 
        State machine implementing the match of pattern ``\A{for}``.

     Figures :ref:`fig-anti-pattern-0` and :ref:`fig-anti-pattern-1` show the 
     state machines for matching the pattern ``for`` and ``\A{for}``. These 
     illustrations demonstrate that the anti-pattern does not match all 
     patterns which are not matched by ``for``. Instead, it matches a 
     'shortest subset'.
   
     Anti-patterns are especially useful for post contexts 
     (section :ref:`sec-pre-and-post-conditions`) and to implement shortest 
     match behavior with a greedy match analyzer engine 
     (section :ref:`usage-context-free-pitfalls`).

     .. note::

        If it is necessary to ensure that only one character is matched in 
        case of failure of all other patterns, then it is best to rely on the
        '.' specifier--as explained above.
