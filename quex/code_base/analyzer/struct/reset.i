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
 * FAILURE => Current lexer: all resources marked absent 
                             -> dysfunctional but destruct-able.
 *            Overtaken objects are destructed and freed!
 *
 * NOTE: The state before the reset is FORGOTTEN. For a 'reminiscent reset' 
 *       the 'include' feature may be considered.
 *
 *______________________________________________________________________________
 * INSIGHT: 
 *
 *    Reset consists of two major phases:
 * 
 *    (1) Resources and contents are reset. FAILURE MAY OCCURR.
 *        If errors occur, the lexer is still UNTOUCHED!
 *
 *    (2) All allocation has been done. SUCCESS IS GRANTED. 
 *        Only then, the lexer object is assigned new content.
 * 
 * The *pivot point* of 'success granted' is inside the function 
 * 'include_push_all_but_buffer()'. If it returns != NULL, success is granted.
 * Anything that might fail, *must happen before* the call to this function.
 * The exact 'pivot point' is marked in a comment by '[PIVOT POINT]'.
 *______________________________________________________________________________
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
/* Reset given setup to initial position. This works on 'byte_loader' buffers
 * as well as buffers initialized to run on memory only.
 *
 * RETURNS: true, in case of success.
 *          false, in case of failure.                                        */
{
    if( me->buffer.filler ) {
        if( ! QUEX_NAME(LexatomLoader_lexatom_index_reset)(me->buffer.filler) ) {
            goto ERROR_0;
        }
    }

    QUEX_NAME(Buffer_init)(&me->buffer, (QUEX_TYPE_LEXATOM*)0); 

    if( ! QUEX_NAME(reset_all_but_buffer)(me, me->__input_name) ) {
        goto ERROR_0;
    }

    return true;

ERROR_0:
    QUEX_NAME(Buffer_destruct)(&me->buffer);
    return false;
}

QUEX_INLINE bool
QUEX_NAME(reset_file_name)(QUEX_TYPE_ANALYZER*   me, 
                           const char*           FileName, 
                           QUEX_NAME(Converter)* new_converter /* = 0 */)
/* Reset on file 'FileName' as C-Standard Lib 'FILE'. 
 *
 *                OWNERSHIP OF 'converter' IS TAKEN OVER!
 *                USER IS **NOT** RESPONSIBLE FOR DELETING IT!
 *
 * 'reset_memory()' or 'include_push_memory()' has been applied before?
 * => 'collect_user_memory()' delivers memory to be user-de-allocated.
 *
 * RETURNS: true, in case of success.
 *          false, in case of failure.                                        */
{
    QUEX_NAME(ByteLoader)*   new_byte_loader;

    /* NEW: ByteLoader.                                                       */
    new_byte_loader = QUEX_NAME(ByteLoader_FILE_new_from_file_name)(FileName);
    if( ! new_byte_loader ) {
        me->error_code = E_Error_Allocation_ByteLoader_Failed; 
        goto ERROR_0;
    }

    if( ! QUEX_NAME(reset_ByteLoader)(me, new_byte_loader, new_converter, FileName) ) {
        goto ERROR_1;
    }
    return true;

ERROR_1:
    /* 'reset_ByteLoader()': deletes and mark absent everything.              */
ERROR_0:
    /* 'destruct' marks resources as absent => double destruction is safe.    */
    QUEX_NAME(destruct)(me);
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
                            QUEX_NAME(ByteLoader)*  new_byte_loader,
                            QUEX_NAME(Converter)*   new_converter /* = 0 */,
                            const char*             InputName /* = 0 */) 
