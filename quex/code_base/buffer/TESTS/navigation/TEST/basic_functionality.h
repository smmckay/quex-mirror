#ifndef QUEX_INCLUDE_GUARD_BUFFER_BASIC_FUNCTIONALITY
#define QUEX_INCLUDE_GUARD_BUFFER_BASIC_FUNCTIONALITY

#include "TESTS/minimum-definitions.h"
#include "ut/lib/definitions"
#include "ut/lib/buffer/Buffer"
#include "ut/lib/MemoryManager"
#include <hwut_unit.h>
#ifdef __cplusplus
#include "ut/lib/buffer/Buffer.i"
#endif

QUEX_NAMESPACE_MAIN_OPEN

bool        basic_functionality(QUEX_NAME(Buffer)* me, const char* ReferenceFileName);
const char* find_reference(const char* file_stem);

QUEX_NAMESPACE_MAIN_CLOSE

#endif /* QUEX_INCLUDE_GUARD_BUFFER_BASIC_FUNCTIONALITY */
