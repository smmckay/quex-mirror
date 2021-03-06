Stability
==========

Quex has grown over the last decade, gained more and more features and became
more and more complex. In the frame of this development much refactoring and
redesign took place in order to maintain a transparent clear code structure.
The basis for a solid refactoring are automated unit tests and system tests. By
means of these tests it is verified that changes to the code or the design do
not influence the functioning of the system.

Additionally to the tests for the implemented modules, it is tried to implement
for every non-trivial bug and feature request a regression test that ensures
that the error does not occur in any future release. Since no release is made
without all tests being passed a certain level of quality is guaranteed.
Nevertheless, no bug is too small to be reported. It is by bug reports that
Quex has gained its actual level of maturity. 

.. note::

    **Please, do not hesitate to report bugs!** 
    
    The few minutes spend to submit a bug may help to improve the quality for
    many other users or pinpoint to new interesting issues. In the humble
    history of Quex there have been several cases where small issues let
    to important design changes. Much of the maturity of Quex is due to 
    changes that were made due to bug reports.

Released versions of Quex come with a file ``unit_test_results.txt`` that
contains descriptions of all performed tests. It allows the user to overview the
level of testing. Any observed lack of coverage may be reported as bug or
feature request.

.. note:: 

    Please, report bugs at 
    
    http://sourceforge.net/tracker/?group_id=168259&atid=846112

    and submit feature requests at

    http://sourceforge.net/tracker/?group_id=168259&atid=846115

Corrections on language or style of the documentation are also welcome. The
most convenient way to do this is to download the PDF documentation and
use common PDF editor such as Okular http://okular.kde.org, or other 
freeware tools (see: http://pdfreaders.org/). Comments to the text are
best added as *inline note*. The edited source may be submitted to 
fschaef@users.sourceforge.net.
