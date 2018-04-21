QUEX_INLINE void
QUEX_NAME(unicode_utf8_character)(const QUEX_TYPE_LEXATOM**  input_pp, 
                                       uint8_t**                  output_pp)
{ 
    switch( sizeof(QUEX_TYPE_LEXATOM) )
    {
    case 1:  QUEX_NAME(utf8_utf8_character)(input_pp, output_pp);  break;
    case 2:  QUEX_NAME(utf16_utf8_character)(input_pp, output_pp); break;
    case 4:  QUEX_NAME(utf32_utf8_character)(input_pp, output_pp); break;
    default: QUEX_ERROR_EXIT("Cannot derive converter for given element size.");
    }
}

QUEX_INLINE void
QUEX_NAME(unicode_utf16_character)(const QUEX_TYPE_LEXATOM**  input_pp, 
                                   uint16_t**                 output_pp)
{ 
    switch( sizeof(QUEX_TYPE_LEXATOM) )
    {
    case 1:  QUEX_NAME(utf8_utf16_character)(input_pp, output_pp);  break;
    case 2:  QUEX_NAME(utf16_utf16_character)(input_pp, output_pp); break;
    case 4:  QUEX_NAME(utf32_utf16_character)(input_pp, output_pp); break;
    default: QUEX_ERROR_EXIT("Cannot derive converter for given element size.");
    }
}

QUEX_INLINE void
QUEX_NAME(unicode_utf32_character)(const QUEX_TYPE_LEXATOM**  input_pp, 
                                   uint32_t**                 output_pp)
{ 
    switch( sizeof(QUEX_TYPE_LEXATOM) )
    {
    case 1:  QUEX_NAME(utf8_utf32_character)(input_pp, output_pp);  break;
    case 2:  QUEX_NAME(utf16_utf32_character)(input_pp, output_pp); break;
    case 4:  QUEX_NAME(utf32_utf32_character)(input_pp, output_pp); break;
    default: QUEX_ERROR_EXIT("Cannot derive converter for given element size.");
    }
}
