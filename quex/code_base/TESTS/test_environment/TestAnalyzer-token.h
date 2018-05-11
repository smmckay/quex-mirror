/* -*- C++ -*-   vim: set syntax=cpp:
* (C) 2004-2017 Frank-Rene Schaefer
* ABSOLUTELY NO WARRANTY
*/
#ifndef __QUEX_INCLUDE_GUARD__TOKEN__GENERATED____TOKEN
#define __QUEX_INCLUDE_GUARD__TOKEN__GENERATED____TOKEN

/* For '--token-class-only' the following option may not come directly
* from the configuration file.                                        */
#ifndef    __QUEX_OPTION_PLAIN_C
#   define __QUEX_OPTION_PLAIN_C
#endif
#include "stddef.h"
#include "test_environment/lib/compatibility/stdint.h"
#include "test_environment/TestAnalyzer-configuration.h"
#include "test_environment/lib/definitions"
#include "test_environment/lib/asserts"
#include "test_environment/lib/MemoryManager"
#include "test_environment/lib/lexeme_base"


#   line 2 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

#include <stdio.h>
#include <string.h>
#include "test_environment/converter-from-lexeme"

struct Token_tag;

extern const char*
QUEX_NAME_TOKEN(get_string)(struct Token_tag* me,  char*  buffer, size_t   BufferSize);



#   line 34 "test_environment/TestAnalyzer-token.h"



typedef struct QUEX_SETTING_USER_CLASS_DECLARATION_EPILOG Token_tag {
TestAnalyzer_token_id_t    id;

#   line 19 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"
const TestAnalyzer_lexatom_t* text;

#   line 42 "test_environment/TestAnalyzer-token.h"


#   line 20 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"
size_t                   number;

#   line 46 "test_environment/TestAnalyzer-token.h"



#   ifdef     QUEX_OPTION_TOKEN_STAMPING_WITH_LINE_AND_COLUMN
#       ifdef QUEX_OPTION_COUNTER_LINE
TestAnalyzer_token_line_n_t    _line_n;
#       endif
#       ifdef  QUEX_OPTION_COUNTER_COLUMN
TestAnalyzer_token_column_n_t  _column_n;
#       endif
#   endif

#   line 105 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

/* Nothing here. */


#   line 62 "test_environment/TestAnalyzer-token.h"


} Token;

QUEX_INLINE void         Token_construct(Token*);
QUEX_INLINE void         Token_copy_construct(Token*,
const Token*);
QUEX_INLINE void         Token_copy(Token*, const Token*);
QUEX_INLINE void         Token_destruct(Token*);

/* NOTE: Setters and getters as in the C++ version of the token class are not
*       necessary, since the members are accessed directly.                   */

QUEX_INLINE void         Token_set(Token*            me,
const TestAnalyzer_token_id_t ID);

QUEX_INLINE const char*  Token_map_id_to_name(const TestAnalyzer_token_id_t);

#ifdef QUEX_OPTION_TOKEN_TAKE_TEXT_SUPPORT
QUEX_INLINE bool         Token_take_text(Token*            me,
const TestAnalyzer_lexatom_t* Begin,
const TestAnalyzer_lexatom_t* End);
#endif

#ifdef QUEX_OPTION_TOKEN_REPETITION_SUPPORT
QUEX_INLINE size_t       Token_repetition_n_get(Token*);
QUEX_INLINE void         Token_repetition_n_set(Token*, size_t);
#endif /* QUEX_OPTION_TOKEN_REPETITION_SUPPORT */

QUEX_NAMESPACE_TOKEN_OPEN
extern TestAnalyzer_lexatom_t   QUEX_NAME(LexemeNull);
QUEX_NAMESPACE_TOKEN_CLOSE


#endif /* __QUEX_INCLUDE_GUARD__TOKEN__GENERATED____TOKEN */
