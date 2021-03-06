#! /usr/bin/env python
# -*- coding: utf8 -*-
import os
import sys
sys.path.insert(0, os.environ["QUEX_PATH"])

import quex.input.regular_expression.engine  as     regex
from   quex.constants                       import E_InputActions
import quex.engine.analyzer.TEST.help        as     help

if "--hwut-info" in sys.argv:
    print "Track Analyzis: With Pre- and Post-Contexts;"
    print "CHOICES: 1, 2, 3, 4, 5, 6, 7, 8, 9;"
    sys.exit()

if   "1" in sys.argv:
    pattern_list = [
        'x/a/bc',
        'y/ab/c',
        'z/abc/',
    ]
elif "2" in sys.argv:
    pattern_list = [
        'x/a/',        
        'a/bc',        
        'a/bcde',        
        'a',
    ]
elif "3" in sys.argv:
    pattern_list = [
        'x/a/',        
        'a/b+c',        
        'a/bcde',        
        'a',
    ]
elif "4" in sys.argv:
    pattern_list = [
        'x/a/bc',        
        'y/abc/',        
        'abcdef',
    ]
elif "5" in sys.argv:
    # Check that positions are stored even for dominated pre-contexts.
    # Pattern "a" dominates "x/a/aa/" when an 'a' arrives. But, at the
    # position of "c" in "(aaa|bb)cd" the pattern "x/a/aa" must win
    # and the right positioning must be applied.
    pattern_list = [
        "aa?",
        "x/a/aa",
        "b",
        "(aaa|bb)cd",
    ]
elif "6" in sys.argv:
    # A pre-context dominates another one, but at some point later the
    # positioning of the 'dominated' must be applied. This is similar
    # to the previous case, but it is not concerned with the 'cut' of
    # the unconditional pattern "aa?" as above.
    pattern_list = [
        "x/aa?/",    # (1) dominating (mentioned first)
        "y/a/aaa",   # (2) dominated (wins by length)
        "aaaab",
    ]
elif "7" in sys.argv:
    # Non-uniform traces with multiple pre-contexts
    pattern_list = [
        '0/a+/',
        '1/b/',
        '2/(a+|bc+)/d+ef',
        '3/(a+|bc+)d+/ef',
        '4/(a+|bc+)d+e/f',
    ]
elif "8" in sys.argv:
    # Case where the acceptance decides about positioning + dependence on pre-context
    #                                       b
    #      ┌───────────────┐              ┌───┐
    #      │               │              ▼   │
    #      │  ┌───┐  x   ┌───────┐  b   ┌───────┐  c   ┌───┐  d   ┌───┐  e   ┌───┐
    #      │  │ 0 │ ───▶ │   1   │ ───▶ │   6*  │ ───▶ │ 3 │ ───▶ │ 4 │ ───▶ │ 5*│
    #      │  └───┘      └───────┘S8    └───────┘R17   └───┘      └───┘      └───┘A44
    #      │                      S17                    ▲                          
    #      │                 a                           │
    #      │               ┌───┐                         │
    #      │               ▼   │                         │
    #      │        a    ┌───────┐  c                    │
    #      └───────────▶ │   2*  │───────────────────────┘
    #                    └───────┘R8
    #____________________________________________________________________
    pattern_list = [
        '0/x/a+',
        '1/x/b+',
        'x(a+|b+)cde',
    ]
elif "9" in sys.argv:
    # Non-uniform traces with multiple pre-contexts
    pattern_list = [
        'x/a/',
        'x/b/',
        'x/(a|bb?c?)de/',
        'x/(a|bb?c?)d/e',
    ]
else:
    assert False


sm = help.prepare(pattern_list)

# For DEBUG purposes: specify 'DRAW' on command line
help.if_DRAW_in_sys_argv(sm)
# help.test(sm, PrintPRM_F=True)
help.test(sm)

