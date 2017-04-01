/* -*- C++ -*- vim: set syntax=cpp:
 * PURPOSE: File containing definition of token-identifier and
 *          a function that maps token identifiers to a string
 *          name.
 *
 * NOTE: This file has been created automatically by Quex.
 *       Visit quex.org for further info.
 *
 * DATE: Sat Apr  1 13:45:52 2017
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

/* The token class definition file can only be included after 
 * the definition of TERMINATION and UNINITIALIZED.          
 * (fschaef 12y03m24d: "I do not rememember why I wrote this.")               */
#include "TestAnalyzer-token.h"

/* Note: When multiple lexical analyzers are included, then their
 *       token prefix must differ! Use '--token-id-prefix'.                   */
#define QUEX_TKN_DEDENT        ((QUEX_TYPE_TOKEN_ID)10000)
#define QUEX_TKN_INDENT        ((QUEX_TYPE_TOKEN_ID)10001)
#define QUEX_TKN_NODENT        ((QUEX_TYPE_TOKEN_ID)10002)
#define QUEX_TKN_TERMINATION   ((QUEX_TYPE_TOKEN_ID)0)
#define QUEX_TKN_UNINITIALIZED ((QUEX_TYPE_TOKEN_ID)10003)
#define QUEX_TKN_X             ((QUEX_TYPE_TOKEN_ID)10004)


QUEX_NAMESPACE_TOKEN_OPEN
extern const char* QUEX_NAME_TOKEN(map_id_to_name)(const QUEX_TYPE_TOKEN_ID TokenID);
QUEX_NAMESPACE_TOKEN_CLOSE

#endif /* __QUEX_INCLUDE_GUARD__AUTO_TOKEN_IDS_QUEX_TESTANALYZER__QUEX_TOKEN__        */
