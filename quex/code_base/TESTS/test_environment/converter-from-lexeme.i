/* -*- C++ -*- vim: set syntax=cpp:
* PURPOSE:
*
* Provide the implementation of character and string converter functions
* FROM the buffer's lexeme_to to utf8, utf16, utf32, char, and wchar_t.
*
* STEPS:
*
* (1) Implement the character converters from buffer's $$SOURCE_ENCODING$$ to
*     utf8, utf16, utf32. Those come out of quex's code generator.
*
* (1b) Derive the converts from $$SOURCE_ENCODING$$ to char and wchar_t from
*      those converters. For this use:
*
*          "../generator/character-converter-char-wchar_t.gi"
*
* (2) Generate the implementation of the string converters in terms
*     of those character converters.
*
*     Use: "../generator/implementation-string-converters.gi"
*
*          which uses
*
*              "../generator/string-converter.gi"
*
*          to implement each string converter from the given
*          character converters.
*
* These functions ARE DEPENDENT on TestAnalyzer_lexatom_t.
* => Thus, they are placed in the analyzer's namespace.
*
* 2010 (C) Frank-Rene Schaefer;
* ABSOLUTELY NO WARRANTY                                                    */
#ifndef __QUEX_INCLUDE_GUARD__TESTANALYZER_UNICODE_UINT8_T_I
#define __QUEX_INCLUDE_GUARD__TESTANALYZER_UNICODE_UINT8_T_I

#include "test_environment/converter-from-lexeme"

#if ! defined(QUEX_OPTION_DISABLE_STD_STRING_USAGE)
#include "test_environment/lib/MemoryManager"
#endif

QUEX_NAMESPACE_MAIN_OPEN

QUEX_INLINE void
QUEX_NAME(lexeme_to_utf32_character)(const TestAnalyzer_lexatom_t** input_pp, uint32_t** output_pp)
{
uint32_t          unicode;
int32_t           offset;
TestAnalyzer_lexatom_t input = *(*input_pp)++;

offset = (int32_t)(0);
unicode = (uint32_t)((int32_t)input + offset);
*(*output_pp)++ = unicode;
return;
}

QUEX_INLINE void
QUEX_NAME(lexeme_to_utf16_character)(const TestAnalyzer_lexatom_t** input_pp, uint16_t** output_pp)
{
uint32_t          unicode;
int32_t           offset;
TestAnalyzer_lexatom_t input = *(*input_pp)++;

offset = (int32_t)(0);
unicode = (uint32_t)((int32_t)input + offset);
*(*output_pp)++ = (uint16_t)(unicode);
return;
}

QUEX_INLINE void
QUEX_NAME(lexeme_to_utf8_character)(const TestAnalyzer_lexatom_t**  input_pp, uint8_t** output_pp)
{
uint32_t          unicode;
int32_t           offset;
TestAnalyzer_lexatom_t input = *(*input_pp)++;

if( input >= 0x80 )  { offset = (int32_t)(0); goto code_unit_n_2; }

else                 { offset = (int32_t)(0); goto code_unit_n_1; }

code_unit_n_1:
unicode = (uint32_t)((int32_t)input + offset);
*(*output_pp)++ = (uint8_t)(unicode);
return;
code_unit_n_2:
unicode = (uint32_t)((int32_t)input + offset);
*(*output_pp)++ = (uint8_t)(0xC0 | (unicode >> 6));
*(*output_pp)++ = (uint8_t)(0x80 | (unicode & (uint32_t)0x3F));
return;
}




/* Converters for 'char', 'pretty_char', and 'wchar_t' _________________________
*                                                                            */
QUEX_INLINE void
QUEX_NAME(lexeme_to_char_character)(const TestAnalyzer_lexatom_t** source_pp,
char**                    drain_pp)
{
switch( sizeof(char) )
{
case 1:  QUEX_NAME(lexeme_to_utf8_character)(source_pp, (uint8_t**)drain_pp); break;
case 2:  QUEX_NAME(lexeme_to_utf16_character)(source_pp, (uint16_t**)drain_pp); break;
case 4:  QUEX_NAME(lexeme_to_utf32_character)(source_pp, (uint32_t**)drain_pp); break;
default: __quex_assert(false); /* Cannot be handled */
}
}

