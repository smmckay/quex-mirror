#! /usr/bin/env python
#
# PURPOSE:
# 
# This file performs four examplatory tests of state combination:
#
#    (1)  FSM_State + FSM_State -> TemplateState
#    (2)  FSM_State + FSM_State -> TemplateState
#    (3)  TemplateState + TemplateState -> TemplateState
#    (4)  TemplateState + FSM_State -> TemplateState
#
# As a starting point a list of five states is generated. All states only 
# transit one transition on the number '10' to a target state. Depending on the
# CHOICE the target states are
#
#   'plain'         -- state '1'.
#   'recursive'     -- the states themselves. 
#   'distinguished' -- some states '1000 + i'.
#     
# This test executes the combinations mentioned in (1) to (4) and prints
# the resulting TemplateStates. 
#
# Process: (1) FSM_State-s from transition maps.
#          (2) PseudoTemplateState-s from FSM_State-s.
#          (3) TemplateStateCandidate from two PseudoTemplateState-s.
#          (4) TemplateState from TemplateStateCandidate
#
# The template combination process operates solely on 'template states'. 
# Thus, FSM_State-s need to be first translated into PseudoTemplateState.
# A TemplateStateCandidate references two states to be combined. The 
# TemplateState constructor takes a TemplateStateCandidate to when constructing
# a new template state.
#
# NOTE: Recursion is not considered during measurement. See note in README.txt.
#
# (C) Frank-Rene Schaefer
#______________________________________________________________________________
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])

import quex.engine.state_machine.index                             as index
from   quex.engine.analyzer.mega_state.template.TEST.templates_aux import *

from   quex.engine.misc.interval_handling import *
from   quex.constants                import E_StateIndices


if "--hwut-info" in sys.argv:
    print "Combine Simple"
    print "CHOICES: plain, recursive, distinguished;"
    sys.exit(0)

if "plain" in sys.argv:
    def transition_map_for_state(i):
        return [ (Interval(10), 100L) ]

elif "recursive" in sys.argv:
    def transition_map_for_state(i):
        return [ (Interval(10), long(i)) ]

elif "distinguished" in sys.argv:
    def transition_map_for_state(i):
        return [ (Interval(10), long(1000 + i)) ]

# FSM_State-s: The base.
analyzer = get_Analyzer( 
    [ 
        # (StateIndex, TransitionMap)
        (long(i), transition_map_for_state(long(i))) 
        for i in xrange(5)
    ]
)

s = [ analyzer.state_db[i] for i in xrange(5) ]

# (1) FSM + FSM -> Template
t01     = combine(analyzer, s[0], s[1], "0", "1")
# (2) FSM + FSM -> Template
t23     = combine(analyzer, s[2], s[3], "2", "3")
# (3) Template + Template -> FSM
t0123   = combine(analyzer, t01, t23, "t(01)", "t(23)")
# (4) Template + FSM -> FSM
t0123_4 = combine(analyzer, t0123, s[4], "t(0123)", "4") 

