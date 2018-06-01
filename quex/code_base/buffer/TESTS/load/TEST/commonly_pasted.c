#include "TESTS/minimum-definitions.h"
#include "ut/lib/buffer/lexatoms/LexatomLoader.i"
#include "ut/lib/buffer/bytes/ByteLoader_Memory"
#include "ut/lib/buffer/bytes/ByteLoader_Memory.i"
#include "ut/lib/buffer/Buffer_print.i"
#include "ut/lib/buffer/Buffer.i"
#include "ut/lib/quex/MemoryManager"
#include "ut/lib/quex/MemoryManager.i"
#include <hwut_unit.h>

typedef struct {
    QUEX_TYPE_LEXATOM*        read_p;
    QUEX_TYPE_LEXATOM*        lexeme_start_p;
    /* '_read_p' must point after the last treated letter. 
     * for reload => to a buffer limit code. 
     * => Interesting is the letter before the '_read_p'.                    */
    QUEX_TYPE_LEXATOM         read_m1;         
    QUEX_TYPE_LEXATOM         lexeme_start_m1;
    QUEX_TYPE_LEXATOM*        position_register_1;
    QUEX_TYPE_LEXATOM*        position_register_3;
    QUEX_TYPE_STREAM_POSITION lexatom_index_begin;
} BufferBefore_t;

typedef struct {
    QUEX_NAME(Buffer)* buffer;
} SomethingContainingABuffer_t;

static const QUEX_TYPE_LEXATOM  PseudoFile[] = {
   1,  2,  3,  4,  5,  6,  7,  8,  9,  10, 11, 12, 13, 14, 15, 16, 
   17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32
};

#define PSEUDO_FILE_SIZE \
        sizeof(PseudoFile)
#define PSEUDO_FILE_ELEMENT_N \
        (sizeof(PseudoFile)/sizeof(PseudoFile[0]))
#define PSEUDO_FILE_LEXATOM_INDEX_AT_END \
        PSEUDO_FILE_ELEMENT_N 

uint8_t  PseudoFileUTF8[] = { /* Maxwell Equations ...    */
    0xe2, 0x81, 0x85, 0xe2, 0x88, 0x87, 0xc3, 0x97, 0xf0, 0x9d, 0x90, 0x81, 0xe2, 0x83, 0x97, 0x20,  
    0x2d, 0xe2, 0x80, 0x89, 0x20, 0x31, 0xe2, 0x88, 0x95, 0x63, 0xe2, 0x80, 0x89, 0x20, 0x28, 0xe2,  
    0x88, 0x82, 0xf0, 0x9d, 0x90, 0x84, 0xe2, 0x83, 0x97, 0x29, 0xe2, 0x88, 0x95, 0x28, 0xe2, 0x88,  
    0x82, 0x74, 0x29, 0x20, 0x26, 0x20, 0x3d, 0x20, 0x28, 0x34, 0xcf, 0x80, 0x29, 0xe2, 0x88, 0x95,  
    0x63, 0x20, 0xf0, 0x9d, 0x90, 0xa3, 0xe2, 0x83, 0x97, 0x20, 0x0a, 0xe2, 0x88, 0x87, 0xe2, 0x8b,  
    0x85, 0xf0, 0x9d, 0x90, 0x84, 0xe2, 0x83, 0x97, 0x20, 0x26, 0x20, 0x3d, 0x20, 0x34, 0x20, 0xcf,  
    0x80, 0xcf, 0x81, 0x20, 0x0a, 0xe2, 0x88, 0x87, 0xc3, 0x97, 0xf0, 0x9d, 0x90, 0x84, 0xe2, 0x83,  
    0x97, 0xe2, 0x80, 0x89, 0x20, 0x2b, 0xe2, 0x80, 0x89, 0x20, 0x31, 0xe2, 0x88, 0x95, 0x63, 0xe2,  
    0x80, 0x89, 0x20, 0x28, 0xe2, 0x88, 0x82, 0xf0, 0x9d, 0x90, 0x81, 0xe2, 0x83, 0x97, 0x29, 0xe2,  
    0x88, 0x95, 0x28, 0xe2, 0x88, 0x82, 0x74, 0x29, 0x20, 0x26, 0x20, 0x3d, 0x20, 0xf0, 0x9d, 0x9f,  
    0x8e, 0xe2, 0x83, 0x97, 0x20, 0x0a, 0xe2, 0x88, 0x87, 0xe2, 0x8b, 0x85, 0xf0, 0x9d, 0x90, 0x81,  
    0xe2, 0x83, 0x97, 0x20, 0x26, 0x20, 0x3d, 0x20, 0x30, 0x0a                    
};

