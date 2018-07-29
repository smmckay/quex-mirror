Important Notes:
================

The 'loop' module is designed with very much detail and flexibility so that
'skip', 'skip_range', 'skip_nested_range', and 'indentation_counting' can be
implemented with it very effectively. Everything is covered with Unit Tests
and for the given set of applications no error could be found.

However, the module has a high level of complexity. It would make sense to
re-design it in order to cope with some basic sources of complexity. 

---------
First steps towards a refactoring are done in the subdirectory 'NEW_IDEAS'.
The new 'core.py' would first generate a complex state machine with all
related sm included, cut the first transition, plug the count action
for the loop and stick them together.
---------

Also, a refactoring might use DFA-AGEBRA effectively.

While the functionality seems to be robust, proven by tests, the author
highly suggests a refactoring to avoid complexity.

July 2018, Frank-Rene Schäfer

