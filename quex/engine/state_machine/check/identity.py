from quex.constants  import E_AcceptanceCondition
from quex.engine.state_machine.core import DFA

class Checker:
    def __init__(self, SM0, SM1):
        """Checks whether the set of patterns matched by SM0 is identical to the
           set of patterns matched by SM1.

           RETURNS: 'True'  if so,
                    'False' if not.
        """
        self.sm1 = SM1
        self.sm0 = SM0
        self.visited_state_index_db = {}

    def do(self):
        return self.__dive(self.sm1.init_state_index, [self.sm0.init_state_index])

    def __dive(self, SM1_StateIndex, SM0_StateIndexList):
        """SM1_StateIndex:     state index in SM1

           SM0_StateIndexList: list of states in the 'sm0 set' state machine that
                               was reached by the same trigger set as SM1_StateIndex.      
                               They are the set of states that can 'mimik' the current
                               state indexed by 'SM1_StateIndex'.
        """
        # (*) Determine the states behind the indices
        sm1_state      = self.sm1.states[SM1_StateIndex]
        sm0_state_list = map(lambda index: self.sm0.states[index], SM0_StateIndexList)
        #     Bookkeeping
        self.visited_state_index_db[SM1_StateIndex] = True
        #     Union of all triggers were the 'mimiking' sm0 states trigger.
        #     (For speed considerations, keep it in prepared, so it does not have to 
        #      be computed each time it is required.)
        sm0_trigger_set_union_db = {} 
        for index in SM0_StateIndexList:
            sm0_trigger_set_union_db[index] = self.sm0.states[index].target_map.get_trigger_set_union()

        sm1_trigger_set_union = sm1_state.target_map.get_trigger_set_union()

        # (*) Here comes the condition:
        #
        #     For every trigger (event) in the 'sm1 state' that triggers to a follow-up state
        #     there must be pendant triggering from the mimiking 'sm0 states'.
        #
        #     That is: 
        #     -- No 'mimiking sm0 state' is allowed to trigger on something beyond
        #        the trigger_set present on sm1, and vice versa.
        for index in SM0_StateIndexList:
            if not sm0_trigger_set_union_db[index].is_equal(sm1_trigger_set_union): 
                return False

        #     -- All 'mimiking sm0 states' must trigger on the given trigger_set to 
        #        a subsequent state of the same 'type' as the 'sm1 state'.
        for target_index, trigger_set in sm1_state.target_map.get_map().items():
            target_state = self.sm1.states[target_index]

            # (*) Collect the states in the 'sm0' that can be reached via the 'trigger_set'
            sm0_target_state_index_list = []
            for sm0_state in sm0_state_list:
                for index in sm0_state.target_map.get_resulting_target_state_index_list(trigger_set):
                    if index in sm0_target_state_index_list: continue
                    sm0_target_state_index_list.append(index)

            # (*) If there is one single state in the collection of follow-up states in sm0
            #     that has not the same type as the target state, then 'sm0' and 'sm1' are 
            #     not identical.
            if not self.__correspondance(target_state, sm0_target_state_index_list): 
                return False

            # (*) No need to go along loops, do not follow paths to states already visited.
            if not self.visited_state_index_db.has_key(target_index):
                if self.__dive(target_index, sm0_target_state_index_list) == False: return False

        # If the condition held for all sub-pathes of all trigger_sets then we can reports
        # that the currently investigated sub-path supports the claim that 'sm1 sm' is a
        # sub set state machine of 'sm0 sm'.
        return True

    def __correspondance(self, S1, S0List):
        """Checks whether all states in SList are of the same type as S0. 
           (With respect to the criteria of out algorithm.)
        """
        for index in S0List:
            S0 = self.sm0.states[index] # core of the 'sm0' state

            if       S0.is_acceptance() \
                 !=  S1.is_acceptance():                                      return False
            elif    (S0.acceptance_condition_id() == E_AcceptanceCondition.NONE) \
                 != (S1.acceptance_condition_id() == E_AcceptanceCondition.NONE):            return False
            elif    (S0.acceptance_condition_id() == E_AcceptanceCondition.BEGIN_OF_LINE) \
                 != (S1.acceptance_condition_id() == E_AcceptanceCondition.BEGIN_OF_LINE):   return False
            elif    (S0.acceptance_condition_id() == E_AcceptanceCondition.BEGIN_OF_STREAM) \
                 != (S1.acceptance_condition_id() == E_AcceptanceCondition.BEGIN_OF_STREAM): return False
            elif     S0.input_position_store_f() \
                 !=  S1.input_position_store_f():                             return False
            elif     S0.input_position_restore_f() \
                 !=  S1.input_position_restore_f():                           return False

        return True

def do(A, B):
    """Assumption: post context are already mounted on core state machines.
    """
    if isinstance(A, DFA):
        assert isinstance(B, DFA)
        return Checker(A, B).do()

    assert not isinstance(B, DFA)

    # Check whether A and B are identical, i.e they match 
    # exactly the same patterns and provide exactly the same behavior of the 
    # lexical analyzer.
    if not Checker(A.sm, B.sm).do(): return False

    A_pre_context = A.get_pre_context_generalized()
    B_pre_context = B.get_pre_context_generalized()

    if A_pre_context is None:
        if B_pre_context is None: 
            return True
        else:
            return False # One depends on pre-context, the other not
    else:
        if B_pre_context is None: 
            return False # One depends on pre-context, the other not
        else:
            return Checker(A_pre_context, B_pre_context).do()


