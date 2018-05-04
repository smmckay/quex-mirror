/* -*- C++ -*-   vim: set syntax=cpp: 
 * (C) 2004-2009 Frank-Rene Schaefer
 * ABSOLUTELY NO WARRANTY
 */
#ifndef __QUEX_INCLUDE_GUARD__TOKEN__GENERATED__QUEX___TOKEN_I
#define __QUEX_INCLUDE_GUARD__TOKEN__GENERATED__QUEX___TOKEN_I

#ifndef    __QUEX_OPTION_PLAIN_C
#   define __QUEX_OPTION_PLAIN_C
#endif

#include "test_environment/TestAnalyzer-token.h"
#include "test_environment/lib/definitions"
#include "test_environment/lib/lexeme_base"
#include "test_environment/lib/lexeme_base.i"
#include "test_environment/TestAnalyzer-token.h"

QUEX_INLINE void 
quex_Token_set(quex_Token*            __this, 
                 const TestAnalyzer_token_id_t ID) 
{ __this->id = ID; }

QUEX_INLINE void 
quex_Token_construct(quex_Token* __this)
{
#   define self (*__this)
#   define LexemeNull  (&QUEX_NAME(LexemeNull))
    (void)__this;

#   line 25 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

       self.number = 0;
       self.text   = LexemeNull;
   
<<<<LINE_PRAGMA_WITH_CURRENT_LINE_N_AND_FILE_NAME>>>>

#   undef  LexemeNull
#   undef  self
}

QUEX_INLINE void 
quex_Token_copy_construct(quex_Token*       __this, 
                            const quex_Token* __That)
{
    QUEX_NAME_TOKEN(construct)(__this);
    QUEX_NAME_TOKEN(copy)(__this, __That);
}

QUEX_INLINE void 
quex_Token_destruct(quex_Token* __this)
{
#   define self (*__this)
#   define LexemeNull  (&QUEX_NAME(LexemeNull))
    if( ! __this ) return;


#   line 30 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

       if( self.text != LexemeNull ) {
           QUEXED(MemoryManager_free)((void*)self.text,
                                      E_MemoryObjectType_TEXT);
           self.text = LexemeNull;
       }
   
<<<<LINE_PRAGMA_WITH_CURRENT_LINE_N_AND_FILE_NAME>>>>

#   undef  LexemeNull
#   undef  self
}

QUEX_INLINE void
quex_Token_copy(quex_Token*       __this, 
                  const quex_Token* __That)
{
#   define self  (*__this)
#   define Other (*__That)
#   define LexemeNull  (&QUEX_NAME(LexemeNull))
    (void)__this;
    (void)__That;

#   line 38 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

        self.id  = Other.id;

        if( self.text != LexemeNull ) {
            QUEXED(MemoryManager_free)((void*)self.text, E_MemoryObjectType_TEXT);
        }
        if( Other.text != LexemeNull ) {
            self.text = QUEX_NAME(lexeme_clone)(self.text, 
                                                      QUEX_NAME(lexeme_length)(Other.text));
            if( ! self.text ) self.text = LexemeNull;
        }
        self.number = Other.number;
    #   ifdef     QUEX_OPTION_TOKEN_STAMPING_WITH_LINE_AND_COLUMN
        __QUEX_IF_COUNT_LINES(self._line_n     = Other._line_n);
        __QUEX_IF_COUNT_COLUMNS(self._column_n = Other._column_n);
    #   endif
   
<<<<LINE_PRAGMA_WITH_CURRENT_LINE_N_AND_FILE_NAME>>>>

#   undef  LexemeNull
#   undef  Other
#   undef  self
    /* If the user even misses to copy the token id, then there's
     * something seriously wrong.                                 */
    __quex_assert(__this->id == __That->id);
#   ifdef QUEX_OPTION_TOKEN_STAMPING_WITH_LINE_AND_COLUMN
    __QUEX_IF_COUNT_LINES(__quex_assert(__this->_line_n == __That->_line_n));
    __QUEX_IF_COUNT_COLUMNS(__quex_assert(__this->_column_n == __That->_column_n));
#   endif
}


#ifdef QUEX_OPTION_TOKEN_TAKE_TEXT_SUPPORT
QUEX_INLINE bool 
quex_Token_take_text(quex_Token*            __this, 
                       const TestAnalyzer_lexatom_t* Begin, 
                       const TestAnalyzer_lexatom_t* End)
