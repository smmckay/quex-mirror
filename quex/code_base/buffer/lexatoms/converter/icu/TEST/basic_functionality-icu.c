/* Implementation of what is specific to 'ICU':
 *
 * test_this(): Create an ICU Converter, call the given 'test' function and 
 *              delete the converter. 
 *
 * Remaining organization and execution of tests is done in 
 * 'basic_functionality.c'.                                     
 *
 * (C) Frank-Rene Schaefer.                                                  */
#include <basic_functionality.h>
#ifdef   __cplusplus
#include "test_cpp/lib/buffer/lexatoms/converter/icu/Converter_ICU.i"
#include "test_cpp/lib/buffer/lexatoms/converter/Converter.i"
#else
#include "test_c/lib/buffer/lexatoms/converter/icu/Converter_ICU.i"
#include "test_c/lib/buffer/lexatoms/converter/Converter.i"
#endif

QUEX_NAMESPACE_MAIN_OPEN

void 
test_this(const char* Codec, void (*test)(QUEX_NAME(Converter)*, const char*))
{
    const char* codec = (strcmp(Codec, "UCS-4BE") == 0) ? "UTF32-BE" : Codec;
    QUEX_NAME(Converter)* converter = QUEX_NAME(Converter_ICU_new)(codec, (const char*)0);
    if( ! converter ) {
        printf("No converter allocated for codec: '%s'.\n", codec);
    }
    test(converter, Codec);   
    print_result(Codec);
    converter->delete_self(converter);
}

QUEX_NAMESPACE_MAIN_CLOSE
