from   quex.engine.state_machine.core                 import DFA
import quex.engine.state_machine.index                as     state_index
from   quex.engine.misc.interval_handling             import NumberSet
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
    def __init__(self, A_init_si):
        """A = First DFA
           B = Second DFA (the 'matching'/'cutting' DFA)
           SearchBeginList = list of A state indices to start the search.
        """
        self.work_list       = []
        self.tail_list       = []
        self.done_set        = set()
        self.state_setup_db  = {}
        self.A_init_si       = A_init_si

    def pop(self):
        return self.work_list.pop()

    def tail_pop(self):
        return self.tail_list.pop()

    def add_begin(self, A_begin_si, B_init_state_index):
        return self.add(A_begin_si, B_init_state_index, BridgeSet=set())

    def add(self, A_si, B_si, BridgeSet):
        result_target_si = self.get_result_state_index(A_si, B_si, BridgeSet)

        if result_target_si in self.done_set: return result_target_si
        self.done_set.add(result_target_si)

        if B_si is not None:
            self.work_list.append((result_target_si, A_si, B_si, copy(BridgeSet)))
        else:
            self.tail_list.append((result_target_si, A_si, B_si, copy(BridgeSet)))

        return result_target_si

    def get_result_state_index(self, A_si, B_si, BridgeSet):
        key = (A_si, B_si, tuple(sorted(BridgeSet)))
        result_si = self.state_setup_db.get(key)
        if result_si is None: 
            result_si = state_index.get()
            self.state_setup_db[key] = result_si
        return result_si

    def done_together(self):
        return not self.work_list

    def late_done(self):
        return not self.tail_list

def __cut_begin_core(A, B, SearchBeginList=None):
    """RETURN: [0] Resulting DFA
               [1] True, if cut has been performed; False else.

    If no cut has been performed, then 'A' is returned as is.
    """
    A.assert_consistency() 
    B.assert_consistency() 

    if   B.is_Empty(): 
        return A, False
    elif SearchBeginList is None: 
        SearchBeginList = [ A.init_state_index ]

    plain_si_db             = {
       A.init_state_index: state_index.get() 
    }
    plain_si_db.update(
        (A_si, state_index.get()) 
        for A_si in SearchBeginList
        if A_si != A.init_state_index
    )

    result = DFA(InitStateIndex = plain_si_db[A.init_state_index], 
                 AcceptanceF    = A.states[A.init_state_index].is_acceptance())

    epsilon_transition_list = []
    work_list               = WorkList(A.init_state_index)
    inadmissible_tm_db      = defaultdict(NumberSet)
    for A_begin_si in SearchBeginList:
        result_begin_si = __together_walk(work_list, A, A_begin_si, B, result, 
                                          epsilon_transition_list, inadmissible_tm_db)

        epsilon_transition_list.append((plain_si_db[A_begin_si], 
                                        result_begin_si,
                                        A.states[A_begin_si].is_acceptance()))

    # The late 'lonely None' walk ...
    __tail_walk(work_list, A, result)

    # if A.init_state_index not in SearchBeginList:
    #    __virgin_walk(A, result, plain_si_db, epsilon_transition_list, inadmissible_tm_db)

    # The 'lonely None' walk from the initial state:
    # => forbidden transitions cannot be walked along.
    # Forbidden transitions in late 'lonely None' walks are conditional.
    # In the case of a path starting from the initial state, transitions
    # are absolute. Now, the 'cut' made in the 'together walk' must be 
    # respected.

    result.delete_hopeless_states()

    return __implement_epsilon_transitions(result, A, epsilon_transition_list)