#if ! defined(__QUEX_OPTION_WCHAR_T_DISABLED)
QUEX_INLINE void
QUEX_NAME(lexeme_to_wchar_t_character)(const TestAnalyzer_lexatom_t** source_pp,
wchar_t**                 drain_pp)
{
switch( sizeof(wchar_t) )
{
case 1:  QUEX_NAME(lexeme_to_utf8_character)(source_pp, (uint8_t**)drain_pp); break;
case 2:  QUEX_NAME(lexeme_to_utf16_character)(source_pp, (uint16_t**)drain_pp); break;
case 4:  QUEX_NAME(lexeme_to_utf32_character)(source_pp, (uint32_t**)drain_pp); break;
default: __quex_assert(false); /* Cannot be handled */
}
}
#endif

QUEX_INLINE void
QUEX_NAME(lexeme_to_pretty_char_character)(const TestAnalyzer_lexatom_t** source_pp,
char**                    drain_pp)
{
char* write_p = *drain_pp;

QUEX_NAME(lexeme_to_char_character)(source_pp, drain_pp);

switch( *write_p ) {
case (int)'\n': *write_p++ = (char)'\\'; *write_p = (char)'n'; break;
case (int)'\t': *write_p++ = (char)'\\'; *write_p = (char)'t'; break;
case (int)'\r': *write_p++ = (char)'\\'; *write_p = (char)'r'; break;
case (int)'\a': *write_p++ = (char)'\\'; *write_p = (char)'a'; break;
case (int)'\b': *write_p++ = (char)'\\'; *write_p = (char)'b'; break;
case (int)'\f': *write_p++ = (char)'\\'; *write_p = (char)'f'; break;
case (int)'\v': *write_p++ = (char)'\\'; *write_p = (char)'v'; break;
default: /* 'drain_pp' has been adapted by converter!       */ return;
}
/* 'drain_pp' is set to the post-adapted position.          */
*drain_pp = &write_p[1];
}


/* Converters for strings ______________________________________________________
*                                                                            */
QUEX_INLINE void
QUEX_NAME(lexeme_nnzt_to_utf8)(const TestAnalyzer_lexatom_t**      source_pp,
const TestAnalyzer_lexatom_t*        SourceEnd,
uint8_t**      drain_pp,
const uint8_t* DrainEnd)
/* Convert a lexeme that is *not necessarily zero terminated* (nnzt), adapt the
* pointer to begin of source and begin of drain for quick iteration over
* larger segments.                                                           */
{
const TestAnalyzer_lexatom_t*  source_iterator;
uint8_t* drain_it;
const ptrdiff_t           TargetMaxCodeUnitN = 4; /* UF32=1, UTF16=2, utf8=... */

__quex_assert(source_pp != 0x0);
__quex_assert(*source_pp != 0x0);
__quex_assert(drain_pp != 0x0);
__quex_assert(*drain_pp != 0x0);

drain_it  = *drain_pp;
for(source_iterator=*source_pp; source_iterator != SourceEnd; ) {
if     ( source_iterator == SourceEnd ) break;
else if( DrainEnd - drain_it < TargetMaxCodeUnitN ) break;
QUEX_NAME(lexeme_to_utf8_character)(&source_iterator, &drain_it);
__quex_assert(source_iterator >  *source_pp);
__quex_assert(source_iterator <= SourceEnd);
}

*drain_pp  = drain_it;
*source_pp = source_iterator;
}

QUEX_INLINE uint8_t*
QUEX_NAME(lexeme_to_utf8)(const TestAnalyzer_lexatom_t*         SourceBegin,
uint8_t*        drain_p,
const uint8_t*  DrainEnd)
/* Convert a zero-terminated lexeme. Adapt the drain pointer for quicker
* iteration over write buffer.
*
* RETURNS: 0, in case that conversion failed due to insufficient drain
*             space.
*          Pointer to END of converted string.                               */
{
const TestAnalyzer_lexatom_t*  source_iterator;
uint8_t* drain_it;
uint8_t* terminating_zero_p;
const ptrdiff_t           TargetMaxCodeUnitN = 4; /* UF32=1, UTF16=2, utf8=... */

__quex_assert(SourceBegin != 0x0);
__quex_assert(drain_p != 0x0);

drain_it = drain_p;
for(source_iterator=SourceBegin; *source_iterator != (TestAnalyzer_lexatom_t)0; ) {
if( DrainEnd - drain_it < TargetMaxCodeUnitN ) {
return (uint8_t*)0;
}
QUEX_NAME(lexeme_to_utf8_character)(&source_iterator,
&drain_it);
__quex_assert(source_iterator > SourceBegin);
__quex_assert(drain_it <= DrainEnd);
}

terminating_zero_p = drain_it;
if( DrainEnd - drain_it < TargetMaxCodeUnitN ) {
return (uint8_t*)0;
}
QUEX_NAME(lexeme_to_utf8_character)(&source_iterator,
&drain_it);
__quex_assert(source_iterator > SourceBegin);
__quex_assert(drain_it <= DrainEnd);

return terminating_zero_p;
}

