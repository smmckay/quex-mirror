#ifndef __QUEX_INCLUDE_GUARD__ANALYZER__TEST__MY_TESTER_H
#define __QUEX_INCLUDE_GUARD__ANALYZER__TEST__MY_TESTER_H


#include <cstdio>

namespace quex {
    //typedef struct {} Token;
    typedef int       CounterLineColumnIndentation;
}

#include "minimum-definitions.h"

#include "ut/lib/analyzer/Counter"
#include "ut/lib/analyzer/Mode"
#include <ut/lib/MemoryManager>
#include "ut/lib/compatibility/stdint.h"

extern int  indentation[64];

class Tester { 
public:
    Tester();
    QUEX_NAME(Counter)   counter;
    QUEX_NAME(Mode)      tester_mini_mode;
    QUEX_NAME(Mode)*     __current_mode_p;
};

typedef Tester my_tester;

inline void 
mini_mode_on_indentation(my_tester* x, size_t Indentation) 
{
    indentation[((my_tester*)x)->counter._line_number_at_end-1] = Indentation;
    printf("indentation = %i\n", (int)Indentation);
}

Tester::Tester() 
{ 
    /* tester_mini_mode.on_indentation = mini_mode_on_indentation; */
    __current_mode_p = &tester_mini_mode; 
}

#include <ut/lib/analyzer/Counter.i>
#include <ut/lib/MemoryManager.i>

#endif // __QUEX_INCLUDE_GUARD__ANALYZER__TEST__MY_TESTER_H
