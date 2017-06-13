Sequential Data Streams
=======================

This section introduces some basic terms and demonstrates their rationale.
These terms are developed for general applications in any lexical analysis
scenario.  However, since they were originally developed in the frame of human
readable text, the are explanation is setup in that context.

In times of prevalent ASCII encoding, there never was a problem calling the
events that cause state transitions 'characters', 'letters', or 'byte'. A byte
carried a letter. In modern times things have changed, though. A 'character'
cannot be considered the correct term for the event that triggers state
transitions in a FSM when encodings such as UTF8 and UTF16 are used directly.
With these encodings characters are composed of varying number of bytes. A
somewhat more fitting term is the term 'code unit' :cite:`Unicode2015`.

Code Unit
    A code unit is a bit sequence used to encode each single character unit
    of a repertoire within an encoding form.

For UTF8, the code unit is a byte and Unicode characters may occupy up to six
bytes [#f5]_. The letter 'A' is encoded in one single byte, that is one code
unit. To encode the Egyptian Hieroglyph P002 four bytes, that is four code
units are used. A code unit in UTF16 is two byte large and characters are
represented by one or two code units. Code units may be considered as the
smallest unit, i.e. the *letter* of the data stream. This, however, deviates
from the general understanding of 'letter' or 'character'. The two terms
are, therefore, not suited to denote elements of the data stream.

However, the term 'code unit' is also not generally valid for elements of the
data stream.  When the lexer runs on converted input, incoming code units may
be translated into four-byte Unicode code points, for example. Then, it is
those integers which are used as events, not code units.  Further, lexers may
be fed with streams not having anything to do with character encodings. To
clarify the entities on which a lexer's state machine triggers, the term
'lexatom' is introduced.

Lexatom
   A lexatom is one element in a sequence of data that make up the
   representation of a character. It is an integer value that describes an
   event in a pattern matching state machine. 

.. _fig:lexatom-explanation:

.. figure:: ../figures/lexatom-explanation.png
   
   Egyptian Hieroglyph P002 and lexatoms/code units according to UTF32, 
   UTF16, and UTF8.

In an ASCII text, every character is made up out of a single byte which carries
a single character. In that case, a lexatom is the ASCII value of a character.
When dealing with Unicode and its encodings things are not that trivial.
Figure :ref:`fig:lexatom-explanation` shows the example of a Unicode character:
the Egyptian Hieroglyph P002. When the state machine runs on Unicode (UTF32)
there is only one lexatom given as '0x1329D'. The cells that carry lexatoms may
be 4 byte wide. When the dynamic length encoding UTF16 is used, the character
is represented by two lexatoms '0xD80C' followed by '0xDE9E'. Then, a cell
carrying a lexatom must be at least 2 byte wide. In UTF8, the same character is
represented by a sequences of lexatoms namely '0xF0',  '0x93', '0x8A', and
'0x9D' which can be carried in bytes. 

The term 'lexatom' has been introduced by the author of this text. Its name,
though, is derived from an established term in computer science: the lexeme
[#f2]_ . Following the definition in :cite:`Aho2007compilers` (p. 111), let
this term be defined more precisely in terms of the new defined term lexatom. 

Lexeme
    A lexeme is a sequence of lexatoms that matches a pattern associated 
    with a category of meaning.

If the input to a lexer is raw text, then the lexatom is equivalent to the
established term 'code unit'. If further, the input encoding describes
characters by a code unit each, then the term lexatom is equivalent to
'character' in its very traditional meaning. Under all circumstances, a
'lexatom' denotes what triggers state transitions in the analyzer's state
machine.

Lexatoms are stored as a sequence in a buffer, so that they can be accessed
quickly by the lexer. Loading greater chunks of lexatoms into a buffer is
likely always faster than loading each lexatom on its own. Given a pointer
``p`` to a lexatom-carrying cell of a buffer and a variable ``v`` to carry the
value, a state machine event is implemented as a sequence of the following
instructions:

   #. Increment ``p``, if current state ≠ initial state.

   #. Set ``v`` = content of cell to where ``p`` points. 

With the lexatom stored in ``v`` the transition map determines the successor
state.  

In this section it has been discussed how lexical analysis is established.  The
terms lexatom and lexeme have been defined and shown in the context of code
units and characters. While the discussion focussed on text, the two terms may
be applied to any scenario--be it natural language processing, DNA analysis, or
compiler construction.  Further, the relation between lexatom and state machine
events has been clarified based on the fact that efficient analysis requires
intermediate storage of data in memory buffers.  The next section discusses how
lexatoms are filled into that buffer.
