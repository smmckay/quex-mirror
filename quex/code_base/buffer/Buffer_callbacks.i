/* vim:set ft=c: -*- C++ -*- */
#ifndef __QUEX_INCLUDE_GUARD__BUFFER__BUFFER_CALLBACKS_I
#define __QUEX_INCLUDE_GUARD__BUFFER__BUFFER_CALLBACKS_I

#include <quex/code_base/buffer/Buffer>

QUEX_NAMESPACE_MAIN_OPEN

QUEX_INLINE void  
QUEX_NAME(Buffer_callbacks_set)(QUEX_NAME(Buffer)* me,
                                     void   (*on_before_change)(void* aux),
                                     void   (*on_overflow)(void*  aux),
                                     void*  aux)
{
    me->event.on_buffer_before_change = on_before_change;
    me->event.on_buffer_overflow      = on_overflow;
    me->event.aux                     = aux;
}

QUEX_INLINE void
QUEX_NAME(Buffer_callbacks_on_buffer_before_change)(QUEX_NAME(Buffer)* me)
{
    QUEX_ASSERT_BUFFER_INVARIANCE_SETUP(bi, me);
    if( me->_backup_lexatom_index_of_lexeme_start_p != (QUEX_TYPE_STREAM_POSITION)-1 ) {
        /* Callbacks must have been called bedore the lexeme start position has
         * been back-uped. No pointer positions inside the buffer are referred
         * to by the user while lexeme start is not present inside the buffer.*/
    }
    else if( me->event.on_buffer_before_change ) {
        me->event.on_buffer_before_change(me->event.aux); 
    }
    QUEX_ASSERT_BUFFER_INVARIANCE_VERIFY_SAME(bi, me);
}

QUEX_INLINE void
QUEX_NAME(Buffer_callbacks_on_buffer_overflow)(QUEX_NAME(Buffer)* me)
{
    QUEX_ASSERT_BUFFER_INVARIANCE_SETUP(bi, me);
    if( me->event.on_buffer_overflow ) {
        me->event.on_buffer_overflow(me->event.aux);
    }
    QUEX_ASSERT_BUFFER_INVARIANCE_VERIFY(bi, me);
}

QUEX_NAMESPACE_MAIN_CLOSE

#endif /* __QUEX_INCLUDE_GUARD__BUFFER__BUFFER_CALLBACKS_I */
