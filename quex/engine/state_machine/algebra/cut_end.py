import quex.engine.state_machine.algebra.reverse      as reverse
import quex.engine.state_machine.algebra.cut_begin    as cut_begin

def do(SM_A, SM_B):
    Ar        = reverse.do(SM_A)
    Br        = reverse.do(SM_B)
    cut_Ar_Br = cut_begin.do(Ar, Br)
    return reverse.do(cut_Ar_Br)
