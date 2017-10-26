Head and Tails
==============

This section defines two operations which are particularly useful in later
sections of arithmetic and post context specifications. The two operations cut
DFAs into pieces according at the first acceptance state which is reached.
The two operations are

.. describe:: \\Head{R}

   The result of this operations is a DFA that matches only those lexemes
   which are matched by the first acceptance state reached. For example,
   ``\Head{x+}`` matches only "x", because with "x" the first acceptance
   state is reached. The remaining 'tail' is abandonned.

   The result can be seen as the DFA that matches the smallest lexemes
   possible for a given DFA ``R``. Figure :ref:`fig-heads-and-tails`
   graphically displays the ``\Head`` operation for ``x+``.

.. describe:: \\Tails{R}

   The result of this operations cuts anything before the first acceptance
   state from the state machine. For example, ``\Tails{x+}`` matches ``x*``.
   The preceeding 'head' is not considered.

   The result can be considered as the DFA that matches those lexeme parts
   which come after the 'mandatory' first part. Figure
   :ref:`fig-heads-and-tails`b graphically displays the ``\Tails`` operation
   for ``x+``. Note, that the ``\Tails`` operation provides a list of DFAs.

The head's and tail's pruning operations are not reversible in general.
Consider, for example the expression ``ab*|cd*``. The head of the expression is
``a|b`` and the tails are ``b*`` and ``d*``. Plain concatenation cannot produce
the original pattern again.
