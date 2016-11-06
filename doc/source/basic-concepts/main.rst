**************
Basic Concepts
**************

This chapter is about concepts and terminology as they are the foundation for
the subsequent chapters.  The discussions partly peek behind the curtain of
what Quex is doing--only for the reader to relax knowing that Quex deals with
the details. 

In a first section *state machines* are introduces as the approach being used
for lexical analysis based on pattern matching. The portmanteau '*lexer*' shall
stand for 'lexical analyzer', that is the program that performs the analysis.
In the second section the lexer's *input* procedure is presented.  It is
designed for a maxium of flexibility with respect to input source and input
content.  The third section discusses a lexer's *output*: tokens. The last
section explains the idea of a *mode* which circumscribes how a lexer produces
output from input at a given point in time.

.. toctree::

   lexical-state-machine.rst
   input.rst
   output.rst
   modes.rst
   summary.rst