#define PSEUDO_FILE_UTF8_SIZE \
        sizeof(PseudoFileUTF8)
#define PSEUDO_FILE_UTF8_ELEMENT_N \
        (sizeof(PseudoFileUTF8)/sizeof(PseudoFileUTF8[0]))
#define PSEUDO_FILE_UTF8_LEXATOM_INDEX_AT_END \
        PSEUDO_FILE_UTF8_ELEMENT_N 

static const uint32_t PseudoFileUCS4[] = { /* Maxwell Equations ...    */
    0x00002045, 0x00002207, 0x000000d7, 0x0001d401,  
    0x000020d7, 0x00000020, 0x0000002d, 0x00002009,  
    0x00000020, 0x00000031, 0x00002215, 0x00000063,  
    0x00002009, 0x00000020, 0x00000028, 0x00002202,  
    0x0001d404, 0x000020d7, 0x00000029, 0x00002215,  
    0x00000028, 0x00002202, 0x00000074, 0x00000029,  
    0x00000020, 0x00000026, 0x00000020, 0x0000003d,  
    0x00000020, 0x00000028, 0x00000034, 0x000003c0,  
    0x00000029, 0x00002215, 0x00000063, 0x00000020,  
    0x0001d423, 0x000020d7, 0x00000020, 0x0000000a,  
    0x00002207, 0x000022c5, 0x0001d404, 0x000020d7,  
    0x00000020, 0x00000026, 0x00000020, 0x0000003d,  
    0x00000020, 0x00000034, 0x00000020, 0x000003c0,  
    0x000003c1, 0x00000020, 0x0000000a, 0x00002207,  
    0x000000d7, 0x0001d404, 0x000020d7, 0x00002009,  
    0x00000020, 0x0000002b, 0x00002009, 0x00000020,  
    0x00000031, 0x00002215, 0x00000063, 0x00002009,  
    0x00000020, 0x00000028, 0x00002202, 0x0001d401,  
    0x000020d7, 0x00000029, 0x00002215, 0x00000028,  
    0x00002202, 0x00000074, 0x00000029, 0x00000020,  
    0x00000026, 0x00000020, 0x0000003d, 0x00000020,  
    0x0001d7ce, 0x000020d7, 0x00000020, 0x0000000a,  
    0x00002207, 0x000022c5, 0x0001d401, 0x000020d7,  
    0x00000020, 0x00000026, 0x00000020, 0x0000003d,  
    0x00000020, 0x00000030, 0x0000000a,
};

#define PSEUDO_FILE_UCS4_SIZE \
        sizeof(PseudoFileUCS4)
#define PSEUDO_FILE_UCS4_ELEMENT_N \
        (sizeof(PseudoFileUCS4)/sizeof(PseudoFileUCS4[0]))
#define PSEUDO_FILE_UCS4_LEXATOM_INDEX_AT_END \
        PSEUDO_FILE_UCS4_ELEMENT_N 

static QUEX_TYPE_LEXATOM* PoisonP = (QUEX_TYPE_LEXATOM*)0x5A5A5A5A; 
static QUEX_TYPE_LEXATOM* NullP   = (QUEX_TYPE_LEXATOM*)0; 

static QUEX_TYPE_LEXATOM* random_between(QUEX_TYPE_LEXATOM* A, 
                                         QUEX_TYPE_LEXATOM* B);

static int common_on_overflow_count = 0;
static int common_on_content_change_count = 0;
static int common_verification_count = 0;

