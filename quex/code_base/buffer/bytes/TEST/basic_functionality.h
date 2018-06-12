#ifndef INCLUDE_GUARD_QUEX_BASIC_FUNCTIONALITY_H
#define INCLUDE_GUARD_QUEX_BASIC_FUNCTIONALITY_H

#define  QUEX_NAME(X) TestAnalyzer_ ## X
#include "test_c/lib/buffer/bytes/ByteLoader"

extern void verify_basic_functionality(QUEX_NAME(ByteLoader)* me);
extern void initial_position(QUEX_NAME(ByteLoader)* me);

#endif  /* INCLUDE_GUARD_QUEX_BASIC_FUNCTIONALITY_H */

