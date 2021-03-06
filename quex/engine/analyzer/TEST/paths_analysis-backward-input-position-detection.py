#! /usr/bin/env python
# -*- coding: utf8 -*-
import os
import sys
sys.path.insert(0, os.environ["QUEX_PATH"])

import quex.input.regular_expression.engine  as regex
import quex.engine.state_machine.construction.combination             as     combination
import quex.engine.analyzer.engine_supply_factory      as     engine
from   quex.constants                       import E_InputActions
import help

from   operator import attrgetter

if "--hwut-info" in sys.argv:
    print "Track Analyzis: Backward Input Position Detection;"
    sys.exit()

# There are no 'special cases'
pattern_list = [
    'ax',        
]

state_machine_list = map(lambda x: regex.do(x, {}).extract_sm(), pattern_list)
sm                 = combination.do(state_machine_list, False) # May be 'True' later.
sm                 = sm.normalized_clone()

# For DEBUG purposes: specify 'DRAW' on command line (in sys.argv)
help.if_DRAW_in_sys_argv(sm)
help.test(sm, engine.Class_BACKWARD_INPUT_POSITION(0))

