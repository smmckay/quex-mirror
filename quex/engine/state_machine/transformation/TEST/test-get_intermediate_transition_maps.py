#! /usr/bin/env python
#
# TESTS: The function '__get_intermediate_transition_maps()' 
#
# Given a list of interval sequences a bunch of intermediate states is to be
# determined to be inserted in between 'FromSi' and 'ToSi'. That is, the 
# transitions in there shall replace the original transition.
#
# This test does not check '__bunch_iterable()', i.e. it does not verify
# where sub-sequences are well-distinguished (a sperate UT exists for that).
#
# CHOICES: 1, 2, 3, 4 -- according to the number of sequences involved.
#               
# (C) Frank-Rene Schaefer
#______________________________________________________________________________
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])

from   quex.engine.misc.interval_handling                   import Interval
from   quex.engine.state_machine.transformation.state_split import __get_intermediate_transition_maps
import quex.engine.state_machine.algorithm.beautifier       as     beautifier

from   quex.blackboard import setup as Setup

Setup.bad_lexatom_detection_f = False

if "--hwut-info" in sys.argv:
    print "Interval Sequences: Iterate over bunches;"
    print "CHOICES: 1, 2, 3, 4;"
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

    for raw_sequence in Input:
        interval_sequence_list.append(
            [ Interval(x, y+1) for x, y in raw_sequence ]
        )

    from_si = 66L
    to_si   = 77L

    tm_db,      \
    tm_end_inv, \
    position_db =  __get_intermediate_transition_maps(from_si, to_si, 
                                                      interval_sequence_list)

    # Insert the 'inverse end transition map' into the 'tm_db'.
    for from_state_index, interval_list in tm_end_inv.iteritems():
        assert to_si not in tm_db[from_state_index]
        tm_db[from_state_index] [to_si] = interval_list

    print
    print "Result:"

    worklist = [ from_si ]
    done     = set([to_si])
    while worklist:
        si = worklist.pop()
        tm = tm_db.pop(si)
        done.add(si)
        for target_si, interval_list in sorted(tm.iteritems()):
            if target_si not in done: worklist.append(target_si)
            if si        == from_si: si        = "B"
            if target_si == to_si:   target_si = "E"
            print "   (%s)-- %s -->(%s)" % (si, interval_list, target_si)

    
    print

if "1" in sys.argv:
    isl = [
        [ (0, 1), ]
    ]
    test(isl)

    isl = [
        [ (0, 1), (0, 1), ],  
    ]
    test(isl)

    isl = [
        [ (0, 1), (0, 1), (0, 1) ],  
    ]
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
        [ (0, 1), (0, 1), (0, 1), ],  
        [ (0, 1), (0, 1), (0, 2), ], 
    ]
    test(isl)

elif "3" in sys.argv:
    isl = [
        [ (0, 1), ],  
        [ (0, 2), ], 
        [ (0, 3), ], 
    ]
    test(isl)

    isl = [
        [ (0, 1), (0, 1) ],  
        [ (0, 2), ], 
        [ (0, 3), ], 
    ]
    test(isl)

    isl = [
        [ (0, 1), (0, 1) ],  
        [ (0, 2), (0, 2) ], 
        [ (0, 3), (0, 3) ], 
    ]
    test(isl)

    isl = [
        [ (0, 1), (0, 1) ],  
        [ (0, 1), (0, 2) ], 
        [ (0, 3), (0, 3) ], 
    ]
    test(isl)

    isl = [
        [ (0, 1), (0, 1) ],  
        [ (0, 1), (0, 2), (0, 2) ], 
        [ (0, 3), (0, 3) ], 
    ]
    test(isl)

elif "4" in sys.argv:
    isl = [
        [ (0, 1), (0, 1), (0, 1), ],  
        [ (0, 1), (0, 1), (0, 2), ], 
        [ (0, 1), (0, 1), (0, 3), ], 
        [ (0, 1), (0, 1), (0, 4), ], 
    ]
    test(isl, 2)

    isl = [
        [ (0, 1), (0, 2), (0, 1), ],  
        [ (0, 1), (0, 2), (0, 1), ], 
        [ (0, 1), (0, 3), (0, 1), ], 
        [ (0, 1), (0, 3), (0, 1), ], 
    ]
    test(isl, 2)

    isl = [
        [ (0, 1), (0, 2), (0, 1), ],  
        [ (0, 1), (0, 2), (0, 1), ], 
        [ (0, 1), (0, 3), (0, 1), ], 
        [ (0, 1), (0, 3), (0, 1), ], 
    ]
    test(isl, 2)

    isl = [
        [ (0, 1), (0, 1), (0, 1), ],  
        [ (0, 2), (0, 1), (0, 1), ], 
        [ (0, 3), (0, 1), (0, 1), ], 
        [ (0, 4), (0, 1), (0, 1), ], 
    ]
    test(isl, 2)