def __together_walk(work_list, A, A_begin_si, B, result, epsilon_transition_list, 
                    inadmissible_tm_db):
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

    RETURNS: 'result' state index corresponding to 'A_begin_si'.
    """
    result_begin_si = work_list.add_begin(A_begin_si, B.init_state_index)

    while not work_list.done_together():
        result_si, A_si, B_si, bridge_set = work_list.pop()
        assert A_si is not None
        assert B_si is not None

        A_map   = A.states[A_si].target_map
        B_map   = B.states[B_si].target_map
        # Line-Up: trigger sets of target state combinations:
        #   
        #       NumberSet      A_target_si, B_target_si
        #       [0:23]   --> [ State1,      State24     ]
        #       [0:23]   --> [ State5,      None        ]
        #       [24:60]  --> [ State1,      State23     ]
        #
        for si_pair, trigger_set in get_intersection_line_up_2((A_map, B_map)):
            A_target_si, B_target_si = si_pair
            # State index = 'None' => state does not transit on 'trigger_set'.
            if A_target_si is None: continue

            if B_target_si is not None and B.states[B_target_si].is_acceptance():
                # Transition in 'B' to acceptance => result *must* drop-out!
                # Cutting = lexemes starting at the target are acceptable.
                #           => merge with init state.
                #           => must again consider cutting matches with 'B'.
                bridge_set.add((A_si, A_target_si))
                result_target_si = work_list.add(A_target_si, B_target_si, bridge_set)
                epsilon_transition_list.append((result_begin_si, result_target_si, 
                                                A.states[A_target_si].is_acceptance()))
                inadmissible_tm_db[A_si].unite_with(trigger_set)
            else:
                # if B_target_si is None => append to 'tail'
                result_target_si = work_list.add(A_target_si, B_target_si, bridge_set)

                result.add_transition(result_si, trigger_set, result_target_si,
                                      AcceptanceF = A.states[A_target_si].is_acceptance())

    return result_begin_si

def __tail_walk(work_list, A, result):
    while not work_list.late_done():
        result_si, A_si, B_si, bridge_set = work_list.tail_pop()
        assert A_si is not None
        assert B_si is None

        A_map = A.states[A_si].target_map
        for A_target_si, trigger_set in A_map.get_map().iteritems():
            result_target_si = work_list.add(A_target_si, None, bridge_set)
            result.add_transition(result_si, trigger_set, result_target_si,
                                  AcceptanceF = A.states[A_target_si].is_acceptance())

def __virgin_walk(A, result, plain_si_db, epsilon_transition_list, inadmissible_tm_db):
    def get_result_si(plain_si_db, A_si):
        si = plain_si_db.get(A_si)
        if si is None: 
            si = state_index.get()
            plain_si_db[A_si] = si
        return si

    def adapt_trigger_set(inadmissible_trigger_set, trigger_set):
        if inadmissible_trigger_set is None:
            return trigger_set
        elif trigger_set.has_intersection(inadmissible_trigger_set):
            trigger_set = trigger_set.difference(inadmissible_trigger_set)

        return trigger_set

    work_list = [ 
        (plain_si_db[A.init_state_index], A.init_state_index) 
    ]
    while work_list:
        result_si, A_si = work_list.pop()

        A_map                    = A.states[A_si].target_map
        inadmissible_trigger_set = inadmissible_tm_db.get(A_si)

        for A_target_si, trigger_set in A_map.get_map().iteritems():
            result_target_si = get_result_si(plain_si_db, A_target_si)
            work_list.append((result_target_si, A_target_si))

            trigger_set = adapt_trigger_set(inadmissible_trigger_set, 
                                            trigger_set)
            if trigger_set.is_empty(): continue

            result.add_transition(result_si, trigger_set, result_target_si,
                                  AcceptanceF = A.states[A_target_si].is_acceptance())

def __implement_epsilon_transitions(result, A, epsilon_transition_list):
    """RETURNS: [0] The resulting state machine, if a 'cut' has happened.
                    The original state machine if no 'cut' has happened.
                [1] True, if a cut has happened, False else.
    """
    if not epsilon_transition_list: 
        return A, False
    else:
        for from_si, to_si, acceptance_f in epsilon_transition_list:
            if from_si == result.init_state_index:
                result.add_epsilon_transition(from_si, to_si) 
            else:
                result.add_epsilon_transition(from_si, to_si, RaiseAcceptanceF=acceptance_f) 
        result.delete_hopeless_states()
        return beautifier.do(result), True

