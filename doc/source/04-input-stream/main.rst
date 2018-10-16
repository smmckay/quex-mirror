*****
Input
*****

The design of the input procedure has a strong impact on the lexer's
application range. This chapter explains the Quex's input procedure as it is
based on on *raw stream reception* and *elementary interpretation*. The former
deals with different streaming APIs and the latter with the procedure of how to
extract *lexatoms*, i.e. what is fed to the lexer. 

For the seek of computational speed, lexical analysis runs on a buffer, i.e.
preloaded sequences of data stored in memory close to the CPU. In this
chapter the role of buffers, their allocation, the related events, and the
input navigation is explained.  Based on a proper understanding of the input
procedure, the three types of input stream initialization are presented, namely
lexer *construction*, *inclusion*, and *reset*. 

A dedicated section explains with raw stream receivers provided by Quex for a
variety of operating system APIs.  Quex also provides with pre-built interfaces
for ICU and IConv for elementary character decoding.  The according section
explains how to use them and how to deal with byte-order-marks (BOM).

Once, the provided implementations of *raw stream receivers* (classes derived
from class `ByteLoader`) and *elementary interpreters* (classes derived from
class `LexatomLoader`) are demonstrated, it is explained how to write
customized versions of both.

.. toctree::

    input-process.rst
    include-stack.rst
    reset.rst
    stream-navigation.rst
    buffer/intro.rst
    encodings/converter.rst
    encodings/engine-codec.rst
    encodings/process.rst
    encodings/converter_helper.rst
    encodings/intro.rst
    encodings/bom.rst
    encodings/user-defined.rst
