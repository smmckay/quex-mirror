/* -*- C++ -*- vim:set syntax=cpp:
 *
 * CONSTRUCTION: Setup a lexical analyzer.
 *
 *   -- Construction may fail, but it never throws an exception!
 *      Failure is notified by the '.error_code' flag.
 *   -- '.receive()' may always be called, but that function might return
 *      immediately if '.error_code' is not 'NONE'.
 *   -- The destructor can be called safely for any object that has been 
 *      'constructed'--even if the construction failed.
 *
 * FAILURE => Lexer is in DYSFUNCTIONAL state.
 *
 *  .error_code == 'NONE': All resources have been allocated. Lexical 
 *                         analysis may start.
 *
 *  .error_code != 'NONE': Error during resource allocation.
 *                         Lexical analysis will immediately send 
 *                         'TERMINATION' token.
 *                         The lexer must (and can) be destructed.
 *
 * DESTRUCTION:
 *
 *   -- never fails, never throws exceptions.
 *
 * (C) 2005-2017 Frank-Rene Schaefer
 * ABSOLUTELY NO WARRANTY                                                     */
#ifndef  __QUEX_INCLUDE_GUARD__ANALYZER__STRUCT__CONSTRUCTOR_I
#define  __QUEX_INCLUDE_GUARD__ANALYZER__STRUCT__CONSTRUCTOR_I

#include <quex/code_base/buffer/Buffer.i>
#include <quex/code_base/buffer/lexatoms/LexatomLoader.i>
#include <quex/code_base/analyzer/struct/include-stack>

QUEX_NAMESPACE_MAIN_OPEN
                    
QUEX_INLINE void   QUEX_NAME(Asserts_user_memory)(QUEX_TYPE_ANALYZER*  me,
                                                  QUEX_TYPE_LEXATOM*   BufferMemoryBegin, 
                                                  size_t               BufferMemorySize,
                                                  QUEX_TYPE_LEXATOM*   BufferEndOfContentP /* = 0 */);
QUEX_INLINE void   QUEX_NAME(Asserts_construct)(const char* CodecName);
QUEX_INLINE void   QUEX_NAME(Tokens_construct)(QUEX_TYPE_ANALYZER* me);
QUEX_INLINE void   QUEX_NAME(Tokens_reset)(QUEX_TYPE_ANALYZER* me);
QUEX_INLINE void   QUEX_NAME(Tokens_destruct)(QUEX_TYPE_ANALYZER* me);
QUEX_INLINE void   QUEX_NAME(ModeStack_construct)(QUEX_TYPE_ANALYZER* me);

QUEX_INLINE void
QUEX_NAME(from_file_name)(QUEX_TYPE_ANALYZER*     me,
                          const char*             FileName, 
                          QUEX_NAME(Converter)*   converter /* = 0 */,
                          const char*             CodecName /* = 0 */)
{
    QUEX_NAME(ByteLoader)*   byte_loader;

    byte_loader = QUEX_NAME(ByteLoader_FILE_new_from_file_name)(FileName);

    if( ! byte_loader ) {
        me->error_code = QUEX_ENUM_ERROR_ALLOCATION_BYTE_LOADER;
        goto ERROR_0;
    }

    QUEX_NAME(from_ByteLoader)(me, byte_loader, converter, CodecName); 

    if( me->error_code != QUEX_ENUM_ERROR_NONE ) {
        goto ERROR_1;
    }

ERROR_1:
    /* from_ByteLoader() error: byte_loader->ownership = LEXICAL_ANALYZER.
     *                          => byte_loader is already deleted.            */
ERROR_0:
    QUEX_NAME(mark_resources_as_absent)(me);
}

/* USE: byte_loader = QUEX_NAME(ByteLoader_FILE_new)(fh, BinaryModeF);
 *      byte_loader = QUEX_NAME(ByteLoader_stream_new)(istream_p, BinaryModeF);
 *      byte_loader = QUEX_NAME(ByteLoader_wstream_new)(wistream_p, BinaryModeF);
 *      ...
 *      Unit Test's StrangeStreams:
 *      byte_loader = QUEX_NAME(ByteLoader_stream_new)(strangestr_p, false);  */

