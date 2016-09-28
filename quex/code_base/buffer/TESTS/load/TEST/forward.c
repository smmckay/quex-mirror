/* PURPOSE: Testin Buffer_load_forward()
 *
 * The load forward is tested sequentially. The '_read_p' is incremented
 * by a given 'delta' after each load forward. The '_lexeme_start_p' follows
 * the '_read_p' at a given distance. This is repeated until the end of 
 * stream is reached. An iterator 'G_t' iterates over possible settings of
 * the '_read_p delta' and the '_lexeme_start_p delta'.
 *
 * The behavior is checked with a set of 'hwut_verify' conditions on the 
 * buffer's state and its relation to its setting before.
 *
 * OUTPUTS:
 *    * adapted pointers: ._read_p, ._lexeme_start_p and position registers.
 *    * buffer's content.
 *    * input.end_p, 
 *      input.lexatom_index_begin, 
 *      input.lexatom_index_end_of_stream
 *
 * The read and lexeme pointers shall point exactly to the same lexatom as
 * before the load procedure. That is, they need
 */

#include "commonly_pasted.c"

static ptrdiff_t   test_load_forward(QUEX_NAME(Buffer)* buffer);
static ptrdiff_t   walk_forward(ptrdiff_t LexemeStartPDelta);

int
main(int argc, char**argv)
{
    int       load_n = 0;
    int       iteration_n = 0;
    ptrdiff_t lexeme_start_p_delta;

    if( argc > 1 && strcmp(argv[1], "--hwut-info") == 0 ) {
        printf("Buffer_load_forward: (BPC=%i, FB=%i);\n", 
               sizeof(QUEX_TYPE_LEXATOM),
               (int)QUEX_SETTING_BUFFER_MIN_FALLBACK_N);
        return 0;
    }

    common_on_overflow_count = 0;
    common_on_content_change_count = 0;


    for(lexeme_start_p_delta = 0, iteration_n = 0; 
        lexeme_start_p_delta < 5; 
        ++lexeme_start_p_delta, ++iteration_n) {

        load_n += walk_forward(lexeme_start_p_delta);
    }
    printf("<terminated %i; load_n: %i; content_change_n: %i; overflow_n: %i>\n", 
           (int)iteration_n, 
           (int)load_n, 
           (int)common_on_content_change_count,
           (int)common_on_overflow_count);
    return 0;
}

static ptrdiff_t
walk_forward(ptrdiff_t LexemeStartPDelta)
/* Walk through file by incrementing the 'read_p' by 'ReadPDelta' until the 
 * end of file is reached. The 'lexeme_start_p' remains in a constant distance 
 * to 'read_p' given by 'LexemeStartPDelta'.                                 */
{
    QUEX_NAME(Buffer)             buffer;
    QUEX_NAME(ByteLoader_Memory)  loader;
    QUEX_NAME(LexatomLoader)*     filler;
    int                           count = 0;
    QUEX_TYPE_LEXATOM             memory[5];
    const int                     MemorySize = 5;

    QUEX_NAME(ByteLoader_Memory_construct)(&loader, 
                                           (const uint8_t*)&PseudoFile[0], 
                                           (const uint8_t*)&PseudoFile[PSEUDO_FILE_ELEMENT_N]);
    filler = QUEX_NAME(LexatomLoader_new)(&loader.base, 
                                         (QUEX_NAME(Converter)*)0, 0);

    QUEX_NAME(Buffer_construct)(&buffer, filler,
                                &memory[0], MemorySize,
                                (QUEX_TYPE_LEXATOM*)0, E_Ownership_EXTERNAL); 
    buffer.on_overflow       = common_on_overflow;
    buffer.on_content_change = common_on_content_change;

    while( buffer.input.lexatom_index_end_of_stream == -1 ) {
        buffer._read_p = buffer._memory._back;

        buffer._lexeme_start_p = buffer._read_p - LexemeStartPDelta;  

        if( buffer._lexeme_start_p > buffer._memory._back ) {
            buffer._lexeme_start_p = buffer._memory._back;
        }
        if( buffer._lexeme_start_p <= buffer._memory._front ) {
            buffer._lexeme_start_p = &buffer._memory._front[1];
        }

        count += test_load_forward(&buffer);

        if(    LexemeStartPDelta 
            >= (ptrdiff_t)(MemorySize - QUEX_SETTING_BUFFER_MIN_FALLBACK_N - 2) ) {
            /* In case the setup implies 'overflow', do not try again.       */
            return 0;
        }
    } 
    /* Reached end => verify that last content has been loaded.              */
    hwut_verify((int)buffer.input.end_p[-1] == 0x20);
    hwut_verify((int)buffer.input.lexatom_index_end_of_stream == 32);

    /* Try to reload twice while it is impossible.                           */
    buffer._read_p = buffer.input.end_p;
    hwut_verify(test_load_forward(&buffer) == 0);
    buffer._read_p = buffer.input.end_p;
    hwut_verify(test_load_forward(&buffer) == 0);

    /* Reached end => verify that last content has been loaded.              */
    hwut_verify((int)buffer.input.end_p[-1] == 0x20);
    hwut_verify((int)buffer.input.lexatom_index_end_of_stream == 32);
    return count;
}

static ptrdiff_t
test_load_forward(QUEX_NAME(Buffer)* buffer) 
{
    size_t             PositionRegisterN = 5;
    QUEX_TYPE_LEXATOM* (position_register[5]);
    BufferBefore_t     before;
    E_LoadResult       verdict;
    ptrdiff_t          delta;

    before_setup(&before, buffer, position_register);

    verdict = QUEX_NAME(Buffer_load_forward)(buffer, &position_register[0], 
                                             PositionRegisterN);
    delta   = before.read_p - buffer->_read_p;

    before_check_consistency(&before, delta, verdict, buffer, position_register);
    return delta;
}

