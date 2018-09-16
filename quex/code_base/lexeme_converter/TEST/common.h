/* Configure this header by defining one of:
 *
 *    TEST_UTF8, TEST_UTF16, TEST_UNICODE, TEST_CODEC
 *                                                      */
#ifndef __INCLUDE_GUARD__COMMON_H
#define __INCLUDE_GUARD__COMMON_H

#define QUEX_SETTING_CHAR_CODEC    8
#define QUEX_SETTING_WCHAR_CODEC   32

#include "ut/lib/quex/asserts"
#include "../../TESTS/minimum-definitions.h"
#include "ut/lib/lexeme/converter-from-utf8.i"
#include "ut/lib/lexeme/converter-from-utf16.i"
#include "ut/lib/lexeme/converter-from-utf32.i"

using namespace std;

#define ____MYSTRING(X) #X
#define __MYSTRING(X) ____MYSTRING(X)


#endif /* __INCLUDE_GUARD__COMMON_H */