#if    ! defined(__QUEX_OPTION_PLAIN_C) \
&& ! defined(QUEX_OPTION_DISABLE_STD_STRING_USAGE)
QUEX_INLINE std::basic_string<uint8_t>
QUEX_NAME(lexeme_to_utf8)(const std::basic_string<TestAnalyzer_lexatom_t>& Source)
{
/* Save iteration over string with existing character converters.
* => copy string to a temporary array.                                   */
uint8_t    tmp_drain[4];
uint8_t*   drain_it;
TestAnalyzer_lexatom_t*          source = (TestAnalyzer_lexatom_t*)
QUEXED(MemoryManager_allocate)(
sizeof(TestAnalyzer_lexatom_t) * (Source.length() + 1),
E_MemoryObjectType_TEXT);
const size_t                SourceLength = Source.length();
const TestAnalyzer_lexatom_t*    source_it;

std::basic_string<uint8_t>  result;


if( SourceLength != Source.copy(&source[0], SourceLength) ) {
QUEXED(MemoryManager_free)(source, E_MemoryObjectType_TEXT);
return result;
}
/* .copy() does not append a terminating zero ...
* and it is not to be copied.                                            */
for(source_it = &source[0]; source_it < &source[SourceLength]; ) {
drain_it = tmp_drain;
QUEX_NAME(lexeme_to_utf8_character)(&source_it, &drain_it);
__quex_assert(source_it >  &source[0]);
__quex_assert(source_it <= &source[SourceLength]);
result.append((uint8_t*)tmp_drain, (size_t)(drain_it - tmp_drain));
}

QUEXED(MemoryManager_free)(source, E_MemoryObjectType_TEXT);
return result;
}
#endif


QUEX_INLINE void
QUEX_NAME(lexeme_nnzt_to_utf16)(const TestAnalyzer_lexatom_t**      source_pp,
const TestAnalyzer_lexatom_t*        SourceEnd,
uint16_t**      drain_pp,
const uint16_t* DrainEnd)
/* Convert a lexeme that is *not necessarily zero terminated* (nnzt), adapt the
* pointer to begin of source and begin of drain for quick iteration over
* larger segments.                                                           */
{
const TestAnalyzer_lexatom_t*  source_iterator;
uint16_t* drain_it;
const ptrdiff_t           TargetMaxCodeUnitN = 2; /* UF32=1, UTF16=2, utf8=... */

__quex_assert(source_pp != 0x0);
__quex_assert(*source_pp != 0x0);
__quex_assert(drain_pp != 0x0);
__quex_assert(*drain_pp != 0x0);

drain_it  = *drain_pp;
for(source_iterator=*source_pp; source_iterator != SourceEnd; ) {
if     ( source_iterator == SourceEnd ) break;
else if( DrainEnd - drain_it < TargetMaxCodeUnitN ) break;
QUEX_NAME(lexeme_to_utf16_character)(&source_iterator, &drain_it);
__quex_assert(source_iterator >  *source_pp);
__quex_assert(source_iterator <= SourceEnd);
}

*drain_pp  = drain_it;
*source_pp = source_iterator;
}

