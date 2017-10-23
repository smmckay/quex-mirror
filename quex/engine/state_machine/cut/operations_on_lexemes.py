from   quex.engine.state_machine.core                   import DFA
import quex.engine.state_machine.index                  as     state_index
import quex.engine.state_machine.algebra.complement     as     complement
import quex.engine.state_machine.algebra.reverse        as     reverse
from   quex.engine.state_machine.state.target_map_ops   import get_intersection_line_up_2
import quex.engine.state_machine.algorithm.beautifier   as     beautifier

from   copy        import copy

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

def cut_end(A, B):
    """Cut End:

    Any lexeme that matches 'A' and ends with a lexeme matching 'B' is 
    pruned by what matches 'B'.
    """
    Ar        = reverse.do(A)
    Br        = reverse.do(B)
    cut_Ar_Br, cut_f = __cut_begin_core(Ar, Br)
    if not cut_f: return A
    else:         return reverse.do(cut_Ar_Br)

def leave_begin(DfaA, DfaB):
    return cut_begin(DfaA, complement.do(DfaB))

def leave_end(DfaA, DfaB):
    return cut_end(DfaA, complement.do(DfaB))

class WorkList:
    def __init__(self):
        """A = First DFA
           B = Second DFA (the 'matching'/'cutting' DFA)
           SearchBeginList = list of A state indices to start the search.
        """
        self.together_list  = []
        self.tail_list      = []
        self.done_set       = set()
        self.state_setup_db = {}

    def add_together(self, A_si, B_si, BridgeSet):
        result_target_si, new_f = self.__access_result_state_index(A_si, B_si, BridgeSet)
        if not new_f: return result_target_si
        self.together_list.append((result_target_si, A_si, B_si, copy(BridgeSet)))
        return result_target_si

    def add_tail(self, A_si, BridgeSet):
        result_target_si, new_f = self.__access_result_state_index(A_si, None, BridgeSet)
        if not new_f: return result_target_si
        self.tail_list.append((result_target_si, A_si, copy(BridgeSet)))
        return result_target_si

    def __access_result_state_index(self, A_si, B_si, BridgeSet):
        result_target_si = self.get_result_si(A_si, B_si, BridgeSet)
        if result_target_si in self.done_set: 
            return result_target_si, False
        else:
            self.done_set.add(result_target_si)
            return result_target_si, True

    def get_result_si(self, A_si, B_si, BridgeSet):
        if BridgeSet is None: key = (A_si, B_si)
        else:                 key = (A_si, B_si, tuple(sorted(BridgeSet)))
        result_si = self.state_setup_db.get(key)
        if result_si is None: 
            result_si = state_index.get()
            self.state_setup_db[key] = result_si
        return result_si

def __cut_begin_core(A, B, SearchBeginList=None):
    """RETURN: [0] Resulting DFA
               [1] True, if cut has been performed; False else.

    If no cut has been performed, then 'A' is returned as is.
    """
    A.assert_consistency() 
    B.assert_consistency() 

    if B.is_Empty(): return A, False

    work_list = WorkList()
    result    = DFA(InitStateIndex = work_list.get_result_si(A.init_state_index, None, None), 
                    AcceptanceF    = A.states[A.init_state_index].is_acceptance())

    epsilon_transition_set = __together_walk(work_list, A, B, result) 
    # No cut => return original DFA
    if epsilon_transition_set is None: return A, False

    __tail_walk(work_list, A, result)

    result.delete_hopeless_states()

    return __implement_epsilon_transitions(result, A, epsilon_transition_set)

