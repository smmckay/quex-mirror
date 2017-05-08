#! /usr/bin/env python
#
# TEST: Mounting of DFA-s in parallel / Check on traced original state machines.
#
# Original state machines are identified via the acceptance id in the acceptance
# states.
#
# Some example state machines are 'parallelize-d'. Most importantly, the result
# is checked against two criteria:
#
#        (1) It matches a superset of every single state machine.
#        (2) The complement result does not have anything in common with 
#            any single state machine.
#______________________________________________________________________________
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])


from   quex.engine.state_machine.core import *
import quex.engine.state_machine.construction.parallelize as     parallelize 
from   quex.engine.state_machine.TEST.test_state_machines import *
import quex.engine.state_machine.check.superset           as     superset
import quex.engine.state_machine.algebra.intersection     as     intersection
import quex.engine.state_machine.algebra.complement       as     complement

if "--hwut-info" in sys.argv:
    print "Tracing origin: Paralellization"
    sys.exit(0)

out_n = 0
def output(Sm):
    global out_n
    if "help" not in sys.argv: 
        print "sm%i: %s" % (out_n, Sm)
    else:                     
        open("tmp%i.dot" % out_n, "wb").write(Sm.get_graphviz_string(NormalizeF=True))
        print "written 'tmp%i.dot'" % out_n
    out_n += 1

sm0.mark_state_origins()    
sm1.mark_state_origins()    
sm2.mark_state_origins()    

output(sm0)
output(sm1)
output(sm2)
sm_list = [sm0, sm1, sm2]
sm = parallelize.do(sm_list) 

print "#-------------------------------------------------------------------------------"
output(sm)

complement_sm = complement.do(sm)
assert all(superset.do(sm, tsm) == True
           for tsm in sm_list)
assert all(DFA.is_Empty(intersection.do([complement_sm, tsm]))
           for tsm in sm_list)

print "<terminated>"
