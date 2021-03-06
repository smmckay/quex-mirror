Byte Order Mark
===============

Unicode character stream may contain a byte order mark (BOM) at the beginning.
Converters like IConv or ICU may possibly not eat the BOM. Also, if an engine
runs in a genuine encoding mode, i.e. without conversion, it does not know about
BOMs.  It is the user's task to cut the BOM--but Quex helps. 

Quex provides functions to handle the recognition and cutting of the BOM from a
character stream. To access the following files must be included:

.. code-block:: cpp

    #include <quex/code_base/bom>

Note, that the corresponding implementation 'bom.i' file is only to be included
manually, if no generated lexer is used. Otherwise, its implementation is part
of the quex-core which is linked anyway.  These files declare and implement BOM
related functions in in the quex namespace. The list of available functions in
C++ is 

.. code-block:: cpp

    namespace quex {
        E_ByteOrderMark      bom_snap(FILE* fh);
        template <class InStream> 
        E_ByteOrderMark      QUEX_NAME(bom_snap)(InStream* is_p);
        E_ByteOrderMark      bom_identify(const uint8_t* const Buffer, size_t* n);
        const char*        bom_name(E_ByteOrderMark BOM);
    } 

and in C

.. code-block:: cpp

    E_ByteOrderMark  quex_bom_snap(FILE* fh);
    E_ByteOrderMark  quex_bom_identify(const uint8_t* const Buffer, size_t* n);
    const char*    quex_bom_name(E_ByteOrderMark BOM);

In the further discussion the functions will be referred to without their name
or namespace prefix. The function ``bom_snap(...)`` checks whether the stream
starts with a byte sequence that is identified as a byte order mark. If so, it
steps over it so that the lexical analysis can start immediately after it. An
exception is the BOM for UTF7; this coding is identified, but the stream does
not step over it. If UTF7 is detected, it has to be considered with care
because it may actually a normal character sequence. The type ``E_ByteOrderMark``
defines constants that identify BOMs. It is defined as follows:

.. code-block::cpp

        QUEX_BOM_NONE            = 0x200,  /* D9 --> NONE/NOT SURE */
        QUEX_BOM_UTF_8           = 0x001,  /* D0 --> UTF 8         */
        QUEX_BOM_UTF_1           = 0x002,  /* D1 --> UTF 1         */
        QUEX_BOM_UTF_EBCDIC      = 0x004,  /* D2 --> UTF EBCDIC    */
        QUEX_BOM_BOCU_1          = 0x008,  /* D3 --> BOCU 1        */
        QUEX_BOM_GB_18030        = 0x010,  /* D4 --> GB_18030      */
        QUEX_BOM_UTF_7           = 0x220,  /* D5 --> UTF 7;        
                                            * D9 --> May be not.   */
        QUEX_BOM_UTF_16          = 0x040,  /* D6 --> UTF 16        */         
        QUEX_BOM_UTF_16_LE       = 0x041,                          
        QUEX_BOM_UTF_16_BE       = 0x042,                          
        QUEX_BOM_UTF_32          = 0x080,  /* D7 --> UTF 32        */
        QUEX_BOM_UTF_32_LE       = 0x081,                          
        QUEX_BOM_UTF_32_BE       = 0x082,                          
        QUEX_BOM_SCSU            = 0x100,  /* D8 --> SCSU          */
        QUEX_BOM_SCSU_TO_UCS     = 0x101,  
        QUEX_BOM_SCSU_W0_TO_FE80 = 0x102, 
        QUEX_BOM_SCSU_W1_TO_FE80 = 0x103, 
        QUEX_BOM_SCSU_W2_TO_FE80 = 0x104, 
        QUEX_BOM_SCSU_W3_TO_FE80 = 0x105, 
        QUEX_BOM_SCSU_W4_TO_FE80 = 0x106, 
        QUEX_BOM_SCSU_W5_TO_FE80 = 0x107, 
        QUEX_BOM_SCSU_W6_TO_FE80 = 0x108, 
        QUEX_BOM_SCSU_W7_TO_FE80 = 0x109, 
    } E_ByteOrderMark;

.. note:: The BOM for UTF7 consists of the three bytes 0x2B, 0x2F, 0x76 
          plus one of 0x2B, 0x2F, 0x38, or 0x39. This corresponds to the
          characters "+", "/", "v" and one of "+", "/", "8", or "9". All
          of them are normal Unicode Characters.  Thus a normal Unicode
          stream could wrongly be identified as an UTF7 stream. Also,
          The last two bits are the beginning of a new character. Thus,
          the BOM cannot easily be snapped from the stream. Instead, 
          the whole byte stream would have to be bit shifted. 

          For the aforementioned reasons, a UTF7 BOM is not cut from 
          the byte stream.

