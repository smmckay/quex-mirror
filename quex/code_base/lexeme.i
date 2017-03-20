/* -*- C++ -*- vim:set syntax=cpp: 
 * (C) Frank-Rene Schaefer    
 * ABSOLUTELY NO WARRANTY                                                     */
#ifndef __QUEX_INCLUDE_GUARD__LEXEME_I
#define __QUEX_INCLUDE_GUARD__LEXEME_I

#include <quex/code_base/definitions>

QUEX_NAMESPACE_MAIN_OPEN

QUEX_INLINE size_t 
QUEX_NAME(lexeme_length)(const QUEX_TYPE_LEXATOM* Str)
{
    const QUEX_TYPE_LEXATOM* iterator = Str;
    while( *iterator != 0 ) ++iterator; 
    return (size_t)(iterator - Str);
}

QUEX_INLINE size_t 
QUEX_NAME(lexeme_compare)(const QUEX_TYPE_LEXATOM* it0, 
                          const QUEX_TYPE_LEXATOM* it1)
{
    for(; *it0 == *it1; ++it0, ++it1) {
        /* Both letters are the same and == 0?
         * => both reach terminall zero without being different.              */
        if( *it0 == 0 ) return 0;
    }
    return (size_t)(*it0) - (size_t)(*it1);
}

/* If QUEX_TYPE_LEXATOM is chosen inappropriately with respect to the
 * character encoding ('wchar_t' carrying 'utf8')
 * => Lexeme helper functions may cause trouble.  
 * => Disable below functions with compile option:
 *
 *                 -DQUEX_OPTION_LEXEME_CONVERTERS_DISABLED                          
 *                                                                            */
#if      defined(QUEX_OPTION_LEXEME_CONVERTERS) \
    && ! defined(QUEX_OPTION_LEXEME_CONVERTERS_DISABLED)


QUEX_INLINE void
QUEX_NAME(lexeme_to_utf8)(const QUEX_TYPE_LEXATOM** source_p, 
                          const QUEX_TYPE_LEXATOM*  SourceEnd,
                          uint8_t**                 drain_p,  
                          const uint8_t*            DrainEnd)
{
    /* If this causes an error, you might carry an encoding in chunks of 
     * inappropriate size (e.g. 'utf8' in a 'wchar_t'). Use the command line
     * option 
     *                '-DQUEX_OPTION_LEXEME_CONVERTERS_DISABLED'
     *
     * to disable this file completely!                                       */
    QUEX_CONVERTER_STRING(QUEX_SETTING_CHARACTER_CODEC,utf8)(
                          source_p, SourceEnd, drain_p, DrainEnd);
}

QUEX_INLINE void
QUEX_NAME(lexeme_to_utf16)(const QUEX_TYPE_LEXATOM** source_p, 
                           const QUEX_TYPE_LEXATOM*  SourceEnd,
                           uint16_t**                drain_p,  
                           const uint16_t*           DrainEnd)
{
    QUEX_CONVERTER_STRING(QUEX_SETTING_CHARACTER_CODEC,utf16)(
                          source_p, SourceEnd, drain_p, DrainEnd);
}

QUEX_INLINE void
QUEX_NAME(lexeme_to_utf32)(const QUEX_TYPE_LEXATOM** source_p, 
                           const QUEX_TYPE_LEXATOM*  SourceEnd,
                           uint32_t**                drain_p,  
                           const uint32_t*           DrainEnd)
{
    QUEX_CONVERTER_STRING(QUEX_SETTING_CHARACTER_CODEC,utf32)(
                          source_p, SourceEnd, drain_p, DrainEnd);
}

QUEX_INLINE void
QUEX_NAME(lexeme_to_char)(const QUEX_TYPE_LEXATOM** source_p, 
                          const QUEX_TYPE_LEXATOM*  SourceEnd,
                          char**                    drain_p,  
                          const char*               DrainEnd)
{
    QUEX_CONVERTER_STRING(QUEX_SETTING_CHARACTER_CODEC,char)(
                          source_p, SourceEnd, drain_p, DrainEnd);
}

#if ! defined(__QUEX_OPTION_WCHAR_T_DISABLED)
QUEX_INLINE void
QUEX_NAME(lexeme_to_wchar)(const QUEX_TYPE_LEXATOM** source_p, 
                           const QUEX_TYPE_LEXATOM*  SourceEnd,
                           wchar_t**                 drain_p,  
                           const wchar_t*            DrainEnd)
{
    QUEX_CONVERTER_STRING(QUEX_SETTING_CHARACTER_CODEC,wchar)(
                          source_p, SourceEnd, drain_p, DrainEnd);
}
#endif
#endif /* ! defined(QUEX_OPTION_LEXEME_CONVERTERS_DISABLED) */

QUEX_NAMESPACE_MAIN_CLOSE

#endif /* __QUEX_INCLUDE_GUARD__LEXEME_I */
