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

QUEX_INLINE const char* 
QUEX_NAME(lexeme_to_pretty_char)(const QUEX_TYPE_LEXATOM* Lexeme, char*   buffer, size_t  BufferSize) 
/* Provides a somehow pretty-print of the text in the token. Note, that the buffer
 * in case of UTF8 should be 4bytes longer than the longest expected string.       */
{
    const QUEX_TYPE_LEXATOM*  LexemeEnd = Lexeme + (size_t)(QUEX_NAME(lexeme_length)(Lexeme)) + 1;

    QUEX_NAME(lexeme_to_char)(&Lexeme, LexemeEnd, &buffer, &buffer[BufferSize]);
    return buffer;
}

#ifndef __QUEX_OPTION_PLAIN_C
QUEX_INLINE const std::string 
QUEX_NAME(lexeme_to_pretty_std_string)(const std::basic_string<QUEX_TYPE_LEXATOM>& Text) 
/* Provides a somehow pretty-print of the text in the token.          */
{
    /* Compiler complains => Are you using 'wchar_t' or 'wistream' ? 
     * => Add file '$QUEX_PATH/quex/code_base/token/CppWChar.qx' to 
     *    the list of quex input files.                               */
    std::string             tmp = QUEX_CONVERTER_STRING(QUEX_SETTING_CHARACTER_CODEC,char)(Text);
    std::string::size_type  pos = 0;

    while( (pos = tmp.find("\n") ) != std::string::npos ) tmp.replace(pos, (size_t)1, "\\n");
    while( (pos = tmp.find("\t") ) != std::string::npos ) tmp.replace(pos, (size_t)1, "\\t");
    while( (pos = tmp.find("\r") ) != std::string::npos ) tmp.replace(pos, (size_t)1, "\\r");

    return tmp;
}

#endif

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
