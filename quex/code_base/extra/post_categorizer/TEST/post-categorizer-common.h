#ifndef  __INCLUDE_GUARD__QUEX__ANALYZER__TEST__POST_CATEGORIZER__COMMON_H
#define  __INCLUDE_GUARD__QUEX__ANALYZER__TEST__POST_CATEGORIZER__COMMON_H

#include <cstdio>
#include <cstdlib>
#include <cstring>
#define QUEX_TYPE_LEXATOM        char
#define QUEX_TKN_UNINITIALIZED   1
#include "test_environment/TestAnalyzer-configuration"
#include "ut/lib/lexeme_converter/from-unicode-buffer"
#undef  QUEX_TYPE_TOKEN_ID
#define QUEX_TYPE_TOKEN_ID  int
#undef  QUEX_OPTION_INCLUDE_STACK
#include "ut/lib/lexeme"
#include "ut/lib/extra/post_categorizer/PostCategorizer.i"
#include "ut/lib/lexeme_converter/from-unicode-buffer.i"
#include "ut/lib/lexeme.i"

#endif /* __INCLUDE_GUARD__QUEX__ANALYZER__TEST__POST_CATEGORIZER__COMMON_H */