QUEX_INLINE void
QUEX_NAME(from_ByteLoader)(QUEX_TYPE_ANALYZER*     me,
                           QUEX_NAME(ByteLoader)*  byte_loader,
                           QUEX_NAME(Converter)*   converter /* = 0 */,
                           const char*             CodecName) 
{
    QUEX_MAP_THIS_TO_ME(QUEX_TYPE_ANALYZER)
    QUEX_NAME(Converter)*     converter = (QUEX_NAME(Converter)*)0;
    QUEX_NAME(LexatomLoader)* filler;
    QUEX_TYPE_LEXATOM*        memory;
    QUEX_NAME(Asserts_construct)(CodecName);

    /* NEW: Filler.                                                           */
    filler = QUEX_NAME(LexatomLoader_new)(byte_loader, converter);

    if( ! filler ) {
        me->error_code = QUEX_ENUM_ERROR_ALLOCATION_LEXATOM_LOADER;
        goto ERROR_0;
    }

    /* NEW: Memory.                                                           */
    memory = (QUEX_TYPE_LEXATOM*)QUEXED(MemoryManager_allocate)(
                       QUEX_SETTING_BUFFER_SIZE * sizeof(QUEX_TYPE_LEXATOM), 
                       E_MemoryObjectType_BUFFER_MEMORY);
    if( ! memory ) {
        me->error_code = QUEX_ENUM_ERROR_ALLOCATION_BUFFER_MEMORY;
        goto ERROR_1;
    }

    QUEX_NAME(Buffer_construct)(&me->buffer, filler,
                                memory, QUEX_SETTING_BUFFER_SIZE, 
                                (QUEX_TYPE_LEXATOM*)0,
                                E_Ownership_LEXICAL_ANALYZER);

    QUEX_NAME(construct_all_but_buffer)(me, (const char*)"<unknown>");
    if( me->error_code != QUEX_ENUM_ERROR_NONE ) {
        goto ERROR_2;
    }

    return;

    /* ERROR CASES: Free Resources __________________________________________*/
ERROR_2:
    QUEX_NAME(Buffer_destruct)(&me->buffer);
ERROR_1:
    me->buffer.filler->delete_self(me->buffer.filler); 
    QUEX_NAME(mark_resources_as_absent)(me);
    return;
ERROR_0:
    byte_loader->delete_self(byte_loader);
    QUEX_NAME(mark_resources_as_absent)(me);
    return;
}

QUEX_INLINE void
QUEX_NAME(from_memory)(QUEX_TYPE_ANALYZER* me,
                       QUEX_TYPE_LEXATOM*  Memory,
                       const size_t        MemorySize,
                       QUEX_TYPE_LEXATOM*  EndOfFileP)

/* When memory is provided from extern, the 'external entity' is responsible
 * for filling it. There is no 'file/stream handle', no 'ByteLoader', and no
 * 'LexatomLoader'.                                                           */
{
    QUEX_MAP_THIS_TO_ME(QUEX_TYPE_ANALYZER)
    QUEX_ASSERT_MEMORY(Memory, MemorySize, EndOfFileP);

    QUEX_NAME(Buffer_construct)(&me->buffer, 
                                (QUEX_NAME(LexatomLoader)*)0,
                                Memory, MemorySize, EndOfFileP,
                                E_Ownership_EXTERNAL);

    if( ! QUEX_NAME(construct_all_but_buffer)(me, (const char*)"<memory>") ) {
        QUEX_NAME(Buffer_destruct)(&me->buffer); 
        QUEX_NAME(mark_resources_as_absent)(me);
    }

    /* No further distinguishing between success and error. User might consider
     * '.error_code' later.                                                   */
}

