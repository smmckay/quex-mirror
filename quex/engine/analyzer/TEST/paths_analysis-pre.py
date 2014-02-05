#! /usr/bin/env python
# -*- coding: utf8 -*-
import os
import sys
sys.path.insert(0, os.environ["QUEX_PATH"])

import quex.input.regular_expression.engine  as regex
from   quex.engine.generator.base            import get_combined_state_machine
from   quex.blackboard                       import E_InputActions
import help

if "--hwut-info" in sys.argv:
    print "Track Analyzis: With Pre-Contexts;"
    print "CHOICES: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14;"
    sys.exit()

if "0" in sys.argv:
   #    ┌───┐  a   ┌───┐  b   ┌───┐
   #    │ 0 │ ───▶ │ 1 │ ───▶ │ 2 │
   #    └───┘      └───┘      └───┘
   #____________________________________________________________________
    pattern_list = [
        'x/a/',        
        'ab',     
    ]
elif "1" in sys.argv:
    pattern_list = [
        'ab',     
        'x/a/',        
    ]
elif "2" in sys.argv:
    pattern_list = [
        'x/a/',        
        'abc',        
    ]
elif "3" in sys.argv:
    #                                                    d                         f
    #                                                  ┌───┐                     ┌───┐
    #                                                  ▼   │                     ▼   │
    #    ┌───┐  a   ┌───┐  b   ┌───┐  c   ┌───┐  d   ┌───────┐  e   ┌───┐  f   ┌───────┐  g   ┌───┐
    #    │ 0 │ ───▶ │ 1 │ ───▶ │ 2 │ ───▶ │ 3 │ ───▶ │   4   │ ───▶ │ 5 │ ───▶ │   6   │ ───▶ │ 7 │
    #    └───┘      └───┘      └───┘      └───┘      └───────┘      └───┘      └───────┘      └───┘
    #____________________________________________________________________
    pattern_list = [
        'abc',        
        'x/a/',        
    ]
elif "4" in sys.argv:
    #    ┌───┐  a   ┌───┐  b   ┌───┐  c   ┌───┐
    #    │ 0 │ ───▶ │ 1 │ ───▶ │ 2 │ ───▶ │ 3 │
    #    └───┘      └───┘      └───┘      └───┘
    #____________________________________________________________________
    pattern_list = [
        'a',        
        'x/abc/'
    ]
elif "5" in sys.argv:
    #    ┌───┐  a   ┌───┐  b   ┌───┐  c   ┌───┐
    #    │ 0 │ ───▶ │ 1 │ ───▶ │ 2 │ ───▶ │ 3 │
    #    └───┘      └───┘      └───┘      └───┘
    #____________________________________________________________________
    pattern_list = [
        'a',
        'x/a/',
        'x/ab/',
        'x/abc/',
    ]
elif "6" in sys.argv:
    #    ┌────┐  a   ┌───┐  b   ┌───┐  c   ┌───┐
    #    │ 0  │ ───▶ │ 1 │ ───▶ │ 2 │ ───▶ │ 3 │
    #    └────┘      └───┘      └───┘      └───┘
    #      │
    #      │ b
    #      ▼
    #    ┌────┐  b   ┌───┐  c   ┌───┐
    #    │ 4  │ ───▶ │ 5 │ ───▶ │ 6 │
    #    └────┘      └───┘      └───┘
    #____________________________________________________________________
    pattern_list = [
        'a',
        'b',
        'x/abc/',
        'x/bbc/',
    ]
elif "7" in sys.argv:
    #    ┌────┐  a   ┌───┐  b   ┌───┐  c   ┌───┐  d   ┌───┐
    #    │ 0  │ ───▶ │ 1 │ ───▶ │ 2 │ ───▶ │ 3 │ ───▶ │ 4 │
    #    └────┘      └───┘      └───┘      └───┘      └───┘
    #      │                                 ▲
    #      │ b                               │
    #      ▼                                 │
    #    ┌────┐  c                           │
    #    │ 5  │ ─────────────────────────────┘
    #    └────┘
    #____________________________________________________________________
    pattern_list = [
        '^[ab]',        
        '((ab)|b)cd',
    ]
elif "8" in sys.argv:
    #    ┌────┐  a   ┌───┐  b   ┌───┐  c   ┌───┐  d   ┌───┐
    #    │ 0  │ ───▶ │ 1 │ ───▶ │ 2 │ ───▶ │ 3 │ ───▶ │ 4 │
    #    └────┘      └───┘      └───┘      └───┘      └───┘
    #      │                                 ▲
    #      │ b                               │
    #      ▼                                 │
    #    ┌────┐  c                           │
    #    │ 5  │ ─────────────────────────────┘
    #    └────┘
    #____________________________________________________________________
    pattern_list = [
        '^a',        
        '^b',        
        '((ab)|b)cd',
    ]
