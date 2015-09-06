/* (C) Frank-Rene Schaefer */
#ifndef QUEX_INCLUDE_GUARD_BYTE_LOADER_I
#define QUEX_INCLUDE_GUARD_BYTE_LOADER_I

QUEX_INLINE QUEX_TYPE_STREAM_POSITION
ByteLoader_tell(ByteLoader* me);

QUEX_INLINE void
ByteLoader_seek(ByteLoader* me, QUEX_TYPE_STREAM_POSITION Position);

QUEX_INLINE void
ByteLoader_construct(ByteLoader* me, 
                     QUEX_TYPE_STREAM_POSITION  (*tell)(ByteLoader* me),
                     void                       (*seek)(ByteLoader* me, QUEX_TYPE_STREAM_POSITION Pos),
                     size_t                     (*load)(ByteLoader*, void*, const size_t),
                     void                       (*delete_self)(ByteLoader*),
                     bool                       (*compare_handle)(const ByteLoader*, const ByteLoader*))
{
    me->tell           = ByteLoader_tell;
    me->seek           = ByteLoader_seek;
    me->derived_tell   = tell;
    me->derived_seek   = seek;
    me->load           = load;
    me->delete_self    = delete_self;
    me->compare_handle = compare_handle;

    me->handle_ownership = E_Ownership_EXTERNAL; /* Default */
    me->ownership        = E_Ownership_EXTERNAL; /* Default */

    me->initial_position = tell(me);
}

QUEX_INLINE QUEX_TYPE_STREAM_POSITION
ByteLoader_tell(ByteLoader* me)
{
    return me->derived_tell(me) - me->initial_position;
}

QUEX_INLINE void
ByteLoader_seek(ByteLoader* me, QUEX_TYPE_STREAM_POSITION Position)
{
    me->derived_seek(me, Position + me->initial_position);
}

QUEX_INLINE bool
ByteLoader_compare(const ByteLoader* A, const ByteLoader* B)
{
    /* If two ByteLoader classes use the same 'load()' function, then they 
     * should not be different. For example, it does not make sense to have
     * two loaders implementing stdandard libraries 'fread()' interface.     
     *
     * Further, it is always safe to return 'false'.                         */
    if( A->load != B->load ) {
        return false;
    }

    /* The 'compare_handle()' function can now safely cast the two pointers
     * to its pointer type.                                                  */
    return A->compare_handle(A, B);
}

QUEX_INLINE void  
ByteLoader_delete(ByteLoader** me)
{
    if( ! *me )                                                 {}
    else if( (*me)->ownership != E_Ownership_LEXICAL_ANALYZER ) {}
    else if( (*me)->delete_self )                               (*me)->delete_self(*me);
    (*me) = (ByteLoader*)0;
}

#include <quex/code_base/buffer/loader/ByteLoader_FILE.i>
#include <quex/code_base/buffer/loader/ByteLoader_stream.i>
#if 0
#   include <quex/buffer/loader/ByteLoader_POSIX.i>    /* (tm) */
#   include <quex/buffer/loader/ByteLoader_FreeRTOS.i> /* (tm) */
#   include <quex/buffer/loader/ByteLoader_PalmOS.i>   /* (tm) */
#endif

#endif /* QUEX_INCLUDE_GUARD_BYTE_LOADER_I */