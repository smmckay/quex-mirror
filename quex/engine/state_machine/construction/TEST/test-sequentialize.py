#! /usr/bin/env python
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])


from   quex.engine.state_machine.core                       import *
import quex.input.regular_expression.engine                 as     regex
import quex.engine.state_machine.algorithm.beautifier       as     beautifier
import quex.engine.state_machine.construction.sequentialize as     sequentialize 
from   quex.engine.state_machine.TEST_help.some_dfas   import *

if "--hwut-info" in sys.argv:
    print "DFA Operations: Sequence"
    print "CHOICES: simply-three;"
    sys.exit(0)
   
if "simply-three" in sys.argv:
    empty_state_machine = DFA(7777)    
    print "##sm0", sm0
    print "##sm1", sm1
    print "##sm2", sm2
    sm = sequentialize.do([empty_state_machine, sm0, 
                           empty_state_machine, sm1, 
                           empty_state_machine, sm2,
                           empty_state_machine  ]) 

    print "-------------------------------------------------------------------------------"
    print "##result = ", sm
else:
    sm0 = regex.do("xy?", {}).sm
    for si in sm0.get_acceptance_state_index_list():
        sm0.states[si].set_read_position_store_f(True)
    sm1 = regex.do("y?a", {}, AllowNothingIsNecessaryF=True).sm
    sm  = sequentialize.do([sm0, sm1])
    print beautifier.do(sm)

