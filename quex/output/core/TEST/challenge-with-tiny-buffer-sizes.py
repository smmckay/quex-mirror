#! /usr/bin/env python
#
# PURPOSE: Border-Tests with pre and post contexts in tiny buffers.
#
# .----------------------------------------------------------------------------.
# | The 'on_buffer_overflow' does not resize the buffer, so that whitespace is |
# | chopped into pieces. The 'challenge-with-tiny-buffer-sizes.qx' test does   |
# | operate with resizing.                                                     |
# '----------------------------------------------------------------------------'
#
# -- Buffer's size to hold exactly a matched lexatom, i.e.
#    buffer size = lexatom length + 2. The '2' is for the border lexatoms.
# -- Include backward conditions which require loading backward that requires
#    multiple reloads beyond the buffer sizes.
# -- Post conditions to check whether the store and restore works properly.
#
# CHOICES: with 'pc'       --> with post context
#          with 'dtc'      --> with dangerous trailing context (special treatment)
#          
#          'l2-b4'         --> lexatom length '2', buffer size = 4.
#          'l3-b5'         --> lexatom length '3', buffer size = 5.
#          'long-way-back' --> with a pre-context that walks along a long 
#                              graph in the state machine over multiple 
#                              backward loads.
#    
# (C) Frank-Rene Schaefer
#______________________________________________________________________________
import generator_test
import sys

if "--hwut-info" in sys.argv:
    print "Special Cases;"
    print "CHOICES: l2, l3, long-way-back, pc-l2, pc-l3, pc-long-way-back, dtc-l2, dtc-l3, dtc-long-way-back;"
    sys.exit(0)

if "l2" in sys.argv:
    pattern_action_pair_list = [
        ('[ ]+/x+/', "WHITESPACE / X+ /"),
        ('x+',       "X+"),
        ('[ ]',      "WHITESPACE")
    ]
    test_str_list = ["xx ", " xx", "xx    ", "     xx", "xx xx  xx   xx    xx"]
    lexeme_size = 2

if "l3" in sys.argv:
    pattern_action_pair_list = [
        ('[ ]+/x+/', "WHITESPACE / X+ /"),
        ('x+',       "X+"),
        ('[ ]',      "WHITESPACE")
    ]
    test_str_list = ["xxx ", " xxx", "xxx    ", "     xxx", "xxx xxx  xxx   xxx    xxx"]
    lexeme_size = 3

if "long-way-back" in sys.argv:
    pattern_action_pair_list = [
        ('long-way-back/x+/', "LONG WAY BACK / X+ /"),
        ('x+',                "X+"),
        ('[longwayback\-]',   "LETTER")
    ]
    test_str_list = ["xxlong-way-back", "long-way-backxx", "xxlong-way-back", "long-way-backxx"]
    lexeme_size = 2

if "pc-l2" in sys.argv:
    pattern_action_pair_list = [
        ('[ ]+/x/y', "WHITESPACE / X / Y"),
        ('x+',       "X+"),
        ('y+',       "Y+"),
        ('[ ]',      "WHITESPACE")
    ]
    test_str_list = ["xy ", " xy", "xy    ", "     xy", "xy xy  xy   xy    xy"]
    lexeme_size = 2

if "pc-l3" in sys.argv:
    pattern_action_pair_list = [
        ('[ ]+/x+/y', "WHITESPACE / X+ / Y"),
        ('x+',       "X+"),
        ('y+',       "Y+"),
        ('[ ]',      "WHITESPACE")
    ]
    test_str_list = ["xxy ", " xxy", "xxy    ", "     xxy", "xxy xxy  xxy   xxy    xxy"]
    lexeme_size = 3

if "pc-long-way-back" in sys.argv:
    pattern_action_pair_list = [
        ('long-way-back/x+/y', "LONG WAY BACK / X+ / Y"),
        ('x+',                 "X+"),
        ('y+',                 "Y+"),
        ('[longwayback\-]',    "LETTER")
    ]
    test_str_list = ["xylong-way-back", "long-way-backxy", "xylong-way-back", "long-way-backxy"]
    lexeme_size = 2

if "dtc-l2" in sys.argv:
    pattern_action_pair_list = [
        ('[ ]+/x+/x', "WHITESPACE / X+ / X"),
        ('x+',        "X+"),
        ('[ ]',       "WHITESPACE")
    ]
    test_str_list = ["xx ", " xx", "xx    ", "     xx", "xx xx  xx   xx    xx"]
    lexeme_size = 2

if "dtc-l3" in sys.argv:
    pattern_action_pair_list = [
        ('[ ]+/x+/x', "WHITESPACE / X+ / X"),
        ('x+',        "X+"),
        ('[ ]',       "WHITESPACE")
    ]
    test_str_list = ["xxx ", " xxx", "xxx    ", "     xxx", "xxx xxx  xxx   xxx    xxx"]
    lexeme_size = 3

if "dtc-long-way-back" in sys.argv:
    pattern_action_pair_list = [
        ('long-way-back/x+/x', "LONG WAY BACK / X+ / X"),
        ('x+',                "X+"),
        ('[longwayback\-]',   "LETTER")
    ]
    test_str_list = ["xxlong-way-back", "long-way-backxx", "xxlong-way-back", "long-way-backxx"]
    lexeme_size = 2

# Minimal buffer size:   lexeme size 
#                      + 1 lexatom to detect end 
#                      + 2 border lexatoms of buffer
generator_test.do(pattern_action_pair_list, test_str_list, {}, "ANSI-C",
                  QuexBufferSize=lexeme_size + 3)    
