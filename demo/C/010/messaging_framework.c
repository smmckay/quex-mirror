#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "messaging_framework.h"

#ifdef QUEX_EXAMPLE_WITH_CONVERTER
    static ELEMENT_TYPE messaging_framework_data[] = 
       "Ελληνικά • Euskara • فارسی • Frysk • Galego • 한국어 • हिन्दी bye";
#else
    static QUEX_TYPE_CHARACTER   messaging_framework_data[] = 
       "hello 4711 bonjour 0815 world 7777 le 31451 monde le monde 00 welt 1234567890 hallo 1212 hello bye";
#endif

static size_t                messaging_framework_data_size()
{ 
    ELEMENT_TYPE* iterator = messaging_framework_data;
    for(; *iterator != 0; ++iterator);
    return (iterator - messaging_framework_data + 1) * sizeof(ELEMENT_TYPE);
}

size_t 
receiver_fill(ELEMENT_TYPE** rx_buffer)
    /* Simulate the reception into a place that is defined by the low 
     * level driver. The low level driver reports the address of that place
     * and the size.                                                         */
{
    static ELEMENT_TYPE*  iterator = messaging_framework_data;
    const size_t          remainder_size =   messaging_framework_data_size() - 1 
                                           - (iterator - messaging_framework_data);
    size_t                size = (size_t)((float)(rand()) / (float)(RAND_MAX) * 10.0) + 1;

    if( size >= remainder_size ) size = remainder_size; 

    *rx_buffer = iterator; 
    iterator += size;

    if( size != 0 ) {
        __quex_assert(iterator < messaging_framework_data + messaging_framework_data_size());
    } else {
        __quex_assert(iterator == messaging_framework_data + messaging_framework_data_size());
    }

    return size;
}

size_t 
receiver_fill_whole_characters(ELEMENT_TYPE** rx_buffer)
    /* Simulate the reception into a place that is defined by the low 
     * level driver. The low level driver reports the address of that place
     * and the size.                                                         */
{
    static ELEMENT_TYPE*  iterator = messaging_framework_data;
    const size_t          remainder_size =   messaging_framework_data_size() - 1 
                                           - (iterator - messaging_framework_data);
    size_t                size = (size_t)((float)(rand()) / (float)(RAND_MAX) * 5.0) + 1;

    if( size >= remainder_size ) size = remainder_size; 

    *rx_buffer = iterator; 
    iterator += size;

    /* We are dealing here with the UTF-8 type of message */
    __quex_assert(sizeof(ELEMENT_TYPE) == sizeof(uint8_t));

    /* If the two highest bits == '10' then it is a follow character in 
     * a utf8 encoded character. Thus, search for the first non '10' 
     * which indicates that we are pointing to a new letter.            */
    while( (*iterator & 0xC0) == 0x80 ) ++iterator;

    size = iterator - *rx_buffer;

    if( size != 0 ) {
        __quex_assert(iterator < messaging_framework_data + messaging_framework_data_size());
    } else {
        __quex_assert(iterator == messaging_framework_data + messaging_framework_data_size());
    }

    return size;
}

size_t 
receiver_fill_syntax_chunk(ELEMENT_TYPE** rx_buffer)
/* Simulate the reception into a place that is defined by the low level driver.
 * The low level driver reports the address of that place and the size.
 *                                                                           */
{
    static ptrdiff_t  cursor = 0;
    ptrdiff_t         cursor_before = cursor;

    *rx_buffer = &messaging_framework_data[cursor]; 

    do {
        ++cursor;
    } while( messaging_framework_data[cursor] && messaging_framework_data[cursor] != ' ' );

    return cursor - cursor_before;
}

size_t 
receiver_copy(ELEMENT_TYPE* BufferBegin, size_t BufferSize)
/* Simulate a low lever driver that is able to fill a specified position in 
 * memory.                                                                   */
{
    static ELEMENT_TYPE*  iterator = messaging_framework_data;
    size_t                size = (size_t)((float)(rand()) / (float)(RAND_MAX) * 5.0) + 1;

    assert(iterator < messaging_framework_data + messaging_framework_data_size());
    if( iterator + size >= messaging_framework_data + messaging_framework_data_size() - 1 ) 
        size = messaging_framework_data_size() - (iterator - messaging_framework_data) - 1; 
    if( size > BufferSize )    
        size = BufferSize;

    memcpy(BufferBegin, iterator, size);
    iterator += size;

    return size;
}

size_t 
receiver_copy_syntax_chunk(ELEMENT_TYPE* BufferBegin, size_t BufferSize)
/* Simulate a low lever driver that is able to fill a specified position in 
 * memory.                                                                   */
{
    static ptrdiff_t  cursor = 0;
    ptrdiff_t         cursor_before = cursor;

    do {
        ++cursor;
    } while( messaging_framework_data[cursor] && messaging_framework_data[cursor] != ' ' );

    /* If the target buffer cannot carry it, we drop it.                     */
    memcpy(BufferBegin, 
           &messaging_framework_data[cursor_before],
           cursor - cursor_before); 

    return cursor - cursor_before;
}

ELEMENT_TYPE   MESSAGING_FRAMEWORK_BUFFER[MESSAGING_FRAMEWORK_BUFFER_SIZE];

size_t
receiver_fill_to_internal_buffer()
/* Simulate a low level driver that iself has a hardware fixed position in
 * memory which it fills on demand.
 *                                                                           */
{
    memcpy(&MESSAGING_FRAMEWORK_BUFFER[1], 
           messaging_framework_data, 
           messaging_framework_data_size() * sizeof(ELEMENT_TYPE));
    return messaging_framework_data_size();
}
