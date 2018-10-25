Output
======

Lexical analysis takes a data sequence as input and produces so called tokens.
A token signalizes the detection of a pattern, i.e. some subsequence of the
data has matched some specified condition. The subsequence is then interpreted
as some atomic element of meaning and value. For example, a sequence of digits
``[0-9]+`` represents the concept of a number. The sequence ``2``, ``5``, ``6``
matches this pattern. Therefore, the sequences carries the meaning of a number
and, therefore, can be interpreted according to its meaning.

Token
   A token identifies an atomic meaning in an input stream. A token object
   contains a distinct *token identifier* which is distinctly related to its
   meaning. It optionally carries information about the lexeme that is
   associated with it.

For example, a token may carry the meaning plus operator with no further
information, it may carry the meaning 'function' together with the name of the
function to which it relates, or it may carry the meaning 'number' with some
numeric value related to it. 

Quex's provides syntax to specify tokens to be sent as a reaction to pattern
matching. At minimum a token must be associated with a token identifier.
Additionally, token content may be assigned which might be extracted from the
matching lexeme.  For human readable text, Quex provides an automatic
functionality to tag tokens with the line and column number of the position
where matching lexeme occurred. This functionality is implemented by the
default token class. There is a dedicated syntax to write customized token
classes. Even extern token classes or extern token identifier definitions may
be included. 

Token classes can be designed following two approaches of storing a 
lexeme's information:

 #. Storing the *uninterpreted* lexeme.

 #. Storing the *interpreted* lexeme, i.e. the information that it
    represents such as a concrete number instead of the sequence of 
    characters that make it up.

Following the first approach is cleaner in the sense that it separates
the lexer's tokenisation from *lexeme interpretation* to be done in a 
separate unit. The second approach, however, may be advantageous with
respect to the required copying and memory footprint of tokens. Quex's
default token class has a 'text' and 'number' member. If this is too
much or not enough, token classes can be designed freely to fit specific 
design purposes.

Tokens are the primary result of lexical analysis. Nevertheless, user code in C
or C++ may be specified to be executed as a reaction to pattern matches,
events, or mode transitions.
 
.. rubric: Footnotes

