Summary
=======

This section introduced some basic concepts. The *state machine approach* for
pattern matching has been presented and two basic terms were defined: the
*lexeme* and the *lexatom*. For fast access lexatoms are stored in a buffer.
The buffer loading process in two steps, namely *byte loading* and *lexatom
loading*, has been shown to provide maximum flexibility with respect to the
input source and input encoding. Lexical analysis has been described as the
process of generating *tokens* from a sequential data stream.  The mode as the
central instance to describe the analysis process has bee discussed in detail.
A final section delivered a complete working example to be used as a starting
point for those who want to get quickly their hands on coding.

The following chapter explains the syntax of Quex input files. The
syntactic elements in its description language will be used as plugs to hook
more detailed discussions.
