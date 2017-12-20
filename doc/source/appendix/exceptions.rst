Exceptions vs. Error State
==========================

Exceptions are completely avoided due to a crucial problem namely the
generation of *"hidden control-flow paths that are difficult for programmers to
reason about"* :cite:`Weimer2008`. In particular, for every function a
programmer calls, he must be aware that it might throw exceptions. The control
flow might not continue directly after the function call but in the exception
catcher block. If no such catcher exists, then the control flow continues in
the first nesting caller that contains an appropriate catcher.  The paths of
control from exception throw to exception catch are, indeed, *obscure*.

Exception safety guarantees have been formalized :cite:`Abrahams2000` and
discussed extensively :cite:`Stroustrup2007`.  *Exception safety axioms* were
discussed :cite:`Dewhurst2003`, namely *exceptions are synchronous*, *it's safe
to destroy*, and *swap does not throw*. Imposing that overloaded operators such
as assignment, plus, etc. shall not throw helps to avoid problems. The *dispose
pattern* :cite:`Shemitz2006` (i.e. the ``with`` statement in Python) helps to
cope with the danger of trailing resource allocations.  In practice, however,
exception safety requires a significant amount of *knowledge*, *expertise*,
*awareness*, and *discipline*. In larger development teams it must be
considered irrational to assume that every member, at every moment, possesses
these virtues. Consequently, it must be assumed that software which is built
with exceptions is inhabited by myriads of ghostly defects lurking in the
imperceptible control paths between the throws and catches.

*The aforementioned paragraphs are by no means a joke!* It lies in the nature
of exceptions to tend to appear only in exceptional occasions. Accordingly,
related bugs tend to be detected lately after the validation phases, the
customer testing, or even the start of serial production.  Being caused by
something exceptional, those bugs tend to be hard to reproduce and the bug
fixing becomes expensive. But, its not only the money a software company that
is at stake.  Errors arising from bad resource allocation (e.g. memory
management) are likely to cause segmentation faults and make a complete system
vulnerable.  When applied in medical devices or military components obscure
exception paths may contain bugs that endanger human life.

In later versions of Quex, exception handling was completely avoided due to the
mentioned insights. Instead, errors are reported through an *error state*.  A
lexer is either in the error state *None* or in the first error state that has
been requested. Requests of error states while an error state is active are not
applied. This ensures that the very first error state is maintained to report
the original error. The error code may be checked in the reception loop 
of analysis, such that the process of lexical analysis terminates as soon
as the error code is reported.


...
TODO
...

Please, do not throw exceptions from inside handlers ...
