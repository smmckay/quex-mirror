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
    """Cut In:

    Any lexeme that matches 'A' and contains a lexeme matching 'B' is 
    pruned by what matched 'B'.
    """
    # si_correspondance_db: A's state index --> result's state index
    si_correspondance_db = dict((si,si) for si in DfaA.states)

    result = DfaA
    for si in DfaA.states:
        result_si = si_correspondance_db.get(si)
        if result_si is None: continue # Already cut out?
        
        result, state_setup_db = __cut_begin_core(result, DfaB, result_si)

        # -- Derive the state index correspondance from 'state_setup_db'.
        update_db = dict(
            # 'si_info[0]' => state index of previous result
            # 'result_si'  => correspondant state index of new result
            (si_info[0], result_si) 
            for si_info, result_si in state_setup_db.iteritems()
        )

        # -- Update the 'si_correspondance_db'
        si_correspondance_db = dict(
            (si, update_db[prev_result_si])
            for si, prev_result_si in si_correspondance_db.iteritems()
            if prev_result_si in result.states
        )

    # Delete orphaned and hopeless states in result
    result.clean_up()
    return beautifier.do(result)

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
    result, _ = __cut_begin_core(A, B, None)
    return result

def __cut_begin_core(A, B, A_begin_state_index):
    """RETURN: [0] Resulting DFA
               [1] state_setup_db:  state index combination --> state index in result
    """
    A.assert_consistency() 
    B.assert_consistency() 

    if B.is_Empty(): 
        result, si_correspondance_db = A.clone_and_get_correspondance_db()
        return result, \
               dict(((si,), result_si) 
                    for si, result_si in si_correspondance_db.iteritems())

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
    # print "A:", A.get_string(NormalizeF=False)
    # print "B:", B.get_string(NormalizeF=False)
    epsilon_transition_list = []
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

        # print "State (%s, %s):" % (A_si, B_si)
        # for si_tuple, trigger_set in line_up.iteritems():
        #    print "   %s --> %s" % (trigger_set, si_tuple)
            
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

                # The short-cut state is now combined with the init state.
                # => Must consider match with 'B'.
                new_result_target_si, \
                new_f                 = state_index_for_combination(state_setup_db,
                                                                    (A_target_si, B.init_state_index))
                if new_f:
                    worklist.insert(0, (new_result_target_si, A_target_si, B.init_state_index))

                epsilon_transition_list.append(new_result_target_si)
                # print "EPSILON --> (%s, %s)" % (A_target_si, B_target_si)

                # result.add_transition(result_si, trigger_set, result_target_si,
                #                       AcceptanceF = acceptance_f)

            else:
                acceptance_f = A.states[A_target_si].is_acceptance()

                result.add_transition(result_si, trigger_set, result_target_si,
                                      AcceptanceF = acceptance_f)

            # # print "   ADD: (%s) -- %s --> (%s)" % (result_si, trigger_set, result_target_si)

            if new_f:
                worklist.append((result_target_si, A_target_si, B_target_si))

    for si in epsilon_transition_list:
        result.add_epsilon_transition(result.init_state_index, si)
    result.delete_hopeless_states()

    return beautifier.do(result), state_setup_db

