/* -*- C++ -*-   vim: set syntax=cpp: 
 * (C) 2004-2017 Frank-Rene Schaefer
 * ABSOLUTELY NO WARRANTY
 */
#ifndef __QUEX_INCLUDE_GUARD__TOKEN__GENERATED__QUEX___TOKEN
#define __QUEX_INCLUDE_GUARD__TOKEN__GENERATED__QUEX___TOKEN

/* For '--token-class-only' the following option may not come directly
 * from the configuration file.                                        */
#ifndef    __QUEX_OPTION_PLAIN_C
#   define __QUEX_OPTION_PLAIN_C
#endif
#include "test_environment/lib/definitions"
#include "test_environment/lib/asserts"
#include "test_environment/lib/compatibility/stdint.h"
#include "test_environment/lib/MemoryManager"


#include "test_environment/lib/lexeme"


#   line 2 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

#include <stdio.h>
#include <string.h>

struct quex_Token_tag;

extern const char* 
QUEX_NAME_TOKEN(get_string)(struct quex_Token_tag* me,  char*  buffer, size_t   BufferSize); 

#include "lib/lexeme_converter/from-unicode-buffer"
   

#   line 36 "test_environment/TestAnalyzer-token.h"

 
typedef struct QUEX_SETTING_USER_CLASS_DECLARATION_EPILOG quex_Token_tag {
    TestAnalyzer_token_id_t    id;

#   line 19 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"
    const TestAnalyzer_lexatom_t* text;

#   line 45 "test_environment/TestAnalyzer-token.h"

#   line 20 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"
    size_t                   number;

#   line 50 "test_environment/TestAnalyzer-token.h"


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
   

#   line 67 "test_environment/TestAnalyzer-token.h"

} quex_Token;

QUEX_INLINE void         quex_Token_construct(quex_Token*);
QUEX_INLINE void         quex_Token_copy_construct(quex_Token*, 
                                                     const quex_Token*);
QUEX_INLINE void         quex_Token_copy(quex_Token*, const quex_Token*);
QUEX_INLINE void         quex_Token_destruct(quex_Token*);

/* NOTE: Setters and getters as in the C++ version of the token class are not
 *       necessary, since the members are accessed directly.                   */

QUEX_INLINE void         quex_Token_set(quex_Token*            me, 
                                          const TestAnalyzer_token_id_t ID);

QUEX_INLINE const char*  quex_Token_map_id_to_name(const TestAnalyzer_token_id_t);

#ifdef QUEX_OPTION_TOKEN_TAKE_TEXT_SUPPORT
QUEX_INLINE bool         quex_Token_take_text(quex_Token*            me, 
                                                const TestAnalyzer_lexatom_t* Begin, 
                                                const TestAnalyzer_lexatom_t* End);
#endif

#ifdef QUEX_OPTION_TOKEN_REPETITION_SUPPORT
QUEX_INLINE size_t       quex_Token_repetition_n_get(quex_Token*);
QUEX_INLINE void         quex_Token_repetition_n_set(quex_Token*, size_t);
#endif /* QUEX_OPTION_TOKEN_REPETITION_SUPPORT */

QUEX_NAMESPACE_TOKEN_OPEN
extern TestAnalyzer_lexatom_t   QUEX_NAME(LexemeNull);
QUEX_NAMESPACE_TOKEN_CLOSE


#endif /* __QUEX_INCLUDE_GUARD__TOKEN__GENERATED__QUEX___TOKEN */
