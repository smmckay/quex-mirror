/* -*- C++ -*-   vim: set syntax=cpp:
* (C) 2004-2009 Frank-Rene Schaefer
* ABSOLUTELY NO WARRANTY
*/
#ifndef __QUEX_INCLUDE_GUARD__TOKEN__GENERATED____TESTANALYZER_TOKEN_I
#define __QUEX_INCLUDE_GUARD__TOKEN__GENERATED____TESTANALYZER_TOKEN_I

#ifndef    __QUEX_OPTION_PLAIN_C
#   define __QUEX_OPTION_PLAIN_C
#endif

#include "test_environment/TestAnalyzer-token.h"
#include "test_environment/TestAnalyzer-token_ids.h"

QUEX_INLINE void
TestAnalyzer_Token_set(TestAnalyzer_Token*            __this,
const TestAnalyzer_token_id_t ID)
{ __this->id = ID; }

QUEX_INLINE void
TestAnalyzer_Token_construct(TestAnalyzer_Token* __this)
{
#   define self (*__this)
#   define LexemeNull  (&TestAnalyzer_LexemeNull)
(void)__this;

#   line 35 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

self.number = 0;
self.text   = LexemeNull;


#   line 32 "test_environment/TestAnalyzer-token.c"


#   undef  LexemeNull
#   undef  self
}

QUEX_INLINE void
TestAnalyzer_Token_copy_construct(TestAnalyzer_Token*       __this,
const TestAnalyzer_Token* __That)
{
TestAnalyzer_Token_construct(__this);
TestAnalyzer_Token_copy(__this, __That);
}

QUEX_INLINE void
TestAnalyzer_Token_destruct(TestAnalyzer_Token* __this)
{
#   define self (*__this)
#   define LexemeNull  (&TestAnalyzer_LexemeNull)
if( ! __this ) return;


#   line 40 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

if( self.text != LexemeNull ) {
QUEXED(MemoryManager_free)((void*)self.text,
E_MemoryObjectType_TEXT);
self.text = LexemeNull;
}


#   line 62 "test_environment/TestAnalyzer-token.c"


#   undef  LexemeNull
#   undef  self
}

QUEX_INLINE void
TestAnalyzer_Token_copy(TestAnalyzer_Token*       __this,
const TestAnalyzer_Token* __That)
{
#   define self  (*__this)
#   define Other (*__That)
#   define LexemeNull  (&TestAnalyzer_LexemeNull)
(void)__this;
(void)__That;

#   line 48 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

self.id  = Other.id;

if( self.text != LexemeNull ) {
QUEXED(MemoryManager_free)((void*)self.text, E_MemoryObjectType_TEXT);
}
if( Other.text != LexemeNull ) {
self.text = TestAnalyzer_lexeme_clone(self.text,
TestAnalyzer_lexeme_length(Other.text));
if( ! self.text ) self.text = LexemeNull;
}
self.number = Other.number;
#   ifdef     QUEX_OPTION_TOKEN_STAMPING_WITH_LINE_AND_COLUMN
__QUEX_IF_COUNT_LINES(self._line_n     = Other._line_n);
__QUEX_IF_COUNT_COLUMNS(self._column_n = Other._column_n);
#   endif


#   line 96 "test_environment/TestAnalyzer-token.c"


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
TestAnalyzer_Token_take_text(TestAnalyzer_Token*            __this,
const TestAnalyzer_lexatom_t* Begin,
const TestAnalyzer_lexatom_t* End)
/* RETURNS: true -- if the token claims ownership over the given memory.
*          false -- if no ownership is claimed.                             */
{
#   define self       (*__this)
#   ifdef  LexemeNull
#   error  "Error LexemeNull shall not be defined here."
#   endif
#   define LexemeNull  (&TestAnalyzer_LexemeNull)
(void)__this;
(void)Begin;
(void)End;

#   line 66 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"


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
self.text = TestAnalyzer_lexeme_clone(Begin, (size_t)(End - Begin));
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


#   line 177 "test_environment/TestAnalyzer-token.c"


#   undef  LexemeNull
#   undef  self
/* Default: no ownership.                                                */
return false;
}
#endif

#ifdef QUEX_OPTION_TOKEN_REPETITION_SUPPORT
QUEX_INLINE size_t
TestAnalyzer_Token_repetition_n_get(TestAnalyzer_Token* __this)
{
#   define self        (*__this)
#   define LexemeNull  (&TestAnalyzer_LexemeNull)
(void)__this;

#   line 123 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

return self.number;


#   line 198 "test_environment/TestAnalyzer-token.c"


#   undef  LexemeNull
#   undef  self
}

QUEX_INLINE void
TestAnalyzer_Token_repetition_n_set(TestAnalyzer_Token* __this, size_t N)
{
#   define self        (*__this)
#   define LexemeNull  (&TestAnalyzer_LexemeNull)
(void)__this;
(void)N;

#   line 119 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

self.number = N;


#   line 216 "test_environment/TestAnalyzer-token.c"


#   undef  LexemeNull
#   undef  self
}
#endif /* QUEX_OPTION_TOKEN_REPETITION_SUPPORT */

QUEX_INLINE const char*
TestAnalyzer_Token_map_id_to_name(const TestAnalyzer_token_id_t TokenID)
{
switch( TokenID ) {
default: {
return "<NUMERIC VALUE OF TOKEN-ID UNDEFINED>";
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


#   line 127 "/home/fschaef/prj/quex/trunk/quex/code_base/token/CDefault.qx"

const char*
TestAnalyzer_Token_get_string(TestAnalyzer_Token* me, char*   buffer, size_t  BufferSize)
{
const char*  token_id_str = TestAnalyzer_Token_map_id_to_name(me->id);
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
writerator = TestAnalyzer_lexeme_to_pretty_char(me->text, writerator, BufferEnd);

/* Closing Quote */
if( BufferEnd - writerator > 1 ) {
*writerator++ = '\'';
}
*writerator = '\0';
return buffer;
}

#include <test_environment/converter-from-lexeme.i>
#include <test_environment/lib/lexeme_base.i>


#   line 281 "test_environment/TestAnalyzer-token.c"



#endif /* __QUEX_INCLUDE_GUARD__TOKEN__GENERATED____TESTANALYZER_TOKEN_I */
