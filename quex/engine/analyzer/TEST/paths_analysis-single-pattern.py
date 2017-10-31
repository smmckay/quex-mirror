#! /usr/bin/env python
# -*- coding: utf8 -*-
import os
import sys
sys.path.insert(0, "./")
from   track_analysis_single_pattern                   import choice_str, pattern_db, choice
import quex.engine.state_machine.cut.stem_and_branches as     stem_and_branches
import help

if "--hwut-info" in sys.argv:
    print "Paths Analysis: Single Pattern;"
    print choice_str
    sys.exit()

stem_and_branches._unit_test_deactivate_branch_pruning_f = True

sm = help.prepare(pattern_db[choice])

# For DEBUG purposes: specify 'DRAW' on command line
help.if_DRAW_in_sys_argv(sm)
help.test(sm)

