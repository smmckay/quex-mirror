from   quex.engine.state_machine.core                 import DFA
import quex.engine.state_machine.algebra.complement   as     complement
import quex.engine.state_machine.algebra.derived      as     derived
import quex.engine.state_machine.algebra.reverse      as     reverse
from   quex.engine.state_machine.algebra.intersection import state_index_for_combination
from   quex.engine.state_machine.state.target_map_ops import get_intersection_line_up_2
import quex.engine.state_machine.algorithm.beautifier as     beautifier

def leave_begin(DfaA, DfaB):
    return cut_begin(DfaA, complement.do(DfaB))

def leave_end(DfaA, DfaB):
    return cut_end(DfaA, complement.do(DfaB))

def leave_in(DfaA, DfaB):
    return cut_in(DfaA, complement.do(DfaB))

def cut_in(DfaA, DfaB):
    """Cut In:

    Any lexeme that matches 'A' and contains a lexeme matching 'B' is 
    pruned by what matched 'B'.

    """
    uni_B     = sequentialize.do([DFA.Universal(), DfaB])
    B_uni     = sequentialize.do([DfaB, DFA.Universal()])

    C_begin   = derived.is_begin(DfaA, uni_B)     # only exemes starting with 'B'
    remainder = difference.do(A, C_begin)
    C_end     = derived.is_end(remainder, B_uni)  # Lexemes starting with 'B'
    remainder = difference.do(remainder, C_end)
    
    DfaC_head = cut_begin(C_begin, uni_B)
    DfaC_tail = cut_end(C_end, B_uni)

    DfaC_cut  = sequentialize.do([DfaC_head, DfaC_tail])
    
    return union.do([remainder, DfaC_cut])


def cut_end(DfaA, DfaB):
    """Cut End:

    Any lexeme that matches 'A' and ends with a lexeme matching 'B' is 
    pruned by what matches 'B'.
    """
    result, cut_f = __cut_end_core(DfaA, DfaB)
    return result

def cut_begin(A, B):
    """PURPOSE: Generate a modified DFA based on A:

        * matches all lexemes of 'A' if they do not start with something that 
          matches 'B'.

        * matches the 'tail' of lexemes of 'A' if their beginning matches 
          something that matches 'B'. The 'tail' is the lexeme without the 
          'head' that matches 'B'.
    """
    result, cut_f = __cut_begin_core(A, B)
    return result

class WorkList:
    def __init__(self):
        self.work_list      = []
        self.state_setup_db = {}

    def pop(self):
        return self.work_list.pop()

    def add(self, A_si, B_si, FirstF=False):
        result_target_si, new_f = self.get_result_state_index(A_si, B_si)

        if new_f:
            if FirstF:
                self.work_list.insert(0, (result_target_si, A_si, B_si))
            else:
                self.work_list.append((result_target_si, A_si, B_si))

        return result_target_si

    def get_result_state_index(self, A_si, B_si):
        result_target_si, \
        new_f             = state_index_for_combination(self.state_setup_db,
                                                        (A_si, B_si))

        return result_target_si, new_f

    def done(self):
        return not self.work_list

def target_map_line_up(A, A_si, B, B_si):
    """Generate Map that shows what lexatoms trigger to what state combination.
    
                NumberSet    Target DFA_State Combination 
                [0:23]   --> [ State1, State24 ]
                [0:23]   --> [ State5, None    ]
                [24:60]  --> [ State1, State23 ]

    """
    A_state = A.states[A_si]
    if B_si is not None:
        B_state = B.states.get(B_si)
        result = get_intersection_line_up_2((A_state.target_map, 
                                             B_state.target_map))
        return ((x[0], x[1], y) for x, y in result.iteritems())
    else:
        return ((target_si, None, trigger_set) 
                for target_si, trigger_set in A_state.target_map.get_map().iteritems())


def __cut_end_core(A, B):
    """RETURN: [0] Resulting DFA
               [1] True, if cut has been performed; False else.

    If no cut has been performed, then 'A' is returned as is.
    """
    Ar        = reverse.do(A)
    Br        = reverse.do(B)
    cut_Ar_Br, cut_f = __cut_begin_core(Ar, Br)
    if not cut_f: return A, False
    else:         return reverse.do(cut_Ar_Br), True 

def __cut_begin_core(A, B):
    """RETURN: [0] Resulting DFA
               [1] True, if cut has been performed; False else.

    If no cut has been performed, then 'A' is returned as is.
    """
    A.assert_consistency() 
    B.assert_consistency() 

    if B.is_Empty(): 
        return A, False

    work_list      = WorkList()
    result_init_si = work_list.add(A.init_state_index, B.init_state_index)
    result         = DFA(InitStateIndex = result_init_si, 
                         AcceptanceF    = A.states[A.init_state_index].is_acceptance())

    epsilon_transition_list = []
    while not work_list.done():
        result_si, A_si, B_si = work_list.pop()
        assert A_si is not None

        for A_target_si, B_target_si, trigger_set in target_map_line_up(A, A_si, B, B_si):
            # State index = 'None' => state does not transit on 'trigger_set'.
            if A_target_si is None: continue

            result_target_si = work_list.add(A_target_si, B_target_si)

            if B_target_si is not None and B.states[B_target_si].is_acceptance():
                # Transition in 'B' to acceptance => result *must* drop-out!
                # Cutting = lexemes starting at the target are acceptable.
                #           => merge with init state.
                #           => must again consider cutting matches with 'B'.
                new_result_target_si = work_list.add(A_target_si, B.init_state_index,
                                                     FirstF=True)
                epsilon_transition_list.append(new_result_target_si)
            else:
                A_acceptance_f = A.states[A_target_si].is_acceptance()
                result.add_transition(result_si, trigger_set, result_target_si,
                                      AcceptanceF = A_acceptance_f)

    return __implement_epsilon_transitions(result, A, epsilon_transition_list)

def __implement_epsilon_transitions(result, A, epsilon_transition_list):
    """RETURNS: [0] The resulting state machine, if a 'cut' has happend.
                    The original state machine if no 'cut' has happend.
                [1] True, if a cut has happend, False else.
    """
    if not epsilon_transition_list: 
        return A, False
    else:
        for si in epsilon_transition_list:
            result.add_epsilon_transition(result.init_state_index, si) 
        result.delete_hopeless_states()
        return beautifier.do(result), True

