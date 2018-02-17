#! /usr/bin/env python
import generator_test
import sys

if "--hwut-info" in sys.argv:
    print "Special Cases;"
    print "CHOICES: l2-b4, l3-b5, long-way-back, pc-l2-b4, pc-l3-b5, pc-long-way-back;"
    sys.exit(0)

if "l2-b4" in sys.argv:
    pattern_action_pair_list = [
        ('[ ]+/x+/', "WHITESPACE / X+ /"),
        ('x+',       "X+"),
        ('[ ]+',     "WHITESPACE")
    ]
    test_str_list = ["xx ", " xx", "xx    ", "     xx"]
    buffer_size = 4

if "l3-b5" in sys.argv:
    pattern_action_pair_list = [
        ('[ ]+/x+/', "WHITESPACE / X+ /"),
        ('x+',       "X+"),
        ('[ ]+',     "WHITESPACE")
    ]
    test_str_list = ["xxx ", " xxx", "xxx    ", "     xxx"]
    buffer_size = 5

if "long-way-back" in sys.argv:
    pattern_action_pair_list = [
        ('long-way-back/x+/', "LONG WAY BACK / X+ /"),
        ('x+',                "X+"),
        ('[longwayback\-]',   "LETTER")
    ]
    test_str_list = ["xxlong-way-back", "long-way-backxx", "xxlong-way-back", "long-way-backxx"]
    buffer_size = 4

#######################
if "pc-l2-b4" in sys.argv:
    pattern_action_pair_list = [
        ('[ ]+/x/y', "WHITESPACE / X / Y"),
        ('x+',       "X+"),
        ('y+',       "Y+"),
        ('[ ]+',     "WHITESPACE")
    ]
    test_str_list = ["xy ", " xy", "xy    ", "     xy"]
    buffer_size = 4

if "pc-l3-b5" in sys.argv:
    pattern_action_pair_list = [
        ('[ ]+/x+/y', "WHITESPACE / X+ / Y"),
        ('x+',       "X+"),
        ('y+',       "Y+"),
        ('[ ]+',     "WHITESPACE")
    ]
    test_str_list = ["xxy ", " xxy", "xxy    ", "     xxy"]
    buffer_size = 5

if "pc-long-way-back" in sys.argv:
    pattern_action_pair_list = [
        ('long-way-back/x+/y', "LONG WAY BACK / X+ / Y"),
        ('x+',              "X+"),
        ('y+',              "Y+"),
        ('[longwayback\-]', "LETTER")
    ]
    test_str_list = ["xylong-way-back", "long-way-backxy", "xylong-way-back", "long-way-backxy"]
    buffer_size = 4

generator_test.do(pattern_action_pair_list, test_str_list, {}, "ANSI-C",
                  QuexBufferSize=buffer_size)    
