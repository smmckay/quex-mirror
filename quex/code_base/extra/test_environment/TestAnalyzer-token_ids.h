/* -*- C++ -*- vim: set syntax=cpp:
 * PURPOSE: File containing definition of token-identifier and
 *          a function that maps token identifiers to a string
 *          name.
 *
 * NOTE: This file has been created automatically by Quex.
 *       Visit quex.org for further info.
 *
 * DATE: Wed Dec 27 12:03:25 2017
 *
 * (C) 2005-2010 Frank-Rene Schaefer
 * ABSOLUTELY NO WARRANTY                                                     */
#ifndef __QUEX_INCLUDE_GUARD__AUTO_TOKEN_IDS_QUEX_TESTANALYZER__QUEX_TOKEN__
#define __QUEX_INCLUDE_GUARD__AUTO_TOKEN_IDS_QUEX_TESTANALYZER__QUEX_TOKEN__

#ifndef __QUEX_OPTION_PLAIN_C
#   include<cstdio> 
#else
#   include<stdio.h> 
#endif

/* Note: When multiple lexical analyzers are included, then their
 *       token prefix must differ! Use '--token-id-prefix'.                   */
#define QUEX_TKN_DEDENT        ((QUEX_TYPE_TOKEN_ID)10000)
#define QUEX_TKN_INDENT        ((QUEX_TYPE_TOKEN_ID)10001)
#define QUEX_TKN_NODENT        ((QUEX_TYPE_TOKEN_ID)10002)
#define QUEX_TKN_TERMINATION   ((QUEX_TYPE_TOKEN_ID)0)
#define QUEX_TKN_UNINITIALIZED ((QUEX_TYPE_TOKEN_ID)10003)
#define QUEX_TKN_X             ((QUEX_TYPE_TOKEN_ID)10004)


#endif /* __QUEX_INCLUDE_GUARD__AUTO_TOKEN_IDS_QUEX_TESTANALYZER__QUEX_TOKEN__        */
