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
    def __init__(self, A_init_si):
        """A = First DFA
           B = Second DFA (the 'matching'/'cutting' DFA)
           SearchBeginList = list of A state indices to start the search.
        """
        self.work_list       = []
        self.done_set        = set()
        self.state_setup_db  = {}
        self.A_init_si       = A_init_si
        # self.result_init_si  = result_init_si

    def pop(self):
        return self.work_list.pop()

    def add_begin(self, A_begin_si, B_init_state_index):
        self.result_begin_si = self.add(A_begin_si, B_init_state_index)
        return self.result_begin_si


    def add(self, A_si, B_si):
        result_target_si = self.get_result_state_index(A_si, B_si)

        if result_target_si not in self.done_set:
            self.done_set.add(result_target_si)
            if B_si is not None:
                self.work_list.append((result_target_si, A_si, B_si))
            else:
                self.work_list.insert(0, (result_target_si, A_si, B_si))

        return result_target_si

    def get_result_state_index(self, A_si, B_si):
        result_target_si, _ = state_index_for_combination(self.state_setup_db,
                                                          (A_si, B_si))

        return result_target_si

    def done_together(self):
        return not self.work_list or self.work_list[-1][2] is None

    def late_done(self):
        return not self.work_list

def __cut_begin_core(A, B, SearchBeginList=None):
    """RETURN: [0] Resulting DFA
               [1] True, if cut has been performed; False else.

    If no cut has been performed, then 'A' is returned as is.
    """
    A.assert_consistency() 
    B.assert_consistency() 

    # print "#A:", A.get_string(NormalizeF=False)
    # print "#B:", B.get_string(NormalizeF=False)

    if   B.is_Empty(): 
        return A, False
    elif SearchBeginList is None: 
        SearchBeginList = [ A.init_state_index ]

    epsilon_transition_list = []
    work_list               = WorkList(A.init_state_index)
    plain_si_db             = {
       A.init_state_index: state_index.get() 
    }
    plain_si_db.update(
        (A_si, state_index.get()) for A_si in SearchBeginList
    )

    result = DFA(InitStateIndex = plain_si_db[A.init_state_index], 
                 AcceptanceF    = A.states[A.init_state_index].is_acceptance())

    for A_begin_si in SearchBeginList:
        result_begin_si = work_list.add_begin(A_begin_si, B.init_state_index)

        result.add_epsilon_transition(plain_si_db[A_begin_si], result_begin_si)
        __together_walk(work_list, A, B, result, epsilon_transition_list)

    # The late 'lonely None' walk ...
    __lonely_walk(work_list, A, result)

    if False and work_list.init_state_virgin_f:
        __virgin_walk(work_list, A, result, inadmissible_tm_db, plain_si_db)

    # The 'lonely None' walk from the initial state:
    # => forbidden transitions cannot be walked along.
    # Forbidden transitions in late 'lonely None' walks are conditional.
    # In the case of a path starting from the initial state, transitions
    # are absolute. Now, the 'cut' made in the 'together walk' must be 
    # respected.

    return __implement_epsilon_transitions(result, A, epsilon_transition_list)

def __together_walk(work_list, A, B, result, epsilon_transition_list):
    inadmissible_tm_db      = defaultdict(NumberSet)
    while not work_list.done_together():
        result_si, A_si, B_si = work_list.pop()
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

            result_target_si = work_list.add(A_target_si, B_target_si)
            # print "#AB", A_si, "--", trigger_set.get_string("hex"), "-->", A_target_si

            if B_target_si is not None and B.states[B_target_si].is_acceptance():
                # Transition in 'B' to acceptance => result *must* drop-out!
                # Cutting = lexemes starting at the target are acceptable.
                #           => merge with init state.
                #           => must again consider cutting matches with 'B'.
                new_result_target_si = work_list.add(A_target_si, B_target_si)
                epsilon_transition_list.append((work_list.result_begin_si, 
                                                new_result_target_si))
                inadmissible_tm_db[A_si].unite_with(trigger_set)
                # print "   cut"
            else:
                A_acceptance_f = A.states[A_target_si].is_acceptance()
                result.add_transition(result_si, trigger_set, result_target_si,
                                      AcceptanceF = A_acceptance_f)

    return epsilon_transition_list

def __lonely_walk(work_list, A, result):
    # print "#entry 'lonely' A:", A.get_string(Option="hex", NormalizeF=False)
    # print "#entry 'lonely' result", result.get_string(Option="hex", NormalizeF=False)

    while not work_list.late_done():
        result_si, A_si, B_si = work_list.pop()
        assert A_si is not None
        assert B_si is None
        # print "   A_si,result_si:", A_si, result_si

        A_map = A.states[A_si].target_map
        for A_target_si, trigger_set in A_map.get_map().iteritems():
            result_target_si = work_list.add(A_target_si, None)
            # print "   %s -> %s %s" % (trigger_set.get_string("hex"), A_target_si, result_target_si)
            A_acceptance_f   = A.states[A_target_si].is_acceptance()
            result.add_transition(result_si, trigger_set, result_target_si,
                                  AcceptanceF = A_acceptance_f)

def __virgin_walk(work_list, A, result, inadmissible_tm_db=None):
    while not work_list.late_done():
        result_si, A_si, B_si = work_list.pop()
        assert A_si is not None
        assert B_si is None

        if    inadmissible_tm_db is None or A_si not in inadmissible_tm_db:
            inadmissible_trigger_set = None
        else:
            inadmissible_trigger_set = inadmissible_tm_db[A_si]

        # print "#A_si,tm:", A_si, inadmissible_trigger_set

        A_map = A.states[A_si].target_map
        for A_target_si, trigger_set in A_map.get_map().iteritems():
            # print "#At:", A_target_si, trigger_set

            result_target_si = work_list.add(A_target_si, None)

            if     inadmissible_trigger_set is not None \
               and trigger_set.has_intersection(inadmissible_trigger_set):
                trigger_set = trigger_set.difference(inadmissible_trigger_set)
                # print "#remainder:", trigger_set
                if trigger_set.is_empty(): continue

            A_acceptance_f = A.states[A_target_si].is_acceptance()
            result.add_transition(result_si, trigger_set, result_target_si,
                                  AcceptanceF = A_acceptance_f)

def __implement_epsilon_transitions(result, A, epsilon_transition_list):
    """RETURNS: [0] The resulting state machine, if a 'cut' has happened.
                    The original state machine if no 'cut' has happened.
                [1] True, if a cut has happened, False else.
    """
    if not epsilon_transition_list: 
        return A, False
    else:
        for from_si, to_si in epsilon_transition_list:
            result.add_epsilon_transition(from_si, to_si) 
        result.delete_hopeless_states()
        return beautifier.do(result), True

