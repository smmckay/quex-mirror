/* -*- C++ -*- vim: set syntax=cpp: */
#ifndef QUEX_INCLUDE_GUARD__BUFFER__ASSERTS_I
#define QUEX_INCLUDE_GUARD__BUFFER__ASSERTS_I

$$INC: buffer/asserts$$
$$INC: buffer/Buffer$$

#ifndef QUEX_OPTION_ASSERTS_EXT

#else

QUEX_NAMESPACE_MAIN_OPEN

QUEX_INLINE void
QUEX_NAME(BUFFER_ASSERT_pointers_in_range_core)(const QUEX_NAME(Buffer)* B)                                      
/* Check whether _read_p and _lexeme_start_p are in ther appropriate range. */
{                                                                                    
    __quex_assert( (B) != 0x0 );                                                     
    if( ! (*B)._memory._front && ! (*B)._memory._back ) {                    
        return;
    }

    __quex_assert((*B).begin(B)        <  (*B).content_space_end(B));                     
    __quex_assert((*B).content_end(B)  >= (*B).content_begin(B));          
    __quex_assert((*B).content_end(B)  <= (*B).content_space_end(B));               

    __quex_assert((*B)._read_p         >= (*B).begin(B));                
    __quex_assert((*B)._read_p         <= (*B).content_end(B));              
    __quex_assert((*B)._lexeme_start_p >= (*B).begin(B));                
    __quex_assert((*B)._lexeme_start_p <= (*B).content_end(B));              
}

QUEX_INLINE void
QUEX_NAME(BUFFER_ASSERT_limit_codes_in_place_core)(const QUEX_NAME(Buffer)* B)                                            
{
    if( ! (*B)._memory._front && ! (*B)._memory._back ) {                    
        return;
    }
    __quex_assert((*B).begin(B)[0]              == QUEX_SETTING_BUFFER_LIMIT_CODE);    
    __quex_assert((*B).content_space_end(B)[0]  == QUEX_SETTING_BUFFER_LIMIT_CODE);    
    __quex_assert((*B).content_end(B)[0]        == QUEX_SETTING_BUFFER_LIMIT_CODE);   
}

QUEX_INLINE void
QUEX_NAME(BUFFER_ASSERT_CONSISTENCY_core)(const QUEX_NAME(Buffer)* B)                                            
{                                                                                    
    const QUEX_NAME(Buffer)* focus;
    if( ! B ) return;
    __quex_assert(   B->input.lexatom_index_begin == -1
                  || B->input.lexatom_index_begin >= 0);
    __quex_assert(   B->input.lexatom_index_end_of_stream == -1 
                  || B->input.lexatom_index_end_of_stream >= B->input.lexatom_index_begin);
    QUEX_NAME(BUFFER_ASSERT_pointers_in_range_core)(B);                                              
    QUEX_NAME(BUFFER_ASSERT_limit_codes_in_place_core)(B);

    if( B->_memory.ownership == E_Ownership_INCLUDING_BUFFER ) {
        __quex_assert(0 != B->_memory.including_buffer);
        /* No cyclic nesting of buffers.                                      */
        for(focus = B; 0 != focus->_memory.including_buffer; ) { 
            __quex_assert(focus->_memory.ownership == E_Ownership_INCLUDING_BUFFER);
            focus = focus->_memory.including_buffer;
            __quex_assert(focus != B);
        }
        /* NOT:
         *     __quex_assert(&including_buffer->_memory._back[1] == &front[0]);
         * BECAUSE: (1) Pointer adaption happens from back to front.
         *              => consistency could not be checked during adaption.
         *          (2) Future versions may store more in the buffer region.  */
    }
    else {
        __quex_assert(0 == B->_memory.including_buffer);
    }
    QUEX_BUFFER_ASSERT_MEMBER_FUNCTIONS(B);
}

QUEX_INLINE void
QUEX_NAME(Buffer_member_functions_assert)(const QUEX_NAME(Buffer)* me)
{
    __quex_assert(me->fill                == QUEX_NAME(Buffer_fill));
    __quex_assert(me->fill_prepare        == QUEX_NAME(Buffer_fill_prepare));
    __quex_assert(me->fill_finish         == QUEX_NAME(Buffer_fill_finish));

    __quex_assert(me->begin               == QUEX_NAME(Buffer_memory_begin));
    __quex_assert(me->end                 == QUEX_NAME(Buffer_memory_end));
    __quex_assert(me->size                == QUEX_NAME(Buffer_memory_size));

    __quex_assert(me->content_space_end   == QUEX_NAME(Buffer_memory_content_space_end));
    __quex_assert(me->content_space_size  == QUEX_NAME(Buffer_memory_content_space_size));

    __quex_assert(me->content_begin       == QUEX_NAME(Buffer_memory_content_begin));
    __quex_assert(me->content_end         == QUEX_NAME(Buffer_memory_content_end));
    __quex_assert(me->content_size        == QUEX_NAME(Buffer_memory_content_size));
}

QUEX_INLINE void
QUEX_NAME(BUFFER_ASSERT_NO_BUFFER_LIMIT_CODE_core)(const QUEX_TYPE_LEXATOM* Begin, 
                                                   const QUEX_TYPE_LEXATOM* End)
{
    const QUEX_TYPE_LEXATOM* iterator = 0x0;
    __quex_assert(Begin <= End);

    for(iterator = Begin; iterator != End; ++iterator) {
        if( *iterator != QUEX_SETTING_BUFFER_LIMIT_CODE ) continue;

        if( iterator == Begin ) {
            QUEX_ERROR_EXIT("Buffer limit code character appeared as first character in buffer.\n"
                            "This is most probably a load failure.\n");
        } else {
            QUEX_ERROR_EXIT("Buffer limit code character appeared as normal text content.\n");
        }
    }
}

QUEX_NAMESPACE_MAIN_CLOSE

#endif

#endif /* QUEX_INCLUDE_GUARD__BUFFER__ASSERTS_I */

