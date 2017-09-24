from   quex.engine.state_machine.core                 import DFA
import quex.engine.state_machine.construction.sequentialize   as     sequentialize
import quex.engine.state_machine.algebra.complement   as     complement
import quex.engine.state_machine.algebra.difference   as     difference
import quex.engine.state_machine.algebra.derived      as     derived
import quex.engine.state_machine.algebra.reverse      as     reverse
import quex.engine.state_machine.algebra.union        as     union
from   quex.engine.state_machine.algebra.intersection import state_index_for_combination
from   quex.engine.state_machine.state.target_map_ops import get_intersection_line_up_2
import quex.engine.state_machine.algorithm.beautifier as     beautifier

from   collections import defaultdict

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

def cut_in(A, B):
    """Cut In:

    Any lexeme that matches 'A' and contains a lexeme matching 'B' is 
    pruned by what matched 'B'.

    """
    # -- Find states that intersect in their transition map with the initial
    #    transition map of 'B'.
    union_tm_B = B.get_init_state().target_map.get_trigger_set_union()

    search_begin_list = [
        si
        for si, state in A.states.iteritems()
        if state.target_map.has_intersection(union_tm_B)
    ]
    # print "#search_begin_list:", search_begin_list

    cut_A_B, cut_f = __cut_begin_core(A, B, search_begin_list)

    if not cut_f: return A
    else:         return cut_A_B

def leave_begin(DfaA, DfaB):
    return cut_begin(DfaA, complement.do(DfaB))

def leave_end(DfaA, DfaB):
    return cut_end(DfaA, complement.do(DfaB))

def leave_in(DfaA, DfaB):
    return cut_in(DfaA, complement.do(DfaB))

class WorkList:
    def __init__(self, A, B, SearchBeginList=None):
        """A = First DFA
           B = Second DFA (the 'matching'/'cutting' DFA)
           SearchBeginList = list of A state indices to start the search.
        """
        self.work_list      = []
        self.state_setup_db = {}

        if SearchBeginList is None:
            self.result_init_si = self.add(A.init_state_index, 
                                           B.init_state_index)
        else:
            self.result_init_si = None
            for A_si in SearchBeginList:
                result_si = self.add(A_si, B.init_state_index)
                if A_si == A.init_state_index: 
                    self.result_init_si = result_si

            if self.result_init_si is None:
                self.result_init_si = self.add(A.init_state_index, None)

    def pop(self):
        return self.work_list.pop()

    def add(self, A_si, B_si):
        result_target_si, new_f = self.get_result_state_index(A_si, B_si)

        if new_f:
            if B_si is not None:
                self.work_list.append((result_target_si, A_si, B_si))
            else:
                self.work_list.insert(0, (result_target_si, A_si, B_si))

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

def __cut_begin_core(A, B, SearchBeginList=None):
    """RETURN: [0] Resulting DFA
               [1] True, if cut has been performed; False else.

    If no cut has been performed, then 'A' is returned as is.
    """
    A.assert_consistency() 
    B.assert_consistency() 

    # print "#A:", A.get_string(NormalizeF=False)
    # print "#B:", B.get_string(NormalizeF=False)

    if B.is_Empty(): return A, False

    work_list = WorkList(A, B, SearchBeginList)
    result    = DFA(InitStateIndex = work_list.result_init_si, 
                    AcceptanceF    = A.states[A.init_state_index].is_acceptance())

    epsilon_transition_list = []
    # done_set = set()
    while not work_list.done():
        result_si, A_si, B_si = work_list.pop()
        # print "#pop:", result_si, A_si, B_si
        # if B_si is None and A_si in done_set: continue
        # if B_si is not None: done_set.add(A_si)
        assert A_si is not None

        for A_target_si, B_target_si, trigger_set in target_map_line_up(A, A_si, B, B_si):
            # State index = 'None' => state does not transit on 'trigger_set'.
            if A_target_si is None: continue
            # print "   %s -> %s %s"  % (trigger_set.get_string("hex"), A_target_si, B_target_si)

            result_target_si = work_list.add(A_target_si, B_target_si)

            if B_target_si is not None and B.states[B_target_si].is_acceptance():
                # Transition in 'B' to acceptance => result *must* drop-out!
                # Cutting = lexemes starting at the target are acceptable.
                #           => merge with init state.
                #           => must again consider cutting matches with 'B'.
                new_result_target_si = work_list.add(A_target_si, B_target_si)
                epsilon_transition_list.append(new_result_target_si)
                # print "   cut", A_target_si, B_target_si
                # print "   eps", new_result_target_si
            else:
                A_acceptance_f = A.states[A_target_si].is_acceptance()
                result.add_transition(result_si, trigger_set, result_target_si,
                                      AcceptanceF = A_acceptance_f)
                # print "   to ", A_target_si, B_target_si

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

