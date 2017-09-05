from   quex.engine.state_machine.core                 import DFA
from   quex.engine.state_machine.state.core           import DFA_State
import quex.engine.state_machine.algebra.reverse      as     reverse
from   quex.engine.state_machine.algebra.intersection import state_index_for_combination
from   quex.engine.state_machine.state.target_map_ops import get_intersection_line_up_2
import quex.engine.state_machine.algorithm.beautifier as     beautifier
import quex.engine.state_machine.index                as     index
from   quex.engine.misc.tree_walker                   import TreeWalker
from   quex.engine.misc.tools                         import r_enumerate

from   itertools import islice

def leave_begin(DfaA, DfaB):
    dfa_b_complement = complement.do(DfaB)
    return cut_begin(DfaA, complement.do(DfaB))

def leave_end(DfaA, DfaB):
    dfa_b_complement = complement.do(DfaB)
    return cut_end(DfaA, complement.do(DfaB))

def leave_in(DfaA, DfaB):
    dfa_b_complement = complement.do(DfaB)
    return cut_in(DfaA, complement.do(DfaB))

def cut_in(DfaA, DfaB):
    """Cut End:

    Any lexeme that matches 'A' and contains a lexeme matching 'B' is 
    pruned by what matched 'B'.
    """
    si_correspondance_db = dict(
        (si, index.get()) for si in sorted(DfaA.states.iterkeys())
    )
    result = DfaA.clone(ReplDbStateIndex=si_correspondance_db)

    backup_init_state_index = result.init_state_index

    for si in DfaA.states:
        DfaA.init_state_index = si

        # cutter = CutBeginWalker(DfaA, DfaB, result, si_correspondance_db)
        cutter = CutBeginWalker(DfaA, DfaB, result)
        cutter.do((DfaA.init_state_index, DfaB.init_state_index, None))

    result.init_state_index = backup_init_state_index

    # Delete orphaned and hopeless states in result
    cutter.result.clean_up()
    return beautifier.do(cutter.result)

def cut_end(DfaA, DfaB):
    """Cut End:

    Any lexeme that matches 'A' and ends with a lexeme matching 'B' is 
    pruned by what matches 'B'.
    """
    Ar        = reverse.do(DfaA)
    Br        = reverse.do(DfaB)
    cut_Ar_Br = cut_begin(Ar, Br)
    return reverse.do(cut_Ar_Br)

def cut_begin(A, B):
    """PURPOSE: Generate a modified DFA based on A:

        * matches all lexemes of 'A' if they do not start with something that 
          matches 'B'.

        * matches the 'tail' of lexemes of 'A' if their beginning matches 
          something that matches 'B'. The 'tail' is the lexeme without the 
          'head' that matches 'B'.
    """
    result, si_correspondance_db = __cut_begin_core(A, B, None)
    return result

def __cut_begin_core(A, B, A_begin_state_index):
    A.assert_consistency() 
    B.assert_consistency() 

    if B.is_Empty(): 
        return A.clone_and_produce_correspondance_db()

    elif A_begin_state_index is None: 
        A_begin_state_index = A.init_state_index

    state_setup_db    = {}
    result_init_si, _ = state_index_for_combination(state_setup_db,
                                                    (A_begin_state_index, B.init_state_index))
    result   = DFA(InitStateIndex = result_init_si, 
                   AcceptanceF    = A.states[A_begin_state_index].is_acceptance())

    worklist = [ 
        (result.init_state_index, A_begin_state_index, B.init_state_index) 
    ]
    while worklist:
        result_si, A_si, B_si = worklist.pop()

        A_state = A.states[A_si]
        B_state = B.states.get(B_si)
        # Generate Map that shows what lexatoms trigger to what state combination.
        #
        #       NumberSet    Target DFA_State Combination 
        #       [0:23]   --> [ State1, State24 ]
        #       [0:23]   --> [ State5, None    ]
        #       [24:60]  --> [ State1, State23 ]
        #
        if B_state is not None:
            line_up = get_intersection_line_up_2((A_state.target_map, B_state.target_map))
        else:
            line_up = dict(((target_si, None), trigger_set) 
                           for target_si, trigger_set in A_state.target_map.get_map().iteritems())

        for si_tuple, trigger_set in line_up.iteritems():
            A_target_si, B_target_si = si_tuple
            
            if A_target_si is None:
                continue

            result_target_si, \
            new_f             = state_index_for_combination(state_setup_db,
                                                            (A_target_si, B_target_si))

            if B_target_si is not None and B.states[B_target_si].is_acceptance():
                # Transition in 'B' to acceptance
                # => Drop-out in result!
                # But, the correspondent state must exist!
                if new_f:
                    result.states[result_target_si] = DFA_State()        
                result.add_epsilon_transition(result.init_state_index, result_target_si)
            else:
                acceptance_f = A.states[A_target_si].is_acceptance()
                result.add_transition(result_si, trigger_set, result_target_si,
                                      AcceptanceF = acceptance_f)

            if new_f:
                worklist.append((result_target_si, A_target_si, B_target_si))


    result.delete_hopeless_states()

    si_correspondance_db = dict(
        (si_info[0], result_si)
        for si_info, result_si in state_setup_db.iteritems()
    )
    return result, si_correspondance_db

