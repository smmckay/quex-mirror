.. _sec:algebra-of-dfas:

Algebra of DFAs
===============

Quex introduces an 'Algebra of DFAs'. That is, there is a set of operations on
state machines and properties that is equivalent to the algebra of sets.  In
fact, the operations on DFAs directly correspond to set operations in the *set
of lexemes* which they match. For example, the union of two DFAs is defined as
an operation that produces a DFA which matches the union of the lexemes which
are matched by the two operand DFAs.  Let the regular expressions P and Q be
defined as below::

       P    [0-9]
       Q    fred

That is, P matches the lexemes "0", "1", "2", ... "9" and Q matches "fred".  In
the space of lexemes the union between the two sets is::

    "0", "1", "2", ... "9", "fred"

The patterns for 'P' and 'Q' can be combined using the already discussed union
operator ``|`` as ``[0-9]|fred``. The same principle of correspondence between
DFA operations and operations on the matching lexemes is implemented for
intersection and complement as well as all derived operations. The result is a
set of operations that shows a symmetric structure and enables a calculus on
DFAs.  The *fundamental operations* are available via the commands:

.. describe:: \\Union{X0 X1 ... Xn}

   matches the *union* of the what is matched by the regular expressions ``X0``,
   ``X1``, ... ``Xn``.

.. describe:: \\Intersection{X0 X1 ... Xn}

   matches the *intersection* of the what is matched by the regular expressions
   ``X0``, ``X1``, ... ``Xn``.

.. describe:: \\Not{X}

   matches the *complementary* set of lexemes of what is matched by the regular
   expressions ``X``.

For the union operation the state machines are setup in parallel. The result of
an intersection is a state machine, that contains only those paths to
acceptance which are present in all operands.  The complementary operation
develops a state machine that matches precisely anything but what is given as
its operand. 

The set of all lexemes, the *universal set*, and the *empty set* of lexemes
find the counterpart in the space of DFAs in the *universally matching DFA* and
the *unmatching DFA* given by:

.. describe:: \\Universal 
   
    matches any lexatom sequence.

.. describe:: \\Empty

    matches no lexeme at all, not even the zero-length lexeme. 

The patterns ``\Empty`` and ``\Universal`` are symmetric with respect to the 
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

The properties and operations constitute a structure that implements all laws
from the algebra of sets, as there are the fundamental laws:

.. describe:: Communativity
    
    .. code:: tex

        \Union{A B}        = \Union{B A}
        \Intersection{A B} = \Intersection{B A}

.. describe:: Associativity

    .. code:: tex

        \Union{\Union{A B} C}               = \Union{A \Union{B C}}
        \Intersection{\Intersection{A B} C} = \Intersection{A \Intersection{B C}}

.. describe:: Distributivity

    .. code:: tex

       \Union{A \Intersection{B C}} = \Intersection{\Union{A B} \Union{A C}}
       \Intersection{A \Union{B C}} = \Union{\Intersection{A B} \Intersection{A C}}

Union and intersection of a given pattern `A` with 'Empty' and the 'Universal' obey
the *identity* and the *complement laws*.


    .. code:: tex

       \Union{A \Empty}            = A
       \Intersection{A \Universal} = A
       \Union{A \Not{A}}           = \Universal
       \Intersection{A \Not{A}}    = \Empty

All of the above laws follow the principle of *symmetric duality*, in that if
``\Union`` and ``\Intersection`` as well as ``\Empty`` and ``\Universal`` are
interchanged, one set of rules translates into another.

Derived Matching Operations
===========================

Based on the fundamental algebraic operations further operations may be derived
which have a specific application in lexical analysis. The following list shows
operations that prune the space of matched lexemes by a pattern `P` by
constraints on the lexeme's beginning or ending. The functions ``\NotBegin``
and ``\NotEnd`` are defined as follows.

.. describe:: ``\NotBegin{P Q}``: 

      All lexemes that match `P`, except for those that *begin* with something
      that matches `Q`.  The corresponding regular expression is::

          \Diff{P (\Universal)Q}  

