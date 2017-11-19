#! /usr/bin/env python
#
# TEST: Mounting of DFA-s in parallel.
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
from   quex.engine.state_machine.TEST_help.some_dfas   import *
import quex.engine.state_machine.check.superset           as     superset
import quex.engine.state_machine.algebra.intersection     as     intersection
import quex.output.languages.core                         as     languages
import quex.engine.state_machine.algebra.complement       as     complement

from   quex.blackboard import setup as Setup

if "--hwut-info" in sys.argv:
    print "DFA Operations: Mount Paralell"
    sys.exit(0)

def test(SmList):
    print "-------------------------------------------------------------------------------"
    for tsm in SmList:
        print "##sm:", tsm

    sm = parallelize.do(SmList)
    print "RESULT:", sm

    complement_sm = complement.do(sm)
    assert all(superset.do(sm, tsm) == True
               for tsm in SmList)
    assert all(DFA.is_Empty(intersection.do([complement_sm, tsm]))
               for tsm in SmList)

tsm0 = trivial_sm('a')
tsm1 = trivial_sm('b')
tsm2 = trivial_sm('c')
test([tsm0, tsm1, tsm2])

test([sm0, sm1, sm2])

print "-------------------------------------------------------------------------------"
empty_state_machine = DFA(7777)    
empty_state_machine.get_init_state().set_acceptance(True)
test([empty_state_machine, sm0, 
      empty_state_machine, sm1, 
      empty_state_machine, sm2, 
      empty_state_machine]) 
print "<terminated>"
