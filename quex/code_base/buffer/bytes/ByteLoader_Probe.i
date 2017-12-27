/* vim: set ft=c:
 * (C) Frank-Rene Schaefer */
#ifndef  __QUEX_INCLUDE_GUARD__BUFFER__BYTES__BYTE_LOADER_PROBE_I
#define  __QUEX_INCLUDE_GUARD__BUFFER__BYTES__BYTE_LOADER_PROBE_I

#include <quex/code_base/MemoryManager>
#include "quex/code_base/buffer/bytes/ByteLoader_Probe"
#include <malloc.h> // DEBUG

QUEX_NAMESPACE_MAIN_OPEN

QUEX_INLINE void                       QUEX_NAME(ByteLoader_Probe_construct)(QUEX_NAME(ByteLoader_Probe)* me,
                                                                             QUEX_NAME(ByteLoader)*       source,
                                                                             void*                        reference_object);
QUEX_INLINE QUEX_TYPE_STREAM_POSITION  QUEX_NAME(ByteLoader_Probe_tell)(QUEX_NAME(ByteLoader)* me);
QUEX_INLINE void                       QUEX_NAME(ByteLoader_Probe_seek)(QUEX_NAME(ByteLoader)*     me, 
                                                                        QUEX_TYPE_STREAM_POSITION  Pos);
QUEX_INLINE size_t                     QUEX_NAME(ByteLoader_Probe_load)(QUEX_NAME(ByteLoader)* me, 
                                                                        void*                  buffer, 
                                                                        const size_t           ByteN, 
                                                                        bool*                  end_of_stream_f);
QUEX_INLINE void                       QUEX_NAME(ByteLoader_Probe_delete_self)(QUEX_NAME(ByteLoader)* me);
QUEX_INLINE void                       QUEX_NAME(ByteLoader_Probe_print_this)(QUEX_NAME(ByteLoader)* me);
QUEX_INLINE bool                       QUEX_NAME(ByteLoader_Probe_compare_handle)(const QUEX_NAME(ByteLoader)* alter_ego_A, 
                                                                                  const QUEX_NAME(ByteLoader)* alter_ego_B);

QUEX_INLINE QUEX_NAME(ByteLoader)*    
QUEX_NAME(ByteLoader_Probe_new)(QUEX_NAME(ByteLoader)* source,
                                void*                  reference_object)
    /* ByteLoader takes over ownership over 'source' */
{
    QUEX_NAME(ByteLoader_Probe)* me;
   
    me = (QUEX_NAME(ByteLoader_Probe)*)QUEXED(MemoryManager_allocate)(
                   sizeof(QUEX_NAME(ByteLoader_Probe)),
                   E_MemoryObjectType_BYTE_LOADER);

    if( ! me ) return (QUEX_NAME(ByteLoader)*)0;

    QUEX_NAME(ByteLoader_Probe_construct)(me, source, reference_object);

    return &me->base;
}

QUEX_INLINE void
QUEX_NAME(ByteLoader_Probe_construct)(QUEX_NAME(ByteLoader_Probe)* me, 
                                      QUEX_NAME(ByteLoader)*       source,
                                      void*                        reference_object)
{
    __QUEX_STD_memset((void*)me, 0, sizeof(*me));

    me->source           = source;
    me->reference_object = reference_object;

    QUEX_NAME(ByteLoader_construct)(&me->base,
                         QUEX_NAME(ByteLoader_Probe_tell),
                         QUEX_NAME(ByteLoader_Probe_seek),
                         QUEX_NAME(ByteLoader_Probe_load),
                         QUEX_NAME(ByteLoader_Probe_delete_self),
                         QUEX_NAME(ByteLoader_Probe_print_this),
                         QUEX_NAME(ByteLoader_Probe_compare_handle));
}

