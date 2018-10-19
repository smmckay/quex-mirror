**************
Basic Concepts
**************

This chapter introduces concepts and terminology.  The first section talks
about lexical analysis and views it in a greater context of communication.  It
elaborates on the applied approach, namely state machines.  The second section
defines the terms '*lexeme*' and '*lexatom*' as they are important for detailed
discussions.  In the third section the presents the design of the *input*
process, i.e. how data is received.  The third section discusses a lexer's
*output*, i.e. tokens.  The last section explains how to model the behavior of
how tokens are produced from data in so called *modes*.

Throughout the text, the portmanteau '*lexer*' shall stand for 'lexical
analyzer', that is the program that performs the analysis.  When this text
talks about the *reader*, it actually addresses *you*.


.. toctree::

   lexical-state-machine.rst
   text.rst
   input.rst
   output.rst
   modes.rst
   summary.rst
