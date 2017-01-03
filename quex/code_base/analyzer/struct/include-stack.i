/* -*- C++ -*- vim:set syntax=cpp:
 *
 * INCLUSION: Include lexical analysis of a new input stream.
 *
 * The current state of the lexical analyzer is stored on a stack in a
 * 'memento'. Then, it is initialized for analysis of the new input stream.
 * When the new input stream terminates, the memento is popped from the stack
 * and the according state is re-established. This process of 'nesting
 * analysis' may be used recursively.
 *
 * PUSH: 'include'
 *
 *   -- Include may fail, but it never throws an exception!
 *      Failure is notified by the '.error_code' flag.
 *   -- '.receive()' may always be called, but that function might return
 *      immediately if '.error_code' is not 'NONE'.
 *   -- The destructor can be called safely for any object that has been 
 *      'included'--even if the inclusion failed.
 *
 * POP: 'return from include'
 *
 *   -- never fails, never throws exceptions.
 *
 * (C) 2004-2017 Frank-Rene Schaefer
 *
 *  __QUEX_INCLUDE_GUARD__ANALYZER__STRUCT__INCLUDE_STACK_I may be undefined in case
 *    that multiple lexical analyzers are used. Then, the name of the
 *    QUEX_NAME(Accumulator) must be different.                               */
#ifndef  __QUEX_INCLUDE_GUARD__ANALYZER__STRUCT__INCLUDE_STACK_I
#define  __QUEX_INCLUDE_GUARD__ANALYZER__STRUCT__INCLUDE_STACK_I

#ifndef   QUEX_TYPE_ANALYZER
#   error "Macro QUEX_TYPE_ANALYZER must be defined before inclusion of this file."
#endif


QUEX_NAMESPACE_MAIN_OPEN

QUEX_INLINE bool
QUEX_NAME(include_push_file_name)(QUEX_TYPE_ANALYZER*     me,
                                  const char*             FileName, 
                                  QUEX_NAME(Converter)*   converter /* = 0 */)
{
    bool                    verdict_f;
    QUEX_NAME(ByteLoader)*  byte_loader;

    byte_loader = QUEX_NAME(ByteLoader_FILE_new_from_file_name)(FileName);
    if( ! byte_loader ) {
        goto ERROR_0;
    }

    QUEX_NAME(include_push)(this, ByteLoader, FileName, byte_loader, 
                            (QUEX_TYPE_CONVERTER_NEW)0); 
    if( ! me->error_code != QUEX_ENUM_ERROR_NONE ) {
        goto ERROR_1;
    }
    return true;

    /* ERROR CASES: Free Resources ___________________________________________*/
ERROR_1:
    /* ByteLoader: 'E_Ownership_LEXICAL_ANALYZER' lets 'filler->delete_self()'
     * take care of its free-ing.                                             */
ERROR_0:
    return false;
}

/* USE: byte_loader = QUEX_NAME(ByteLoader_FILE_new)(fh, BinaryModeF);
 *      byte_loader = QUEX_NAME(ByteLoader_stream_new)(istream_p, BinaryModeF);
 *      byte_loader = QUEX_NAME(ByteLoader_wstream_new)(wistream_p, BinaryModeF);
 *      ...
 *      Unit Test's StrangeStreams:
 *      byte_loader = QUEX_NAME(ByteLoader_stream_new)(strangestr_p, false);  */
