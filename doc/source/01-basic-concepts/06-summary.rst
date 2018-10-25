Summary
=======

This section showed a *state machine* based approach for lexical
analysis of sequential data streams. A lexer signalizes when conditions are met
in a sequential data stream that identify a pattern. The triggering events in
the state machine that guided to the signalizing state are called *lexatoms*.
The sequence of lexatoms that is called *lexeme*.

For the sake of computational efficiency lexatoms are stored in a buffer.  The
buffer loading process in two steps, namely *byte loading* and *lexatom
loading*, has been shown to provide maximum flexibility with respect to the
choice of input source and encoding. Lexical analysis has been described
as the process of generating *tokens* from a sequential data stream.  The
concept of a *mode* has been introduced as the basic means to describe a
lexer's behavior. 

