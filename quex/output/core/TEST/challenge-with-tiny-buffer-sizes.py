#! /usr/bin/env python
import os
import sys
sys.path.insert(0, "../")
import generator_test
import sys

if "--hwut-info" in sys.argv:
    print "Special Cases;"
    print "CHOICES: l2-b5;"
    sys.exit(0)

if "l2-b5" in sys.argv:
    pattern_action_pair_list = [
        ('[ ]+/x+/', "WHITESPACE / X+ /"),
        ('x+',       "X+"),
        ('[ ]+',     "WHITESPACE")
    ]
    test_str    = "xx "
    buffer_size = 5

generator_test.do(pattern_action_pair_list, 
                  test_str, {}, "ANSI-C",
                  QuexBufferSize=buffer_size)    