QUEX_INLINE bool
QUEX_NAME(include_push_ByteLoader)(QUEX_TYPE_ANALYZER*     me,
                                   const char*             InputName,
                                   QUEX_NAME(ByteLoader)*  byte_loader,
                                   QUEX_NAME(Converter)*   converter /* = 0 */)
{
    bool                      verdict_f;
    QUEX_NAME(Converter)*     converter;
    QUEX_NAME(LexatomLoader)* filler;
    QUEX_TYPE_LEXATOM*        memory;
    QUEX_NAME(Buffer)         new_buffer_setup;
    QUEX_NAME(Asserts_construct)(CodecName);

    filler = QUEX_NAME(LexatomLoader_new)(byte_loader, converter);

    /* NOT: Abort/return if filler == 0 !!
     *      Incomplete construction => propper destruction IMPOSSIBLE!        */
    if( ! filler ) {
        goto ERROR_0;
    }

    memory = (QUEX_TYPE_LEXATOM*)QUEXED(MemoryManager_allocate)(
                       QUEX_SETTING_BUFFER_SIZE * sizeof(QUEX_TYPE_LEXATOM), 
                       E_MemoryObjectType_BUFFER_MEMORY);
    if( ! memory ) {
        goto ERROR_1;
    }

    QUEX_NAME(Buffer_construct)(&new_buffer_setup, filler,
                                memory, QUEX_SETTING_BUFFER_SIZE, 
                                (QUEX_TYPE_LEXATOM*)0,
                                E_Ownership_LEXICAL_ANALYZER);

    /* The 'new_buffer_setup' is only copied including the reference to the
     * new memory. However, the box object 'new_buffer_setup' is left alone.  */
    if( ! QUEX_NAME(include_push_all_but_buffer)(this, InputName, &new_buffer_setup) ) {
        goto ERROR_2;
    }
    return true;

    /* ERROR CASES: Free Resources ___________________________________________*/
ERROR_2:
    /* Memory 'E_Ownership_LEXICAL_ANALYZER' => destruct frees the memory.   */
    QUEX_NAME(Buffer_destruct)(&me->buffer);
ERROR_1:
    me->buffer.filler->delete_self(me->buffer.filler); 
    me->buffer.filler = (QUEX_NAME(LexatomLoader)*)0;
ERROR_0:
    return false;
}

QUEX_INLINE void
QUEX_NAME(include_push_memory)(QUEX_TYPE_ANALYZER* me,
                               const char*         InputName,
                               QUEX_TYPE_LEXATOM*  Memory,
                               const size_t        MemorySize,
                               QUEX_TYPE_LEXATOM*  EndOfFileP)
/* When memory is provided from extern, the 'external entity' is
 * responsible for filling it. There is no 'file/stream handle', no 'byte
 * loader', and 'no buffer filler'.                                           */
{
    QUEX_NAME(Buffer) new_buffer_setup;
    QUEX_ASSERT_MEMORY(Memory, MemorySize, EndOfFileP);

    QUEX_NAME(Buffer_construct)(&new_buffer_setup, 
                                (QUEX_NAME(LexatomLoader)*)0,
                                Memory, MemorySize, EndOfFileP,
                                E_Ownership_EXTERNAL);

    /* The 'new_buffer_setup' is only copied including the reference to the
     * new memory. However, the box object 'new_buffer_setup' is left alone.  */
    QUEX_NAME(include_push_all_but_buffer)(this,, InputName, &new_buffer_setup);

    /* ERROR: 'Buffer_destruct()' does not make sense, since the complete
     *         content is provided from extern. 
     * => User needs to check the 'error_code' after include_push.            */
}

QUEX_INLINE bool
QUEX_NAME(include_push_all_but_buffer)(QUEX_TYPE_ANALYZER* me 
                                       const char*         InputNameP,
                                       QUEX_NAME(Buffer)*  new_buffer_setup)
{
    QUEX_NAME(Memento)* memento;
   
    memento = (QUEX_NAME(Memento)*)QUEXED(MemoryManager_allocate)(
                                          sizeof(QUEX_NAME(Memento)), 
                                          E_MemoryObjectType_MEMENTO);
    if( ! memento ) {
        goto ERROR_0;
    }
#   ifndef __QUEX_OPTION_PLAIN_C
    /* Use placement 'new' for explicit call of constructor. 
     * Necessary in C++: Call to constructor for user defined members.       */
    new ((void*)memento) QUEX_NAME(Memento);
#   endif

    if( me->buffer.filler )
    {
        /* By default overtake the byte order reversion behavior of the 
         * including buffer.                                                 */
        new_buffer_setup->filler->_byte_order_reversion_active_f = \
                          me->buffer.filler->_byte_order_reversion_active_f;
    }

    /* 'memento->__input_name' points to previously allocated memory.        */
    memento->__input_name  = me->__input_name;
    me->__input_name       = (char*)0;                 /* Release ownership. */
    memento->_parent_memento                  = me->_parent_memento;
    memento->buffer                           = me->buffer;
    memento->__current_mode_p                 = me->__current_mode_p; 
    memento->current_analyzer_function        = me->current_analyzer_function;
#   if    defined(QUEX_OPTION_AUTOMATIC_ANALYSIS_CONTINUATION_ON_MODE_CHANGE) \
       || defined(QUEX_OPTION_ASSERTS)
    memento->DEBUG_analyzer_function_at_entry = me->DEBUG_analyzer_function_at_entry;
#   endif
    __QUEX_IF_COUNT(memento->counter          = me->counter);

    me->buffer                                = *new_buffer_setup;
    __QUEX_IF_COUNT(QUEX_NAME(Counter_construct)(&me->counter); )

    /* Deriberately not subject to include handling:
     *    -- Mode stack.
     *    -- Token and token queues.
     *    -- Post categorizer.                                               */
    if( ! QUEX_MEMBER_FUNCTION_CALLO2(user_memento_pack, InputNameP, memento) ) {
        goto ERROR_1;
    }
    else if( ! QUEX_NAME(input_name_set)(me, InputNameP) ) {
        goto ERROR_1;
    }

    /* Put memento on stack AFTER user has done to it its duties.            */
    me->_parent_memento = memento;

    return true;

    /* ERROR CASES: Free Resources __________________________________________*/
ERROR_1:
    QUEXED(MemoryManager_free)(memento, E_MemoryObjectType_MEMENTO);
ERROR_0:
    return false;
}   

