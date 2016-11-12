Summary
=======

This section introduced some basic concepts. The *state machine approach* for
pattern matching has been presented and two basic terms were defined: the
*lexeme* and the *lexatom*. For fast access lexatoms are stored in a buffer.
The buffer loading process in two steps, namely *byte loading* and *buffer
filling*, has been shown to provide maximum flexibility with respect to the
input source and input encoding. Lexical analysis has been described as the
process of generating *tokens* from a sequential data stream.  A final section
elaborated on modes of a lexical analyzer as specification of its behavior.

The following chapter explains the syntax of Quex input files. The
syntactic elements in its description language will be used as plugs to hook
more detailed discussions.
