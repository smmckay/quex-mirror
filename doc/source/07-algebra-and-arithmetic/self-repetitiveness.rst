.. sec:sec-concatenation-optionality-reptition

Concatenation, Optionality, and Repetition
==========================================

Concatenation is an operation where a sequence of patterns composes a longer
pattern. This operation, though, has some subtle characteristics when applied
optionally on the same pattern. In particular some effects of repeated patterns
are discussed in this section. 

A DFA state cannot transit into two different states with the same trigger.
Thus, when a DFA matching ``x?`` shall receive a tail ``xxx``, this cannot
result in a state machine as in figure :ref:`fig-bad-concatenation`, since
state 'X' would transit on 'x' to two different states. Instead, a DFA is
produced that corresponds to :ref:`fig-good-concatenation`. As can be seen, the
finite number of repetition is pulled in front of the optional two acceptance
states, i.e. the optionality is post-poned upon concatenation::

     (x|xx)xxx ---> xxx(x|xx)

Both expressions have the same logical implication, i.e. they match an
arbitrary number of repetitions, as long as there are at least ``N``.  However,
the first expression is not practical. Repetitions with more than one number of
possible repetitions are a special case of optionality. Thus, the same
post-poning happens for the following cases

     x{3,5}xxx ---> xxx(x{3,5})
     x{3,}xxx  ---> xxx(x{3,})
     x*xxx     ---> xxx(x*)

Let this effect of pushing finite number of repetitions in front of the 
optionality be called the *post-poning effect of concatenation optionality*
as defined below.

Post-poning Effect of Concatenated Optionality
     Let ``O`` be a pattern matching against at least two different 
     number of repetitions of ``P``, then the concatenation of ``OP``
     is implemented as a DFA acccording to ``PO``.

In particular, the arbitrary number of repetitions ``P*`` is an optionality,
since it represents ``P|P{2}|P{3}|...``. When it is concatenated with a finite
number of repetitions, the finite number of repetitions is pushed in front.::

    P*P{N} --> P{N}P*

Naturally, the concatenation of ``N`` repetitions and ``M`` repetitions results
in ``N+M`` reptitions. This implies that the concatenation in this case is
commutable, i.e.  ``P{N}P{M} = P{N+M} = P{M}P{N}``.  In the context of the
post-poning effect of concatenated optionality, it follows, that if ``O``
matches against at least two different number of repetitions of ``P``, then::

    P{N}OP{M} --> P{N+M}O

The post-poning effect is a direct consequence of the requirement that DFAs the
relation between a state's target state and the trigger is distinct.  It is not
the result of deliberate programming activities. Instead, it results from the
application of the NFA-to-DFA transformation on the concatenated DFAs. The
post-poning effect itself is far reaching. One consequence of it is the the
*dangerous trailing context* (section :ref:`sec-dangerous-trailing-context`).

Repeated pattern have special properties. For example the concatenation of the
arbitrarily repeated pattern ``P*`` with itself results in ``P*``, i.e.::

    P*P* = P*

Another subject is that of self-repetitiveness.  Applying the repetition
operator on any pattern results in a pattern which is self-repetitive, i.e. in
that case ``P*`` is equal to ``P`` itself. Such a pattern is invariant under
the repetition operation.

Self Repetitiveness
    A pattern ``R`` is self-repetitive of grade 0, if and only if::

                  R = R{0,}

    A pattern ``R`` is self-repetitive of grade 1, if and only if::

                  R = R{1,}


Let, for example ``R`` be defined as ``x*``, so it matches matches::

        ""  
        "x"
        "xx"
        "xxx" 
        ...

The expression ``R*``, i.e. ``(x*)*`` matches anything that ``R`` matched at
any repetition number. Thus, it matches::

        ""  
        "x"   --> "" "x" "xx" "xxx" ...
        "xx"  --> "" "xx" "xxxx" "xxxxxx" ...
        ...

There are no lexemes in ``(x*)*`` which are not in ``x*`` and vice versa.
Hence, ``R`` =  ``R*``. For ``x*`` is *self-repetitive* of grade 0.
For a pattern ``x+`` the set of matched lexemes is::

        "x"
        "xx"
        "xxx" 
        ...

The expression ``(x+)+`` matches anything that ``x`` matched at any repetition
greater or equal one, i.e.::

        "x"
        "xx"
        "xxx" 
        ...

For ``x+`` is *self-repetitive* of grade 1. If a pattern is self-repetitive
with respect to a number i, then it is also self-repetitive with respect
to i*k for any k > 1.::

        R = R{i,}  <=> R = R{i*k,}

In particular, if a pattern is self-repetitive with grade 0, then it is 
self-repetitive of any grade, i.e.::

        R = R{0,}  <=> R = R{i,} for any i >= 0

On the other hand, if ``R`` is not self-repetitive with respect to i, then
it cannot be repetitive with respect to i*k.

        R != R{i,} <=> R = R{i*k,0}

For a pattern to be self-repetitive of grade 'i_0', 'i_0' must either be 0
or one, or there must be a 'i_0' and a 'k' so that 'i_0 = i_1*k', where
R is self-repetitive of grade 'i_1'. This recursion leads to the following
statement

Minimum Self-Repetitiveness
    A pattern can only be self-repetitive of grade i > 1 if it is 
    self-repetitive of grade 0 or 1. 

                        R = R{i,}  =>  R = R{0,} or R = R{1,}

    respectively,

        R != R{0,} and R != R{1,}  =>  R != R{i,} for i > 1

Let the absence of any repetition be defined as 'finiteness'.

Finiteness
    A pattern ``Q`` is infinite, if and only if there are no three patterns
    patterns ``A``, ``B``, and ``C`` such that::

                   Q = A(B*)C

    where ``A`` and ``C`` can be ``\Empty`` or ``\Nothing``. ``C`` must be
    different from ``\Empty`` and ``\Nothing``. If such patterns cannot be
    found for a pattern ``Q``, then ``Q`` is finite.

    A pattern that is finite cannot be self-repetitive at any grade.::

                Q is finite => Q != Q{i,} for any i

With an infinite pattern being described as ``A(B*)C``, constraints on ``A``, 
``B``, and ``C`` can be derived for the self-repetitiveness. The following
can only holds::

      Q* = (AB*C)* = (A|AB*|AB*C)* = AB*C = Q

if and only if ``A`` and ``C`` are both ``\Empty`` or ``\Nothing``. The 
self-repetitiveness of grade 1, i.e.::

      Q+ = (AB*C)+ = (A|AB*|AB*C)+ = AB*C = Q

only holds if ``A`` is equal to ``B`` and ``C`` is ``\Empty`` or ``\Nothing``.

TODO: Talk about concatenation 'x*' and 'x+' which results in 'x+'