QUEX_INLINE bool
QUEX_NAME(include_pop)(QUEX_TYPE_ANALYZER* me)
/* RETURNS: true, if there was a memento that has been restored. 
 *          false, else.                                                     */
{
    QUEX_NAME(Memento)* memento;
    /* Not included? return 'false' to indicate we're on the top level       */
    if( ! me->_parent_memento ) return false;                             
                                                                            
    /* Buffer_destruct() takes care of propper destructor calls for byte-
     * loaders, buffer fillers, and converters.                              */
    QUEX_NAME(Buffer_destruct)(&me->buffer);                              

    memento             = me->_parent_memento;
    me->_parent_memento = memento->_parent_memento;
    /* memento_unpack():                                                    
     *    => Current mode                                                   
     *           => __current_mode_p                                        
     *              current_analyzer_function                                           
     *              DEBUG_analyzer_function_at_entry                                       
     *    => Line/Column Counters                                           
     *                                                                      
     * Unchanged by memento_unpack():                                       
     *    -- Mode stack                                                     
     *    -- Tokens and token queues.                                       
     *    -- Accumulator.                                                   
     *    -- Post categorizer.                                              
     *    -- File handle by constructor                                      */
                                                                            
    /* Copy Back of content that was stored upon inclusion.                  */

    if( me->__input_name ) {
        QUEXED(MemoryManager_free)(me->__input_name, E_MemoryObjectType_BUFFER_MEMORY);
    }
    /* 'memento->__input_name' points to previously allocated memory.        
     * 'me->__input_name' takes ownership again over allocated memory.       */
    me->__input_name                     = memento->__input_name;
    me->buffer                           = memento->buffer;
    me->__current_mode_p                 = memento->__current_mode_p; 
    me->current_analyzer_function        = memento->current_analyzer_function;
#   if    defined(QUEX_OPTION_AUTOMATIC_ANALYSIS_CONTINUATION_ON_MODE_CHANGE) \
       || defined(QUEX_OPTION_ASSERTS)
    me->DEBUG_analyzer_function_at_entry = memento->DEBUG_analyzer_function_at_entry;
#   endif
    __QUEX_IF_COUNT(me->counter          = memento->counter);

    QUEX_MEMBER_FUNCTION_CALLO1(user_memento_unpack,memento);

#   ifndef __QUEX_OPTION_PLAIN_C
    /* Counterpart to placement new: Explicit destructor call.
     * Necessary in C++: Trigger call to destructor for user defined members.*/
    memento->~QUEX_NAME(Memento_tag)();
#   endif

    QUEXED(MemoryManager_free)((void*)memento, E_MemoryObjectType_MEMENTO); 

    /* Return to including file succesful                                    */
    return true;
}
     
QUEX_INLINE void
QUEX_NAME(include_stack_delete)(QUEX_TYPE_ANALYZER* me)
{
    while( QUEX_MEMBER_FUNCTION_CALLO(include_pop) );
}

QUEX_INLINE bool
QUEX_NAME(include_detect_recursion)(QUEX_TYPE_ANALYZER* me,
                                    const char*         InputName)
{
    QUEX_NAME(Memento)* iterator;
    for(iterator = me->_parent_memento; iterator ; 
        iterator = iterator->_parent_memento ) {
        if( __QUEX_STD_strcmp(iterator->__input_name, InputName) == 0 ) {
            return true;
        }
    }
    return false;
}

QUEX_NAMESPACE_MAIN_CLOSE

#endif /*  __QUEX_INCLUDE_GUARD__ANALYZER__STRUCT__INCLUDE_STACK_I */
