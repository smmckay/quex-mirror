from   quex.engine.state_machine.core                 import DFA
from   quex.engine.state_machine.state.core           import DFA_State
import quex.engine.state_machine.algebra.reverse      as     reverse
from   quex.engine.state_machine.algebra.intersection import state_index_for_combination
from   quex.engine.state_machine.state.target_map_ops import get_intersection_line_up_2
import quex.engine.state_machine.algorithm.beautifier as     beautifier
import quex.engine.state_machine.index                as     index
from   quex.engine.misc.tree_walker                   import TreeWalker
from   quex.engine.misc.tools                         import r_enumerate
from   quex.constants                                 import E_StateIndices

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
    result = DfaA
    cut_f  = True
    while cut_f:
        cut_f = False
        for si in result.states:
            result_backup = result
            result, cut_f = __cut_begin_core(result, DfaB, A_begin_state_index=si)
            if cut_f: break
            result = result_backup
    return result

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
    result, cut_f = __cut_begin_core(A, B)
    return result

def __cut_begin_core(A, B, A_begin_state_index=None):
    """RETURN: [0] Resulting DFA
               [1] True, if cut has been performed; False else.
    """
    A.assert_consistency() 
    B.assert_consistency() 
    assert    A_begin_state_index is None \
           or A_begin_state_index in A.states

    class WorkList:
        def __init__(self, A_begin_state_index, B_init_state_index):
            self.work_list      = []
            self.state_setup_db = {}
            self.A_begin_state_index = A_begin_state_index
            self.B_init_state_index  = B_init_state_index

        def pop(self):
            return self.work_list.pop()

        def add(self, A_si, B_si, FirstF=False):
            if     A_si == self.A_begin_state_index \
               and B_si == E_StateIndices.BEFORE_PATH_WALK: 
                B_si = self.B_init_state_index

            # print "   #after:", A_si, B_si
            
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
        if B_si not in (E_StateIndices.AFTER_PATH_WALK, E_StateIndices.BEFORE_PATH_WALK):
            B_state = B.states.get(B_si)
            result = get_intersection_line_up_2((A_state.target_map, 
                                                 B_state.target_map))
            return ((x[0], x[1], y) for x, y in result.iteritems())
        else:
            return ((target_si, None, trigger_set) 
                    for target_si, trigger_set in A_state.target_map.get_map().iteritems())


    if B.is_Empty(): 
        result, si_correspondance_db = A.clone_and_get_correspondance_db()
        return result, False
    elif A_begin_state_index is None:
        A_begin_state_index = A.init_state_index 

    work_list      = WorkList(A_begin_state_index, B.init_state_index)
    result_init_si = work_list.add(A.init_state_index, 
                                   E_StateIndices.BEFORE_PATH_WALK)
    result         = DFA(InitStateIndex = result_init_si, 
                         AcceptanceF    = A.states[A.init_state_index].is_acceptance())

    epsilon_transition_list = []
    cut_f                   = False
    # print "-----------------"
    # print "A:", A.get_string(NormalizeF=False)
    # print "Begin:", A_begin_state_index
    # print "B:", B.get_string(NormalizeF=False)
    while not work_list.done():
        result_si, A_si, B_si = work_list.pop()
        assert A_si is not None
        assert B_si is not None
        # print "#B_si", B_si

        # print "#result, etc:", result_si, A_si, B_si
        for A_target_si, B_target_si, trigger_set in target_map_line_up(A, A_si, B, B_si):
            # print "   %s --> %s %s" % (trigger_set, A_target_si, B_target_si)
            # State index = 'None' => state does not transit on 'trigger_set'.
            if A_target_si is None: 
                continue

            elif B_target_si is None:
                if B_si == E_StateIndices.BEFORE_PATH_WALK:
                    B_target_si = E_StateIndices.BEFORE_PATH_WALK
                else:
                    B_target_si = E_StateIndices.AFTER_PATH_WALK

            elif B.states[B_target_si].is_acceptance():
                result_target_si = work_list.add(A_target_si, B_target_si)
                # Transition in 'B' to acceptance => result *must* drop-out!
                # Cutting = lexemes starting at the target are acceptable.
                #           => merge with init state.
                #           => must again consider cutting matches with 'B'.
                new_result_target_si = work_list.add(A_target_si, B.init_state_index,
                                                     FirstF=True)
                epsilon_transition_list.append(new_result_target_si)
                cut_f = True
                # print "   cut"
                continue

            result_target_si = work_list.add(A_target_si, B_target_si)
            acceptance_f = A.states[A_target_si].is_acceptance()

            result.add_transition(result_si, trigger_set, result_target_si,
                                  AcceptanceF = acceptance_f)
            # print "   add", A_target_si, B_target_si

    result_begin_state_index,_ = work_list.get_result_state_index(A_begin_state_index, 
                                                                  B.init_state_index)
    for si in epsilon_transition_list:
        # print "#eps:", result_begin_state_index, si
        result.add_epsilon_transition(result_begin_state_index, si)

    result.delete_hopeless_states()

    cut_f = len(epsilon_transition_list) != 0
    return beautifier.do(result), cut_f

