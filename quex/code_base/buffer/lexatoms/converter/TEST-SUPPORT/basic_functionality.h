#include "minimum-definitions.h"
#ifdef __cplusplus
#include "test_cpp/lib/buffer/lexatoms/converter/Converter"
#else
#include "test_c/lib/buffer/lexatoms/converter/Converter"
#endif
#include <stdint.h>

QUEX_NAMESPACE_MAIN_OPEN

extern void test_with_available_codecs(void (*test)(QUEX_NAME(Converter)*, const char*));

extern void test_conversion_in_one_beat(QUEX_NAME(Converter)* converter, 
                                        const char*           CodecName);

extern void test_conversion_stepwise_source(QUEX_NAME(Converter)* converter, 
                                            const char*           CodecName);

extern void test_conversion_stepwise_drain(QUEX_NAME(Converter)* converter, 
                                           const char*           CodecName);
extern void print_result(const char*);

#define STR_CORE(X) #X
#define STR(X) STR_CORE(X)

QUEX_NAMESPACE_MAIN_CLOSE
