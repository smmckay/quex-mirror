#! /usr/bin/env python
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])

from   quex.engine.state_machine.core                       import *
import quex.engine.state_machine.construction.sequentialize as     sequentialize 
from   quex.engine.state_machine.TEST_help.some_dfas   import *

from   quex.blackboard import setup 

if "--hwut-info" in sys.argv:
    print "DFA: Cloning"
    sys.exit(0)
    
print "------------------------------------------"
print sm0
print sm0.clone()

print "------------------------------------------"
print sm1
print sm1.clone()

print "------------------------------------------"
print sm2
print sm2.clone()

print "------------------------------------------"
sm3.mark_state_origins()
print sm3
print sm3.clone()


# print Interval(ord('a'), ord('g')+1).inverse()