/* Resets the 'filler' to a new 'new_byte_loader' and 'new_converter'. If it fails
 * the 'filler' is freed and set to NULL. '.error_code' contains the code of
 * the error that occurred.
 *
 *                OWNERSHIP OF 'new_byte_loader' IS TAKEN OVER!
 *                OWNERSHIP OF 'new_converter' IS TAKEN OVER!
 *                USER IS **NOT** RESPONSIBLE FOR DELETING IT!
 *
 * 'reset_memory()' or 'include_push_memory()' has been applied before?
 * => 'collect_user_memory()' delivers memory to be user-de-allocated.
 *
 * RETURNS: true, in case of success.
 *          false, in case of failure.                                        */
{
    QUEX_NAME(LexatomLoader)* new_filler;

    if( QUEX_NAME(Buffer_resources_absent)(&me->buffer) ) {
        /* The buffer has not even been setup. Quit.                          */
        me->error_code = E_Error_Reset_BufferResourcesAbsent;
        goto ERROR_0;
    }
     
    new_filler = QUEX_NAME(LexatomLoader_new)(new_byte_loader, new_converter);
    if( ! new_filler ) {
        goto ERROR_0;
    }
    if( me->buffer.filler ) {
        me->buffer.filler->delete_self(me->buffer.filler);
    }
    me->buffer.filler = new_filler;

    QUEX_NAME(Buffer_init)(&me->buffer, (QUEX_TYPE_LEXATOM*)0);

    if( ! QUEX_NAME(reset_all_but_buffer)(me, InputName) ) {
        goto ERROR_1;
    }
    return true;

    /* ERROR CASES: Free Resources ___________________________________________*/
ERROR_1:
    /* 'reset_all_but_buffer()' destructed and marked absent any resource 
     *                          but the buffer.                               */
    QUEX_NAME(Buffer_destruct)(&me->buffer);
    /* 'Buffer_destruct()' destructs and marks absent the 'new_filler' and in 
     *                     'new_byte_loader' and 'new_converter'.             */
    return false;

ERROR_0:
    if( new_byte_loader ) new_byte_loader->delete_self(new_byte_loader);
    if( new_converter )   new_converter->delete_self(new_converter);
    /* 'destruct' marks resources as absent => double destruction is safe.    */
    QUEX_NAME(destruct)(me);  /* Destructs also 'me->buffer'                  */
    return false;
}

QUEX_INLINE bool
QUEX_NAME(reset_memory)(QUEX_TYPE_ANALYZER*  me, 
                        QUEX_TYPE_LEXATOM*   Memory,
                        const size_t         MemorySize,
                        QUEX_TYPE_LEXATOM*   EndOfFileP)
/* Take-in a user's chunk of memory--filled as it is. There is no LexatomLoader.
 * If the buffer's current memory is owned externally, a pointer to it is 
 * returned. Else, zero is returned.
 *
 *                  OWNERSHIP OF 'Memory' REMAINS AT USER!
 *                  USER IS RESPONSIBLE FOR DELETING IT!
 *
 * 'reset_memory()' or 'include_push_memory()' has been applied before?
 * => 'collect_user_memory()' delivers memory to be user-de-allocated.
 *
 * RETURNS: true, in case of success.
 *          false, in case of failure.                                        */
{
    QUEX_ASSERT_MEMORY(Memory, MemorySize, EndOfFileP);

    QUEX_NAME(Buffer_destruct)(&me->buffer); 
    /* Buffer's memory owned externally => memory NOT freed!
     * but 'me->buffer._memory._front = NULL'!                                */

    if( ! QUEX_NAME(reset_all_but_buffer)(me, "<memory>") ) {
        goto ERROR_0;
    }

    QUEX_NAME(Buffer_construct)(&me->buffer, 
                                (QUEX_NAME(LexatomLoader)*)0,
                                Memory, MemorySize, EndOfFileP,
                                E_Ownership_EXTERNAL);
    return true;

    /* ERROR CASES: Free Resources ___________________________________________*/
ERROR_0:
    /* 'reset_all_but_buffer()' All but the buffer resource destructed and 
     *                          marked as absent. 
     * 'Buffer_destruct()' marked buffer resources as absent.                 */
    return false;
}

QUEX_INLINE bool
QUEX_NAME(reset_all_but_buffer)(QUEX_TYPE_ANALYZER*  me, 
                                const char*          InputName) 
/* Resets anything but 'Buffer'. 
 *
 * FAILURE: All but the buffer's resources are destructed and marked absent.
 * 
 * RETURNS: true, for success.
 *          false, else. Buffer's resource must be destructed/marked absent.  */
{
    QUEX_NAME(destruct_all_but_buffer)(me);

    /*__________________________________________________________________________
     *
     * [PIVOT POINT] All but buffer's resources are desctructed.
     *
     * From here: Construct new lexical analyzer object.
     *________________________________________________________________________*/

    if( ! QUEX_MEMBER_FUNCTION_CALLO(user_reset) ) {
        goto ERROR_0;
    }
    else if( ! QUEX_NAME(construct_all_but_buffer)(me, InputName) ) {
        goto ERROR_0;
    }
    return true;

    /* ERROR CASES: Free Resources ___________________________________________*/
ERROR_0:
    return false;
}


QUEX_NAMESPACE_MAIN_CLOSE

#endif /* __QUEX_INCLUDE_GUARD__ANALYZER__STRUCT__RESET_I */
