#ifndef __INCLUDE_GUARD__MESSAGING_FRAMEWORK__
#define __INCLUDE_GUARD__MESSAGING_FRAMEWORK__

#include <inttypes.h>
#include <stddef.h>

#define ELEMENT_TYPE uint8_t

extern size_t receiver_get_pointer_to_received(ELEMENT_TYPE** buffer);
extern size_t receiver_get_pointer_to_received_whole_characters(ELEMENT_TYPE** rx_buffer);
extern size_t receiver_get_pointer_to_received_to_internal_buffer();
/* extern size_t receiver_fill_here(QUEX_TYPE_LEXATOM* place, size_t MaxN); */
extern size_t receiver_receive_in_this_place(ELEMENT_TYPE* BeginP, 
                                             const ELEMENT_TYPE* EndP);

#endif /*_INCLUDE_GUARD__MESSAGING_FRAMEWORK_*/
