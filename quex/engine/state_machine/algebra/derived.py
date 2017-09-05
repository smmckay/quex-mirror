import quex.engine.state_machine.algebra.complement         as     complement
import quex.engine.state_machine.algebra.difference         as     difference 
import quex.engine.state_machine.construction.sequentialize as     sequentialize
import quex.engine.state_machine.construction.repeat        as     repeat       
import quex.engine.state_machine.algorithm.beautifier       as     beautifier
from   quex.engine.state_machine.core                       import DFA

def not_begin(P, Q):
    tmp = sequentialize.do([Q, DFA.Universal()])
    tmp = beautifier.do(tmp)
    return beautifier.do(difference.do(P, tmp))

def not_end(P, Q):
    tmp = sequentialize.do([DFA.Universal(), Q])
    tmp = beautifier.do(tmp)
    return beautifier.do(difference.do(P, tmp))

def not_in(P, Q):
    tmp        = sequentialize.do([DFA.Universal(), 
                                   Q, 
                                   DFA.Universal()])
    tmp = beautifier.do(tmp)
    return beautifier.do(difference.do(P, tmp))

def is_begin(P, Q):
    tmp = sequentialize.do([Q, DFA.Universal()])
    tmp = beautifier.do(tmp)
    return beautifier.do(intersection.do(P, tmp))

def is_end(P, Q):
    tmp = sequentialize.do([DFA.Universal(), Q])
    tmp = beautifier.do(tmp)
    return beautifier.do(intersection.do(P, tmp))

def is_in(P, Q):
    tmp = sequentialize.do([DFA.Universal(), Q, DFA.Universal()])
    return beautifier.do(intersection.do(P, tmp))