static ptrdiff_t
verify_content(QUEX_NAME(Buffer)* me)
{
    QUEX_TYPE_LEXATOM  expected;
    QUEX_TYPE_LEXATOM* p;
    ptrdiff_t          count = 0;
    ptrdiff_t          lexatom_index_at_end_p;
    (void)lexatom_index_at_end_p;
    (void)expected;

    hwut_verify(me->begin(me)[0]             == QUEX_SETTING_BUFFER_LIMIT_CODE);
    hwut_verify(me->content_space_end(me)[0] == QUEX_SETTING_BUFFER_LIMIT_CODE);
    hwut_verify(me->content_end(me)[0]       == QUEX_SETTING_BUFFER_LIMIT_CODE);

    /* If end_p does not stand on buffer boarder, then it must stand according
     * to the 'lexatom_index_begin' at the end of the pseudo files content.*/
    if( me->content_end(me) != me->content_space_end(me) ) {
        lexatom_index_at_end_p = me->content_size(me);
#       ifndef HWUT_OPTION_NO_ASSUMPTION_ON_LEXATOM_INDEX_AT_END
        hwut_verify(lexatom_index_at_end_p + me->input.lexatom_index_begin
                    == PSEUDO_FILE_LEXATOM_INDEX_AT_END);
#       endif
    }
    /* Make sure that the content has been loaded properly. From the 
     * variable 'pseudo_file' it can be previewed what the content is 
     * supposed to be.                                                       */
    for(p=me->content_begin(me); p != me->content_end(me) ; ++p) {
        expected = PseudoFile[me->input.lexatom_index_begin + p - me->content_begin(me)];
        hwut_verify(*p == expected);
        ++count;
    }
    hwut_verify(count == me->content_size(me));

    common_verification_count += count;
    return count;
}

static ptrdiff_t
verify_ucs4_content(QUEX_NAME(Buffer)* me)
{
    QUEX_TYPE_LEXATOM  expected;
    QUEX_TYPE_LEXATOM* p;
    ptrdiff_t          count = 0;
    ptrdiff_t          lexatom_index_at_end_p;
    (void)lexatom_index_at_end_p;
    (void)expected;

    hwut_verify(me->begin(me)[0] == QUEX_SETTING_BUFFER_LIMIT_CODE);
    hwut_verify(me->content_space_end(me)[0]    == QUEX_SETTING_BUFFER_LIMIT_CODE);
    hwut_verify(me->content_end(me)[0]              == QUEX_SETTING_BUFFER_LIMIT_CODE);

    /* If end_p does not stand on buffer boarder, then it must stand according
     * to the 'lexatom_index_begin' at the end of the pseudo files content.*/
    if( me->content_end(me) != me->content_space_end(me) ) {
        lexatom_index_at_end_p = me->content_size(me);
        hwut_verify(lexatom_index_at_end_p + me->input.lexatom_index_begin
                    == PSEUDO_FILE_UCS4_LEXATOM_INDEX_AT_END);
    }
    /* Make sure that the content has been loaded properly. From the 
     * variable 'pseudo_file' it can be previewed what the content is 
     * supposed to be.                                                       */
    for(p=me->content_begin(me); p != me->content_end(me) ; ++p) {
        expected = PseudoFileUCS4[me->input.lexatom_index_begin + p - me->content_begin(me)];
        hwut_verify(*p == expected);
        ++count;
    }
    hwut_verify(count == me->content_size(me));

    return count;
}

static void
before_setup(BufferBefore_t* me, QUEX_NAME(Buffer)* buffer, 
             QUEX_TYPE_LEXATOM* (position_register[5]))
{
    if( position_register ) {
        position_register[0] = PoisonP; 
        position_register[1] = random_between(buffer->_lexeme_start_p, buffer->_read_p);
        position_register[2] = NullP;   
        position_register[3] = random_between(buffer->_lexeme_start_p, buffer->_read_p);
        position_register[4] = PoisonP; 

        me->position_register_1 = position_register[1];
        me->position_register_3 = position_register[3];
    }

    me->read_p              = buffer->_read_p;
    me->read_m1             = buffer->_read_p == buffer->_memory._front ? 
                              QUEX_SETTING_BUFFER_LIMIT_CODE : buffer->_read_p[-1];
    me->lexeme_start_p      = buffer->_lexeme_start_p;
    me->lexeme_start_m1     = buffer->_lexeme_start_p == buffer->_memory._front ? 
                              QUEX_SETTING_BUFFER_LIMIT_CODE : buffer->_lexeme_start_p[-1];

    me->lexatom_index_begin = buffer->input.lexatom_index_begin;

}