QUEX_INLINE void    
QUEX_NAME(ByteLoader_Probe_delete_self)(QUEX_NAME(ByteLoader)* alter_ego)
{
    QUEX_NAME(ByteLoader_Probe)* me = (QUEX_NAME(ByteLoader_Probe)*)(alter_ego);

    if( me->on_delete_self ) {
        me->on_delete_self(me);
    }
    me->source->delete_self(me->source);

    QUEXED(MemoryManager_free)((void*)me->source, E_MemoryObjectType_BYTE_LOADER);
    QUEXED(MemoryManager_free)((void*)me, E_MemoryObjectType_BYTE_LOADER);

}

QUEX_INLINE QUEX_TYPE_STREAM_POSITION    
QUEX_NAME(ByteLoader_Probe_tell)(QUEX_NAME(ByteLoader)* alter_ego)            
{ 
    QUEX_NAME(ByteLoader_Probe)* me = (QUEX_NAME(ByteLoader_Probe)*)(alter_ego);
    QUEX_TYPE_STREAM_POSITION    position;

    position = me->source->tell(me->source);

    ++(me->tell_n);
    me->position_last_tell = position;

    if( me->on_tell ) {
        return me->on_tell(me, position);
    }

    return position;
}

QUEX_INLINE void    
QUEX_NAME(ByteLoader_Probe_seek)(QUEX_NAME(ByteLoader)* alter_ego, QUEX_TYPE_STREAM_POSITION Pos) 
{ 
    QUEX_NAME(ByteLoader_Probe)* me = (QUEX_NAME(ByteLoader_Probe)*)(alter_ego);
    QUEX_TYPE_STREAM_POSITION    position;

    if( me->on_seek ) {
        position = me->on_seek(me, Pos);
    }
    else {
        position = Pos;
    }

    me->source->seek(me->source, position);

    ++(me->seek_n);
    me->position_last_seek = position;
}

QUEX_INLINE size_t  
QUEX_NAME(ByteLoader_Probe_load)(QUEX_NAME(ByteLoader)*   alter_ego, 
                                 void*                    buffer, 
                                 const size_t             ByteN, 
                                 bool*                    end_of_stream_f) 
{ 
    QUEX_NAME(ByteLoader_Probe)* me = (QUEX_NAME(ByteLoader_Probe)*)(alter_ego);
    size_t                       loaded_byte_n;
    size_t                       byte_n;

    if( me->on_before_load ) {
        byte_n = me->on_before_load(me, ByteN);
    }
    else {
        byte_n = ByteN;
    }

    loaded_byte_n = me->source->load(me->source, buffer, byte_n, end_of_stream_f);

    if( me->on_after_load ) {
        loaded_byte_n = me->on_after_load(me, buffer, loaded_byte_n, end_of_stream_f);
    }

    ++(me->load_n);
    me->loaded_byte_n += loaded_byte_n;

    return loaded_byte_n;
}

QUEX_INLINE bool  
QUEX_NAME(ByteLoader_Probe_compare_handle)(const QUEX_NAME(ByteLoader)* alter_ego_A, 
                                                      const QUEX_NAME(ByteLoader)* alter_ego_B) 
/* RETURNS: true  -- if A and B point to the same Memory object.
 *          false -- else.                                                   */
{ 
    const QUEX_NAME(ByteLoader_Probe)* me = (QUEX_NAME(ByteLoader_Probe)*)(alter_ego_A);
    bool                                          result;

    result = me->source->compare_handle(me->source, alter_ego_B);

    return result;
}

QUEX_INLINE void                       
QUEX_NAME(ByteLoader_Probe_print_this)(QUEX_NAME(ByteLoader)* alter_ego)
{
    QUEX_NAME(ByteLoader_Probe)* me = (QUEX_NAME(ByteLoader_Probe)*)(alter_ego);

    __QUEX_STD_printf("        remote_controlled: {\n");
    me->source->print_this(me->source);
    __QUEX_STD_printf("        }\n");
}

QUEX_NAMESPACE_MAIN_CLOSE

#endif /* __QUEX_INCLUDE_GUARD__BUFFER__BYTES__BYTE_LOADER_PROBE_I */
