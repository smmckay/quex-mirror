#! /usr/bin/env python
# -*- coding: utf8 -*-
# 
# 'shared_tail.get(A, B)' identifies commands from A and B which can be
# combined into an appended shared tail. 
#
# The main part of the function is done in 'can_be_moved_to_tail()' and
# 'find_last_common()'. Those two functions are tested in dedicated tests.
#
#  => No need to test:
#       if the last common is found correctly.
#       if the command is judged as being moveable to the tail.
#
#  => Test, if the tail is extracted correctly, that is:
#       All tail-commands: (1) appear in the tail,
#                          (2) in their propper sequence.
#
# (C) Frank-Rene Schaefer
#______________________________________________________________________________

import os 
import sys 
sys.path.insert(0, os.environ["QUEX_PATH"])

from   quex.constants                             import E_Op
from   quex.engine.operations.operation_list         import *
import quex.engine.operations.shared_tail  as     shared_tail
from   quex.engine.operations.TEST.helper  import *
from   quex.engine.analyzer.door_id_address_label import DoorID

from   collections import defaultdict
from   itertools   import izip, permutations
from   copy        import deepcopy

if "--hwut-info" in sys.argv:
    print "Op.shared_tail: find_last_common;"
    print "CHOICES: one-or-none, two, two-bad, multiple;"
    sys.exit()

A = Op.Assign(E_R.LoopRestartP,  E_R.Input)
B = Op.Assign(E_R.LoopRestartP,  E_R.LexemeEnd)
C = Op.Assign(E_R.LoopRestartP,  E_R.Line)
D = Op.Assign(E_R.TemplateStateKey, E_R.Line)

x = [ remaining for i, remaining in generator() if remaining not in (A, B, C) ]
x[2] = Op.ColumnCountAdd(1)
x[3] = Op.ColumnCountGridAdd(1)


def print_tail_vs_cmd_list(CutList, OpList):
    t = 0
    for i, cmd in enumerate(OpList):
        if i in CutList: label = "<%i>" % t; t += 1
        else:            label = "   "
        print "   %s %s" % (label, str(cmd))

def test(Cl0, Cl1):
    result, x_cut_list, y_cut_list = shared_tail.get(Cl0, Cl1)
    if result is None: result = (); x_cut_list = y_cut_list = []
    assert len(x_cut_list) == len(y_cut_list) == len(result)
    assert set(result) == set(Cl0[i] for i in reversed(x_cut_list))
    assert set(result) == set(Cl1[k] for k in reversed(y_cut_list))
    print
    print "_" * 80
    print "tail(A, B): {"
    print_tail_vs_cmd_list(x_cut_list, Cl0)
    print "   - - - - - - "
    print_tail_vs_cmd_list(y_cut_list, Cl1)
    print "}"

    iresult, ix_cut_list, iy_cut_list = shared_tail.get(Cl1, Cl0)
    if iresult is None: iresult = (); ix_cut_list = iy_cut_list = []
    assert len(ix_cut_list) == len(iy_cut_list) == len(result)
    assert set(iresult) == set(Cl1[i] for i in reversed(ix_cut_list))
    assert set(iresult) == set(Cl0[k] for k in reversed(iy_cut_list))
    assert set(result) == set(iresult)

    print "tail(B, A): {"
    if ix_cut_list != y_cut_list or iy_cut_list != x_cut_list:
        # Print error case
        print_tail_vs_cmd_list(ix_cut_list, Cl0)
        print "   - - - - - - "
        print_tail_vs_cmd_list(iy_cut_list, Cl1)

    print "    %s x same" % len(result)
    print "}"

if "one-or-none" in sys.argv:
    test([], [])
    test([ A ], [])
    test([ A ], [ A ])
    test([ A ], [ B ])
    test([ A ], [ x[0], x[1] ])
    test([ A ], [ x[0], A, x[1] ])
    test([ A ], [ x[0], B, x[1] ])
    test([ x[2], A, x[3] ], [ x[0], x[1] ])
    test([ x[2], A, x[3] ], [ x[0], A, x[1] ])
    test([ x[2], A, x[3] ], [ x[0], B, x[1] ])
elif "two" in sys.argv:
    test([ A, D ], [ D, A ])
    test([ A, B ], [ A, B ])
    test([ A, B ], [ A, B, x[0] ])
    test([ A, B ], [ A, x[0], B ])
    test([ A, B ], [ x[0], A, B ])
    test([ A, B ], [ x[0], A, x[1], B, x[2] ])

elif "two-bad" in sys.argv:
    test([ B, A ], [ A, B ])
    test([ B, A ], [ A, B, x[0] ])
    test([ B, A ], [ A, x[0], B ])
    test([ B, A ], [ x[0], A, B ])
    test([ B, A ], [ x[0], A, x[1], B, x[2] ])

elif "multiple" in sys.argv:
    A = Op.Assign(E_R.Line,            E_R.Input)
    B = Op.Assign(E_R.Column,          E_R.LexemeEnd)
    C = Op.Assign(E_R.LoopRestartP, E_R.LoopRestartP)

    test([ A, A, B ],    [ A ])
    test([ A, A, B ],    [ A, B ])
    test([ A, A, B, B ], [ A, B ])
    test([ A, A, B, B ], [ A, B, B ])
    test([ A, A, B ],    [ A, x[0] ])
    test([ A, A, B ],    [ A, x[0], B ])
    test([ A, A, B, B ], [ A, x[0], B ])
    test([ A, A, B, B ], [ A, x[0], B, B ])
    test([ A, x[1], A, x[2], B, x[1] ],    [ A, x[0] ])
    test([ A, x[1], A, x[2], B, x[1] ],    [ A, x[0], B ])
    test([ A, x[1], A, x[2], B, x[1], B ], [ A, x[0], B ])
    test([ A, x[1], A, x[2], B, x[1], B ], [ A, x[0], B, B ])

