import quex.input.regular_expression.engine                 as     regex
import quex.engine.state_machine.construction.sequentialize as sequentialize
from   quex.engine.state_machine.core                       import DFA
import quex.engine.state_machine.construction.repeat        as repeat
import quex.engine.state_machine.algorithm.beautifier       as beautifier
import quex.engine.state_machine.check.identity             as     identity

def more_DFAs(A, B):
    """RETURNS: [0] B+
                [1] B*
                [2] B*A
    """
    B_plus   = repeat.do(B)
    B_star   = repeat.do(B, min_repetition_n=0)
    B_star_A = beautifier.do(sequentialize.do([B_star, A]))
    return beautifier.do(B_plus), \
           beautifier.do(B_star), \
           B_star_A

def unary_checks(Q, operation):
    Q_plus      = beautifier.do(repeat.do(Q))
    Q_star      = beautifier.do(repeat.do(Q, min_repetition_n=0))
    
    Q_is_Q_star = identity.do(Q, Q_star)
    Q_is_Q_plus = identity.do(Q, Q_plus)

    # \Cut{Q Q} = \Nothing
    y = operation(Q, Q)
    assert y.is_Nothing()

    # if Q != Q+: \CutBegin{Q+ Q} = Q*
    if not Q_is_Q_plus:
        y = operation(Q_plus, Q)
        assert identity.do(y, Q_star)

    # if Q != Q*: \CutBegin{Q* Q} = Q*
    if not Q_is_Q_star:
        y = operation(Q_star, Q)
        assert identity.do(y, Q_star)

    # \Cut{Q \Nothing} = Q
    y = operation(Q, DFA.Nothing())
    assert identity.do(y, Q)

    # \Cut{\Nothing Q} = \Nothing
    y = operation(DFA.Nothing(), Q)
    assert y.is_Nothing()

    # \Cut{Q \Universal} = \Nothing
    y = operation(Q, DFA.Universal())
    assert y.is_Nothing()

    # NOT: \Cut{\Universal Q} = \Universal
    if not Q_is_Q_star and not Q_is_Q_plus:
        y = operation(Q, DFA.Universal())
        assert y.is_Nothing()

    return Q_star, Q_plus

def parse_REs(A_txt, B_txt):
    print ("Original = " + A_txt).replace("\n", "\\n").replace("\t", "\\t")
    print ("Cutter   = " + B_txt).replace("\n", "\\n").replace("\t", "\\t")
    A = regex.do(A_txt, {}).sm
    B = regex.do("%s" % B_txt, {}).sm
    return A, B