static void
before_check_consistency(BufferBefore_t*    me, 
                         ptrdiff_t          Delta, 
                         E_LoadResult       Verdict,
                         QUEX_NAME(Buffer)* buffer, 
                         QUEX_TYPE_LEXATOM* (position_register[5]), 
                         bool               ConverterF)
{
    int count; 

    if( Delta || buffer->input.lexatom_index_begin == 0 ) { 
        hwut_verify(Delta <= buffer->_memory._back - &buffer->_memory._front[1]);
        /* NOT: hwut_verify(Verdict);  
         * Because, even if no content has been loaded, the pointers may have
         * been adapted during the 'move-away' of passed content.            */
    }
    else {
        hwut_verify(Verdict != E_LoadResult_DONE);  
    }

    hwut_verify(buffer->input.lexatom_index_begin - me->lexatom_index_begin == Delta);

    if( Verdict == E_LoadResult_FAILURE ) {
        /* Overflow: common_on_overflow() sets 'lexeme_start_p = read_p'.
         * => in that case it is excused.                                    */
    }
    else if( buffer->_backup_lexatom_index_of_lexeme_start_p == (QUEX_TYPE_STREAM_POSITION)-1 ) {
        hwut_verify(me->lexeme_start_p - buffer->_lexeme_start_p == Delta);
        if(    buffer->_lexeme_start_p > &buffer->_memory._front[1] 
            && me->lexeme_start_m1 != QUEX_SETTING_BUFFER_LIMIT_CODE ) {
            hwut_verify(buffer->_lexeme_start_p[-1] == me->lexeme_start_m1);
        }
    }

    if( position_register ) {
        //hwut_verify(position_register[0] == PoisonP);
        hwut_verify(me->position_register_1 -  position_register[1] == Delta);
        //hwut_verify(position_register[2] == NullP);
        hwut_verify(me->position_register_3 -  position_register[3] == Delta);
        //hwut_verify(position_register[4] == PoisonP);
    }

    if(    buffer->_read_p > &buffer->_memory._front[1] 
        && me->read_m1 != QUEX_SETTING_BUFFER_LIMIT_CODE ) {
        hwut_verify(buffer->_read_p[-1] == me->read_m1);
    }

    /* Make sure that the content has been loaded properly. From the 
     * variable 'pseudo_file' it can be previewed what the content is 
     * supposed to be.                                                   */
    if( ! ConverterF ) count = verify_content(buffer);
    else               count = verify_ucs4_content(buffer);

    hwut_verify(count == buffer->input.end_p - &buffer->_memory._front[1]);
    hwut_verify(buffer->input.end_p[0] == QUEX_SETTING_BUFFER_LIMIT_CODE);

    return;
}

static QUEX_TYPE_LEXATOM*
random_between(QUEX_TYPE_LEXATOM* A, QUEX_TYPE_LEXATOM* B)
{
    QUEX_TYPE_LEXATOM* min   = A > B ? B : A;
    QUEX_TYPE_LEXATOM* max   = A > B ? A : B;
    ptrdiff_t            delta = max - min;
    static uint32_t      seed  = 971;

    if( ! delta ) return min;

    seed = (seed << 16) % 537;
        
    return &min[seed % delta];
}

static void      
common_on_content_change(void* aux)
{
    common_on_content_change_count += 1;
}

static void
common_on_overflow(void* aux)
{
    QUEX_NAME(Buffer)* me = ((SomethingContainingABuffer_t*)aux)->buffer;
    (void)me;

    /* me->_lexeme_start_p = me->_read_p; */
    common_on_overflow_count += 1;
}
