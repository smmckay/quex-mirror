/* PURPOSE: This header defines standard integer types.
 *
 * This is done here, because some compiler distributions or versions of 
 * compiler distributions do not provide according C99 standard headers. 
 *
 * For the standard reference, please review: "The Open Group Base 
 * Specifications Issue 6, IEEE Std 1003.1, 2004 Edition".
 *
 * (C) 2008-2018  Frank-Rene Schaefer                                         */           
#ifndef __QUEX_INCLUDE_GUARD__COMPATIBILITY__STDINT_H
#define __QUEX_INCLUDE_GUARD__COMPATIBILITY__STDINT_H

#ifdef __cplusplus
extern "C" {
#endif

#if defined (_MSC_VER)
$$INC: quex/compatibility/win/msc_stdint.h$$
#elif defined(__BORLANDC__)
$$INC: quex/compatibility/win/borland_stdint.h$$
#elif defined(__sun) && defined(__sparc)
#   include <inttypes.h>      /* Thanks to sbellon@users.sourceforge.net */ 
#else
#   include <stdint.h>
#endif

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif /* __QUEX_INCLUDE_GUARD__COMPATIBILITY__STDINT_H */
