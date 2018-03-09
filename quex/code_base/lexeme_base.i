/* -*- C++ -*- vim:set syntax=cpp: 
 * (C) Frank-Rene Schaefer    
 * ABSOLUTELY NO WARRANTY                                                     */
#ifndef __QUEX_INCLUDE_GUARD__LEXEME_BASE_I
#define __QUEX_INCLUDE_GUARD__LEXEME_BASE_I

$$INC: definitions$$
#if   ! defined(QUEX_INLINE)
#   error "QUEX_INLINE definition missing."
#elif ! defined(QUEX_NAME_TOKEN)
#   error "QUEX_NAME_TOKEN definition missing."
#elif ! defined(QUEX_TYPE_LEXATOM)
#   error "QUEX_TYPE_LEXATOM definition missing."
#endif

QUEX_NAMESPACE_TOKEN_OPEN

extern QUEX_TYPE_LEXATOM   QUEX_NAME_TOKEN(LexemeNull);

QUEX_INLINE size_t 
QUEX_NAME_TOKEN(lexeme_length)(const QUEX_TYPE_LEXATOM* Str)
{
    const QUEX_TYPE_LEXATOM* iterator = Str;
    while( *iterator != 0 ) ++iterator; 
    return (size_t)(iterator - Str);
}

QUEX_INLINE QUEX_TYPE_LEXATOM*
QUEX_NAME_TOKEN(lexeme_clone)(const QUEX_TYPE_LEXATOM* BeginP,
                              size_t                   Length)
{
    QUEX_TYPE_LEXATOM* result;

    if( BeginP == &QUEX_NAME_TOKEN(LexemeNull) || ! BeginP ) {
        return &QUEX_NAME_TOKEN(LexemeNull);
    }
    
    result = (QUEX_TYPE_LEXATOM*)QUEXED(MemoryManager_allocate)(
                   sizeof(QUEX_TYPE_LEXATOM) * (Length + 1),
                   E_MemoryObjectType_TEXT);

    if( result ) {
        __QUEX_STD_memcpy((void*)result, (void*)BeginP, 
                          sizeof(QUEX_TYPE_LEXATOM) * (Length + 1));
    }
    else {
        result = &QUEX_NAME_TOKEN(LexemeNull); 
    }
    return result;
}

QUEX_INLINE size_t 
QUEX_NAME_TOKEN(lexeme_compare)(const QUEX_TYPE_LEXATOM* it0, 
                                const QUEX_TYPE_LEXATOM* it1)
{
    for(; *it0 == *it1; ++it0, ++it1) {
        /* Both letters are the same and == 0?
         * => both reach terminall zero without being different.              */
        if( *it0 == 0 ) return 0;
    }
    return (size_t)(*it0) - (size_t)(*it1);
}

QUEX_NAMESPACE_TOKEN_CLOSE

#endif /* __QUEX_INCLUDE_GUARD__LEXEME_BASE_I */
