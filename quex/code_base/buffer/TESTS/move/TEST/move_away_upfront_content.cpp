/* PURPOSE: Test Buffer_free_front()
 *
 * The tested function shall free some space in the rear buffer,
 * so that old content can be reloaded. Detailed comment, see function
 * definition.
 *
 * Moving depends on:   * _read_p, 
 *                      * _lexeme_start_p
 *                      * whether the buffer contains the end of file or not.
 *                      * begin_lexatom_index
 *                      * QUEX_TYPE_LEXATOM
 *
 * The last one is controlled by a compile-time parameter. The others are
 * varried dynamically. The begin_lexatom_index is dealt with by setting
 * the end lexatom index to 'content size + 3'. So there will be cases
 * where the begin lexatom index == 0 and therefore prohibits moving.
 *
 * EXPERIMENT: Setup buffer of 5 elements.
 *
 * Multiple versions of compiled objects exist:
 *
 *        QUEX_TYPE_LEXATOM:  uint8_t, uint16_t, uint32_t           
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
 * CHOICES: Character index at begin of buffer: "cib=0", "cib=1", "cib=2".
 *                                                                           */

/* 
<<hwut-iterator: G>> 
------------------------------------------------------------------------
#include <stdint.h>
------------------------------------------------------------------------
    int lexeme_start_i;    int read_i;                                    
    |0:5|;                 |lexeme_start_i-1:lexeme_start_i+1| in |0:5|; 

------------------------------------------------------------------------
*/

#include <move_away_upfront_content-gen.h>
#include "commonly-pasted.cpp" /* requires 'G_t' from above header. */

static QUEX_TYPE_LEXATOM  content[] = { '6', '5', '4', '3', '2', '1' }; 
ptrdiff_t                   ContentSize = sizeof(content)/sizeof(content[0]);
static QUEX_TYPE_LEXATOM  memory[11];
const  ptrdiff_t            MemorySize = sizeof(memory)/sizeof(memory[0]);

QUEX_INLINE ptrdiff_t  QUEX_NAME(Buffer_free_front)(QUEX_NAME(Buffer)* me);

QUEX_INLINE ptrdiff_t        
QUEX_NAME(Buffer_free_front)(QUEX_NAME(Buffer)* me)
/* Free some space in the REAR so that previous content can be re-loaded. Some 
 * content is to be left in front, so that no immediate reload is necessary
 * once the analysis goes forward again. Following things need to be respected:
 *
 *    _lexeme_start_p  --> points to the lexeme that is currently treated.
 *                         MUST BE INSIDE BUFFER!
 *    _read_p          --> points to the lexatom that is currently used
 *                         for triggering. MUST BE INSIDE BUFFER!
 *
 * RETURNS: Moved distance >  0: OK.
 *                         == 0: Nothing has been moved.                     
 *                         <  0: Overflow. Nothing has been moved. 
 *                               Lexeme fills complete buffer.                */
{
    ptrdiff_t   move_distance;

    QUEX_BUFFER_ASSERT_CONSISTENCY(me);

    if( 0 == me->input.lexatom_index_begin ) {
        return 0;
    }
    
    move_distance = QUEX_NAME(Buffer_move_get_max_distance_towards_end)(me);

    if( 0 == move_distance ) {
        return 0;
    }
    else if( me->_backup_lexatom_index_of_lexeme_start_p == (QUEX_TYPE_STREAM_POSITION)-1 ) {
        QUEX_NAME(Buffer_callbacks_on_buffer_before_change)(me);
    }
    else {
        /* Content has already been completely moved. No notification.        */
    }

    (void)QUEX_NAME(Buffer_move_towards_end)(me, move_distance);

    /*________________________________________________________________________*/
    QUEX_BUFFER_ASSERT_CONSISTENCY(me);

    return move_distance;
}