QUEX_INLINE bool
QUEX_NAME(construct_all_but_buffer)(QUEX_TYPE_ANALYZER* me, const char* InputNameP)
/* Constructs anything but 'LexatomLoader' and 'Buffer'.
 * 
 * RETURNS: true, for success.
 *          false, for failure.                                               */
{
    QUEX_MAP_THIS_TO_ME(QUEX_TYPE_ANALYZER)

    __QUEX_IF_INCLUDE_STACK(me->_parent_memento = (QUEX_NAME(Memento)*)0);

    if( ! QUEX_NAME(Tokens_construct)(me) ) {
        goto ERROR_0;
    }
    else if( ! QUEX_NAME(ModeStack_construct)(me) ) {
        goto ERROR_1;
    }
#   ifdef QUEX_OPTION_STRING_ACCUMULATOR
    else if( ! QUEX_NAME(Accumulator_construct)(&me->accumulator, me) ) {
        me->error_code = QUEX_ENUM_ERROR_CONSTRUCT_ACCUMULATOR;
        goto ERROR_2;
    }
#   endif
#   ifdef QUEX_OPTION_POST_CATEGORIZER
    else if( ! QUEX_NAME(PostCategorizer_construct)(&me->post_categorizer) ) {
        me->error_code = QUEX_ENUM_ERROR_CONSTRUCT_POST_CATEGORIZER;
        goto ERROR_3;
    }
#   endif
#   ifdef QUEX_OPTION_COUNT
    else if( ! QUEX_NAME(Counter_construct)(&me->counter) ) {
        me->error_code = QUEX_ENUM_ERROR_CONSTRUCT_COUNTER;
        goto ERROR_4;
    }
#   endif

    /* A user's mode change callbacks may be called as a consequence of the 
     * call to 'set_mode_brutally_by_id()'. The current mode must be set to '0'
     * so that the user may detect whether this is the first mode transition.*/
    me->__current_mode_p = (QUEX_NAME(Mode)*)0;
    QUEX_NAME(set_mode_brutally_by_id)(me, __QUEX_SETTING_INITIAL_LEXER_MODE_ID);

    me->__input_name = (char*)0;
    if( ! QUEX_MEMBER_FUNCTION_CALLO1(input_name_set, InputNameP) ) {
        me->error_code = QUEX_ENUM_ERROR_INPUT_NAME_SET;
        goto ERROR_5;
    }
    else if( ! QUEX_MEMBER_FUNCTION_CALLO(user_constructor) ) {
        me->error_code = QUEX_ENUM_ERROR_USER_CONSTRUCTOR;
        goto ERROR_5;
    }

    me->error_code = QUEX_ENUM_ERROR_NONE;
    return true;

    /* ERROR CASES: Free Resources ___________________________________________*/
ERROR_6:
    (void)QUEX_NAME(input_name_set)(me, (const char*)0);
ERROR_5:
    /* NO ALLOCATED RESOURCES IN: 'me->counter'                               */
ERROR_4:
    __QUEX_IF_POST_CATEGORIZER(QUEX_NAME(PostCategorizer_destruct)(&me->post_categorizer));
ERROR_3:
    __QUEX_IF_STRING_ACCUMULATOR(QUEX_NAME(Accumulator_destruct)(&me->accumulator, me));
ERROR_2:
    /* NO ALLOCATED RESOURCES IN: 'me->mode_stack'                            */
ERROR_1:
    QUEX_NAME(Tokens_destruct)(me);
ERROR_0:
    /* NO ALLOCATED RESOURCES IN: 'me->_parent_memento = 0'                   */
    return false;
}

QUEX_INLINE 
QUEX_NAME(destruct)(QUEX_TYPE_ANALYZER* me)
{
    QUEX_NAME(destruct_all_but_buffer)(me);

    QUEX_NAME(Buffer_destruct)(&me->buffer);

    /* Protect against double destruction.                                    */
    QUEX_NAME(mark_resources_as_absent)(me);
}

QUEX_INLINE void
QUEX_NAME(destruct_all_but_buffer)(QUEX_TYPE_ANALYZER* me)
{
    __QUEX_IF_INCLUDE_STACK(QUEX_MEMBER_FUNCTION_CALLO(include_stack_delete));
    /*
     *              DESTRUCT ANYTHING ONLY AFTER INCLUDE STACK                
     *
     * During destruction the all previously pushed analyzer states are 
     * popped and destructed, until only the outest state remains. This
     * is then the state that is destructed here.                             */
    QUEX_NAME(Tokens_destruct)(me);
    __QUEX_IF_STRING_ACCUMULATOR(QUEX_NAME(Accumulator_destruct)(&me->accumulator));
    __QUEX_IF_POST_CATEGORIZER(  QUEX_NAME(PostCategorizer_destruct)(&me->post_categorizer));


    if( me->__input_name ) {
        QUEXED(MemoryManager_free)(me->__input_name, E_MemoryObjectType_BUFFER_MEMORY);
    }
}

void
QUEX_NAME(mark_resources_as_absent)(QUEX_TYPE_ANALYZER* me)
/* Resouces = 'absent' => Destructor knows that it must not be freed. 
 * 
 * This function is essential to set the lexical analyzer into a state
 * where it is safe to be destructed, even if some resources were missing.    
 *
 * IMPORTANT: The '.error_code' remains intact!
 *______________________________________________________________________________
 * WARNING: This function is NOT to be called, if not all resources are 
 *          disattached (destructed/freed) from the lexical analyzer. 
 *          Otherwise: unreferenced trailing objects; memory leaks.
 *____________________________________________________________________________*/
{
    E_Error  backup = me->error_code;

    memset((void*)me, 0, sizeof(QUEX_TYPE_ANALYZER));
    /* => ._parent_memento == 0 (include stack is marked as 'clear')
     * => ._token          == 0 (if not token queue, the token is 'clear')
     *                          For the case of 'token queue' a dedicated
     *                          'mark_resources_as_absent' is called.
     * => .__input_name    == 0                                               */
#   if defined(QUEX_OPTION_TOKEN_POLICY_QUEUE)
    QUEX_NAME(TokenQueue_mark_resources_as_absent)(&me->_token_queue);
#   endif 
#   if defined(QUEX_OPTION_STRING_ACCUMULATOR)
    QUEX_NAME(Accumulator_mark_resources_as_absent)(&me->accumulator)
#   endif
#   if defined(QUEX_OPTION_POST_CATEGORIZER)
    QUEX_NAME(PostCategorizer_mark_resources_as_absent)(&me->post_categorizer)
#   endif
    QUEX_NAME(Buffer_mark_resources_as_absent)(&me->buffer);

    me->error_code = backup;
}