def __together_walk(work_list, A, B, result):
    """Walk along 'A' and 'B' starting at 'A_begin_si' and 'B.init_state_index'
    as long as 'B' matches the path. For each matching state a new state in 
    'result' is generated based on the key '(A_si, B_si)' of the path.

    Whenever 'B' cannot walk any further along a path in 'A' a 'tail state'
    is introduced. It is produced based on the key '(A_si, None)'. Tail states
    are not handled in this function.

      (*) Beginning state of together walk:

          (A_begin_si, B.init_state_index) <--> result_begin_si

      (*) Tail state, where 'B' does not match any longer:

          (A_si, None)                     <--> tail state index in result

      (*) State that is obstructed by last transition:

          (A_si, B_acceptance_state_si)    <--> hanging result state index

    ADAPTS:  'result' DFA 
    RETURNS: set of epsilon transitions to implement.
             None, if no cut has happened.
    """
    result_begin_si = work_list.add_together(A.init_state_index, B.init_state_index, 
                                             BridgeSet=set())
    epsilon_transition_set = []
    while work_list.together_list:
        result_si, A_si, B_si, bridge_set = work_list.together_list.pop()
        assert A_si is not None
        assert B_si is not None

        # Line-Up: trigger sets of target state combinations:
        #   
        #       NumberSet      A_target_si, B_target_si
        #       [0:23]   --> [ State1,      State24     ]
        #       [0:23]   --> [ State5,      None        ]
        #       [24:60]  --> [ State1,      State23     ]
        #
        A_map = A.states[A_si].target_map
        B_map = B.states[B_si].target_map
        for si_pair, trigger_set in get_intersection_line_up_2((A_map, B_map)):
            A_target_si, B_target_si = si_pair
            if A_target_si is None: 
                continue

            A_target_acceptance_f = A.states[A_target_si].is_acceptance()
            if B_target_si is None:
                # if B_target_si is None => append to 'tail'
                result_target_si = work_list.add_tail(A_target_si, bridge_set)
                result.add_transition(result_si, trigger_set, result_target_si,
                                      A_target_acceptance_f)
                
            else:
                result_target_si = work_list.add_together(A_target_si, B_target_si, 
                                                          bridge_set)

                if not B.states[B_target_si].is_acceptance():
                    result.add_transition(result_si, trigger_set, result_target_si,
                                          A_target_acceptance_f)
                else:
                    # Transition in 'B' to acceptance => result *must* drop-out! 
                    # Cutting = lexemes starting at the target are acceptable.
                    #           => merge with begin state.
                    #           => must again consider cutting matches with 'B'.
                    bridge_set.add((A_si, A_target_si))
                    epsilon_transition_set.add((result_begin_si, result_target_si, 
                                                A_target_acceptance_f))

    if not epsilon_transition_set:
        return None
    else:
        # The epsilon transition 'initial state' to 'begin search' is always there!
        epsilon_transition_set.append((result.init_state_index, result_begin_si,
                                        A.states[A.init_state_index].is_acceptance()))
        return epsilon_transition_set

def __tail_walk(work_list, A, result):
    while work_list.tail_list:
        result_si, A_si, bridge_set = work_list.tail_list.pop()
        assert A_si is not None

        A_map = A.states[A_si].target_map
        for A_target_si, trigger_set in A_map.get_map().iteritems():
            result_target_si = work_list.add_tail(A_target_si, bridge_set)
            result.add_transition(result_si, trigger_set, result_target_si, 
                                  AcceptanceF = A.states[A_target_si].is_acceptance())

def __implement_epsilon_transitions(result, A, epsilon_transition_set):
    """RETURNS: [0] The resulting state machine, if a 'cut' has happened.
                    The original state machine if no 'cut' has happened.
                [1] True, if a cut has happened, False else.
    """
    if not epsilon_transition_set: 
        return A, False
    else:
        for from_si, to_si, acceptance_f in epsilon_transition_set:
            if from_si == result.init_state_index:
                result.add_epsilon_transition(from_si, to_si) 
            else:
                result.add_epsilon_transition(from_si, to_si, RaiseAcceptanceF=acceptance_f) 
        result.delete_hopeless_states()
        return beautifier.do(result), True

