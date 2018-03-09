#ifndef QUEX_INCLUDE_GUARD_BUFFER_BASIC_FUNCTIONALITY
#define QUEX_INCLUDE_GUARD_BUFFER_BASIC_FUNCTIONALITY

$$INC: extra/test_environment/TestAnalyzer-configuration$$
$$INC: definitions$$
$$INC: buffer/Buffer$$
$$INC: MemoryManager$$
#include <hwut_unit.h>
#ifdef __cplusplus
$$INC: buffer/Buffer.i$$
#endif

QUEX_NAMESPACE_MAIN_OPEN

bool        basic_functionality(QUEX_NAME(Buffer)* me, const char* ReferenceFileName);
const char* find_reference(const char* file_stem);

QUEX_NAMESPACE_MAIN_CLOSE

#endif /* QUEX_INCLUDE_GUARD_BUFFER_BASIC_FUNCTIONALITY */
