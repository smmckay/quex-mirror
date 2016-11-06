Output
======

Lexical analysis is the first step in understanding a sequential stream
of data. As such it produces *atomic chunks of meaning*, so called *tokens*.
A token carries the information about the content category that it carries and
possibly the lexeme or interpretation of the lexeme that matched when the token
was produced.  In this sense, lexical analysis is *tokenization*. 

Token
   A token contains a *unique token identifier* which identifies the category 
   of meaning that it carries. Optionally, it may carry further information 
   about the matched lexeme. 

For example, a token may carry the meaning 'plus operator' with no further
information, it may carry the meaning 'function' together with the name of the
function to which it relates, or it may carry the meaning 'number' with some
numeric value related to it. 

A Quex-generated lexer is aware of the token class. The pattern matching syntax
provides 'token send' commands, where a token is prepared and sent to the
receiver. Also, when line and column numbers are computed they are entered into
the token directly from inside the lexer's engine. For the majority of
applications, the default token class may do. However, there is a dedicated
mini-language to describe customized token classes. Even free-style manual
token classes may be passed to the lexer engine.

Token classes can be designed following two approaches of storing a 
lexeme's information:

 #. Storing the *uninterpreted* lexeme, i.e. the plain matching string.

 #. Storing the *interpreted* lexeme, i.e. the information that it
    represents such as a 'number', a 'string', etc.

Following the first approach is cleaner in the sense that it separates
the lexer's tokenisation from *lexeme interpretation* being done in a 
dedicated unit. The second approach, however, may be advantageous with
respect to the required copying and memory footprint of tokens. Quex's
default token class has a 'text' and 'number' member. If this is too
much or not enough, token classes can be designed freely to fit specific 
design purposes.

TODO:
.. Talk about the 'lexeme in buffer': In this case, though, a callback must be
   implemented which reacts on the buffer's content change. On this event the
   callback must saveguard all related strings.

Tokens may either be communicated one-by-one, or in a queue. A token queue is
required, in cases where one lexical unit may cause multiple tokens.  For
example, a newline in indentation based lexical analysis (see 'offside rule'
:cite:`todo`) may cause multiple scopes to be closed. While there is only one
match, multiple tokens must be sent. Without a token queue such scenarios
cannot be handled.

.. rubric: Footnotes

