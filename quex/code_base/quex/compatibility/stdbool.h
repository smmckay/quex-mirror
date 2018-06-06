/* PURPOSE: This header defines standard bool data types for use
 *          in plain 'C' lexical analyser engines. 
 *
 * This is done here, because some compiler distributions or versions of 
 * compiler distributions do not provide this C99 standard header. 
 *
 * For the standard reference, please review: "The Open Group Base 
 * Specifications Issue 6, IEEE Std 1003.1, 2004 Edition".
 *
 * (C) 2008-2018  Frank-Rene Schaefer                                         */           
#ifndef __QUEX_INCLUDE_GUARD__COMPATIBILITY__STDBOOL_H
#define __QUEX_INCLUDE_GUARD__COMPATIBILITY__STDBOOL_H

#if defined(__QUEX_OPTION_PLAIN_C)

#if    (defined(__STDC_VERSION__) && __STDC_VERSION__ < 199901L) \
    || (defined(_MSC_VER)         && _MSC_VER < 1800)

   /* Helper definition for the case that the compiler distribution does not
    * provide 'stdbool.h'.                                                    */
#  if ! defined(__bool_true_false_are_defined)
      typedef int _Bool;
#     define bool  _Bool
#     define true  ((_Bool)1)
#     define false ((_Bool)0)
#     define __bool_true_false_are_defined ((int)(1))
#  endif

#else
   /* Include fails => compiler distribution does not provide 'stdbool.h'.
    * Use helper definitions above (and report problem, so that special
    * case can be included in later versions of Quex).                        */
#  include <stdbool.h>

#endif

#endif /* __QUEX_OPTION_PLAIN_C */
#endif /* __QUEX_INCLUDE_GUARD__COMPATIBILITY__STDBOOL_H */