QUEX_INLINE uint16_t*
QUEX_NAME(lexeme_to_utf16)(const TestAnalyzer_lexatom_t*         SourceBegin,
uint16_t*        drain_p,
const uint16_t*  DrainEnd)
/* Convert a zero-terminated lexeme. Adapt the drain pointer for quicker
* iteration over write buffer.
*
* RETURNS: 0, in case that conversion failed due to insufficient drain
*             space.
*          Pointer to END of converted string.                               */
{
const TestAnalyzer_lexatom_t*  source_iterator;
uint16_t* drain_it;
uint16_t* terminating_zero_p;
const ptrdiff_t           TargetMaxCodeUnitN = 2; /* UF32=1, UTF16=2, utf8=... */

__quex_assert(SourceBegin != 0x0);
__quex_assert(drain_p != 0x0);

drain_it = drain_p;
for(source_iterator=SourceBegin; *source_iterator != (TestAnalyzer_lexatom_t)0; ) {
if( DrainEnd - drain_it < TargetMaxCodeUnitN ) {
return (uint16_t*)0;
}
QUEX_NAME(lexeme_to_utf16_character)(&source_iterator,
&drain_it);
__quex_assert(source_iterator > SourceBegin);
__quex_assert(drain_it <= DrainEnd);
}

terminating_zero_p = drain_it;
if( DrainEnd - drain_it < TargetMaxCodeUnitN ) {
return (uint16_t*)0;
}
QUEX_NAME(lexeme_to_utf16_character)(&source_iterator,
&drain_it);
__quex_assert(source_iterator > SourceBegin);
__quex_assert(drain_it <= DrainEnd);

return terminating_zero_p;
}

#if    ! defined(__QUEX_OPTION_PLAIN_C) \
&& ! defined(QUEX_OPTION_DISABLE_STD_STRING_USAGE)
QUEX_INLINE std::basic_string<uint16_t>
QUEX_NAME(lexeme_to_utf16)(const std::basic_string<TestAnalyzer_lexatom_t>& Source)
{
/* Save iteration over string with existing character converters.
* => copy string to a temporary array.                                   */
uint16_t    tmp_drain[2];
uint16_t*   drain_it;
TestAnalyzer_lexatom_t*          source = (TestAnalyzer_lexatom_t*)
QUEXED(MemoryManager_allocate)(
sizeof(TestAnalyzer_lexatom_t) * (Source.length() + 1),
E_MemoryObjectType_TEXT);
const size_t                SourceLength = Source.length();
const TestAnalyzer_lexatom_t*    source_it;

std::basic_string<uint16_t>  result;


if( SourceLength != Source.copy(&source[0], SourceLength) ) {
QUEXED(MemoryManager_free)(source, E_MemoryObjectType_TEXT);
return result;
}
/* .copy() does not append a terminating zero ...
* and it is not to be copied.                                            */
for(source_it = &source[0]; source_it < &source[SourceLength]; ) {
drain_it = tmp_drain;
QUEX_NAME(lexeme_to_utf16_character)(&source_it, &drain_it);
__quex_assert(source_it >  &source[0]);
__quex_assert(source_it <= &source[SourceLength]);
result.append((uint16_t*)tmp_drain, (size_t)(drain_it - tmp_drain));
}

QUEXED(MemoryManager_free)(source, E_MemoryObjectType_TEXT);
return result;
}
#endif


QUEX_INLINE void
QUEX_NAME(lexeme_nnzt_to_utf32)(const TestAnalyzer_lexatom_t**      source_pp,
const TestAnalyzer_lexatom_t*        SourceEnd,
uint32_t**      drain_pp,
const uint32_t* DrainEnd)
/* Convert a lexeme that is *not necessarily zero terminated* (nnzt), adapt the
* pointer to begin of source and begin of drain for quick iteration over
* larger segments.                                                           */
{
const TestAnalyzer_lexatom_t*  source_iterator;
uint32_t* drain_it;
const ptrdiff_t           TargetMaxCodeUnitN = 1; /* UF32=1, UTF16=2, utf8=... */

__quex_assert(source_pp != 0x0);
__quex_assert(*source_pp != 0x0);
__quex_assert(drain_pp != 0x0);
__quex_assert(*drain_pp != 0x0);

drain_it  = *drain_pp;
for(source_iterator=*source_pp; source_iterator != SourceEnd; ) {
if     ( source_iterator == SourceEnd ) break;
else if( DrainEnd - drain_it < TargetMaxCodeUnitN ) break;
QUEX_NAME(lexeme_to_utf32_character)(&source_iterator, &drain_it);
__quex_assert(source_iterator >  *source_pp);
__quex_assert(source_iterator <= SourceEnd);
}

*drain_pp  = drain_it;
*source_pp = source_iterator;
}

