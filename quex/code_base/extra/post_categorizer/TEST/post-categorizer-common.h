#ifndef  __INCLUDE_GUARD__QUEX__ANALYZER__TEST__POST_CATEGORIZER__COMMON_H
#define  __INCLUDE_GUARD__QUEX__ANALYZER__TEST__POST_CATEGORIZER__COMMON_H

#include <cstdio>
#include <cstdlib>
#include <cstring>
#define QUEX_TYPE_LEXATOM        char
#define QUEX_TKN_UNINITIALIZED   1
$$INC: extra/test_environment/TestAnalyzer-configuration$$
$$INC: lexeme_converter/from-unicode-buffer$$
#undef  QUEX_TYPE_TOKEN_ID
#define QUEX_TYPE_TOKEN_ID  int
#undef  QUEX_OPTION_INCLUDE_STACK
$$INC: lexeme$$
$$INC: extra/post_categorizer/PostCategorizer.i$$
$$INC: lexeme_converter/from-unicode-buffer.i$$
$$INC: lexeme.i$$

#endif /* __INCLUDE_GUARD__QUEX__ANALYZER__TEST__POST_CATEGORIZER__COMMON_H */
