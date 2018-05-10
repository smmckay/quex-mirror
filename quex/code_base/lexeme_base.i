/* -*- C++ -*- vim:set syntax=cpp: 
 * (C) Frank-Rene Schaefer    
 * ABSOLUTELY NO WARRANTY                                                     */
#ifndef __QUEX_INCLUDE_GUARD__LEXEME_BASE_I
#define __QUEX_INCLUDE_GUARD__LEXEME_BASE_I

$$INC: definitions$$
#if   ! defined(QUEX_INLINE)
#   error "QUEX_INLINE definition missing."
#endif

QUEX_NAMESPACE_MAIN_OPEN

extern QUEX_TYPE_LEXATOM QUEX_NAME(LexemeNull);

QUEX_INLINE size_t 
QUEX_NAME(lexeme_length)(const QUEX_TYPE_LEXATOM* Str)
{
    const QUEX_TYPE_LEXATOM* iterator = Str;
    while( *iterator ) ++iterator; 
    return (size_t)(iterator - Str);
}

QUEX_INLINE QUEX_TYPE_LEXATOM*
QUEX_NAME(lexeme_clone)(const QUEX_TYPE_LEXATOM* BeginP,
                        size_t                   Length)
{
    QUEX_TYPE_LEXATOM* result;

    if( ! BeginP || ! *BeginP ) {
        return &QUEX_NAME(LexemeNull);
    }
    
    result = (QUEX_TYPE_LEXATOM*)QUEXED(MemoryManager_allocate)(
                   sizeof(QUEX_TYPE_LEXATOM) * (Length + 1),
                   E_MemoryObjectType_TEXT);

    if( result ) {
        __QUEX_STD_memcpy((void*)result, (void*)BeginP, 
                          sizeof(QUEX_TYPE_LEXATOM) * (Length + 1));
    }
    else {
        result = &QUEX_NAME(LexemeNull); 
    }
    return result;
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

QUEX_NAMESPACE_MAIN_CLOSE

#endif /* __QUEX_INCLUDE_GUARD__LEXEME_BASE_I */
