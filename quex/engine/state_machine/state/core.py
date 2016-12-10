from   quex.engine.state_machine.state.single_entry import SingleEntry, \
                                                           SeAccept, \
                                                           SeStoreInputPosition
from   quex.engine.state_machine.state.target_map   import TargetMap
from   quex.engine.misc.tools import typed 
from   quex.constants         import E_PreContextIDs, \
                                     E_IncidenceIDs

class State:
    """A state consisting of ONE entry and multiple transitions to other
    states.  One entry means that the exact same actions are applied upon state
    entry, independent from where the state is entered.

           ...   ----->---.                               .--->   ...
                           \                     .-----.-'
           ...   ----->-----+--->[ StateOp ]----( State )----->   ...
                           /                     '-----'
           ...   ----->---'        

    Transitions are of two types:
    
     -- normal transitions: Happen when an input character fits a trigger set.
     -- epsilon transition: Happen without any input.
    
    Collections of states connected by transitions build a StateMachine. States 
    may be used in NFA-s (non-deterministic finite state automatons) and DFA-s
    (deterministic finite state automatons). Where NFA-s put no restrictions on
    transitions, DFA-s do. A state in a DFA has the following properties:
    
       -- Trigger sets of normal transitions do not intersect.
       -- There are no epsilon transitions. 

    Whether or not a state complies to the requirements of a DFA can be checked
    by '.is_DFA_compliant()'.
    """
    @typed(AcceptanceF=bool, CloneF=bool)
    def __init__(self, AcceptanceF=False, CloneF=False):
        """Contructor of a State, i.e. a aggregation of transitions.
        """
        if CloneF: return

        self.__target_map   = TargetMap()
        self.__single_entry = SingleEntry()
        if AcceptanceF: self.set_acceptance()

    def clone(self, ReplDbStateIndex=None, ReplDbPreContext=None, ReplDbAcceptance=None):
        """Creates a copy of all transitions, but replaces any state index with the ones 
           determined in the ReplDbStateIndex."""
        assert ReplDbStateIndex is None or isinstance(ReplDbStateIndex, dict)
        result = State(CloneF=True)
        result.__target_map   = self.__target_map.clone(ReplDbStateIndex)
        result.__single_entry = self.__single_entry.clone(ReplDbPreContext=ReplDbPreContext,
                                                          ReplDbAcceptance=ReplDbAcceptance)

        return result

    @staticmethod
    def from_state_iterable(StateList):
        """Does not set '.__target_map'
        """
        result = State()
        result.__target_map   = TargetMap()
        result.__single_entry = SingleEntry() 
        result.__single_entry.merge_list(state.single_entry for state in StateList)
        return result

    @property
    def single_entry(self):
        return self.__single_entry

    def set_single_entry(self, Other):
        self.__single_entry = Other

    @property
    def target_map(self):
        return self.__target_map

    @staticmethod
    def interference(StateList):
        """RETURNS: True, if either the single_entry objects differ.
                          Or, if the transition maps intersect.
                    False, else.
        """
        if len(StateList) < 1: 
            return False
        prototype = StateList[0]
        for s in StateList[1:]:
            if not s.__single_entry.is_equal(prototype.__single_entry):
                return True

        prototype_tsu = prototype.target_map.get_trigger_set_union()
        for s in StateList[1:]:
            tsu = s.target_map.get_trigger_set_union()
            if tsu.has_intersection(prototype_tsu):
                return True
            prototype_tsu.unite_with(tsu)
        
        # All single_entry operations are equal.
        # No transition trigger set intersects.
        # => no interference!
        return False

    def has_transitions(self):
        return not self.target_map.is_empty()

    def is_acceptance(self):
        cmd = self.single_entry.find(SeAccept) 
        if cmd is None: return False 
        return not any(cmd.acceptance_id() == E_IncidenceIDs.BAD_LEXATOM
                       for cmd in self.single_entry)

    def get_highest_precedence_acceptance_id(self):
        """RETURNS: incidence_id of the highest non-E_IncidenceIDs pattern
                                 that matches in this state.
                    None, else.
        """
        return self.single_entry.get_highest_precedence_acceptance_id()

    def input_position_store_f(self):
        return self.single_entry.find(SeStoreInputPosition) is not None

    def input_position_restore_f(self):
        for cmd in self.single_entry:
            if cmd.__class__ != SeAccept: continue
            elif cmd.restore_position_register_f(): return True
        return False

    def pre_context_id(self):
        cmd = self.single_entry.find(SeAccept)
        if cmd is None: return E_PreContextIDs.NONE
        else:           return cmd.pre_context_id()

    def set_pre_context_id(self, Value=True):
        accept_cmd = self.single_entry.find(SeAccept)
        assert accept_cmd is not None
        accept_cmd.set_pre_context_id(Value)

    def set_acceptance(self, Value=True):
        if Value: self.single_entry.add_Op(SeAccept)
        else:     self.single_entry.remove_Op(SeAccept)

    def has_specific_acceptance_id(self):
        return any(cmd.acceptance_id() != E_IncidenceIDs.MATCH_FAILURE 
                   for cmd in self.single_entry)

    def set_specific_acceptance_id(self, AcceptanceID):
        """Sets a specific acceptance id, but does not modify the 'store input
        position' behavior. 
        """
        accept_cmd = self.single_entry.find(SeAccept)
        if accept_cmd is None:
            self.single_entry.add_Op(SeAccept)
            accept_cmd = self.single_entry.find(SeAccept)
        accept_cmd.set_acceptance_id(AcceptanceID)

    def mark_acceptance_id(self, AcceptanceID):
        for cmd in self.single_entry:
            if not hasattr(cmd, "set_acceptance_id"): continue
            cmd.set_acceptance_id(AcceptanceID)

    def has_acceptance_id(self, AcceptanceID):
        return any(cmd.acceptance_id() == AcceptanceID 
                   for cmd in self.single_entry)

    def accepts_incidence(self):
        return any(cmd.acceptance_id() in E_IncidenceIDs
                   for cmd in self.single_entry)

    def set_read_position_restore_f(self, Value=True):
        accept_cmd = self.single_entry.find(SeAccept)
        assert accept_cmd is not None
        accept_cmd.set_restore_position_register_f()

    def set_read_position_store_f(self, Value=True):
        if Value: self.single_entry.add_Op(SeStoreInputPosition)
        else:     self.single_entry.remove_Op(SeStoreInputPosition)

    def add_transition(self, Trigger, TargetStateIdx): 
        self.__target_map.add_transition(Trigger, TargetStateIdx)

    def get_string(self, StateIndexMap=None, Option="utf8", OriginalStatesF=True):
        # if information about origins of the state is present, then print
        se_str = self.single_entry.get_string(OriginalStatesF)
        # print out transitionts
        tm_str = self.target_map.get_string("    ", StateIndexMap, Option)
        return " %s%s" % (se_str, tm_str)

    def get_graphviz_string(self, OwnStateIdx, StateIndexMap, Option):
        assert Option in ["hex", "utf8"]
        return self.target_map.get_graphviz_string(OwnStateIdx, StateIndexMap, Option)

    def __repr__(self):
        return self.get_string()
