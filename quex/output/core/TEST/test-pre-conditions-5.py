#! /usr/bin/env python
# -*- coding: utf8 -*-
import sys
import generator_test

if "--hwut-info" in sys.argv:
    print "Pre-conditions: Test with UTF8;"
    print "CHOICES: ANSI-C, Cpp-Path-CG, Cpp-Template;"
    print "SAME;"
    sys.exit(0)

if len(sys.argv) < 2:
    print "Language argument not acceptable, use --hwut-info"
    sys.exit(0)

choice = sys.argv[1]

pattern_list = [
    # -- pre-conditioned expressions need to preceed same (non-preoconditioned) expressions,
    #    otherwise, the un-conditional expressions gain precedence and the un-conditional
    #    pattern is never matched.
    #
    # -- post-conditioned patterns do not need to appear before the same non-postconditioned
    #    patterns, since they are always longer.
    #
    # repetition of 'x' (one or more) **preceded** by 'good' + whitespace
    '黑森林/X/',
    'X/黑森林/',
    'X',
    '黑森林',
    '[ ]',
]
pattern_action_pair_list = map(lambda re: (re, re.replace("\\t", "\\\\t").replace("\\n", "\\\\n")), 
                               pattern_list)

test_str = """X黑森林 黑森林 X黑森林 黑森林X"""
generator_test.do(pattern_action_pair_list, test_str, {}, choice, QuexBufferSize=12, Encoding="utf8")    
