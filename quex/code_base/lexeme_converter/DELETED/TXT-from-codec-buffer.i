/* -*- C++ -*- vim: set syntax=cpp:
 * PURPOSE: 
 *
 * Provide the implementation of character and string converter functions
 * FROM the buffer's $$SOURCE_ENCODING$$ to utf8, utf16, utf32, char, and wchar_t.
 *
 * STEPS:
 *
 * (1) Implement the character converters from buffer's $$SOURCE_ENCODING$$ to 
 *     utf8, utf16, utf32. Those come out of quex's code generator.
 *
 * (1b) Derive the converts from $$SOURCE_ENCODING$$ to char and wchar_t from
 *      those converters. For this use:
 *
 *          "../generator/character-converter-char-wchar_t.gi"
 *
 * (2) Generate the implementation of the string converters in terms
 *     of those character converters.
 *
 *     Use: "../generator/implementation-string-converters.gi"
 *
 *          which uses
 *
 *              "../generator/string-converter.gi"
 *
 *          to implement each string converter from the given 
 *          character converters. 
 *
 * These functions ARE DEPENDENT on QUEX_TYPE_LEXATOM.
 * => Thus, they are placed in the analyzer's namespace.
 *
 * 2010 (C) Frank-Rene Schaefer; 
 * ABSOLUTELY NO WARRANTY                                                    */
#ifndef __QUEX_INCLUDE_GUARD__LEXEME_CONVERTER__$$SOURCE_ENCODING$$_I
#define __QUEX_INCLUDE_GUARD__LEXEME_CONVERTER__$$SOURCE_ENCODING$$_I

#include "$$CONVERTER_HEADER$$"
#include "$$CONVERTER_CORE$$"

QUEX_NAMESPACE_MAIN_OPEN

/* Converters for 'char', 'pretty_char', and 'wchar_t' _________________________
 *                                                                            */
QUEX_INLINE void
QUEX_NAME($$SOURCE_ENCODING$$_char_character)(const QUEX_TYPE_LEXATOM** source_pp, 
                                              char**                    drain_pp)  
{
    switch( sizeof(char) )
    {
    case 1:  QUEX_NAME($$SOURCE_ENCODING$$_utf8_character)(source_pp, (uint8_t**)drain_pp); break;
    case 2:  QUEX_NAME($$SOURCE_ENCODING$$_utf16_character)(source_pp, (uint16_t**)drain_pp); break;
    case 4:  QUEX_NAME($$SOURCE_ENCODING$$_utf32_character)(source_pp, (uint32_t**)drain_pp); break;
    default: __quex_assert(false); /* Cannot be handled */
    }
}

#if ! defined(__QUEX_OPTION_WCHAR_T_DISABLED)
QUEX_INLINE void
QUEX_NAME($$SOURCE_ENCODING$$_wchar_character)(const QUEX_TYPE_LEXATOM** source_pp, 
                                               wchar_t**                 drain_pp)  
{
    switch( sizeof(wchar_t) )
    {
    case 1:  QUEX_NAME($$SOURCE_ENCODING$$, utf8_character)(source_pp, (uint8_t**)drain_pp); break;
    case 2:  QUEX_NAME($$SOURCE_ENCODING$$, utf16_character)(source_pp, (uint16_t**)drain_pp); break;
    case 4:  QUEX_NAME($$SOURCE_ENCODING$$, utf32_character)(source_pp, (uint32_t**)drain_pp); break;
    default: __quex_assert(false); /* Cannot be handled */
    }
}
#endif

QUEX_INLINE void
QUEX_NAME($$SOURCE_ENCODING$$_pretty_char_character)(const QUEX_TYPE_LEXATOM** source_pp, 
                                                     char**                    drain_pp)  
{
    char* write_p = *drain_pp;

    QUEX_NAME($$SOURCE_ENCODING$$_char_character)(source_pp, drain_pp);
   
    switch( *write_p ) { 
    case (int)'\n': *write_p++ = (char)'\\'; *write_p = (char)'n'; break;
    case (int)'\t': *write_p++ = (char)'\\'; *write_p = (char)'t'; break;
    case (int)'\r': *write_p++ = (char)'\\'; *write_p = (char)'r'; break;
    case (int)'\a': *write_p++ = (char)'\\'; *write_p = (char)'a'; break;
    case (int)'\b': *write_p++ = (char)'\\'; *write_p = (char)'b'; break;
    case (int)'\f': *write_p++ = (char)'\\'; *write_p = (char)'f'; break;
    case (int)'\v': *write_p++ = (char)'\\'; *write_p = (char)'v'; break;
    default: /* 'drain_pp' has been adapted by converter!       */ return;
    }
    /* 'drain_pp' is set to the post-adapted position.          */
    *drain_pp = &write_p[1];
}


/* Converters for strings ______________________________________________________
 *                                                                            */
$$STRING_CONVERTERS$$

QUEX_NAMESPACE_MAIN_CLOSE

#endif /* __QUEX_INCLUDE_GUARD__LEXEME_CONVERTER__$$SOURCE_ENCODING$$_I */

