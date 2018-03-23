#ifndef INCLUDE_GUARD_TEST_MOVE_AWAY_PASSED_CONTENT_COMMON_H
#define INCLUDE_GUARD_TEST_MOVE_AWAY_PASSED_CONTENT_COMMON_H

#include "TESTS/minimum-definitions.h"
#include "ut/lib/buffer/lexatoms/LexatomLoader.i"
#include "ut/lib/buffer/Buffer_print.i"
#include "ut/lib/buffer/Buffer.i"
#include "ut/lib/buffer/asserts.i"
#include "ut/lib/lexeme_converter/from-unicode-buffer.i"
#include "ut/lib/single.i"
#include <cstring>
#include <hwut_unit.h>

/* Define static functions included in each test file:
 * => avoid dedicated compilation for each setup.
 * => avoid mentioning the 'common.cpp' on each compiler command line.       */
using namespace quex; /* One should not do this in a header ...              */

typedef struct {
    QUEX_NAME(Buffer)* buffer;
} SomethingContainingABuffer_t;


static void self_print(QUEX_NAME(Buffer)* buffer);
static void memory_fill_with_content(QUEX_TYPE_LEXATOM* memory, size_t MemorySize, 
                                     QUEX_TYPE_LEXATOM* content, size_t ContentSize);
static int  cl_has(int argc, char** argv, const char* What);
static void instantiate_iterator(QUEX_NAME(Buffer)* buffer, G_t* it,
                                 bool EndOfStreamInBufferF,
                                 QUEX_TYPE_LEXATOM* memory, ptrdiff_t MemorySize,
                                 QUEX_TYPE_LEXATOM* content, ptrdiff_t ContentSize);
static void self_on_content_change(void* aux);
static void self_on_overflow(void* aux);


static int cl_has(int argc, char** argv, const char* What)
{ return argc > 1 && strcmp(argv[1], What) == 0; }

static void
memory_fill_with_content(QUEX_TYPE_LEXATOM* memory, size_t MemorySize, 
                         QUEX_TYPE_LEXATOM* content, size_t ContentSize)
{
    memset((void*)&memory[1], 0xFF, 
           (MemorySize - 2)*sizeof(QUEX_TYPE_LEXATOM));
    memcpy((void*)&memory[1], (void*)content, 
           ContentSize*sizeof(QUEX_TYPE_LEXATOM)); 
}

static void
self_print(QUEX_NAME(Buffer)* buffer)
{
    printf("        @%i '%c';         @%i '%c'; @%2i;   @%i;       ", 
           (int)(buffer->_lexeme_start_p - buffer->_memory._front),
           (int)(*(buffer->_lexeme_start_p)),
           (int)(buffer->_read_p - buffer->_memory._front),
           (int)(*(buffer->_read_p)),
           (int)(buffer->input.end_p ? buffer->input.end_p - buffer->_memory._front : -1),
           (int)(buffer->input.lexatom_index_end_of_stream));

    QUEX_NAME(Buffer_print_content)(buffer);
    printf("\n");
}

static void
instantiate_iterator(QUEX_NAME(Buffer)* buffer, G_t* it,
                     bool EndOfStreamInBufferF,
                     QUEX_TYPE_LEXATOM* memory, ptrdiff_t MemorySize,
                     QUEX_TYPE_LEXATOM* content, ptrdiff_t ContentSize)
/* Sets the buffer up according to what is specified in the iterator:
 *
 *  it.read_i         --> position of the buffer's _read_p.
 *  it.lexeme_start_i --> position of the buffer's _lexeme_start_p.
 *                                                                           */
{
    QUEX_TYPE_LEXATOM*   BeginP;
    QUEX_TYPE_LEXATOM*   end_p;
    ptrdiff_t            memory_size = EndOfStreamInBufferF ? MemorySize : ContentSize + 2;

    end_p  = &memory[ContentSize + 1];
    *end_p = QUEX_SETTING_BUFFER_LIMIT_CODE;

    /* Filler = 0x0, otherwise, buffer would start loading content */
    assert(memory_size <= MemorySize);
    assert(end_p - &memory[1] < memory_size);
    QUEX_NAME(Buffer_construct)(buffer, 
                                (QUEX_NAME(LexatomLoader)*)0x0, 
                                &memory[0], memory_size, end_p, 
                                E_Ownership_EXTERNAL,
                                (QUEX_NAME(Buffer)*)0);

    memory_fill_with_content(&memory[0], MemorySize, 
                             &content[0], ContentSize);

    BeginP                  = &buffer->_memory._front[1];
    buffer->_lexeme_start_p = &BeginP[it->lexeme_start_i];
    buffer->_read_p         = &BeginP[it->read_i];

    QUEX_NAME(Buffer_register_content)(buffer, end_p, 0);
    if( EndOfStreamInBufferF ) {
        buffer->input.lexatom_index_end_of_stream =   buffer->input.lexatom_index_begin \
                                                      + (QUEX_TYPE_STREAM_POSITION)(end_p - BeginP);
    }
    else {
        buffer->input.lexatom_index_end_of_stream = (QUEX_TYPE_STREAM_POSITION)-1;
    }

    QUEX_BUFFER_ASSERT_limit_codes_in_place(buffer);
}

static void
self_on_content_change(void* aux)
{ 
    const QUEX_TYPE_LEXATOM* BeginP = &((SomethingContainingABuffer_t*)aux)->buffer->_memory._front[1];
    const QUEX_TYPE_LEXATOM* EndP   = ((SomethingContainingABuffer_t*)aux)->buffer->input.end_p;
    printf("on_content_change: size: %i;\n", (int)(EndP - BeginP));
}

static void
self_on_overflow(void* aux) 
{ 
    printf("on_buffer_overflow: %s;\n", "forward");
}

#endif /* INCLUDE_GUARD_TEST_MOVE_AWAY_PASSED_CONTENT_COMMON_H */

