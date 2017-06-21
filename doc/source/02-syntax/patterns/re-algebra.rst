Algebra of DFAs
===============

Quex introduces an 'Algebra of DFAs'. That is, there is a set of operations on
state machines and properties that is equivalent to the algebra of sets.  In
fact, the operations on DFAs directly correspond to set operations in the *set
of lexemes* which they match. For example, the union of two DFAs is defined as
an operation that produces a DFA which matches the union of the lexemes which
are matched by the two operand DFAs.  Let the regular
expressions P and Q be defined as below::

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