.. describe:: ``\NotEnd{P Q}`` 

      All lexemes that match `P`, except for those that *end* with something
      that matches `Q`.  The corresponding regular expression is::

          \Diff{P (\Universal)Q}  

.. describe:: ``\NotIn{P Q}`` 

      All lexemes that match `P`, except for those that *contain* a subsequence 
      that matches `Q`.  The corresponding regular expression is::

          \Diff{P (\Universal)Q(\Universal)}  


The possitive cases are:

.. describe:: ``\Begin{P Q}``: 

      Only those lexemes that match `P` which *begin* with something
      that matches `Q`.  The corresponding regular expression is::

          \Intersection{P (\Universal)Q}  

.. describe:: ``\End{P Q}`` 

      Only those lexemes that match `P` which *end* with something
      that matches `Q`.  The corresponding regular expression is::

          \Intersection{P (\Universal)Q}  

.. describe:: ``\In{P Q}`` 

      Only lexemes that match `P` which *contain* a subsequence 
      that matches `Q`.  The corresponding regular expression is::

          \Intersection{P (\Universal)Q(\Universal)}  

While ``\Diff`` and ``\Intersection`` proved above to produce meaningful
operations, no meaningful according operation based on ``\Union`` is known to
to the author Quex. Consequently, no shorthand for such operations exists.

Algebraic expressions may *prune the set of matching lexemes*. However, they
*may not produce sets of pruned lexemes*. For example, for given string
patterns such as `Mr. Bone` it is not possible to find an generic algebraic
expression that cuts the characters `Mr.` from the front so that only the last
name is matched. In order to prune the lexemes at the beginning or the end the
following functions may be used.

.. describe:: \\CutBegin{P Q}

   Matches the set of lexemes:
   
   * lexemes matched by `P` which *do not start* with something that matches `Q`. 

   * the 'tail' of lexemes matched by `P` which start with something `Q`. The
     'tail' of a lexeme is what comes after what is matched by `Q`.
   
   For example, let `P` be defined as `("Mr. "|"Mrs. ")"Bone"` which matches
   `Mr. Bone` and `Mrs. Bone`. Then, the pruned pattern `\\CutBegin{{P} "Mr. "}
   matches `Bone` and `Mrs. Bone`.

.. describe:: \\CutEnd{P Q}

   Matches the set of lexemes:
   
   * lexemes matched by `P` which *do not end* with something that matches `Q`. 

   * the 'head' of lexemes matched by `P` which end with something `Q`. The
     'head' of a lexeme is what comes before what is matched by `Q`.

   With `P` defined as `("Mr. "|"Mrs. ")"Bone"` the resulting pattern of
   `\\CutEnd{{P} " Bone"} matches `Mr.` and `Mrs.`.

.. describe:: \\CutIn{P Q}

   Matches the set of lexemes:

   * lexemes matched by `P` which *do not contain* with something that matches
     `Q`. 

   * the 'tail' and 'head' of lexemes matched by `P` which contain something
     matching `Q`.  The 'tail' and 'head' of a lexeme are the borders around
     what is matched by `Q` inside the pattern.

   With `P` defined as `"car(pet)?"` matching `car` and `carpet`. Then, 
   `\\CutIn{{P} "rpe"} matches `car`  and `cat``.


.. note::

   The operations ``\CutBegin{P Q}``, ``\CutEnd{P Q}``, and ``\CutEnd{P Q}``
   ensure that the resulting pattern does not begin, end or contain the second
   pattern.  Since, the cut-out expression may contain the pattern ``Q`` again,
   these operations iterate. Consequently, the following equivalences hold::

        \CutBegin{P Q}  = \CutBegin{P Q+}
        \CutEnd{P Q}    = \CutEnd{P Q+}
        \CutIn{P Q}     = \CutIn{P Q+}

   This is, cutting a pattern ``Q`` is equivalent to cutting ``Q+``.