QUEX_INLINE void
QUEX_NAME(Asserts_user_memory)(QUEX_TYPE_ANALYZER* me,
                               QUEX_TYPE_LEXATOM*  BufferMemoryBegin, 
                               size_t              BufferMemorySize,
                               QUEX_TYPE_LEXATOM*  BufferEndOfContentP /* = 0 */)
{
#   ifdef QUEX_OPTION_ASSERTS
    size_t               memory_size = BufferMemoryBegin ? BufferMemorySize 
                                       :                   QUEX_SETTING_BUFFER_SIZE;
    QUEX_TYPE_LEXATOM*   iterator = 0x0;

    __quex_assert(memory_size == 0 || memory_size > 2);
    if( BufferMemoryBegin ) {
        /* End of File must be inside the buffer, because we assume that the 
         * buffer contains all that is required.                              */
        if( BufferMemorySize <= QUEX_SETTING_BUFFER_MIN_FALLBACK_N + 2) {
            QUEX_ERROR_EXIT("\nConstructor: Provided memory size must be more than 2 greater than\n"
                            "Constructor: QUEX_SETTING_BUFFER_MIN_FALLBACK_N. If in doubt, specify\n"
                            "Constructor: -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=0 as compile option.\n");
        }
        if(    BufferEndOfContentP < BufferMemoryBegin 
            || BufferEndOfContentP > (BufferMemoryBegin + BufferMemorySize - 1)) {
            QUEX_ERROR_EXIT("\nConstructor: Argument 'BufferEndOfContentP' must be inside the provided memory\n"
                            "Constructor: buffer (speficied by 'BufferMemoryBegin' and 'BufferMemorySize').\n"
                            "Constructor: Note, that the last element of the buffer is to be filled with\n"
                            "Constructor: the buffer limit code character.\n");
        }
    }
    if( BufferEndOfContentP ) {
        __quex_assert(BufferEndOfContentP >  BufferMemoryBegin);
        __quex_assert(BufferEndOfContentP <= BufferMemoryBegin + memory_size - 1);

        /* The memory provided must be initialized. If it is not, then that's wrong.
         * Try to detect me by searching for BLC and PTC.                         */
        for(iterator = BufferMemoryBegin + 1; iterator != BufferEndOfContentP; ++iterator) {
            if(    *iterator == QUEX_SETTING_BUFFER_LIMIT_CODE 
                || *iterator == QUEX_SETTING_PATH_TERMINATION_CODE ) {
                QUEX_ERROR_EXIT("\nConstructor: Buffer limit code and/or path termination code appeared in buffer\n"
                                "Constructor: when pointed to user memory. Note, that the memory pointed to must\n"
                                "Constructor: be initialized! You might redefine QUEX_SETTING_PATH_TERMINATION_CODE\n"
                                "Constructor: and/or QUEX_SETTING_PATH_TERMINATION_CODE; or use command line arguments\n"
                                "Constructor: '--buffer-limit' and '--path-termination'.");
            }
        }
    }
#   endif

    /* NOT: before ifdef, otherwise c90 issue: mixed declarations and code   */
    (void)me; (void)BufferMemoryBegin; (void)BufferMemorySize; (void)BufferEndOfContentP;
}

/* AUXILIARY FUNCTIONS FOR CONSTRUCTION _______________________________________                                     
 *                                                                           */