QUEX_INLINE uint32_t*
QUEX_NAME(lexeme_to_utf32)(const TestAnalyzer_lexatom_t*         SourceBegin,
uint32_t*        drain_p,
const uint32_t*  DrainEnd)
/* Convert a zero-terminated lexeme. Adapt the drain pointer for quicker
* iteration over write buffer.
*
* RETURNS: 0, in case that conversion failed due to insufficient drain
*             space.
*          Pointer to END of converted string.                               */
{
const TestAnalyzer_lexatom_t*  source_iterator;
uint32_t* drain_it;
uint32_t* terminating_zero_p;
const ptrdiff_t           TargetMaxCodeUnitN = 1; /* UF32=1, UTF16=2, utf8=... */

__quex_assert(SourceBegin != 0x0);
__quex_assert(drain_p != 0x0);

drain_it = drain_p;
for(source_iterator=SourceBegin; *source_iterator != (TestAnalyzer_lexatom_t)0; ) {
if( DrainEnd - drain_it < TargetMaxCodeUnitN ) {
return (uint32_t*)0;
}
QUEX_NAME(lexeme_to_utf32_character)(&source_iterator,
&drain_it);
__quex_assert(source_iterator > SourceBegin);
__quex_assert(drain_it <= DrainEnd);
}

terminating_zero_p = drain_it;
if( DrainEnd - drain_it < TargetMaxCodeUnitN ) {
return (uint32_t*)0;
}
QUEX_NAME(lexeme_to_utf32_character)(&source_iterator,
&drain_it);
__quex_assert(source_iterator > SourceBegin);
__quex_assert(drain_it <= DrainEnd);

return terminating_zero_p;
}

#if    ! defined(__QUEX_OPTION_PLAIN_C) \
&& ! defined(QUEX_OPTION_DISABLE_STD_STRING_USAGE)
QUEX_INLINE std::basic_string<uint32_t>
QUEX_NAME(lexeme_to_utf32)(const std::basic_string<TestAnalyzer_lexatom_t>& Source)
{
/* Save iteration over string with existing character converters.
* => copy string to a temporary array.                                   */
uint32_t    tmp_drain[1];
uint32_t*   drain_it;
TestAnalyzer_lexatom_t*          source = (TestAnalyzer_lexatom_t*)
QUEXED(MemoryManager_allocate)(
sizeof(TestAnalyzer_lexatom_t) * (Source.length() + 1),
E_MemoryObjectType_TEXT);
const size_t                SourceLength = Source.length();
const TestAnalyzer_lexatom_t*    source_it;

std::basic_string<uint32_t>  result;


if( SourceLength != Source.copy(&source[0], SourceLength) ) {
QUEXED(MemoryManager_free)(source, E_MemoryObjectType_TEXT);
return result;
}
/* .copy() does not append a terminating zero ...
* and it is not to be copied.                                            */
for(source_it = &source[0]; source_it < &source[SourceLength]; ) {
drain_it = tmp_drain;
QUEX_NAME(lexeme_to_utf32_character)(&source_it, &drain_it);
__quex_assert(source_it >  &source[0]);
__quex_assert(source_it <= &source[SourceLength]);
result.append((uint32_t*)tmp_drain, (size_t)(drain_it - tmp_drain));
}

QUEXED(MemoryManager_free)(source, E_MemoryObjectType_TEXT);
return result;
}
#endif


QUEX_INLINE void
QUEX_NAME(lexeme_nnzt_to_char)(const TestAnalyzer_lexatom_t**      source_pp,
const TestAnalyzer_lexatom_t*        SourceEnd,
char**      drain_pp,
const char* DrainEnd)
/* Convert a lexeme that is *not necessarily zero terminated* (nnzt), adapt the
* pointer to begin of source and begin of drain for quick iteration over
* larger segments.                                                           */
{
const TestAnalyzer_lexatom_t*  source_iterator;
char* drain_it;
const ptrdiff_t           TargetMaxCodeUnitN = 4; /* UF32=1, UTF16=2, utf8=... */

__quex_assert(source_pp != 0x0);
__quex_assert(*source_pp != 0x0);
__quex_assert(drain_pp != 0x0);
__quex_assert(*drain_pp != 0x0);

drain_it  = *drain_pp;
for(source_iterator=*source_pp; source_iterator != SourceEnd; ) {
if     ( source_iterator == SourceEnd ) break;
else if( DrainEnd - drain_it < TargetMaxCodeUnitN ) break;
QUEX_NAME(lexeme_to_char_character)(&source_iterator, &drain_it);
__quex_assert(source_iterator >  *source_pp);
__quex_assert(source_iterator <= SourceEnd);
}

*drain_pp  = drain_it;
*source_pp = source_iterator;
}

