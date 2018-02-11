/* PURPOSE: Test Buffer_free_back()
 *
 * The tested function shall free some space ahead inside the buffer,
 * so that new content can be loaded. Detailed comment, see function
 * definition.
 *
 * Moving depends on:   * _read_p, 
 *                      * _lexeme_start_p
 *                      * whether the buffer contains the end of file or not.
 *                      * QUEX_SETTING_BUFFER_MIN_FALLBACK_N
 *                      * QUEX_TYPE_LEXATOM
 *
 * The last two are compile-time parameters. The first three may be
 * varried dynamically. 
 *
 * EXPERIMENT: Setup buffer of 5 elements.
 *
 * Let this file be compiled with '-DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=3'
 * for all experiments. Multiple versions of compiled objects may exist:
 *
 *        QUEX_TYPE_LEXATOM  QUEX_SETTING_BUFFER_MIN_FALLBACK_N
 *          uint8_t             0
 *          uint8_t             1
 *          uint8_t             2
 *          uint32_t            2
 *
 * The parameters '_read_p' and '_lexeme_start_p' are varried the following
 * way:
 *    _lexeme_start_p -> begin ... end of buffer
 *    _read_p         -> begin, 
 *                       _lexeme_start_p-1, _lexeme_start_p, _lexeme_start_p+1, 
 *                       end of buffer
 *    end of file     = true, false
 *
 * Before each copying process the buffer is reset into its initial state. Test
 * cases are generated by hwuts generator, i.e. 'hwut gen this-file.c'.      
 *
 * CHOICES: EoS -- End of Stream inside buffer.
 *          NoEoS -- End of Steam not inside buffer.                         */

/* 
<<hwut-iterator: G>> 
------------------------------------------------------------------------
#include <stdint.h>
------------------------------------------------------------------------
    int lexeme_start_i;    int read_i;                                   
    |0:4|;                 |lexeme_start_i-1:lexeme_start_i+1| in |0:4|; 
------------------------------------------------------------------------
*/
#include <move_away_passed_content-gen.h>
#include "commonly-pasted.cpp" /* requires 'G_t' from above header. */

static QUEX_TYPE_LEXATOM  content[] = { '5', '4', '3', '2', '1' }; 
const  ptrdiff_t            ContentSize = sizeof(content)/sizeof(content[0]);
static QUEX_TYPE_LEXATOM  memory[12];
const  ptrdiff_t            MemorySize = sizeof(memory)/sizeof(memory[0]);

QUEX_INLINE ptrdiff_t
QUEX_NAME(Buffer_free_back)(QUEX_NAME(Buffer)*  me,
                            QUEX_TYPE_LEXATOM** position_register,
                            const size_t        PositionRegisterN);

QUEX_INLINE ptrdiff_t
QUEX_NAME(Buffer_free_back)(QUEX_NAME(Buffer)*  me,
                            QUEX_TYPE_LEXATOM** position_register,
                            const size_t        PositionRegisterN)
/*    ..    WARNING: 
 *   /  \   Pointers to the '_memory' object may change!
 *  /    \  References to pointers from prior a call to this function
 *  '----'  become INVALID!
 *
 * Free some space AHEAD so that new content can be loaded. Content that 
 * is still used, or expected to be used shall remain inside the buffer.
 * Following things need to be respected:
 *
 *    _lexeme_start_p  --> points to the lexeme that is currently treated.
 *                         MUST BE INSIDE BUFFER!
 *    _read_p          --> points to the lexatom that is currently used
 *                         for triggering. MUST BE INSIDE BUFFER!
 *    fall back region --> A used defined buffer backwards from the lexeme
 *                         start. Shall help to avoid extensive backward
 *                         loading.
 *
 * RETURNS: Free space at end of buffer to fill new data.
 *          0, if there is none.                                              */
{ 
    ptrdiff_t  free_space;
    ptrdiff_t  move_distance;
    ptrdiff_t  move_size;
    (void)move_size;

    QUEX_BUFFER_ASSERT_CONSISTENCY(me);

    move_distance = QUEX_NAME(Buffer_get_move_distance_max_towards_begin)(me); 

    if( 0 == move_distance ) {
        if( ! QUEX_NAME(Buffer_on_cannot_move_towards_begin)(me, &move_distance) ) {
            return 0;
        }
    }

    if( move_distance ) {
        (void)QUEX_NAME(Buffer_move_towards_begin)(me, move_distance,
                                                   position_register, PositionRegisterN); 
    }

    free_space = me->_memory._back - me->input.end_p;

    /*________________________________________________________________________*/
    QUEX_IF_ASSERTS_poison(&me->_memory._back[- move_distance + 1], 
                           me->_memory._back);

    QUEX_BUFFER_ASSERT_CONSISTENCY(me);

    return free_space;
}