Basic characteristics can be identified by binary 'and' operations.  For
example

.. code-block:: cpp

    bom_type = bom_snap(file_handle);

    if( bom_type & (QUEX_BOM_UTF32 | QUEX_BOM_NONE) ) {
        ...
    }

Checks whether a BOM of encoding UTF32 was found, or if there was no BOM. The
statement also holds if a UTF7 BOM is found, since the ``QUEX_BOM_UTF7`` has
the ``QUEX_BOM_NONE`` bit raised. The exact information about the byte order
can be detected by considering the whole value, e.g.

.. code-block:: cpp

    ...
    switch( bom_type ) {
    /* Little ending BOM  => use the little endian converter. */
    case QUEX_BOM_UTF_32_LE: encoding_name = "UTF32LE"; break;
    /* No BOM, or big endian bom => use big endian converter. */
    case QUEX_BOM_UTF7:
    case QUEX_BOM_NONE:
    case QUEX_BOM_UTF_32_BE: encoding_name = "UTF32BE"; break;
    /* Unkown BOM => break                                    */
    default: 
         error_msg("Unknown BOM detected %s", bom_name(bom_type)); 
    }

The example above, already, mentions another helper function that maps
a BOM identifier to a human readable string


.. code-block:: cpp
 
    const char*     bom_name(E_ByteOrderMark BOM);

If the user wishes to identify on some chunk of arbitrary memory the following
function may be used

.. code-block:: cpp
 
    E_ByteOrderMark   bom_identify(const uint8_t* const Buffer, size_t* n);

It receives a byte array in ``Buffer`` which must at least be of size four.  It
reports the found BOM as a return value and fills the number of bytes that the
BOM occupies into what the second argument ``n`` points.

One important thing to notice is that the constructor does the first 
load from the data stream. Thus, if the BOM-cutting happens after the
construction of the lexical analyzer object the 'cut' would not have
any effect. Thus, the constructor call must be delayed after the
call to ``BOM_snap(...)``. If the initial call to the
constructor cannot be avoided, then the call to the BOM snap function
must be followed by a call to the ``reset(...)`` function. Also, 
an attempt to cut the BOM, after the constructor has done its 
initial load must fail.

.. warning:: Do not use the file or stream handle that is used 
   for BOM cutting in the lexical analyzer constructor **before**
   the BOM cutting. If this is desired, then the constructor
   call **happen** after the BOM cut.

An example of how to cut the BOM can be found in ``demo/*/003`` in 
``example-bom.c``, respectively ``example-bom.c``. The following code
fragment shows an initialization in C language:

.. code-block:: cpp

    FILE*           fh = NULL; 
    EasyLexer       qlex;
    E_ByteOrderMark   bom_type = QUEX_BOM_NONE;

    fh = fopen(file_name, "rb");

    /* Either there is no BOM, or if there is one, then it must be UTF8 */
    E_ByteOrderMark   bom_type = quex_bom_snap(fh);
    if( (bom_type & (QUEX_BOM_UTF_8 | QUEX_BOM_NONE)) == 0 ) {
        printf("Found a non-UTF8 BOM. Exit\n");
        fclose(fh);
        return 0;
    }

    /* The lexer **must** be constructed after the BOM-cut */
    QUEX_NAME(from_FILE)(&qlex, fh, "UTF8", false);

    /* Now, the qlex is ready for analysis. */
    ... 

If a running lexer needs to set the bom dynamically, a pattern like the
following may be followed:

.. code-block:: cpp

   quex::my_lexer  qlex(...);
   ...
   switch( quex::bom_snap(fh) )
   {
       case QUEX_BOM_UTF_8:      qlex.reset(fh, "utf-8");      break;
       case QUEX_BOM_UTF_1:      qlex.reset(fh, "iso-10646");  break;
       case QUEX_BOM_UTF_EBCDIC: qlex.reset(fh, "ebcdic-us");  break;
       case QUEX_BOM_GB_18030:   qlex.reset(fh, "gb18030");    break;
       case QUEX_BOM_UTF_7:      qlex.reset(fh, "utf-7");      break;
       case QUEX_BOM_UTF_16:     qlex.reset(fh, "utf-16");     break;
       case QUEX_BOM_UTF_16_LE:  qlex.reset(fh, "utf-16le");   break;
       case QUEX_BOM_UTF_16_BE:  qlex.reset(fh, "utf-16be");   break;
       case QUEX_BOM_UTF_32:     qlex.reset(fh, "utf-32");     break;
       case QUEX_BOM_UTF_32_LE:  qlex.reset(fh, "utf-32le");   break;
       case QUEX_BOM_UTF_32_BE:  qlex.reset(fh, "utf-32be");   break;
       //...
       default:                  qlex.reset(fh, get_file_encoding(fh));
                                 break;
  }