QUEX_INLINE char*
QUEX_NAME(lexeme_to_char)(const TestAnalyzer_lexatom_t*         SourceBegin,
char*        drain_p,
const char*  DrainEnd)
/* Convert a zero-terminated lexeme. Adapt the drain pointer for quicker
* iteration over write buffer.
*
* RETURNS: 0, in case that conversion failed due to insufficient drain
*             space.
*          Pointer to END of converted string.                               */
{
const TestAnalyzer_lexatom_t*  source_iterator;
char* drain_it;
char* terminating_zero_p;
const ptrdiff_t           TargetMaxCodeUnitN = 4; /* UF32=1, UTF16=2, utf8=... */

__quex_assert(SourceBegin != 0x0);
__quex_assert(drain_p != 0x0);

drain_it = drain_p;
for(source_iterator=SourceBegin; *source_iterator != (TestAnalyzer_lexatom_t)0; ) {
if( DrainEnd - drain_it < TargetMaxCodeUnitN ) {
return (char*)0;
}
QUEX_NAME(lexeme_to_char_character)(&source_iterator,
&drain_it);
__quex_assert(source_iterator > SourceBegin);
__quex_assert(drain_it <= DrainEnd);
}

terminating_zero_p = drain_it;
if( DrainEnd - drain_it < TargetMaxCodeUnitN ) {
return (char*)0;
}
QUEX_NAME(lexeme_to_char_character)(&source_iterator,
&drain_it);
__quex_assert(source_iterator > SourceBegin);
__quex_assert(drain_it <= DrainEnd);

return terminating_zero_p;
}

#if    ! defined(__QUEX_OPTION_PLAIN_C) \
&& ! defined(QUEX_OPTION_DISABLE_STD_STRING_USAGE)
QUEX_INLINE std::basic_string<char>
QUEX_NAME(lexeme_to_char)(const std::basic_string<TestAnalyzer_lexatom_t>& Source)
{
/* Save iteration over string with existing character converters.
* => copy string to a temporary array.                                   */
char    tmp_drain[4];
char*   drain_it;
TestAnalyzer_lexatom_t*          source = (TestAnalyzer_lexatom_t*)
QUEXED(MemoryManager_allocate)(
sizeof(TestAnalyzer_lexatom_t) * (Source.length() + 1),
E_MemoryObjectType_TEXT);
const size_t                SourceLength = Source.length();
const TestAnalyzer_lexatom_t*    source_it;

std::basic_string<char>  result;


if( SourceLength != Source.copy(&source[0], SourceLength) ) {
QUEXED(MemoryManager_free)(source, E_MemoryObjectType_TEXT);
return result;
}
/* .copy() does not append a terminating zero ...
* and it is not to be copied.                                            */
for(source_it = &source[0]; source_it < &source[SourceLength]; ) {
drain_it = tmp_drain;
QUEX_NAME(lexeme_to_char_character)(&source_it, &drain_it);
__quex_assert(source_it >  &source[0]);
__quex_assert(source_it <= &source[SourceLength]);
result.append((char*)tmp_drain, (size_t)(drain_it - tmp_drain));
}

QUEXED(MemoryManager_free)(source, E_MemoryObjectType_TEXT);
return result;
}
#endif


QUEX_INLINE void
QUEX_NAME(lexeme_nnzt_to_wchar_t)(const TestAnalyzer_lexatom_t**      source_pp,
const TestAnalyzer_lexatom_t*        SourceEnd,
wchar_t**      drain_pp,
const wchar_t* DrainEnd)
/* Convert a lexeme that is *not necessarily zero terminated* (nnzt), adapt the
* pointer to begin of source and begin of drain for quick iteration over
* larger segments.                                                           */
{
const TestAnalyzer_lexatom_t*  source_iterator;
wchar_t* drain_it;
const ptrdiff_t           TargetMaxCodeUnitN = 4; /* UF32=1, UTF16=2, utf8=... */

__quex_assert(source_pp != 0x0);
__quex_assert(*source_pp != 0x0);
__quex_assert(drain_pp != 0x0);
__quex_assert(*drain_pp != 0x0);

drain_it  = *drain_pp;
for(source_iterator=*source_pp; source_iterator != SourceEnd; ) {
if     ( source_iterator == SourceEnd ) break;
else if( DrainEnd - drain_it < TargetMaxCodeUnitN ) break;
QUEX_NAME(lexeme_to_wchar_t_character)(&source_iterator, &drain_it);
__quex_assert(source_iterator >  *source_pp);
__quex_assert(source_iterator <= SourceEnd);
}

*drain_pp  = drain_it;
*source_pp = source_iterator;
}

