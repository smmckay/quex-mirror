.. _sec:sub-dfa-computation:

Cut/Concetenate Arithmetic
==========================

Algebraic expressions may *prune the set* of matching lexemes. However, they
may not produce *sets of pruned lexemes*. This section produces DFA that
actually prune lexemes which are matched by a DFA. Subsets of lexemes are then
specified in which the concatenation operation can be inverted. Finally, 
a arithmetic frame is introduced ... TODO.

Cut operations to be introduced are the following:

.. describe:: \\CutBegin{P Q}

   Matches the set of lexemes:
   
   * lexemes matched by `P` which *do not start* with something that matches `Q`. 

   * the 'tail' of lexemes matched by `P` which start with something `Q`. The
     'tail' of a lexeme is what comes after what is matched by `Q`.
   
.. describe:: \\CutEnd{P Q}

   Matches the set of lexemes:
   
   * lexemes matched by `P` which *do not end* with something that matches `Q`. 

   * the 'head' of lexemes matched by `P` which end with something `Q`. The
     'head' of a lexeme is what comes before what is matched by `Q`.

The precise operation of these functions becomes clearer when seen in contrast
to set-pruning operations. For example, the set-pruning operation ``\NotBegin``
and the lexeme-pruning operation ``\CutBegin`` applied on the expressions
``friedhelm|otto`` and ``fried`` deliver the following::

    \NotBegin{friedhelm|otto fried}  -> "otto"
    \CutBegin{friedhelm|otto fried}  -> "helm", "otto"

The expression ``friedhelm|otto`` matches two lexemes namely "friedhelm" and
"otto". The ``\NotBegin`` operation removes any lexeme that starts with
``fried``, so that "friedhelm" is completely taken out. The ``CutBegin``
operation, however, cuts "fried" from the beginning of "friedhelm". What
remains is the lexeme "helm". The lexeme "otto" is not effected, since it does
not start with "fried".

*Neutral Element*

There is a neutral element with respect to ``\CutBegin`` and ``\CutEnd`` is
the ``\Nothing`` DFA. That is, for any pattern ``P`` it holds that::

             \CutBegin{P \Nothing} = P
             \CutEnd{P \Nothing}   = P

Respectively, the neutral element acts on concatenation

             (\Nothing)P = P
             P(\Nothing) = P

Cutting a DFA ``P`` from itself results in the neutral element.

             \CutBegin{P P} = \Nothing
             \CutEnd{P P}   = \Nothing

In the section :ref:`self-repetitiveness` it has been discussed how a DFA
in its repeated version is equivalent to itself. For such DFAs special rules
apply. Obviously, if ``Q = Q{i,}`` for some ``i >= 0``, then 

    \CutBegin{Q{i,} Q} = \Nothing


*\\Empty and Emptiness*

The DFA ``\Empty`` does not match any lexeme. Therefore, any pruning 
operation results in ``\Empty`` itself, i.e.

       \CutBegin{\Empty Q} = \Empty
       \CutEnd{\Empty Q}   = \Empty

for any DFA ``Q``.  Cutting never removes lexemes from the set of matching
lexemes.  Consequently, a cutting operation on a non-empty DFA cannot result in
``\Empty`` since at maximum all lexemes are pruned to the zero-length lexeme,
resulting in ``\Nothing``. 

``\Empty`` cannot be concatenated before a DFA, since it has no acceptance
state to mount on. ``\Empty`` cannot be concatenated after a DFA, since the
first DFA's acceptance states are cancelled and the suffix ``\Empty`` does not
provide any.  Respectively, pruning ``\Empty`` must be considered
inadmissible.::

         (\Empty)R           --> inadmissible
         R(\Empty)           --> inadmissible
         \CutBegin{R \Empty} --> inadmissible
         \CutEnd{R \Empty}   --> inadmissible

*Symmetric Duality*

The operations ``\CutBegin`` and ``\CutEnd`` are symmetrically related through
the reverse operation::

      \R{\CutEnd{P Q}}   = \CutBegin{\R{P} \R{Q}}
      \R{\CutBegin{P Q}} = \CutEnd{\R{P}   \R{Q}}

*Conditions on Beginning and Ending*

Obviously, if the match filtering operations produce empty sets, then the 
cut operations do not change anything, i.e.

   \Begin{P Q} = \Empty  => \CutBegin{P Q} = P
   \End{P Q}   = \Empty  => \CutEnd{P Q} = P

and

   \NotBegin{P Q} = P  => \CutBegin{P Q} = P
   \NotEnd{P Q}   = P  => \CutEnd{P Q} = P

However in general, it cannot be assumed that the result of the operation ``\CutBegin{P
Q}`` does not begin with something matching ``Q``. Respectively, ``\CutEnd{P
Q}`` does not generally produce something which does not end with ``Q``. 


*Cut/Concatenate Reversibility*

Intuitively, the cut operation does exactly the opposite of what concatenation
does. This, however, is not generally true. Consider the expressions ``(pet)*``
and ``peter`` being concatenated, i.e. ``(pet)*peter``. This expression matches::

   peter
   petpeter
   petpetpeter
   ...

However, applying ``\CutBegin{(pet)*peter (pet)*}`` cut as many repetitions of
``pet`` as possible. So the result would match solely the lexeme ``er``, which
is not the original lexeme ``peter``.  Having the end of ``Q`` matching the
beginning of ``P`` is not enough a condition, though.  Consider ``pet`` and
``peter`` being concatenated. There, ``\CutBegin{petpeter pet}`` delivers
correctly ``peter`` and ``\CutEnd{petpeter peter}`` delivers correctly ``pet``.
As long as it is determined where another pattern is mounted, the matching
ending and beginning of ``P`` and ``Q`` do not disable reversibility.
Irreversibility is linked to a possible match in ``Q`` with a certain length
and the possibility to walk then along the beginning of ``P`` an reach another
match of ``Q``.  Using the ``\Tails`` function this condition can be precised 

Reversibility of Concatenation
    The concatenation ``AB`` of two DFAs A and B is reversible by the 
    ``\CutBegin{AB A}`` operation, if and only if::

      \CutBegin{A T} = \Empty for all ``T`` in ``\Tails{B}``. 
      
    Similarly, the concatenation is reversible by the ``\\CutEnd{AB B}``
    operation, if and only if::

      \CutBegin{\R{P} T} = \Empty for all T in \Tails{\R{Q}}.

The reversibility condition for ``\CutEnd`` can be derived from the 
dual symmetry::

    \CutEnd{P Q} = \R{\CutBegin{\R{P} \R{Q}}}
   
Replacing P with ``AB``, Q with ``B``, and applying ``\R{\R{P}} = R``.

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


