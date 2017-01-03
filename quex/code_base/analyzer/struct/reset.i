/* -*- C++ -*- vim:set syntax=cpp:
 *
 * RESET: Reset lexical analysis with a new input stream.
 *
 * All components of the lexer are reset into a state so that the new input
 * stream can be analyzed. 
 *
 *   -- Reset may fail, but it never throws an exception!
 *      Failure is notified by the '.error_code' flag.
 *   -- '.receive()' may always be called, but that function might return
 *      immediately if '.error_code' is not 'NONE'.
 *   -- The destructor can be called safely for any object that has been 
 *      'reset'--even if the reset failed.
 *
 * FAILURE => Lexer is in DYSFUNCTIONAL state.
 *
 * NOTE: The state before the reset is FORGOTTEN. For a 'reminiscent reset' 
 *       the 'include' feature may be considered.
 *
 * (C) 2006-2017 Frank-Rene Schaefer
 * ABSOLUTELY NO WARRANTY                                                     */
#ifndef __QUEX_INCLUDE_GUARD__ANALYZER__STRUCT__RESET_I
#define __QUEX_INCLUDE_GUARD__ANALYZER__STRUCT__RESET_I

#include <quex/code_base/buffer/Buffer.i>
#include <quex/code_base/analyzer/struct/reset>

QUEX_NAMESPACE_MAIN_OPEN

QUEX_INLINE bool
QUEX_NAME(reset)(QUEX_TYPE_ANALYZER* me)  
{
    QUEX_NAME(LexatomLoader)* filler = me->buffer.filler;

    QUEX_NAME(LexatomLoader_lexatom_index_reset)(me);
    QUEX_NAME(Buffer_reset)(&me->buffer);

    /* Reset all but 'LexatomLoader' and 'Buffer'.                            */
    if( ! QUEX_NAME(reset_all_but_buffer)(me, me->input_name) ) {
        QUEX_NAME(Buffer_destruct)(&me->buffer);
        QUEX_NAME(mark_resources_as_absent)(me);
    }
}

QUEX_INLINE bool
QUEX_NAME(reset_file_name)(QUEX_TYPE_ANALYZER*   me, 
                           const char*           FileName, 
                           QUEX_NAME(Converter)* converter /* = 0 */,
                           const char*           CodecName /* = 0 */) 
/* Open 'FileName' as C-Standard Lib 'FILE'. 
 *
 *                OWNERSHIP OF 'converter' IS TAKEN OVER!
 *                USER IS **NOT** RESPONSIBLE FOR DELETING IT!
 *
 * RETURNS: true, in case of success.
 *          false, in case of failure.                                        */
{
    QUEX_NAME(ByteLoader)*   byte_loader;

    /* NEW: ByteLoader.                                                       */
    byte_loader = QUEX_NAME(ByteLoader_FILE_new_from_file_name)(FileName);
    if( ! byte_loader ) {
        me->error_code = QUEX_ENUM_ERROR_RESET_BYTE_LOADER_ALLOCATION;
        goto ERROR_0;
    }

    /* DELEGATE TO: 'reset_ByteLoader()'                                      */
    if( ! QUEX_NAME(reset_ByteLoader)(me, byte_loader, ConverterNew, 
                                      CodecName, FileName) ) {
        goto ERROR_1;
    }
    return true;

ERROR_1:
    /* 'reset_ByteLoader()' error: => byte_loader is already deleted.         */
ERROR_0:
    QUEX_NAME(mark_resources_as_absent)(me);
    return false;
}

/* USE: byte_loader = QUEX_NAME(ByteLoader_FILE_new)(fh, BinaryModeF);
 *      byte_loader = QUEX_NAME(ByteLoader_stream_new)(istream_p, BinaryModeF);
 *      byte_loader = QUEX_NAME(ByteLoader_wstream_new)(wistream_p, BinaryModeF);
 *      ...
 *      Unit Test's StrangeStreams:
 *      byte_loader = QUEX_NAME(ByteLoader_stream_new)(strangestr_p, false);  */
QUEX_INLINE bool
QUEX_NAME(reset_ByteLoader)(QUEX_TYPE_ANALYZER*     me,
                            QUEX_NAME(ByteLoader)*  byte_loader,
                            QUEX_NAME(Converter)*   converter /* = 0 */,
                            const char*             CodecName /* = 0 */, 
                            const char*             InputName /* = 0 */) 
