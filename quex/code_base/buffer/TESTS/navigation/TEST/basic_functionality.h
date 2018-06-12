#ifndef QUEX_INCLUDE_GUARD_BUFFER_BASIC_FUNCTIONALITY
#define QUEX_INCLUDE_GUARD_BUFFER_BASIC_FUNCTIONALITY

#include "TESTS/minimum-definitions.h"
#include <hwut_unit.h>
#ifdef __cplusplus
#include "test_cpp/lib/definitions"
#include "test_cpp/lib/buffer/Buffer"
#include "test_cpp/lib/quex/MemoryManager"
#include "test_cpp/lib/buffer/Buffer.i"
#else
#include "test_c/lib/definitions"
#include "test_c/lib/buffer/Buffer"
#include "test_c/lib/quex/MemoryManager"
#endif

QUEX_NAMESPACE_MAIN_OPEN

bool        basic_functionality(QUEX_NAME(Buffer)* me, const char* ReferenceFileName);
const char* find_reference(const char* file_stem);

QUEX_NAMESPACE_MAIN_CLOSE

#endif /* QUEX_INCLUDE_GUARD_BUFFER_BASIC_FUNCTIONALITY */