QUEX_INLINE wchar_t*
QUEX_NAME(lexeme_to_wchar_t)(const TestAnalyzer_lexatom_t*         SourceBegin,
wchar_t*        drain_p,
const wchar_t*  DrainEnd)
/* Convert a zero-terminated lexeme. Adapt the drain pointer for quicker
* iteration over write buffer.
*
* RETURNS: 0, in case that conversion failed due to insufficient drain
*             space.
*          Pointer to END of converted string.                               */
{
const TestAnalyzer_lexatom_t*  source_iterator;
wchar_t* drain_it;
wchar_t* terminating_zero_p;
const ptrdiff_t           TargetMaxCodeUnitN = 4; /* UF32=1, UTF16=2, utf8=... */

__quex_assert(SourceBegin != 0x0);
__quex_assert(drain_p != 0x0);

drain_it = drain_p;
for(source_iterator=SourceBegin; *source_iterator != (TestAnalyzer_lexatom_t)0; ) {
if( DrainEnd - drain_it < TargetMaxCodeUnitN ) {
return (wchar_t*)0;
}
QUEX_NAME(lexeme_to_wchar_t_character)(&source_iterator,
&drain_it);
__quex_assert(source_iterator > SourceBegin);
__quex_assert(drain_it <= DrainEnd);
}

terminating_zero_p = drain_it;
if( DrainEnd - drain_it < TargetMaxCodeUnitN ) {
return (wchar_t*)0;
}
QUEX_NAME(lexeme_to_wchar_t_character)(&source_iterator,
&drain_it);
__quex_assert(source_iterator > SourceBegin);
__quex_assert(drain_it <= DrainEnd);

return terminating_zero_p;
}

#if    ! defined(__QUEX_OPTION_PLAIN_C) \
&& ! defined(QUEX_OPTION_DISABLE_STD_STRING_USAGE)
QUEX_INLINE std::basic_string<wchar_t>
QUEX_NAME(lexeme_to_wchar_t)(const std::basic_string<TestAnalyzer_lexatom_t>& Source)
{
/* Save iteration over string with existing character converters.
* => copy string to a temporary array.                                   */
wchar_t    tmp_drain[4];
wchar_t*   drain_it;
TestAnalyzer_lexatom_t*          source = (TestAnalyzer_lexatom_t*)
QUEXED(MemoryManager_allocate)(
sizeof(TestAnalyzer_lexatom_t) * (Source.length() + 1),
E_MemoryObjectType_TEXT);
const size_t                SourceLength = Source.length();
const TestAnalyzer_lexatom_t*    source_it;

std::basic_string<wchar_t>  result;


if( SourceLength != Source.copy(&source[0], SourceLength) ) {
QUEXED(MemoryManager_free)(source, E_MemoryObjectType_TEXT);
return result;
}
/* .copy() does not append a terminating zero ...
* and it is not to be copied.                                            */
for(source_it = &source[0]; source_it < &source[SourceLength]; ) {
drain_it = tmp_drain;
QUEX_NAME(lexeme_to_wchar_t_character)(&source_it, &drain_it);
__quex_assert(source_it >  &source[0]);
__quex_assert(source_it <= &source[SourceLength]);
result.append((wchar_t*)tmp_drain, (size_t)(drain_it - tmp_drain));
}

QUEXED(MemoryManager_free)(source, E_MemoryObjectType_TEXT);
return result;
}
#endif


