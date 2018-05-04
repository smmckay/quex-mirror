/* -*- C++ -*- vim:set syntax=cpp:
 * (C) 2005-2010 Frank-Rene Schaefer
 * ABSOLUTELY NO WARRANTY                      */
#ifndef __QUEX_INCLUDE_GUARD__ANALYZER__HEADERS_I
#define __QUEX_INCLUDE_GUARD__ANALYZER__HEADERS_I

#if ! defined(__QUEX_INCLUDE_INDICATOR__ANALYZER__CONFIGURATION)
#   error "No configuration header included before this header."
#endif

/* NOT: "$$INC: lexeme.i$$"
 *
 * Converters and helpers of 'lexeme.i' are only to be included from inside the
 * token class header.  Otherwise, it may occur multiple times when same token
 * class is used for multiple lexical analyzers.                              */

$$INC: analyzer/asserts.i$$
$$INC: buffer/asserts.i$$

$$INC: analyzer/member/token-receiving.i$$
$$INC: analyzer/member/mode-handling.i$$
$$INC: analyzer/member/misc.i$$
$$INC: analyzer/member/navigation.i$$
$$INC: analyzer/struct/constructor.i$$
$$INC: analyzer/struct/include-stack.i$$
$$INC: analyzer/struct/reset.i$$

$$INC: analyzer/Mode.i$$
$$INC: token/TokenQueue.i$$

$$INC: buffer/Buffer.i$$
$$INC: buffer/lexatoms/LexatomLoader.i$$
$$INC: buffer/bytes/ByteLoader$$

#ifdef QUEX_OPTION_COUNTER
$$INC: analyzer/Counter.i$$
#endif

#endif /* __QUEX_INCLUDE_GUARD__ANALYZER__HEADERS_I */