/* Resets the 'filler' to a new 'byte_loader' and 'converter'. If it fails
 * the 'filler' is freed and set to NULL. '.error_code' contains the code of
 * the error that occurred.
 *
 *                OWNERSHIP OF 'byte_loader' IS TAKEN OVER!
 *                OWNERSHIP OF 'converter' IS TAKEN OVER!
 *                USER IS **NOT** RESPONSIBLE FOR DELETING IT!
 *
 * RETURNS: true, in case of success.
 *          false, in case of failure.                                        */
{
    QUEX_MAP_THIS_TO_ME(QUEX_TYPE_ANALYZER)
    QUEX_NAME(LexatomLoader)* filler    = me->buffer.filler;
     
    QUEX_NAME(Asserts_construct)(CodecName);

    if( me->buffer.filler ) {
        filler->delete_self(filler);
    }
    me->buffer.filler = QUEX_NAME(LexatomLoader_new)(byte_loader, converter);
    if( ! me->buffer.filler ) {
        goto ERROR_0;
    }

    QUEX_NAME(Buffer_reset)(&me->buffer);

    if( ! QUEX_NAME(reset_all_but_buffer)(me, InputName) ) {
        goto ERROR_1;
    }
    return true;

ERROR_1:
    QUEX_NAME(Buffer_destruct)(&me->buffer);
    QUEX_NAME(mark_resources_as_absent)(me);
    return false;

ERROR_0:
    if( converter ) {
        converter->delete_self(converter);
    }
    QUEX_NAME(mark_resources_as_absent)(me);
    return false;
}

QUEX_INLINE QUEX_TYPE_LEXATOM*
QUEX_NAME(reset_memory)(QUEX_TYPE_ANALYZER*  me, 
                        QUEX_TYPE_LEXATOM*   Memory,
                        const size_t         MemorySize,
                        QUEX_TYPE_LEXATOM*   EndOfFileP)
/* Take-in a user's chunk of memory--filled as it is. There is no LexatomLoader.
 * If the buffer's current memory is owned externally, a pointer to it is 
 * returned. Else, zero is returned.
 *
 *                  OWNERSHIP OF 'Memory' REMAINS AT USER!
 *                   USER IS RESPONSIBLE FOR DELETING IT!
 *
 * RETURN: != 0, pointer to previous memory owned by user.
 *         == 0, no user-owned memory inside the buffer before reset.        
 *
 * Success or failure of reset is accessed by '.error_code'.                  */
{
    QUEX_TYPE_LEXATOM*  user_owned_memory;
    QUEX_ASSERT_MEMORY(Memory, MemorySize, EndOfFileP);

    user_owned_memory = me->buffer._memory.ownership == E_Ownership_LEXICAL_ANALYZER ?
                        (const QUEX_TYPE_LEXATOM*)0 : me->buffer._memory._front;

    QUEX_NAME(Buffer_destruct)(&me->buffer); 
    /* In case, that the memory was owned by the analyzer, the destructor did
     * not delete it and did not set 'me->buffer._memory._front' to zero.     */

    if( QUEX_NAME(reset_all_but_buffer)(me, "<memory>") ) {
        QUEX_NAME(Buffer_construct)(&me->buffer, 
                                    (QUEX_NAME(LexatomLoader)*)0,
                                    Memory, MemorySize, EndOfFileP,
                                    E_Ownership_EXTERNAL);
    }
    else {
        QUEX_NAME(mark_resources_as_absent)(me);
    }
    return user_owned_memory;
}

QUEX_INLINE bool
QUEX_NAME(reset_all_but_buffer)(QUEX_TYPE_ANALYZER*  me, 
                                const char*          InputName) 
/* Resets anything but 'Buffer'.
 * 
 * RETURNS: true, for success.
 *          false, for failure.                                               */
{
    QUEX_NAME(destruct_all_but_buffer)(me);

    /* If user reset fails, all non-buffer components are destructed. 
     * => Safe to return. Caller must take care of buffer.                    */
    if( ! QUEX_MEMBER_FUNCTION_CALLO(user_reset) ) {
        return false;
    }

    return QUEX_NAME(construct_all_but_buffer)(me);
}


QUEX_NAMESPACE_MAIN_CLOSE

#endif /* __QUEX_INCLUDE_GUARD__ANALYZER__STRUCT__RESET_I */