QUEX_INLINE void
QUEX_NAME(lexeme_nnzt_to_pretty_char)(const TestAnalyzer_lexatom_t**      source_pp,
const TestAnalyzer_lexatom_t*        SourceEnd,
char**      drain_pp,
const char* DrainEnd)
/* Convert a lexeme that is *not necessarily zero terminated* (nnzt), adapt the
* pointer to begin of source and begin of drain for quick iteration over
* larger segments.                                                           */
{
const TestAnalyzer_lexatom_t*  source_iterator;
char* drain_it;
const ptrdiff_t           TargetMaxCodeUnitN = 4; /* UF32=1, UTF16=2, utf8=... */

__quex_assert(source_pp != 0x0);
__quex_assert(*source_pp != 0x0);
__quex_assert(drain_pp != 0x0);
__quex_assert(*drain_pp != 0x0);

drain_it  = *drain_pp;
for(source_iterator=*source_pp; source_iterator != SourceEnd; ) {
if     ( source_iterator == SourceEnd ) break;
else if( DrainEnd - drain_it < TargetMaxCodeUnitN ) break;
QUEX_NAME(lexeme_to_pretty_char_character)(&source_iterator, &drain_it);
__quex_assert(source_iterator >  *source_pp);
__quex_assert(source_iterator <= SourceEnd);
}

*drain_pp  = drain_it;
*source_pp = source_iterator;
}

QUEX_INLINE char*
QUEX_NAME(lexeme_to_pretty_char)(const TestAnalyzer_lexatom_t*         SourceBegin,
char*        drain_p,
const char*  DrainEnd)
/* Convert a zero-terminated lexeme. Adapt the drain pointer for quicker
* iteration over write buffer.
*
* RETURNS: 0, in case that conversion failed due to insufficient drain
*             space.
*          Pointer to END of converted string.                               */
{
const TestAnalyzer_lexatom_t*  source_iterator;
char* drain_it;
char* terminating_zero_p;
const ptrdiff_t           TargetMaxCodeUnitN = 4; /* UF32=1, UTF16=2, utf8=... */

__quex_assert(SourceBegin != 0x0);
__quex_assert(drain_p != 0x0);

drain_it = drain_p;
for(source_iterator=SourceBegin; *source_iterator != (TestAnalyzer_lexatom_t)0; ) {
if( DrainEnd - drain_it < TargetMaxCodeUnitN ) {
return (char*)0;
}
QUEX_NAME(lexeme_to_pretty_char_character)(&source_iterator,
&drain_it);
__quex_assert(source_iterator > SourceBegin);
__quex_assert(drain_it <= DrainEnd);
}

terminating_zero_p = drain_it;
if( DrainEnd - drain_it < TargetMaxCodeUnitN ) {
return (char*)0;
}
QUEX_NAME(lexeme_to_pretty_char_character)(&source_iterator,
&drain_it);
__quex_assert(source_iterator > SourceBegin);
__quex_assert(drain_it <= DrainEnd);

return terminating_zero_p;
}

#if    ! defined(__QUEX_OPTION_PLAIN_C) \
&& ! defined(QUEX_OPTION_DISABLE_STD_STRING_USAGE)
QUEX_INLINE std::basic_string<char>
QUEX_NAME(lexeme_to_pretty_char)(const std::basic_string<TestAnalyzer_lexatom_t>& Source)
{
/* Save iteration over string with existing character converters.
* => copy string to a temporary array.                                   */
char    tmp_drain[4];
char*   drain_it;
TestAnalyzer_lexatom_t*          source = (TestAnalyzer_lexatom_t*)
QUEXED(MemoryManager_allocate)(
sizeof(TestAnalyzer_lexatom_t) * (Source.length() + 1),
E_MemoryObjectType_TEXT);
const size_t                SourceLength = Source.length();
const TestAnalyzer_lexatom_t*    source_it;

std::basic_string<char>  result;


if( SourceLength != Source.copy(&source[0], SourceLength) ) {
QUEXED(MemoryManager_free)(source, E_MemoryObjectType_TEXT);
return result;
}
/* .copy() does not append a terminating zero ...
* and it is not to be copied.                                            */
for(source_it = &source[0]; source_it < &source[SourceLength]; ) {
drain_it = tmp_drain;
QUEX_NAME(lexeme_to_pretty_char_character)(&source_it, &drain_it);
__quex_assert(source_it >  &source[0]);
__quex_assert(source_it <= &source[SourceLength]);
result.append((char*)tmp_drain, (size_t)(drain_it - tmp_drain));
}

QUEXED(MemoryManager_free)(source, E_MemoryObjectType_TEXT);
return result;
}
#endif



QUEX_NAMESPACE_MAIN_CLOSE

#endif /* __QUEX_INCLUDE_GUARD__TESTANALYZER_UNICODE_UINT8_T */

