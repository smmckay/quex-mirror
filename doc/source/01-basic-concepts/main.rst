**************
Basic Concepts
**************

This chapter is about concepts and terminology as the foundation for the
subsequent chapters.  The discussions partly peek behind the curtain of what
Quex is doing--only for the reader to relax knowing that Quex deals with the
details. 

The first section talks about lexical analysis in general and views it in a
greater context of communication.  It demonstrates the approach used to perform
lexical analysis, namely state machines. The second section defines the terms
'lexeme' and 'lexatom' as they are important for detailed discussions. 

The portmanteau '*lexer*' shall stand for 'lexical analyzer', that is the
program that performs the analysis.  In the third section the lexer's *input*
procedure is presented.  It is designed for a maxium of flexibility with
respect to input source and input content.  The third section discusses a
lexer's *output*: tokens. The last but one section explains the idea of a
*mode* which circumscribes how a lexer produces output from input at a given
point in time. 

Finally, a minimalist example is demonstrated. Despite the lack of knowledge
about the Quex syntax, at that point, the example provides the reader with the
ability to get started with his first lexer. This lexer might then be adapter
according to the added knowledge of later chapters.

.. toctree::

   lexical-state-machine.rst
   text.rst
   input.rst
   output.rst
   modes.rst
   minimalist-example.rst
   summary.rst