int
main(int argc, char** argv)
{
    QUEX_NAME(Buffer)    buffer;
    G_t                  it;
    struct {
        QUEX_TYPE_LEXATOM* end_p;     
        QUEX_TYPE_LEXATOM* read_p;     
        QUEX_TYPE_LEXATOM  read_char;
        QUEX_TYPE_LEXATOM* lexeme_start_p;     
        QUEX_TYPE_LEXATOM  lexeme_start_char;
    } before;
    QUEX_TYPE_LEXATOM* min_p;     
    bool               end_of_stream_in_buffer_f;
    ptrdiff_t          move_distance;
    ptrdiff_t          free_space;
    QUEX_TYPE_LEXATOM  backup[MemorySize*2];
    int                count = 0;

    SomethingContainingABuffer_t theAux;
    theAux.buffer = &buffer;

    if( cl_has(argc, argv, "--hwut-info") ) {
        printf("move_away_passed_content: (BPC=%i, FB=%i);\n", 
               (int)sizeof(QUEX_TYPE_LEXATOM),
               (int)QUEX_SETTING_BUFFER_MIN_FALLBACK_N);
        printf("CHOICES: EoS, NoEoS;\n");
        return 0;
    }
    stderr = stdout;
    hwut_if_choice("EoS")   end_of_stream_in_buffer_f = true;
    hwut_if_choice("NoEoS") end_of_stream_in_buffer_f = false;

    G_init(&it);
    
    printf("        lexeme_start_p: read_p: end_p: end_index: buffer:\n");
    while( G_next(&it) ) {
        instantiate_iterator(&buffer, &it, 
                             end_of_stream_in_buffer_f,
                             &memory[0],  MemorySize, 
                             &content[0], ContentSize);
        QUEX_NAME(Buffer_set_event_handlers)(&buffer, 
                                             self_on_content_change,
                                             self_on_overflow,
                                             &theAux);

        printf("\n-( %2i )---------------------------------------------\n", (int)G_key_get(&it));
        self_print(&buffer);

        before.end_p             = buffer.input.end_p;
        before.read_p            = buffer._read_p;
        before.read_char         = *buffer._read_p;
        before.lexeme_start_p    = buffer._lexeme_start_p;
        before.lexeme_start_char = *buffer._lexeme_start_p;
        min_p                    = QUEX_MIN(buffer._read_p, buffer._lexeme_start_p);
        memcpy(&backup[0], min_p, buffer.input.end_p - min_p);

        free_space = QUEX_NAME(Buffer_free_back)(&buffer, (QUEX_TYPE_LEXATOM**)0, 0);
        (void)free_space;
        move_distance = before.end_p - buffer.input.end_p;

        self_print(&buffer);

        /* Asserts after print, so that errors appear clearly. */
        hwut_verify(buffer.input.end_p      == &before.end_p[- move_distance]);
        hwut_verify(buffer._read_p          == &before.read_p[- move_distance]);
        hwut_verify(*buffer._read_p         == before.read_char);
        hwut_verify(buffer._lexeme_start_p  == &before.lexeme_start_p[- move_distance]);
        hwut_verify(*buffer._lexeme_start_p == before.lexeme_start_char);
        min_p = QUEX_MIN(buffer._read_p, buffer._lexeme_start_p);
        hwut_verify(memcmp(&backup[0], min_p, buffer.input.end_p - min_p) == 0);

        if( ! end_of_stream_in_buffer_f && (min_p - &buffer._memory._front[1] >= QUEX_SETTING_BUFFER_MIN_FALLBACK_N) ) {
            /* The move is only restricted by '_read_p', '_lexeme_start_p' and 
             * the fallback region size. Thus, ...                           */
            hwut_verify(   (buffer._read_p         - &buffer._memory._front[1] == QUEX_SETTING_BUFFER_MIN_FALLBACK_N)
                        || (buffer._lexeme_start_p - &buffer._memory._front[1] == QUEX_SETTING_BUFFER_MIN_FALLBACK_N));
        }
        else {
            hwut_verify(! move_distance);
        }

        QUEX_NAME(Buffer_destruct)(&buffer);
        ++count;
    }
    printf("<terminated %i>\n", count);
}


