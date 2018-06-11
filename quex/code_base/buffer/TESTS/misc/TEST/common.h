#ifndef UNIT_TEST_COMMON_H
#define UNIT_TEST_COMMON_H

#define  QUEX_OPTION_PLAIN_C_EXT
#include "minimum-definitions.h"
#include "ut/lib/definitions"
#include "ut/lib/buffer/Buffer"
#include "ut/lib/quex/MemoryManager"
#include <hwut_unit.h>
#include <stdio.h>
#include <stddef.h>

void      common_clone(QUEX_NAME(Buffer)* reference, 
                       QUEX_NAME(Buffer)* subject);
void      common_test_single_migration(QUEX_NAME(Buffer)* reference, 
                                       size_t             NewSize,
                                       ptrdiff_t*         shrink_n);
void      common_test_single_extension(QUEX_NAME(Buffer)* reference, 
                                       size_t             NewSize);
void      common_construct_reference_base(QUEX_NAME(Buffer)* reference, 
                                          size_t             reference_size);
ptrdiff_t common_iterate(QUEX_NAME(Buffer)* reference, size_t NewSize, 
                         ptrdiff_t* shrink_n);

void      common_verify_offset(QUEX_NAME(Buffer)* reference, 
                             QUEX_NAME(Buffer)* subject, 
                             QUEX_TYPE_LEXATOM* reference_p, 
                             QUEX_TYPE_LEXATOM* subject_p);
bool      common_verify(QUEX_NAME(Buffer)* reference, 
                      QUEX_NAME(Buffer)* subject);

extern int common_recursion_count_n;

#endif 