/* RETURNS: true -- if the token claims ownership over the given memory.
 *          false -- if no ownership is claimed.                             */
{
#   define self       (*__this)
#   ifdef  LexemeNull
#   error  "Error LexemeNull shall not be defined here."
#   endif
#   define LexemeNull  (&QUEX_NAME(LexemeNull))
    (void)__this;
    (void)Begin;
    (void)End;

#   line 56 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"


#       if 0
        /* Hint for debug: To check take_text change "#if 0" to "#if 1" */
        {
            const TestAnalyzer_lexatom_t* it = (void*)0x0;
            printf("previous:  '");
            if( self.text != LexemeNull ) {
                for(it = self.text; *it ; ++it) printf("%04X.", (int)*it);
                printf("%04X.", (int)*it);
            }
            printf("'\n");
            printf("take_text: '");
            for(it = Begin; it != End; ++it) printf("%04X.", (int)*it);
            printf("%04X.", (int)*it);
            printf("'\n");
        }
#       endif

        if( self.text != LexemeNull ) {
            QUEXED(MemoryManager_free)((void*)self.text, E_MemoryObjectType_TEXT);
        }
        if( Begin != LexemeNull ) {
            __quex_assert(End >= Begin);
            self.text = QUEX_NAME(lexeme_clone)(Begin, (size_t)(End - Begin));
            if( ! self.text ) self.text = LexemeNull;
            *((TestAnalyzer_lexatom_t*)(self.text + (End - Begin))) = (TestAnalyzer_lexatom_t)0;
        } else {
            self.text = LexemeNull;
        }

#       if 0
        /* Hint for debug: To check take_text change "#if 0" to "#if 1"       */
        {
            const TestAnalyzer_lexatom_t* it = 0x0;
            printf("after:     '");
            if( self.text != LexemeNull ) { 
                for(it = self.text; *it ; ++it) printf("%04X.", (int)*it);
                printf("%04X.", (int)*it);
            }
            printf("'\n");
        }
#       endif

        /* This token copied the text from the chunk into the string, 
         * so we do not claim ownership over it.                             */
        return false;
   
<<<<LINE_PRAGMA_WITH_CURRENT_LINE_N_AND_FILE_NAME>>>>

#   undef  LexemeNull
#   undef  self
    /* Default: no ownership.                                                */
    return false;
}
#endif

#ifdef QUEX_OPTION_TOKEN_REPETITION_SUPPORT
QUEX_INLINE size_t 
quex_Token_repetition_n_get(quex_Token* __this)
{
#   define self        (*__this)
#   define LexemeNull  (&QUEX_NAME(LexemeNull))
    (void)__this;

#   line 113 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

       return self.number;
   
<<<<LINE_PRAGMA_WITH_CURRENT_LINE_N_AND_FILE_NAME>>>>

#   undef  LexemeNull
#   undef  self
}

QUEX_INLINE void 
quex_Token_repetition_n_set(quex_Token* __this, size_t N)
{
#   define self        (*__this)
#   define LexemeNull  (&QUEX_NAME(LexemeNull))
    (void)__this;
    (void)N;

#   line 109 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

       self.number = N;
   
<<<<LINE_PRAGMA_WITH_CURRENT_LINE_N_AND_FILE_NAME>>>>

#   undef  LexemeNull
#   undef  self
}
#endif /* QUEX_OPTION_TOKEN_REPETITION_SUPPORT */

QUEX_INLINE const char*
quex_Token_map_id_to_name(const TestAnalyzer_token_id_t TokenID)
{
   static char  error_string[64];

   /* NOTE: This implementation works only for token id types that are 
    *       some type of integer or enum. In case an alien type is to
    *       used, this function needs to be redefined.                  */
   switch( TokenID ) {
   default: {
       __QUEX_STD_sprintf(error_string, "<UNKNOWN TOKEN-ID: %i>", (int)TokenID);
       return error_string;
   }

   case QUEX_TKN_TERMINATION:    return "<TERMINATION>";
   case QUEX_TKN_UNINITIALIZED:  return "<UNINITIALIZED>";
#  if defined(QUEX_OPTION_INDENTATION_TRIGGER)
   case QUEX_TKN_INDENT:         return "<INDENT>";
   case QUEX_TKN_DEDENT:         return "<DEDENT>";
   case QUEX_TKN_NODENT:         return "<NODENT>";
#  endif
   case QUEX_TKN_X:             return "X";


   }
}


#   line 117 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

        const char* 
        quex_Token_get_string(quex_Token* me, char*   buffer, size_t  BufferSize) 
        {
            const char*  token_id_str = quex_Token_map_id_to_name(me->id);
            const char*  BufferEnd    = buffer + BufferSize;
            char*        writerator   = 0;

            if( ! BufferSize ) return NULL;

            /* Token Type */
            writerator = buffer; 
            writerator += __QUEX_STD_strlcpy(writerator, token_id_str, 
                                             BufferEnd - writerator);

            /* Opening Quote */
            if( BufferEnd - writerator > 2 ) {
                *writerator++ = ' ';
                *writerator++ = '\'';
            }

            /* The String */
            writerator = QUEX_NAME(lexeme_to_pretty_char)(me->text, writerator, BufferEnd);

            /* Closing Quote */
            if( BufferEnd - writerator > 1 ) {
                *writerator++ = '\'';
            }
            *writerator = '\0';
            return buffer;
        }

#include "test_environment/converter-from-lexeme.i"
   
<<<<LINE_PRAGMA_WITH_CURRENT_LINE_N_AND_FILE_NAME>>>>


#endif /* __QUEX_INCLUDE_GUARD__TOKEN__GENERATED__QUEX___TOKEN_I */
QUEX_NAMESPACE_TOKEN_OPEN
TestAnalyzer_lexatom_t   QUEX_NAME(LexemeNull) = (TestAnalyzer_lexatom_t)0;
QUEX_NAMESPACE_TOKEN_CLOSE
