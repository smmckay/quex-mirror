*****
Input
*****

Lexers need input, and this chapter discusses fundamental things about it.
First, the input provision procedure is reflected. After introducing the
interface for byte stream loading, it is shown how to perform input stream
conversion.  Based on a proper understanding of the input procedure, the three
types of input stream initialization are presented, namely lexer
*construction*, *inclusion*, and *reset*. Then, it is shown how to navigate in
the input stream on lexatom level. 

.. toctree::

    input-process.rst
    include-stack.rst
    stream-navigation.rst
    buffer/intro.rst
    encodings/converter.rst
    encodings/engine-codec.rst
    encodings/process.rst
    encodings/converter_helper.rst
    encodings/intro.rst
    encodings/bom.rst
    encodings/user-defined.rst
    reset.rst
