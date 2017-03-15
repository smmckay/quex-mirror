/* -*- C++ -*-   vim: set syntax=cpp:
 * CONTENT: 
 *
 * (1) Includes for required standard headers.
 * (2) Definitions of options and settings for the particular application.
 * (3) #include <quex/code_base/definitions> for default settings.
 * (4) Lexical Analyzer class TestAnalyzer and its memento class.
 * (5) Constructor and init core of TestAnalyzer.
 * (6) Memento pack and unpack functions.
 *
 * File content generated by Quex 0.67.2.
 *
 * (C) 2005-2012 Frank-Rene Schaefer
 * ABSOLUTELY NO WARRANTY                                                      */
#ifndef __QUEX_INCLUDE_GUARD__ANALYZER__GENERATED__QUEX___TESTANALYZER
#define __QUEX_INCLUDE_GUARD__ANALYZER__GENERATED__QUEX___TESTANALYZER

#ifdef      __QUEX_INCLUDE_INDICATOR__ANALYZER__MAIN
    /* In case that multiple lexical analyzers are used the same header
     * files are compiled with a different setting of the macros. The
     * undef of the include guards happens in the following file.              */
#   ifdef   __QUEX_SIGNAL_DEFINED_LEXER_IN_NAMESPACE_QUEX_
#      error "More than one lexical analyzer have been generated in the same name space. Read documentation on command line option '-o'."
#   endif
#   ifndef  QUEX_OPTION_MULTI
#      error "Multiple lexical analyzers detected. QUEX_OPTION_MULTI must be defined and 'quex/code_base/multi.i' must be included in one single file!"
#   endif
#   include <quex/code_base/include-guard-undef>
#   include <quex/code_base/analyzer/member/token-sending-undef.i>
#   undef   __QUEX_INCLUDE_GUARD__ANALYZER__CONFIGURATION__QUEX___TESTANALYZER
#else
#   define  __QUEX_INCLUDE_INDICATOR__ANALYZER__MAIN
#endif
#define     __QUEX_SIGNAL_DEFINED_LEXER_IN_NAMESPACE_QUEX_

#include "TestAnalyzer-configuration.h"

#include <quex/code_base/definitions>

struct  QUEX_NAME(Engine_tag);
struct  QUEX_NAME(Memento_tag);
QUEX_TYPE0_ANALYZER;    /* quex_TestAnalyzer */
typedef __QUEX_TYPE_ANALYZER_RETURN_VALUE  (*QUEX_NAME(AnalyzerFunctionP))(QUEX_TYPE0_ANALYZER*);

/* Token Class Declaration must preceed the user's header, so that the user
 * can refer to it at ease.                                                    */
QUEX_TYPE0_TOKEN;

/* START: User defined header content _________________________________________
 *        Must come before token class definition, since the token class 
 *        might rely on contents of the header.                                */

extern bool UserConstructor_UnitTest_return_value;
extern bool UserReset_UnitTest_return_value;
extern bool UserMementoPack_UnitTest_return_value;


/* END: _______________________________________________________________________*/
#include <quex/code_base/converter_helper/from-unicode-buffer>

#include <quex/code_base/analyzer/headers>

#include "TestAnalyzer-token_ids.h"
#include "TestAnalyzer-token.h"


QUEX_NAMESPACE_MAIN_OPEN 

enum {
    QUEX_NAME(ModeID_M) = 0
};
    
        extern QUEX_NAME(Mode)  QUEX_NAME(M);


extern     __QUEX_TYPE_ANALYZER_RETURN_VALUE QUEX_NAME(M_analyzer_function)(QUEX_TYPE_ANALYZER*);
#ifdef QUEX_OPTION_RUNTIME_MODE_TRANSITION_CHECK
extern     bool QUEX_NAME(M_has_base)(const QUEX_NAME(Mode)*);
extern     bool QUEX_NAME(M_has_entry_from)(const QUEX_NAME(Mode)*);
extern     bool QUEX_NAME(M_has_exit_to)(const QUEX_NAME(Mode)*);
#endif



