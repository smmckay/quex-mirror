.. _sec:sub-dfa-computation:

Cut Operations
==============

Algebraic expressions may *prune the set of matching lexemes*. However, they
*may not produce sets of pruned lexemes*. For example, for string patterns such
as `Mr. Bone` it is not possible to find an generic algebraic expression that
cuts the characters `Mr.` from the front so that only the last name is matched.
In order to prune the lexemes at the beginning or the end the following
functions may be used.

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

TODO: \Nothing is the neutral element with respect to the 'cut' operation.
      \CutBegin{P \Nothing} = P
      \CutIn{P \Nothing} = P
      \CutEnd{P \Nothing} = P

      \Empty is for cutting what '0' is for division.

Cutting may produce 'insane' patterns, that need to be sanitized, 
``\CutBegin{otto|fritz otto}`` produces something that matches '\Nothing'
and '"fritz"'. It 

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


