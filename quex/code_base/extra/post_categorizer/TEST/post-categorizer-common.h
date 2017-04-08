#ifndef  __INCLUDE_GUARD__QUEX__ANALYZER__TEST__POST_CATEGORIZER__COMMON_H
#define  __INCLUDE_GUARD__QUEX__ANALYZER__TEST__POST_CATEGORIZER__COMMON_H

#include <cstdio>
#include <cstdlib>
#include <cstring>
#define QUEX_TYPE_LEXATOM char
#define QUEX_OPTION_POST_CATEGORIZER
#define QUEX_TKN_UNINITIALIZED   1
#include <quex/code_base/extra/test_environment/TestAnalyzer-configuration>
#include <quex/code_base/converter_helper/from-unicode-buffer>
#undef  QUEX_TYPE_TOKEN_ID
#define QUEX_TYPE_TOKEN_ID  int
#undef  QUEX_OPTION_INCLUDE_STACK
#include <quex/code_base/lexeme>
#include <quex/code_base/extra/post_categorizer/PostCategorizer.i>
#include <quex/code_base/converter_helper/from-unicode-buffer.i>
#include <quex/code_base/lexeme.i>

#endif /* __INCLUDE_GUARD__QUEX__ANALYZER__TEST__POST_CATEGORIZER__COMMON_H */