typedef struct QUEX_SETTING_USER_CLASS_DECLARATION_EPILOG QUEX_NAME(Memento_tag) {
#   include <quex/code_base/analyzer/EngineMemento_body>

    /* Con- and Destruction are **not** necessary in C. No con- or de-
     * structors of members need to be triggered.                              */

/* START: User's memento extentions ___________________________________________*/

/* END: _______________________________________________________________________*/
} QUEX_NAME(Memento);

QUEX_NAMESPACE_MAIN_CLOSE 

QUEX_NAMESPACE_MAIN_OPEN 

extern QUEX_NAME(Mode)*  (QUEX_NAME(mode_db)[__QUEX_SETTING_MAX_MODE_CLASS_N]);  

typedef struct QUEX_SETTING_USER_CLASS_DECLARATION_EPILOG quex_TestAnalyzer_tag {

#include <quex/code_base/analyzer/Engine_body>
#define self  (*(QUEX_TYPE_DERIVED_ANALYZER*)this)
/* START: User's class body extensions _____________________________________________*/

/* END: ____________________________________________________________________________*/
#undef  self

} quex_TestAnalyzer;

QUEX_NAMESPACE_MAIN_CLOSE

#endif /* __QUEX_INCLUDE_GUARD__ANALYZER__GENERATED__QUEX___TESTANALYZER */
#ifndef QUEX_OPTION_UNIT_TEST_NO_IMPLEMENTATION_IN_HEADER

QUEX_NAMESPACE_MAIN_OPEN

bool
QUEX_NAME(user_constructor)(QUEX_TYPE_ANALYZER* me)
{
    (void)me;

    __quex_assert(QUEX_NAME(mode_db)[QUEX_NAME(ModeID_M)] == &QUEX_NAME(M));


#define self  (*(QUEX_TYPE_DERIVED_ANALYZER*)me)
/* START: User's constructor extensions _______________________________________*/
return UserConstructor_UnitTest_return_value;
/* END: _______________________________________________________________________*/
#undef self
    return true;
}

void
QUEX_NAME(user_destructor)(QUEX_TYPE_ANALYZER* me)
{
    (void)me;

#define self  (*(QUEX_TYPE_DERIVED_ANALYZER*)me)
/* START: User's constructor extensions _______________________________________*/

/* END: _______________________________________________________________________*/
#undef self
}

bool
QUEX_NAME(user_reset)(QUEX_TYPE_ANALYZER* me)
{
    (void)me;

#define self  (*(QUEX_TYPE_DERIVED_ANALYZER*)me)
/* START: User's 'reset' ______________________________________________________*/
return UserReset_UnitTest_return_value;
/* END: _______________________________________________________________________*/
#undef self
    return true;
}

#ifdef QUEX_OPTION_INCLUDE_STACK

bool
QUEX_NAME(user_memento_pack)(QUEX_TYPE_ANALYZER* me, 
                             const char*         InputName, 
                             QUEX_NAME(Memento)* memento) 
{
    (void)me; (void)memento; (void)InputName;

#define self  (*(QUEX_TYPE_DERIVED_ANALYZER*)me)
/* START: User's memento 'pack' _______________________________________________*/
return UserMementoPack_UnitTest_return_value;
/* END: _______________________________________________________________________*/
#undef self
    return true;
}

void
QUEX_NAME(user_memento_unpack)(QUEX_TYPE_ANALYZER*  me, 
                               QUEX_NAME(Memento)*  memento)
{
    (void)me; (void)memento;

#define self  (*(QUEX_TYPE_DERIVED_ANALYZER*)me)
/* START: User's memento 'unpack' _____________________________________________*/

/* END: _______________________________________________________________________*/
#undef self
}
#endif /* QUEX_OPTION_INCLUDE_STACK */

QUEX_NAMESPACE_MAIN_CLOSE


#include <quex/code_base/converter_helper/from-unicode-buffer.i>

