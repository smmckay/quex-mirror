#ifndef __INCLUDE_GUARD__MESSAGING_FRAMEWORK__
#define __INCLUDE_GUARD__MESSAGING_FRAMEWORK__

#include <inttypes.h>
#include <stddef.h>

#define ELEMENT_TYPE uint8_t

typedef struct {
    ELEMENT_TYPE* begin_p;
    ELEMENT_TYPE* end_p;
} MemoryChunk;

/* Assume that some low level driver communicates the place where 
 * input is placed via macros.                                     */
#define  MESSAGING_FRAMEWORK_BUFFER_SIZE  ((size_t)(512))
extern ELEMENT_TYPE   MESSAGING_FRAMEWORK_BUFFER[MESSAGING_FRAMEWORK_BUFFER_SIZE];

extern size_t receiver_get_pointer_to_received(ELEMENT_TYPE** buffer);
extern size_t receiver_get_pointer_to_received_whole_characters(ELEMENT_TYPE** rx_buffer);
extern size_t receiver_get_pointer_to_received_to_internal_buffer();
/* extern size_t receiver_fill_here(QUEX_TYPE_LEXATOM* place, size_t MaxN); */
extern size_t receiver_fill(ELEMENT_TYPE*, size_t);

#endif /*_INCLUDE_GUARD__MESSAGING_FRAMEWORK_*/
