#! /usr/bin/env python
# -*- coding: utf8 -*-
import os
import sys
sys.path.insert(0, os.environ["QUEX_PATH"])

from   quex.engine.misc.interval_handling       import Interval
from   quex.engine.analyzer.transition_map import TransitionMap
from   quex.constant import INTEGER_MAX
from   copy import deepcopy
from   itertools import islice

if "--hwut-info" in sys.argv:
    print "Transition Map Tools: prune;"
    print "CHOICES: 1, 2, 3;"
    sys.exit()

B = 15

def construct_tm(IntervalList):
    letter = ord('a')

    return TransitionMap.from_iterable([ 
       (Interval(x[0], x[1]), letter + i) 
       for i, x in enumerate(IntervalList) 
    ])

def get_borders(IntervalList):
    def add(border_set, X):
        if X != -INTEGER_MAX: border_set.add(X - 1)
        if X !=  INTEGER_MAX: border_set.add(X + 1)
        border_set.add(X)

    border_set = set([-INTEGER_MAX, INTEGER_MAX])
    for begin, end in IntervalList:
        add(border_set, begin)
        add(border_set, end)
        if end - begin < 100:
            add(border_set, int((begin + end) / 2))

    border_list = sorted(list(border_set))
    
    return border_list

def iterate(TM, BorderList):
    for i, begin in enumerate(BorderList):
        for end in islice(BorderList, i, None):
            show_pruner(begin, end)
            dummy = deepcopy(TM)
            dummy.prune(begin, end)
            show_tm(dummy)

def stringey(Value):
    if   Value == -INTEGER_MAX:     return "-oo"
    elif Value == -INTEGER_MAX + 1: return "-oo+1"
    elif Value == INTEGER_MAX:      return "oo"
    elif Value == INTEGER_MAX - 1:  return "+oo-1"
    else:                          return "%s" % Value

def nicey(Value):
    if   Value == -INTEGER_MAX:   return -20
    elif Value < -19:            return -19
    elif Value ==  INTEGER_MAX:   return  20
    elif Value > 19:             return  19
    else:                        return Value
   
def show_scale():
    global B
    print " " * B + "-oo       -10        0         10        oo "
    print " " * B + " |         |         |         |         |  " 
    print " " * B + " *- - -----+---------+---------+----- - -*  "

def show_tm(TM):
    global B
    if len(TM) == 0:
        print " " * B + "                    < >"
        return

    x_iterable = [-INTEGER_MAX, -INTEGER_MAX+1] \
                 + range(-18, 19)             \
                 + [INTEGER_MAX-1, INTEGER_MAX]
    L          = len(TM)
    txt        = [" " * (B+1)]
    target     = None
    current_i  = 0
    for x in x_iterable:
        while 1 + 1 == 2:
            if TM[current_i][0].begin == x: 
                target = TM[current_i][1]

            if TM[current_i][0].end == x: 
                target     = None 
                current_i += 1
                if current_i == L: break
                continue
            break
        if current_i == L: break

        if target is None: txt.append(" ")
        else:              txt.append("%c" % chr(target))

    print "".join(txt)

def show_pruner(Begin, End):
    begin_str = stringey(Begin)
    end_str   = stringey(End)
    Begin = nicey(Begin)
    End   = nicey(End)
    assert End - Begin < 100
    s0 = " " * (Begin + 20)
    s1 = " " * (End - Begin - 1)
    if Begin == End:
        txt = "%s|" % s0
    else:
        txt = "%s[%s)" % (s0, s1)
    info_txt = "[%s, %s)" % (begin_str, end_str)
    print "%s %s%s" % (info_txt, " " * (B - len(info_txt)), txt)

def test(*IntervalList):
    tm          = construct_tm(IntervalList)
    border_list = get_borders(IntervalList)

    show_scale()
    print "original:"
    show_tm(tm)
    iterate(tm, border_list)

if   "1" in sys.argv:
    test((-5,6))
    test((-INTEGER_MAX,0))
    test((0,1))
    test((0,INTEGER_MAX))
    test((-INTEGER_MAX,INTEGER_MAX))

elif "2" in sys.argv:
    test((0, 6),           (6, 12))
    test((0, 5),           (6, 11))
    test((0, 4),           (8, 12))
    test((-INTEGER_MAX, 6), (6, 12))
    test((-INTEGER_MAX, 5), (6, 11))
    test((0, 6),           (6, INTEGER_MAX))
    test((0, 5),           (6, INTEGER_MAX))

elif "3" in sys.argv:
    test((-1,0),   (0, 1), (1, 2))
    test((-2,-1),  (0, 1), (1, 2))
    test((-2,0),   (0, 1), (2, 3))
    test((-2,-1),  (0, 1), (2, 3))

sys.exit()

def show(TM):
    txt = TM.get_string(Option="dec")
    txt = txt.replace("%s" % -INTEGER_MAX, "-oo")
    txt = txt.replace("%s" % (INTEGER_MAX-1), "oo")
    print txt

def test(TM, Target="X"):
    tm = [ (Interval(x[0], x[1]), y) for x, y in TM ]
    print "____________________________________________________________________"
    range_list = [
        (-INTEGER_MAX, INTEGER_MAX),
        (-INTEGER_MAX, 10),
        (-INTEGER_MAX, 1),
        (-INTEGER_MAX, 0),
        (-INTEGER_MAX, -INTEGER_MAX),

        (0, INTEGER_MAX),
        (0, 10),
        (0, 1),
        (0, 0),

        (1, INTEGER_MAX),
        (1, 10),
        (1, 1),

        (10, INTEGER_MAX),
        (10, 10),

        (INTEGER_MAX, INTEGER_MAX),
    ]

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




