#! /usr/bin/env python
# -*- coding: utf8 -*-
import os
import sys
sys.path.insert(0, os.environ["QUEX_PATH"])

from   quex.engine.misc.interval_handling       import Interval
import quex.engine.analyzer.transition_map as     transition_map_tools
from   quex.engine.analyzer.transition_map import TransitionMap
from   quex.constants import INTEGER_MAX
from   copy import deepcopy

if "--hwut-info" in sys.argv:
    print "Transition Map Tools: combine_adjacent;"
    print "CHOICES: 1, 2-same, 2-diff, 3-same, 3-diff;"
    sys.exit()


def show(TM):
    txt = TM.get_string(Option="dec")
    txt = txt.replace("%s" % -INTEGER_MAX, "-oo")
    txt = txt.replace("%s" % (INTEGER_MAX-1), "oo")
    print txt

def test(TM, Target="X"):
    tm = TransitionMap.from_iterable([ (Interval(x[0], x[1]), y) for x, y in TM ])
    print "____________________________________________________________________"
    print "BEFORE:"
    show(tm)
    tm.combine_adjacents()
    tm.assert_continuity(StrictF=True)
    print "AFTER:"
    show(tm)

#test([((0, 1),           "1"), ((10, 11),        "2")], "1")
#sys.exit()

if "1" in sys.argv:
    test([((0, 1),                    "1")])
    test([((-INTEGER_MAX, 1),          "1")])
    test([((0, INTEGER_MAX),           "1")])
    test([((-INTEGER_MAX, INTEGER_MAX), "1")])

    print "# Required: Smoothing ______________________________________________"
    test([((0, 1),                    "1")], "1")
    test([((-INTEGER_MAX, 1),          "1")], "1")
    test([((0, INTEGER_MAX),           "1")], "1")
    test([((-INTEGER_MAX, INTEGER_MAX), "1")], "1")

elif "2-same" in sys.argv:

    test([((0, 1),           "1"), ((10, 11),        "1")])
    test([((0, 1),           "1"), ((1, 2),          "1")])
    test([((-INTEGER_MAX, 1), "1"), ((10, 11),        "1")])
    test([((0, 1),           "1"), ((1, INTEGER_MAX), "1")])
    test([((-INTEGER_MAX, 1), "1"), ((1, INTEGER_MAX), "1")])

    print "# Required: Smoothing ______________________________________________"
    test([((0, 1),           "1"), ((10, 11),        "1")], "1")
    test([((0, 1),           "1"), ((1, 2),          "1")], "1")
    test([((-INTEGER_MAX, 1), "1"), ((10, 11),        "1")], "1")
    test([((0, 1),           "1"), ((1, INTEGER_MAX), "1")], "1")
    test([((-INTEGER_MAX, 1), "1"), ((1, INTEGER_MAX), "1")], "1")

elif "2-diff" in sys.argv:

    test([((0, 1),           "1"), ((10, 11),        "2")])
    test([((0, 1),           "1"), ((1, 2),          "2")])
    test([((-INTEGER_MAX, 1), "1"), ((10, 11),        "2")])
    test([((0, 1),           "1"), ((1, INTEGER_MAX), "2")])
    test([((-INTEGER_MAX, 1), "1"), ((1, INTEGER_MAX), "2")])

    print "# Required: Smoothing ______________________________________________"
    test([((0, 1),           "1"), ((10, 11),        "2")], "1")
    test([((0, 1),           "1"), ((1, 2),          "2")], "1")
    test([((-INTEGER_MAX, 1), "1"), ((10, 11),        "2")], "1")
    test([((0, 1),           "1"), ((1, INTEGER_MAX), "2")], "1")
    test([((-INTEGER_MAX, 1), "1"), ((1, INTEGER_MAX), "2")], "1")

    test([((0, 1),           "1"), ((10, 11),        "2")], "2")
    test([((0, 1),           "1"), ((1, 2),          "2")], "2")
    test([((-INTEGER_MAX, 1), "1"), ((10, 11),        "2")], "2")
    test([((0, 1),           "1"), ((1, INTEGER_MAX), "2")], "2")
    test([((-INTEGER_MAX, 1), "1"), ((1, INTEGER_MAX), "2")], "2")