#include <quex/code_base/analyzer/headers.i>
#include <quex/code_base/analyzer/C-adaptions.h>
bool UserConstructor_UnitTest_return_value = true;
bool UserReset_UnitTest_return_value       = true;
bool UserMementoPack_UnitTest_return_value = true;
#endif /* QUEX_OPTION_UNIT_TEST_NO_IMPLEMENTATION_IN_HEADER */
#ifndef QUEX_OPTION_UNIT_TEST_NO_IMPLEMENTATION_IN_HEADER
/* -*- C++ -*-   vim: set syntax=cpp: 
 * (C) 2004-2009 Frank-Rene Schaefer
 * ABSOLUTELY NO WARRANTY
 */
#ifndef __QUEX_INCLUDE_GUARD__TOKEN__GENERATED__QUEX___TOKEN_I
#define __QUEX_INCLUDE_GUARD__TOKEN__GENERATED__QUEX___TOKEN_I

#ifndef    __QUEX_OPTION_PLAIN_C
#   define __QUEX_OPTION_PLAIN_C
#endif

#include "TestAnalyzer-token.h"
#include <quex/code_base/definitions>

QUEX_NAMESPACE_LEXEME_NULL_OPEN
extern QUEX_TYPE_LEXATOM   QUEX_LEXEME_NULL_IN_ITS_NAMESPACE;
QUEX_NAMESPACE_LEXEME_NULL_CLOSE


QUEX_INLINE void 
quex_Token_set(quex_Token*            __this, 
                 const QUEX_TYPE_TOKEN_ID ID) 
{ __this->_id = ID; }

QUEX_INLINE const char*    
quex_Token_map_id_to_name(QUEX_TYPE_TOKEN_ID);

QUEX_INLINE void 
quex_Token_construct(quex_Token* __this)
{
#   define self (*__this)
#   define LexemeNull  &QUEX_LEXEME_NULL
    (void)__this;

#   line 33 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

       self.number = 0;
       self.text   = LexemeNull;
   

#   line 245 "TestAnalyzer.h"

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
#   define LexemeNull  &QUEX_LEXEME_NULL
    if( ! __this ) return;


#   line 38 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

       if( self.text != LexemeNull ) {
           QUEXED(MemoryManager_free)((void*)self.text,
                                          E_MemoryObjectType_TEXT);
           self.text = LexemeNull;
       }
   

#   line 276 "TestAnalyzer.h"

#   undef  LexemeNull
#   undef  self
}

QUEX_INLINE void
quex_Token_copy(quex_Token*       __this, 
                  const quex_Token* __That)
{
#   define self  (*__this)
#   define Other (*__That)
#   define LexemeNull  &QUEX_LEXEME_NULL
    (void)__this;
    (void)__That;

#   line 46 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

        self._id  = Other._id;

        if( self.text != LexemeNull ) {
            QUEXED(MemoryManager_free)((void*)self.text,
                                       E_MemoryObjectType_TEXT);
        }
        if( Other.text != LexemeNull ) {
            self.text = \
               (QUEX_TYPE_LEXATOM*)
               QUEXED(MemoryManager_allocate)(
                      sizeof(QUEX_TYPE_LEXATOM) * (QUEX_NAME(strlen)(Other.text) + 1),
                      E_MemoryObjectType_TEXT);
            __QUEX_STD_memcpy((void*)self.text, (void*)Other.text, 
                                sizeof(QUEX_TYPE_LEXATOM) 
                              * (QUEX_NAME(strlen)(Other.text) + 1));
        }
        self.number = Other.number;
    #   ifdef     QUEX_OPTION_TOKEN_STAMPING_WITH_LINE_AND_COLUMN
        __QUEX_IF_COUNT_LINES(self._line_n     = Other._line_n);
        __QUEX_IF_COUNT_COLUMNS(self._column_n = Other._column_n);
    #   endif
   

#   line 317 "TestAnalyzer.h"

#   undef  LexemeNull
#   undef  Other
#   undef  self
    /* If the user even misses to copy the token id, then there's
     * something seriously wrong.                                 */
    __quex_assert(__this->_id == __That->_id);
#   ifdef QUEX_OPTION_TOKEN_STAMPING_WITH_LINE_AND_COLUMN
    __QUEX_IF_COUNT_LINES(__quex_assert(__this->_line_n == __That->_line_n));
    __QUEX_IF_COUNT_COLUMNS(__quex_assert(__this->_column_n == __That->_column_n));
#   endif
}


