#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "receiver.h"

#ifdef QUEX_EXAMPLE_WITH_CONVERTER
#   include "lexConverter"
    static ELEMENT_TYPE receiver_data[] = 
       "Ελληνικά • Euskara • فارسی • Frysk • Galego • 한국어 • हिन्दी bye";
#else
#   include "lexPlain"
    static QUEX_TYPE_LEXATOM   receiver_data[] = 
       "A little nonsense now and then is cherished by the wisest men bye";
#endif

/* Content size without the implicit terminating zero. */
#define CONTENT_SIZE   ((sizeof(receiver_data)/sizeof(receiver_data[0])) - 1)

size_t 
receiver_get_pointer_to_received(ELEMENT_TYPE** rx_buffer)
/* Simulate the reception into a place that is defined by the low level driver.
 * The low level driver reports the address of that place and the size.
 *                                                                           */
{
    static ELEMENT_TYPE*  iterator       = &receiver_data[0];
    const size_t          remainder_size =   CONTENT_SIZE  
                                           - (iterator - &receiver_data[0]);
    size_t                size = (size_t)((float)(rand()) / (float)(RAND_MAX) * 10.0) + 1;

    if( size >= remainder_size ) size = remainder_size; 

    *rx_buffer = iterator; 
    iterator += size;

    if( size != 0 ) {
        __quex_assert(iterator <= receiver_data + CONTENT_SIZE);
    } else {
        __quex_assert(iterator == receiver_data + CONTENT_SIZE + 1);
    }

    return size;
}

size_t 
receiver_get_pointer_to_received_whole_characters(ELEMENT_TYPE** rx_buffer)
    /* Simulate the reception into a place that is defined by the low 
     * level driver. The low level driver reports the address of that place
     * and the size.                                                         */
{
    static ELEMENT_TYPE*  iterator = receiver_data;
    const size_t          remainder_size =   CONTENT_SIZE - 1 
                                           - (iterator - receiver_data);
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
        __quex_assert(iterator <= receiver_data + CONTENT_SIZE);
    } else {
        __quex_assert(iterator == receiver_data + CONTENT_SIZE + 1);
    }

    return size;
}

size_t 
receiver_receive_in_this_place(ELEMENT_TYPE* BeginP, const ELEMENT_TYPE* EndP)
/* Simulate a low lever driver that is able to fill a specified position in 
 * memory.                                                                   */
{
    static ELEMENT_TYPE*  iterator   = receiver_data;
    const size_t          BufferSize = EndP - BeginP;
    size_t                size = (size_t)((float)(rand()) / (float)(RAND_MAX) * 10.0) + 1;

    assert(iterator <= receiver_data + CONTENT_SIZE);
    if( iterator + size >= receiver_data + CONTENT_SIZE ) 
        size = CONTENT_SIZE - (iterator - receiver_data); 
    if( size > BufferSize ) size = BufferSize;

    memcpy(BeginP, iterator, size);
    iterator += size;

    return size;
}

size_t
receiver_fill_here(QUEX_TYPE_LEXATOM* place, size_t MaxN)
/* Simulate a low level driver that iself has a hardware fixed position in
 * memory which it fills on demand.
 *                                                                           */
{
    const size_t ElementN = sizeof(receiver_data) / sizeof(receiver_data[0]);
    const size_t LetterN  = ElementN - 1;
    assert(MaxN >= ElementN);

    memcpy((void*)place, (void*)&receiver_data[0], 
           LetterN * sizeof(QUEX_TYPE_LEXATOM));
    return LetterN;
}

