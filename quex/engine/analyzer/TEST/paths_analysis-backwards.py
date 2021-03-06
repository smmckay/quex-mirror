#! /usr/bin/env python
# -*- coding: utf8 -*-
import os
import sys
sys.path.insert(0, os.environ["QUEX_PATH"])

import quex.input.regular_expression.engine  as regex
import quex.engine.analyzer.engine_supply_factory as     engine
from   quex.constants                            import E_InputActions
import help

if "--hwut-info" in sys.argv:
    print "Track Analyzis: Backwards - For Pre-Context;"
    print "CHOICES: 0, 1;"
    sys.exit()

if "0" in sys.argv:
    pattern_list = [
        'x/a/',        
        'y/a/',     
    ]
elif "1" in sys.argv:
    pattern_list = [
        'x+/a/',        
        'yx+/a/',     
    ]
else:
    assert False

sm = help.prepare(pattern_list, GetPreContextSM_F=True)

# For DEBUG purposes: specify 'DRAW' on command line
help.if_DRAW_in_sys_argv(sm)
help.test(sm, EngineType=engine.BACKWARD_PRE_CONTEXT)
