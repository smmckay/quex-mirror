#! /usr/bin/env python
#
# TESTS: The function '__bunch_iterable()' which iteraters over groups of
#        sequence list with the same interval at a specific position.
#
# Entry comment of this function or the function 'plug_interval_sequence()' is
# very instructive.
#
# CHOICES:
#
#     1 -- Tests with only one interval sequence, trivial but must also work.
#
#     2 -- Tests with only two interval sequences focussing on index == 0.
#          Sub tests vary in that the interval at index is same or different
#          as well as the length of the related sequences.
#
#     3 -- Tests with three intervals. All combinations are permuated, that is:
#          (1) all different
#          (2) first two same
#          (3) last two same
#          (4) all same
#          The length of the sequences is no longer considered.
#
#     index -- Tests with indices > 0
#
#     limit -- Tests with sequences that are shorter than 'index+1'
#               
# (C) Frank-Rene Schaefer
#______________________________________________________________________________
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])

from   quex.engine.misc.interval_handling                   import Interval
from   quex.engine.state_machine.transformation.state_split import __bunch_iterable as bunch_iterable
import quex.engine.state_machine.algorithm.beautifier       as     beautifier

from   quex.blackboard import setup as Setup

Setup.bad_lexatom_detection_f = False

if "--hwut-info" in sys.argv:
    print "Interval Sequences: Iterate over bunches;"
    print "CHOICES: 1, 2, 3, index, limit;"
    sys.exit(0)

test_i = -1
def test(Input, Index=0):
    global test_i
    test_i += 1

    print "--( %i )-------------------------------------------------------" % test_i
    print
    interval_sequence_list = []
    for raw_sequence in Input:
        print "  ", raw_sequence

    print
    print "( Groups: index = %i)" % Index
    print
    for raw_sequence in Input:
        interval_sequence_list.append(
            [ Interval(x, y+1) for x, y in raw_sequence ]
        )

    for interval, sub_group, last_f in bunch_iterable(interval_sequence_list, Index):
        print
        if last_f: print "   -- Same ", interval, "(terminal)"
        else:      print "   -- Same ", interval
        for sequence in sub_group:
            print "  ", sequence

if "1" in sys.argv:
    isl = [
        [ (0, 1), ]
    ]
    test(isl)

    isl = [
        [ (0, 1), (0, 1), (0, 1), ],  
    ]
    for index in range(3):
        test(isl)
elif "2" in sys.argv:
    isl = [
        [ (0, 1), ],  
        [ (0, 1), ], 
    ]
    test(isl)

    isl = [
        [ (0, 1), ],  
        [ (0, 2), ], 
    ]
    test(isl)

    isl = [
        [ (0, 1), (0, 1), ],  
        [ (0, 1), (0, 1), ], 
    ]
    test(isl)

    isl = [
        [ (0, 1), (0, 1), ],  
        [ (0, 1), (0, 2), ], 
    ]
    test(isl)

    isl = [
        [ (0, 1), (0, 1), ],  
        [ (0, 2), (0, 1), ], 
    ]
    test(isl)

    isl = [
        [ (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), ],  
        [ (0, 2), (0, 1), (0, 2), (0, 1), (0, 2), (0, 1), (0, 2), (0, 1), (0, 2), (0, 1), (0, 2), (0, 1), ], 
    ]
    test(isl)

elif "3" in sys.argv:
    isl = [
        [ (0, 1), ],  
        [ (0, 1), ], 
        [ (0, 1), ], 
    ]
    test(isl)

    isl = [
        [ (0, 1), ],  
        [ (0, 1), ], 
        [ (0, 2), ], 
    ]
    test(isl)

    isl = [
        [ (0, 1), ],  
        [ (0, 2), ], 
        [ (0, 2), ], 
    ]
    test(isl)

    isl = [
        [ (0, 1), ],  
        [ (0, 2), ], 
        [ (0, 3), ], 
    ]
    test(isl)

elif "index" in sys.argv:
    isl = [
        [ (0, 1), (0, 2), (0, 3), ],  
        [ (0, 1), (0, 2), (0, 3), ], 
        [ (0, 1), (0, 3), (0, 3), ], 
        [ (0, 1), (0, 3), (0, 3), ], 
    ]
    test(isl, 1)

    isl = [
        [ (0, 1), (0, 3), (0, 2), ],  
        [ (0, 1), (0, 3), (0, 2), ], 
        [ (0, 1), (0, 3), (0, 3), ], 
        [ (0, 1), (0, 3), (0, 3), ], 
    ]
    test(isl, 2)

elif "limit" in sys.argv:
    isl = [
        [ (0, 1), (0, 2), (0, 3), ],  
        [ (0, 1), (0, 2),         ], 
        [ (0, 1),                 ], 
    ]
    test(isl)
    isl = [
        [ (0, 1), (0, 2), (0, 2), (0, 3), ],  
        [ (0, 1), (0, 2), (0, 2),         ], 
        [ (0, 1), (0, 2),                 ], 
    ]
    test(isl, 1)
