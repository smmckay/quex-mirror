#! /usr/bin/env python
# -*- coding: utf8 -*-
import os
import sys
sys.path.insert(0, os.environ["QUEX_PATH"])

import quex.input.regular_expression.engine                   as     regex
import quex.engine.state_machine.algorithm.acceptance_pruning as     acceptance_pruning
from   quex.constants                                         import E_InputActions
import help

choice_str = "CHOICES: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10;"
choice     = sys.argv[1]

pattern_list_db = { 

"0": [
        'a',        
        'ab',     
   ],
   #    ┌────┐  a   ┌────┐  b   ┌────┐
   #    │ 26 │ ───▶ │ 27 │ ───▶ │ 28 │
   #    └────┘      └────┘      └────┘
   #____________________________________________________________________

"1": [
        'a',        
        'abc',     
   ],
   #    ┌────┐  a   ┌────┐  b   ┌────┐  c   ┌────┐
   #    │ 37 │ ───▶ │ 38 │ ───▶ │ 39 │ ───▶ │ 40 │
   #    └────┘      └────┘      └────┘      └────┘
   #____________________________________________________________________

"2": [
        'a',        
        'b',     
        '[ab]c'
   ],
   #    ┌────┐  a   ┌────┐  c   ┌────┐
   #    │ 35 │ ───▶ │ 36 │ ───▶ │ 38 │
   #    └────┘      └────┘      └────┘
   #      │                       ▲
   #      │ b                     │
   #      ▼                       │
   #    ┌────┐  c                 │
   #    │ 37 │ ───────────────────┘
   #    └────┘
   #____________________________________________________________________

"3": [
        'a',        
        'b',     
        '[ab]cd'
   ],
   #    ┌────┐  a   ┌────┐  c   ┌────┐  d   ┌────┐
   #    │ 45 │ ───▶ │ 46 │ ───▶ │ 48 │ ───▶ │ 49 │
   #    └────┘      └────┘      └────┘      └────┘
   #      │                       ▲
   #      │ b                     │
   #      ▼                       │
   #    ┌────┐  c                 │
   #    │ 47 │ ───────────────────┘
   #    └────┘
   #____________________________________________________________________

"4": [
        'aa?',        
        'aa?cd'
   ],
   #                       c
   #                  ┌───────────────────────┐
   #                  │                       ▼
   #    ┌────┐  a   ┌────┐  a   ┌────┐  c   ┌────┐  d   ┌────┐
   #    │ 56 │ ───▶ │ 57 │ ───▶ │ 59 │ ───▶ │ 58 │ ───▶ │ 60 │
   #    └────┘      └────┘      └────┘      └────┘      └────┘
   #____________________________________________________________________

"5": [
        '[ab]',        
        '((aa?)|b)cd'
   ],
   #                       c
   #                  ┌───────────────────────┐
   #                  │                       ▼
   #    ┌────┐  a   ┌────┐  a   ┌────┐  c   ┌────┐  d   ┌────┐
   #    │ 68 │ ───▶ │ 69 │ ───▶ │ 73 │ ───▶ │ 71 │ ───▶ │ 72 │
   #    └────┘      └────┘      └────┘      └────┘      └────┘
   #      │                                   ▲
   #      │ b                                 │
   #      ▼                                   │
   #    ┌────┐  c                             │
   #    │ 70 │ ───────────────────────────────┘
   #    └────┘
   #____________________________________________________________________

"6": [
        '[ab]',        
        '((ab)|b)cd',
   ],
   #    ┌────┐  a   ┌────┐  b   ┌────┐  c   ┌────┐  d   ┌────┐
   #    │ 68 │ ───▶ │ 69 │ ───▶ │ 73 │ ───▶ │ 71 │ ───▶ │ 72 │
   #    └────┘      └────┘      └────┘      └────┘      └────┘
   #      │                                   ▲
   #      │ b                                 │
   #      ▼                                   │
   #    ┌────┐  c                             │
   #    │ 70 │ ───────────────────────────────┘
   #    └────┘
   #____________________________________________________________________

"7": [
        'a+',        
        'b+c',        
        '(a+|(b+c))de',
   ],
   #                             b
   #                           ┌───┐
   #                           ▼   │
   #          ┌───────┐  b   ┌───────┐  c   ┌─────┐  d   ┌─────┐  e   ┌─────┐
   #      ┌── │  131  │ ───▶ │  133  │ ───▶ │ 134 │ ───▶ │ 135 │ ───▶ │ 136 │
   #      │   └───────┘      └───────┘      └─────┘      └─────┘      └─────┘
   #      │       a                                        ▲
   #      │ a   ┌───┐                                      │
   #      │     ▼   │                                      │
   #      │   ┌───────┐  d                                 │
   #      └─▶ │  132  │ ───────────────────────────────────┘
   #          └───────┘
   #____________________________________________________________________

"8": [
        'a+',        
        'b',        
        '(a+|(bc+))de',
   ],
   #                                          c
   #                                        ┌───┐
   #                                        ▼   │
   #          ┌───────┐  b   ┌─────┐  c   ┌───────┐  d   ┌─────┐  e   ┌─────┐
   #      ┌── │  112  │ ───▶ │ 114 │ ───▶ │  115  │ ───▶ │ 116 │ ───▶ │ 117 │
   #      │   └───────┘      └─────┘      └───────┘      └─────┘      └─────┘
   #      │       a                                        ▲
   #      │ a   ┌───┐                                      │
   #      │     ▼   │                                      │
   #      │   ┌───────┐  d                                 │
   #      └─▶ │  113  │ ───────────────────────────────────┘
   #          └───────┘
   #____________________________________________________________________

"9": [
        'if',        
        '[a-z]+',
   ],
   #           ['a', 'h'], ['j', 'z']
   #      ┌────────────────────────────────────────────┐
   #      │                                            ▼
   #    ┌────┐      ┌────┐      ┌────┐               ┌────┐   ['a', 'z']
   #    │    │      │    │      │    │               │    │ ─────────────┐
   #    │ 39 │  i   │ 41 │  f   │ 42 │  ['a', 'z']   │ 40 │              │
   #    │    │ ───▶ │    │ ───▶ │    │ ────────────▶ │    │ ◀────────────┘
   #    └────┘      └────┘      └────┘               └────┘
   #                  │    ['a', 'e'], ['g', 'z']      ▲
   #                  └────────────────────────────────┘
   #____________________________________________________________________

"10": 
   # Generate a case where the acceptance is not clear but there are multiple 
   # places on the path where it is stored. The last acceptance state must
   # always store.
   [
        "a|ab",
        "(1|ab|ax)ef",
   ],
   #          1
   #      ┌──────────────────────┐
   #      │                      ▼
   #    ┌───┐  a   ┌────┐  x   ┌───┐  e   ┌───┐  f   ┌───┐
   #    │ 0 │ ───▶ │ 4  │ ───▶ │ 1 │ ───▶ │ 2 │ ───▶ │ 3 │
   #    └───┘      └────┘      └───┘      └───┘      └───┘
   #              A1 │                      ▲        A2
   #                 │ b                    │
   #                 ▼                      │
   #               ┌────┐  e                │
   #               │ 5  │ ──────────────────┘
   #               └────┘
   #______________A1____________________________________________________

"Nonsense": [
        'ade',
        'abc',        
   ],
}

if __name__ == "__main__":
    if "--hwut-info" in sys.argv:
        print "Track Analyzis: Without Pre- and Post-Contexts;"
        print choice_str
        sys.exit()

    acceptance_pruning._deactivated_for_unit_test_f = True

    sm = help.prepare(pattern_list_db[choice])

    # For DEBUG purposes: specify 'DRAW' on command line
    help.if_DRAW_in_sys_argv(sm)
    help.test_track_analysis(sm)