QUEX_INLINE bool 
quex_Token_take_text(quex_Token*              __this, 
                       QUEX_TYPE_ANALYZER*        __analyzer, 
                       const QUEX_TYPE_LEXATOM* Begin, 
                       const QUEX_TYPE_LEXATOM* End)
/* RETURNS: true -- if the token claims ownership over the given memory.
 *          false -- if no ownership is claimed.                             */
{
#   define self       (*__this)
#   define analyzer   (*__analyzer)
#   ifdef  LexemeNull
#   error  "Error LexemeNull shall not be defined here."
#   endif
#   define LexemeNull  &QUEX_LEXEME_NULL
    (void)__this;
    (void)__analyzer;
    (void)Begin;
    (void)End;

#   line 70 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"


#       if 0
        /* Hint for debug: To check take_text change "#if 0" to "#if 1" */
        {
            const QUEX_TYPE_LEXATOM* it = (void*)0x0;
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
            QUEXED(MemoryManager_free)((void*)self.text,
                                          E_MemoryObjectType_TEXT);
        }
        if( Begin != LexemeNull ) {
            __quex_assert(End >= Begin);
            self.text = \
                 (QUEX_TYPE_LEXATOM*)
                 QUEXED(MemoryManager_allocate)(
                              sizeof(QUEX_TYPE_LEXATOM) * (size_t)(End - Begin + 1), 
                              E_MemoryObjectType_TEXT);
            __QUEX_STD_memcpy((void*)self.text, (void*)Begin, 
                              sizeof(QUEX_TYPE_LEXATOM) * (size_t)(End - Begin));
            /* The string is not necessarily zero terminated, so terminate it here. */
            *((QUEX_TYPE_LEXATOM*)(self.text + (End - Begin))) = (QUEX_TYPE_LEXATOM)0;
        } else {
            self.text = LexemeNull;
        }

#       if 0
        /* Hint for debug: To check take_text change "#if 0" to "#if 1"       */
        {
            const QUEX_TYPE_LEXATOM* it = 0x0;
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
   

#   line 408 "TestAnalyzer.h"

#   undef  LexemeNull
#   undef  analyzer
#   undef  self
    /* Default: no ownership.                                                */
    return false;
}

#ifdef QUEX_OPTION_TOKEN_REPETITION_SUPPORT
QUEX_INLINE size_t 
quex_Token_repetition_n_get(quex_Token* __this)
{
#   define self        (*__this)
#   define LexemeNull  &QUEX_LEXEME_NULL
    (void)__this;
    
#   line 135 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

       return self.number;
   

#   line 430 "TestAnalyzer.h"

#   undef  LexemeNull
#   undef  self
}

QUEX_INLINE void 
quex_Token_repetition_n_set(quex_Token* __this, size_t N)
{
#   define self        (*__this)
#   define LexemeNull  &QUEX_LEXEME_NULL
    (void)__this;
    (void)N;
    
#   line 131 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

       self.number = N;
   

#   line 449 "TestAnalyzer.h"

#   undef  LexemeNull
#   undef  self
}
#endif /* QUEX_OPTION_TOKEN_REPETITION_SUPPORT */


#   line 139 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

        const char* 
        quex_Token_get_string(quex_Token* me, char*   buffer, size_t  BufferSize) 
        {
            const char*  token_type_str = quex_Token_map_id_to_name(me->_id);
            const char*  BufferEnd  = buffer + BufferSize;
            const char*  iterator   = 0;
            char*        writerator = 0;

            /* Token Type */
            iterator = token_type_str;
            writerator = buffer; 
            while( (*iterator) && writerator != BufferEnd ) {
                *writerator++ = *iterator++;
            }

            /* Opening Quote */
            if( BufferEnd - writerator > 2 ) {
                *writerator++ = ' ';
                *writerator++ = '\'';
            }

            /* The String */
            quex_Token_pretty_char_text(me, writerator, (size_t)(BufferEnd - writerator));

            while( *writerator ) {
                ++writerator;
            }

            /* Closing Quote */
            if( BufferEnd - writerator > 1 ) {
                *writerator++ = '\'';
            }
            *writerator = '\0';
            return buffer;
        }

        const char* 
        quex_Token_pretty_char_text(quex_Token* me, char*   buffer, size_t  BufferSize) 
        /* Provides a somehow pretty-print of the text in the token. Note, that the buffer
         * in case of UTF8 should be 4bytes longer than the longest expected string.       */
        {
            const QUEX_TYPE_LEXATOM*  source    = me->text;
            char*                       drain     = buffer;
            const char*                 DrainEnd  = buffer + BufferSize;

            const QUEX_TYPE_LEXATOM*  SourceEnd = me->text + (size_t)(QUEX_NAME(strlen)(source)) + 1;
            QUEX_CONVERTER_STRING(unicode,char)(&source, SourceEnd, &drain, DrainEnd);
            return buffer;
        }

#       if ! defined(__QUEX_OPTION_WCHAR_T_DISABLED)
        const wchar_t* 
        quex_Token_pretty_wchar_text(quex_Token* me, wchar_t*  buffer, size_t    BufferSize) 
        {
            wchar_t*                    drain     = buffer;
            const wchar_t*              DrainEnd  = buffer + (ptrdiff_t)BufferSize;
            const QUEX_TYPE_LEXATOM*  source    = me->text;
            const QUEX_TYPE_LEXATOM*  SourceEnd = me->text + (ptrdiff_t)(QUEX_NAME(strlen)(source)) + 1;

            QUEX_CONVERTER_STRING(unicode,wchar)(&source, SourceEnd, &drain, DrainEnd);
            return buffer;
        }
#       endif

#include <quex/code_base/converter_helper/from-unicode-buffer.i>

   

#   line 527 "TestAnalyzer.h"




#endif /* __QUEX_INCLUDE_GUARD__TOKEN__GENERATED__QUEX___TOKEN_I */


QUEX_NAMESPACE_TOKEN_OPEN

const char*
QUEX_NAME_TOKEN(map_id_to_name)(const QUEX_TYPE_TOKEN_ID TokenID)
{
   static char  error_string[64];
   static const char  uninitialized_string[] = "<UNINITIALIZED>";
   static const char  termination_string[]   = "<TERMINATION>";
#  if defined(QUEX_OPTION_INDENTATION_TRIGGER)
   static const char  indent_string[]        = "<INDENT>";
   static const char  dedent_string[]        = "<DEDENT>";
   static const char  nodent_string[]        = "<NODENT>";
#  endif
   static const char  token_id_str_X[]             = "X";
       

   /* NOTE: This implementation works only for token id types that are 
    *       some type of integer or enum. In case an alien type is to
    *       used, this function needs to be redefined.                  */
   switch( TokenID ) {
   default: {
       __QUEX_STD_sprintf(error_string, "<UNKNOWN TOKEN-ID: %i>", (int)TokenID);
       return error_string;
   }
   case QUEX_TKN_TERMINATION:    return termination_string;
   case QUEX_TKN_UNINITIALIZED:  return uninitialized_string;
#  if defined(QUEX_OPTION_INDENTATION_TRIGGER)
   case QUEX_TKN_INDENT:         return indent_string;
   case QUEX_TKN_DEDENT:         return dedent_string;
   case QUEX_TKN_NODENT:         return nodent_string;
#  endif
   case QUEX_TKN_X:             return token_id_str_X;

   }
}

QUEX_NAMESPACE_TOKEN_CLOSE
#endif /* QUEX_OPTION_UNIT_TEST_NO_IMPLEMENTATION_IN_HEADER */