elif "3-same" in sys.argv:

    test([((0, 1),           "1"), ((5, 6),          "1"), ((10, 11),        "1")])
    test([((0, 1),           "1"), ((1, 2),          "1"), ((10, 11),        "1")])
    test([((0, 1),           "1"), ((9, 10),         "1"), ((10, 11),        "1")])
    test([((0, 1),           "1"), ((1, 2),          "1"), ((2, 4),          "1")])

    test([((-INTEGER_MAX, 1), "1"), ((5, 6),          "1"), ((10, 11),         "1")])
    test([((0, 1),           "1"), ((5, 6),          "1"), ((10, INTEGER_MAX), "1")])

    test([((-INTEGER_MAX, 1), "1"), ((5, 6),          "1"), ((10, INTEGER_MAX), "1")])
    test([((-INTEGER_MAX, 1), "1"), ((1, 2),          "1"), ((10, INTEGER_MAX), "1")])
    test([((-INTEGER_MAX, 1), "1"), ((9, 10),         "1"), ((10, INTEGER_MAX), "1")])
    test([((-INTEGER_MAX, 1), "1"), ((1, 2),          "1"), ((2,  INTEGER_MAX), "1")])

    print "# Required: Smoothing ______________________________________________"
    test([((0, 1),           "1"), ((5, 6),          "1"), ((10, 11),        "1")], "1")
    test([((0, 1),           "1"), ((1, 2),          "1"), ((10, 11),        "1")], "1")
    test([((0, 1),           "1"), ((9, 10),         "1"), ((10, 11),        "1")], "1")
    test([((0, 1),           "1"), ((1, 2),          "1"), ((2, 4),          "1")], "1")

    test([((-INTEGER_MAX, 1), "1"), ((5, 6),          "1"), ((10, 11),         "1")], "1")
    test([((0, 1),           "1"), ((5, 6),          "1"), ((10, INTEGER_MAX), "1")], "1")

    test([((-INTEGER_MAX, 1), "1"), ((5, 6),          "1"), ((10, INTEGER_MAX), "1")], "1")
    test([((-INTEGER_MAX, 1), "1"), ((1, 2),          "1"), ((10, INTEGER_MAX), "1")], "1")
    test([((-INTEGER_MAX, 1), "1"), ((9, 10),         "1"), ((10, INTEGER_MAX), "1")], "1")
    test([((-INTEGER_MAX, 1), "1"), ((1, 2),          "1"), ((2,  INTEGER_MAX), "1")], "1")


elif "3-diff" in sys.argv:

    test([((0, 1),           "1"), ((5, 6),          "2"), ((10, 11),        "1")])
    test([((0, 1),           "1"), ((1, 2),          "2"), ((10, 11),        "1")])
    test([((0, 1),           "1"), ((9, 10),         "2"), ((10, 11),        "1")])
    test([((0, 1),           "1"), ((1, 2),          "2"), ((2, 4),          "1")])

    test([((-INTEGER_MAX, 1), "1"), ((5, 6),          "2"), ((10, 11),         "1")])
    test([((0, 1),           "1"), ((5, 6),          "2"), ((10, INTEGER_MAX), "1")])

    test([((-INTEGER_MAX, 1), "1"), ((5, 6),          "2"), ((10, INTEGER_MAX), "1")])
    test([((-INTEGER_MAX, 1), "1"), ((1, 2),          "2"), ((10, INTEGER_MAX), "1")])
    test([((-INTEGER_MAX, 1), "1"), ((9, 10),         "2"), ((10, INTEGER_MAX), "1")])
    test([((-INTEGER_MAX, 1), "1"), ((1, 2),          "2"), ((2,  INTEGER_MAX), "1")])

    print "# Required: Smoothing ______________________________________________"
    print "# --> 1"
    test([((0, 1),           "1"), ((5, 6),          "2"), ((10, 11),        "1")], "1")
    test([((0, 1),           "1"), ((1, 2),          "2"), ((10, 11),        "1")], "1")
    test([((0, 1),           "1"), ((9, 10),         "2"), ((10, 11),        "1")], "1")
    test([((0, 1),           "1"), ((1, 2),          "2"), ((2, 4),          "1")], "1")

    test([((-INTEGER_MAX, 1), "1"), ((5, 6),          "2"), ((10, 11),         "1")], "1")
    test([((0, 1),           "1"), ((5, 6),          "2"), ((10, INTEGER_MAX), "1")], "1")

    test([((-INTEGER_MAX, 1), "1"), ((5, 6),          "2"), ((10, INTEGER_MAX), "1")], "1")
    test([((-INTEGER_MAX, 1), "1"), ((1, 2),          "2"), ((10, INTEGER_MAX), "1")], "1")
    test([((-INTEGER_MAX, 1), "1"), ((9, 10),         "2"), ((10, INTEGER_MAX), "1")], "1")
    test([((-INTEGER_MAX, 1), "1"), ((1, 2),          "2"), ((2,  INTEGER_MAX), "1")], "1")

    print "# --> 2"
    test([((0, 1),           "1"), ((5, 6),          "2"), ((10, 11),        "1")], "2")
    test([((0, 1),           "1"), ((1, 2),          "2"), ((10, 11),        "1")], "2")
    test([((0, 1),           "1"), ((9, 10),         "2"), ((10, 11),        "1")], "2")
    test([((0, 1),           "1"), ((1, 2),          "2"), ((2, 4),          "1")], "2")

    test([((-INTEGER_MAX, 1), "1"), ((5, 6),          "2"), ((10, 11),         "1")], "2")
    test([((0, 1),           "1"), ((5, 6),          "2"), ((10, INTEGER_MAX), "1")], "2")

    test([((-INTEGER_MAX, 1), "1"), ((5, 6),          "2"), ((10, INTEGER_MAX), "1")], "2")
    test([((-INTEGER_MAX, 1), "1"), ((1, 2),          "2"), ((10, INTEGER_MAX), "1")], "2")
    test([((-INTEGER_MAX, 1), "1"), ((9, 10),         "2"), ((10, INTEGER_MAX), "1")], "2")
    test([((-INTEGER_MAX, 1), "1"), ((1, 2),          "2"), ((2,  INTEGER_MAX), "1")], "2")