int
main(int argc, char** argv)
{
    QUEX_NAME(Buffer)         buffer;
    G_t                       it;
    struct {
        QUEX_TYPE_LEXATOM* end_p;     
        QUEX_TYPE_LEXATOM* read_p;     
        QUEX_TYPE_LEXATOM  read_char;
        QUEX_TYPE_LEXATOM* lexeme_start_p;     
        QUEX_TYPE_LEXATOM  lexeme_start_char;
    } before;
    QUEX_TYPE_LEXATOM*        min_p;     
    QUEX_TYPE_STREAM_POSITION lexatom_index_at_begin;
    bool                      end_of_stream_in_buffer_f;
    ptrdiff_t                 move_distance;
    QUEX_TYPE_LEXATOM         backup[MemorySize * 2];
    int                       count = 0;
    SomethingContainingABuffer_t theAux;
    theAux.buffer = &buffer;

    if( cl_has(argc, argv, "--hwut-info") ) {
        printf("move_away_upfront_content: (BPC=%i);\n", 
               (int)sizeof(QUEX_TYPE_LEXATOM));
        printf("CHOICES: cib=0, cib=1, cib=2, cib=0:EOS, cib=1:EOS, cib=2:EOS;\n");
        return 0;
    };
    stderr = stdout;
    hwut_if_choice("cib=0")     { lexatom_index_at_begin = 0; end_of_stream_in_buffer_f = false; }
    hwut_if_choice("cib=1")     { lexatom_index_at_begin = 1; end_of_stream_in_buffer_f = false; }
    hwut_if_choice("cib=2")     { lexatom_index_at_begin = 2; end_of_stream_in_buffer_f = false; }
    hwut_if_choice("cib=0:EOS") { lexatom_index_at_begin = 0; end_of_stream_in_buffer_f = true;  }
    hwut_if_choice("cib=1:EOS") { lexatom_index_at_begin = 1; end_of_stream_in_buffer_f = true;  }
    hwut_if_choice("cib=2:EOS") { lexatom_index_at_begin = 2; end_of_stream_in_buffer_f = true;  }

    G_init(&it);
    
    printf("        lexeme_start_p: read_p: end_p: begin_ci: end_ci: buffer:\n");
    while( G_next(&it) ) {
        instantiate_iterator(&buffer, &it, 
                             end_of_stream_in_buffer_f,
                             &memory[0], MemorySize, 
                             &content[0], ContentSize);
        buffer.input.lexatom_index_begin = lexatom_index_at_begin;
        QUEX_NAME(Buffer_callbacks_set)(&buffer, 
                                             self_on_content_change,
                                             self_on_overflow,
                                             &theAux);


        printf("\n-( %2i )---------------------------------------------\n", (int)G_key_get(&it));
        self_print(&buffer);

        /* Preparation of Verification_______________________________________*/
        before.end_p     = buffer.input.end_p;
        before.read_p    = buffer._read_p;
        before.read_char = *buffer._read_p;
        if( buffer._lexeme_start_p ) {
            before.lexeme_start_p    = buffer._lexeme_start_p;
            before.lexeme_start_char = *buffer._lexeme_start_p;
            min_p                    = QUEX_MIN(buffer._read_p, buffer._lexeme_start_p);
        }
        else {
            min_p                    = buffer._read_p;
        }
        memcpy(&backup[0], min_p, buffer.input.end_p - min_p);

        /* Call Function under Test _________________________________________*/
        move_distance = QUEX_NAME(Buffer_free_front)(&buffer);

        self_print(&buffer);

        /* Verification _____________________________________________________*/
        if( buffer._memory._back - before.end_p > move_distance ) {
            hwut_verify(buffer.input.end_p == &before.end_p[move_distance]);
        } 
        else {
            hwut_verify(buffer.input.end_p == buffer._memory._back);
        }
        hwut_verify(buffer._read_p  == &before.read_p[move_distance]);
        hwut_verify(*buffer._read_p == before.read_char);
        if(    before.lexeme_start_p 
            && buffer._backup_lexatom_index_of_lexeme_start_p == (QUEX_TYPE_STREAM_POSITION)-1 ) {
            hwut_verify(buffer._lexeme_start_p  == &before.lexeme_start_p[move_distance]);
            hwut_verify(*buffer._lexeme_start_p == before.lexeme_start_char);
            min_p = QUEX_MIN(buffer._read_p, buffer._lexeme_start_p);
        }
        else {
            min_p = buffer._read_p;
        }
        hwut_verify(memcmp(&backup[0], min_p, buffer.input.end_p - min_p) == 0);

        QUEX_NAME(Buffer_destruct)(&buffer);
        ++count;
    }
    printf("<terminated %i>\n", count);
}

