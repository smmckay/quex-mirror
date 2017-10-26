Self-Repetitiveness
===================

Repetition is a special form of concatenation where a pattern is appended to
itself for an arbitrary number. For the upcoming discussion on cut/concatenate
arithmetic, the subject of self-repetitiveness needs to be discussed.  Patterns
may be indifferent with respect to repetition operations. 

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

Thus, for this case ``R`` =  ``R*``. For ``x*`` is *self-repetitive* of grade .
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

