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
#include <quex/code_base/definitions>
#include <quex/code_base/asserts>
#include <quex/code_base/compatibility/stdint.h>
#include <quex/code_base/MemoryManager>




#   line 2 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

#include <stdio.h>
#include <string.h>

struct quex_Token_tag;

extern const char* 
QUEX_NAME_TOKEN(get_string)(struct quex_Token_tag* me,  char*  buffer, size_t   BufferSize); 

#include <quex/code_base/lexeme_converter/from-unicode-buffer>

#include <quex/code_base/lexeme>
   

#   line 37 "TestAnalyzer-token.h"

 
typedef struct QUEX_SETTING_USER_CLASS_DECLARATION_EPILOG quex_Token_tag {
    QUEX_TYPE_TOKEN_ID    _id;

#   line 20 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"
    const QUEX_TYPE_LEXATOM* text;

#   line 46 "TestAnalyzer-token.h"

#   line 21 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"
    size_t                   number;

#   line 51 "TestAnalyzer-token.h"


#   ifdef     QUEX_OPTION_TOKEN_STAMPING_WITH_LINE_AND_COLUMN
#       ifdef QUEX_OPTION_COUNTER_LINE
        QUEX_TYPE_TOKEN_LINE_N    _line_n;
#       endif
#       ifdef  QUEX_OPTION_COUNTER_COLUMN
        QUEX_TYPE_TOKEN_COLUMN_N  _column_n;
#       endif
#   endif

#   line 119 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

       /*
        */
   

#   line 69 "TestAnalyzer-token.h"

} quex_Token;

QUEX_INLINE void         quex_Token_construct(quex_Token*);
QUEX_INLINE void         quex_Token_copy_construct(quex_Token*, 
                                                     const quex_Token*);
QUEX_INLINE void         quex_Token_copy(quex_Token*, const quex_Token*);
QUEX_INLINE void         quex_Token_destruct(quex_Token*);

/* NOTE: Setters and getters as in the C++ version of the token class are not
 *       necessary, since the members are accessed directly.                   */

QUEX_INLINE void         quex_Token_set(quex_Token*            __this, 
                                          const QUEX_TYPE_TOKEN_ID ID);

QUEX_INLINE const char*  quex_Token_map_id_to_name(const QUEX_TYPE_TOKEN_ID);

QUEX_INLINE bool         quex_Token_take_text(quex_Token*            __this, 
                                                const QUEX_TYPE_LEXATOM* Begin, 
                                                const QUEX_TYPE_LEXATOM* End);

#ifdef QUEX_OPTION_TOKEN_REPETITION_SUPPORT
QUEX_INLINE size_t       quex_Token_repetition_n_get(quex_Token*);
QUEX_INLINE void         quex_Token_repetition_n_set(quex_Token*, size_t);
#endif /* QUEX_OPTION_TOKEN_REPETITION_SUPPORT */

QUEX_NAMESPACE_TOKEN_OPEN
extern QUEX_TYPE_LEXATOM   QUEX_NAME_TOKEN(LexemeNull);
QUEX_NAMESPACE_TOKEN_CLOSE


#endif /* __QUEX_INCLUDE_GUARD__TOKEN__GENERATED__QUEX___TOKEN */