elif "9" in sys.argv:
    #    ┌────┐  a   ┌───┐  b   ┌───┐  c   ┌───┐  d   ┌───┐
    #    │ 0  │ ───▶ │ 1 │ ───▶ │ 2 │ ───▶ │ 3 │ ───▶ │ 4 │
    #    └────┘      └───┘      └───┘      └───┘      └───┘
    #      │                                 ▲
    #      │ b                               │
    #      ▼                                 │
    #    ┌────┐  c                           │
    #    │ 5  │ ─────────────────────────────┘
    #    └────┘
    #____________________________________________________________________
    pattern_list = [
        '^a',        
        'b',        
        '((ab)|b)cd',
    ]
elif "10" in sys.argv:
    # Non-uniform traces with multiple pre-contexts
    #                                        c
    #                                      ┌───┐
    #                                      ▼   │
    #          ┌───────┐  b   ┌───┐  c   ┌───────┐  d   ┌───┐  e   ┌───┐  f   ┌───┐
    #      ┌── │   0   │ ───▶ │ 5 │ ───▶ │   6   │ ───▶ │ 2 │ ───▶ │ 3 │ ───▶ │ 4 │
    #      │   └───────┘      └───┘      └───────┘      └───┘      └───┘      └───┘
    #      │       a                                      ▲
    #      │ a   ┌───┐                                    │
    #      │     ▼   │                                    │
    #      │   ┌───────┐  d                               │
    #      └─▶ │   1   │ ─────────────────────────────────┘
    #          └───────┘
    #____________________________________________________________________
    pattern_list = [
        'x/a+/',
        'x/b/',
        '(a+|bc+)de',
        '0/(a+|bc+)def/',
        '1/(a+|bc+)def/',
        '2/(a+|bc+)def/',
    ]
elif "11" in sys.argv:
    # Non-uniform traces with multiple pre-contexts
    #                      c
    #                  ┌─────────────────────┐
    #                  │                     ▼
    #    ┌────┐  b   ┌───┐  b   ┌───┐  c   ┌───┐  d   ┌───┐  e   ┌───┐
    #    │ 0  │ ───▶ │ 4 │ ───▶ │ 5 │ ───▶ │ 6 │ ───▶ │   │ ───▶ │ 3 │
    #    └────┘      └───┘      └───┘      └───┘      │   │      └───┘
    #      │           │          │              d    │   │
    #      │ a         └──────────┼─────────────────▶ │ 2 │
    #      ▼                      │                   │   │
    #    ┌────┐                   │              d    │   │
    #    │ 1  │ ────────────┐     └─────────────────▶ │   │
    #    └────┘             │                         └───┘
    #                       │    d                      ▲
    #                       └───────────────────────────┘
    #____________________________________________________________________
    pattern_list = [
        'x/a/',
        'x/b/',
        '0/(a|bb?c?)de/',
        '1/(a|bb?c?)de/',
        '2/(a|bb?c?)de/',
    ]
elif "12" in sys.argv:
    #                                                    d                         f
    #                                                  ┌───┐                     ┌───┐
    #                                                  ▼   │                     ▼   │
    #    ┌───┐  a   ┌───┐  b   ┌───┐  c   ┌───┐  d   ┌───────┐  e   ┌───┐  f   ┌───────┐  g   ┌───┐
    #    │ 0 │ ───▶ │ 1 │ ───▶ │ 2 │ ───▶ │ 3 │ ───▶ │   4   │ ───▶ │ 5 │ ───▶ │   6   │ ───▶ │ 7 │
    #    └───┘      └───┘      └───┘      └───┘      └───────┘      └───┘      └───────┘      └───┘
    #____________________________________________________________________
    pattern_list = [
        '0/abc/',
        '1/abcd+e/',
        '2/abc/',
        '3/abcd+e/',
        '4/abc/',
        '5/abcd+e/',
        'a',
        'abc',
        'abcd+ef+g',
    ]
elif "13" in sys.argv:
    pattern_list = [
        '0/a/',        
        '1/b/',     
        '2/[ab]cd/',     
    ]
elif "14" in sys.argv:
    #    ┌────┐  a   ┌───┐  c   ┌───┐  d   ┌───┐
    #    │ 0  │ ───▶ │ 1 │ ───▶ │ 2 │ ───▶ │ 3 │
    #    └────┘      └───┘      └───┘      └───┘
    #      │                      ▲
    #      │ b                    │
    #      ▼                      │
    #    ┌────┐  c                │
    #    │ 4  │ ──────────────────┘
    #    └────┘
    #____________________________________________________________________
    pattern_list = [
        '0/a/',        
        '1/b/',     
        '2/[ab]/',     
        '[ab]cd',
    ]
else:
    assert False


sm = help.prepare(pattern_list)

# For DEBUG purposes: specify 'DRAW' on command line
help.if_DRAW_in_sys_argv(sm)
help.test(sm, PrintPRM_F=True)