QUEX_INLINE void
QUEX_NAME(Asserts_construct)(const char* CodecName)
{
    (void)CodecName;

#   if      defined(QUEX_OPTION_ASSERTS) \
       && ! defined(QUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED)
    __QUEX_STD_printf(__QUEX_MESSAGE_ASSERTS_INFO);
#   endif

#   if defined(QUEX_OPTION_ASSERTS) 
    if( QUEX_SETTING_BUFFER_LIMIT_CODE == QUEX_SETTING_PATH_TERMINATION_CODE ) {
        QUEX_ERROR_EXIT("Path termination code (PTC) and buffer limit code (BLC) must be different.\n");
    }
#   endif

#   if defined(__QUEX_OPTION_ENGINE_RUNNING_ON_CODEC)
    if( CodecName ) {
        __QUEX_STD_printf(__QUEX_MESSAGE_CHARACTER_ENCODING_SPECIFIED_WITHOUT_CONVERTER, CodecName);
    }
#   endif
}

#if ! defined(QUEX_TYPE_TOKEN)
#      error "QUEX_TYPE_TOKEN must be defined before inclusion of this file."
#endif
QUEX_INLINE void
QUEX_NAME(Tokens_construct)(QUEX_TYPE_ANALYZER* me)
{
#if defined(QUEX_OPTION_TOKEN_POLICY_QUEUE)
#   if defined(QUEX_OPTION_USER_MANAGED_TOKEN_MEMORY)
    /* Assume that the user will pass us a constructed token queue */
    QUEX_NAME(TokenQueue_mark_resources_as_absent)(&me->_token_queue);
#   else
    QUEX_NAME(TokenQueue_construct)(&me->_token_queue, 
                                    (QUEX_TYPE_TOKEN*)&me->__memory_token_queue,
                                    QUEX_SETTING_TOKEN_QUEUE_SIZE);
#   endif
#elif defined(QUEX_OPTION_USER_MANAGED_TOKEN_MEMORY)
    /* Assume that the user will pass us a constructed token                  */
    me->token = (QUEX_TYPE_TOKEN*)0x0;     
#   else
    me->token = &me->__memory_token;     
#   ifdef __QUEX_OPTION_PLAIN_C
    QUEX_NAME_TOKEN(construct)(me->token);
#   endif
#endif
}

QUEX_INLINE void
QUEX_NAME(Tokens_destruct)(QUEX_TYPE_ANALYZER* me)
{
    /* Even if the token memory is user managed, the destruction (not the
     * freeing of memory) must happen at this place.                          */
#ifdef QUEX_OPTION_TOKEN_POLICY_QUEUE 
    QUEX_NAME(TokenQueue_destruct)(&me->_token_queue);
#else
#   if      defined(__QUEX_OPTION_PLAIN_C) \
       && ! defined(QUEX_OPTION_USER_MANAGED_TOKEN_MEMORY)
    QUEX_NAME_TOKEN(destruct)(me->token);
#   endif
#endif
}

QUEX_INLINE void 
QUEX_NAME(Tokens_reset)(QUEX_TYPE_ANALYZER* me)
{
#ifdef QUEX_OPTION_TOKEN_POLICY_QUEUE
    QUEX_NAME(TokenQueue_reset)(&me->_token_queue);
#else
    QUEX_NAME(Tokens_destruct(me));
    QUEX_NAME(Tokens_construct(me));
#endif
}

QUEX_INLINE void
QUEX_NAME(ModeStack_construct)(QUEX_TYPE_ANALYZER* me)
{
    me->_mode_stack.end        = me->_mode_stack.begin;
    me->_mode_stack.memory_end = &me->_mode_stack.begin[QUEX_SETTING_MODE_STACK_SIZE];
}

QUEX_INLINE const char*
QUEX_NAME(input_name)(QUEX_TYPE_ANALYZER* me)
{ return me->__input_name; }

QUEX_INLINE bool
QUEX_NAME(input_name_set)(QUEX_TYPE_ANALYZER* me, const char* InputNameP)
/* Sets the 'input name', i.e. some string that identifies the input stream.
 * In case of failure '.__input_name' is set to NULL.
 *
 * RETURNS: true, for success. false, else.                                   */
{ 
    if( me->__input_name ) {
        QUEXED(MemoryManager_free)(me->__input_name, E_MemoryObjectType_BUFFER_MEMORY);
    }
    me->__input_name = (char*)QUEXED(MemoryManager_allocate)(
                                    sizeof(char)*(__QUEX_STD_strlen(InputNameP)+1),
                                    E_MemoryObjectType_BUFFER_MEMORY);
    if( me->__input_name ) {
        __QUEX_STD_strcpy(me->__input_name, InputNameP);
        return true;
    }
    return false;
}

QUEX_NAMESPACE_MAIN_CLOSE

#endif /*  __QUEX_INCLUDE_GUARD__ANALYZER__STRUCT__CONSTRUCTOR_I */
