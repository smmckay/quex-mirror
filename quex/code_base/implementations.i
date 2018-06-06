/* -*- C++ -*- vim:set syntax=cpp:
 * (C) 2005-2010 Frank-Rene Schaefer
 * ABSOLUTELY NO WARRANTY                      */
#ifndef QUEX_INCLUDE_GUARD__ANALYZER__IMPLEMENTATIONS_I
#define QUEX_INCLUDE_GUARD__ANALYZER__IMPLEMENTATIONS_I

#if ! defined(__cplusplus)

$$INC: analyzer/asserts.i$$
$$INC: buffer/asserts.i$$

$$INCLUDE_TOKEN_CLASS_IMPLEMENTATION$$
$$INC: token/TokenQueue.i$$
$$INC: token/receiving.i$$

$$INC: analyzer/member/mode-handling.i$$
$$INC: analyzer/member/misc.i$$
$$INC: analyzer/member/navigation.i$$

$$INC: analyzer/struct/constructor.i$$
$$INC: analyzer/struct/include-stack.i$$
$$INC: analyzer/struct/reset.i$$

$$INC: buffer/Buffer.i$$
$$INC: buffer/lexatoms/LexatomLoader.i$$
$$INC: buffer/bytes/ByteLoader.i$$

$$INC: analyzer/Mode.i$$

$$INC: lexeme_base.i$$
$$INC: <count> analyzer/Counter.i$$

#endif


#if ! defined(QUEX_OPTION_USER_DEFINED_MEMORY_MANAGER)
$$INC: <lib-quex> quex/MemoryManager.i$$
#endif

QUEX_TYPE_LEXATOM   QUEX_NAME(LexemeNull) = (QUEX_TYPE_LEXATOM)0;


#endif /* QUEX_INCLUDE_GUARD__ANALYZER__HEADERS_I */
