**************
Basic Concepts
**************

This chapter introduces concepts and terminology.  The first section talks
about lexical analysis in general and views it in a greater context of
communication.  It explains the approach used to perform lexical analysis,
namely state machines. The second section defines the terms '*lexeme*' and
'*lexatom*' as they are important for detailed discussions.  In the third
section the elaborates on the  *input* procedure, i.e. how data is received.
The third section discusses *output*, i.e. tokens. The last section explains
the idea of a *mode*, i.e.  how tokens are produced from data.

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