The equivalence of pruning ``Q`` and pruning ``Q+`` is not an arbitrary design
decision. While it may be intuitive to make the pruning operations the inverse
of the concatenation, it must be stated that there is no general solution to
the inverse of concatenation! If a lexeme of ``Q`` appended by the begin of a
lexeme of ``P`` is again a lexeme of ``Q``, then it is impossible to separate
``Q`` out of the concatenation ``QP``.  For example, let ``Q`` be ``ab|abcd``.
Then, let ``P`` be ``cd|zz``.  The concatenation ``QP`` namely
``(ab|abcd)(cd|zz)`` is equivalent to ``abcd|abzz|abcdcd|abcdzz``.  In order to
reverse the concatenation, the ``ab`` must be cut from ``abcd`` but ``abcd``
must be cut from ``abcdcd`` and ``abcdzz``. Paths in DFAs are indifferent.
There is no way to derive such a behavior logically. Thus, the inverse
operation of concatenation is impossible for the general case.

.. note::

   Cutting *does not undo* concatenation! From the previous rule, it follows
   that cutting operations prune potentially more than what has been
   concatenated.  The same holds for ``\CutEnd``, i.e.
        
        \CutBegin{QP Q} does not match necessarily a subset of ``P``.

        \CutEnd{PQ Q} does not match necessarily a subset of ``P``.

Cutting at the beginning, however prevents match interference. Similar 
statements can be made for ``\CutEnd`` and ``\CutIn`` as summarized below.

      \Intersection{\CutBegin{P Q} Q} = \Empty
      \Intersection{\CutEnd{P Q}   (\Universal)Q} = \Empty
      \Intersection{\CutIn{P Q}    (\Universal)Q(\Universal)} = \Empty

The operations ``\CutBegin`` and ``\CutEnd`` are related through the following
relationship::

      \CutEnd   = \R{\CutBegin{\R{P} \R{Q}}}
      \CutBegin = \R{\CutEnd{\R{P}   \R{Q}}}

Figure :ref:`fig:cut-in` displays the effect of the ``\CutIn`` operation
applied on the pattern ``"fun"|"for"|"sun"`` cut by ``"o"|"un"``. No path
matching containing an ``"o"`` or ``"un"`` is left in the result.

.. describe:: \\LeaveBegin{P Q}

   Matches the 'head' of lexemes of `P`, where the 'head' is the beginning
   of the lexeme that matches Q.
   
   For example, let `P` be defined as `("Mr. "|"Mrs. ")"Bone"` which matches
   `Mr. Bone` and `Mrs. Bone`. Then, `\\LeaveBegin{{P} "Mr."|"Mrs."}`
   matches `Mr.` and `Mrs`.

.. describe:: \\LeaveEnd{P Q}

   Matches the 'tail' of lexemes of `P`, where the 'tail' is the end 
   of the lexeme that matches Q.
   
   With `P` defined as `("Mr. "|"Mrs. ")"Bone"` the expression
   `\\LeaveEnd{{P} "Bone"} matches `Bone`.

.. describe:: \\LeaveIn{P Q}

   Matches the 'stomach' of lexemes of `P`, where the 'stomach' is the part 
   of the lexeme that matches Q.

   With `P` defined as `"carpenter"` the result of `\\LeaveIn{{P} "pent"}
   matches `pent`.

Figure :ref:`fig:leave-in` displays the effect of the ``\LeaveIn`` operation
applied on the pattern ``"fun"|"for"|"sun"`` leave by ``"o"|"un"``. No path
matching containing an ``"o"`` or ``"un"`` is left in the result. The
operations seem to be trivial enough to perform manually. However, consider the
case where general DNA patterns given by ``[ATD]+`` are to be matched that do
not contain a certain sequence ``"ATAT"`` as shown in Figure
:ref:`fig-dna-cut-in`. The ``CutIn`` operation results in a massively 
modified state machine.

