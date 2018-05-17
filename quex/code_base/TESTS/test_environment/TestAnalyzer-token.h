/* -*- C++ -*-   vim: set syntax=cpp:
* (C) 2004-2017 Frank-Rene Schaefer
* ABSOLUTELY NO WARRANTY
*/
#ifndef __QUEX_INCLUDE_GUARD__TOKEN__GENERATED____TESTANALYZER_TOKEN
#define __QUEX_INCLUDE_GUARD__TOKEN__GENERATED____TESTANALYZER_TOKEN

/* For '--token-class-only' the following option may not come directly
* from the configuration file.                                        */
#ifndef    __QUEX_OPTION_PLAIN_C
#   define __QUEX_OPTION_PLAIN_C
#endif

#   line 2 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <test_environment/lib/compatibility/stdint.h>
#include <test_environment/lib/definitions>
#include <test_environment/lib/asserts>
#include <test_environment/lib/MemoryManager>
#include <test_environment/lib/lexeme_base>
#include <test_environment/converter-from-lexeme>

struct TestAnalyzer_Token_tag;

extern const char*
TestAnalyzer_Token_get_string(struct TestAnalyzer_Token_tag* me,
char*                       buffer,
size_t                      BufferSize);



#   line 34 "test_environment/TestAnalyzer-token.h"



#include "test_environment/TestAnalyzer-configuration.h"

struct TestAnalyzer_Token_tag;

inline void         TestAnalyzer_Token_construct(struct TestAnalyzer_Token_tag*);
inline void         TestAnalyzer_Token_copy(struct TestAnalyzer_Token_tag*,
const struct TestAnalyzer_Token_tag*);
inline void         TestAnalyzer_Token_destruct(struct TestAnalyzer_Token_tag*);

/* NOTE: Setters and getters as in the C++ version of the token class are not
*       necessary, since the members are accessed directly.                   */

inline void         TestAnalyzer_Token_set(struct TestAnalyzer_Token_tag* me,
const TestAnalyzer_token_id_t    ID);

inline const char*  TestAnalyzer_Token_map_id_to_name(const TestAnalyzer_token_id_t);

#ifdef QUEX_OPTION_TOKEN_TAKE_TEXT_SUPPORT
inline bool         TestAnalyzer_Token_take_text(struct TestAnalyzer_Token_tag* me,
const TestAnalyzer_lexatom_t*    Begin,
const TestAnalyzer_lexatom_t*    End);
#endif

#ifdef QUEX_OPTION_TOKEN_REPETITION_SUPPORT
inline size_t       TestAnalyzer_Token_repetition_n_get(struct TestAnalyzer_Token_tag*);
inline void         TestAnalyzer_Token_repetition_n_set(struct TestAnalyzer_Token_tag*, size_t);
#endif /* QUEX_OPTION_TOKEN_REPETITION_SUPPORT */


typedef struct QUEX_SETTING_USER_CLASS_DECLARATION_EPILOG TestAnalyzer_Token_tag {
TestAnalyzer_token_id_t    id;

#   line 27 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"
const TestAnalyzer_lexatom_t* text;

#   line 71 "test_environment/TestAnalyzer-token.h"


#   line 28 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"
size_t                   number;

#   line 75 "test_environment/TestAnalyzer-token.h"



#   ifdef     QUEX_OPTION_TOKEN_STAMPING_WITH_LINE_AND_COLUMN
#       ifdef QUEX_OPTION_COUNTER_LINE
TestAnalyzer_token_line_n_t    _line_n;
#       endif
#       ifdef  QUEX_OPTION_COUNTER_COLUMN
TestAnalyzer_token_column_n_t  _column_n;
#       endif
#   endif

#   line 113 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

/* Nothing here. */


#   line 91 "test_environment/TestAnalyzer-token.h"


} TestAnalyzer_Token;

extern TestAnalyzer_lexatom_t TestAnalyzer_LexemeNull;

#endif /* __QUEX_INCLUDE_GUARD__TOKEN__GENERATED____TESTANALYZER_TOKEN */
