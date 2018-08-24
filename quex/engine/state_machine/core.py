from   quex.engine.misc.string_handling             import blue_print
#
from   quex.engine.misc.interval_handling           import NumberSet, Interval, \
                                                           NumberSet_All
import quex.engine.state_machine.index              as     state_machine_index
from   quex.engine.state_machine.state.core         import DFA_State
from   quex.engine.state_machine.state.single_entry import SeAccept

from   quex.engine.misc.tools  import typed, flatten_it_list_of_lists
from   quex.constants          import E_IncidenceIDs, \
                                      E_AcceptanceCondition, \
                                      E_StateIndices, \
                                      INTEGER_MAX

from   copy        import deepcopy, copy
from   operator    import itemgetter
from   itertools   import ifilter, imap
from   collections import defaultdict

class DFA(object):
    """A 'DFA', in Quex-Lingo, is a finite state automaton where all entries 
    into a state are subject to the same entry action. 

                  events
           ...   ----->---.                              .--->   ...
                           \                    .-----.-'
           ...   ----->-----+--->[ Action ]----( State )----->   ...
                           /                    '-----'
           ...   ----->---'        

    A 'DFA' must be considered in contrast to a 'FSM', a finite state machine
    where every transition into a state triggers its dedicated action.

    The term DFA comes from its closeness to the scientific definition of a
    DFA which "is a finite-state machine that accepts and rejects strings of
    symbols and only produces a unique computation of the automaton for each
    input string." (en.wikipedia.org/wiki/Deterministic_finite_automaton)

    However, a Quex-DFA-s can do more than just accept or reject patterns. They
    may count colum and line numbers, set jump positions for post-context
    pattern, or compute CRCs on the fly.
    """
    def __init__(self, InitStateIndex=None, AcceptanceF=False, InitState=None, DoNothingF=False, DfaId=None):
        if DfaId is None: self.set_id(state_machine_index.get_state_machine_id())
        else:             self.set_id(DfaId)

        if DoNothingF: return

        if InitStateIndex is None: InitStateIndex = state_machine_index.get()
        self.init_state_index = InitStateIndex
            
        # DFA_State Index => DFA_State (information about what triggers transition to what target state).
        if InitState is None: InitState = DFA_State(AcceptanceF=AcceptanceF)
        self.states = { self.init_state_index: InitState }        

    @staticmethod
    def Empty():
        """'Empty' <=> Matches nothing
                                                 .---.
                                                 |   |
                                                 '---'
        """
        return DFA()

    def is_Empty(self):
        if   len(self.states) != 1:                 return False
        elif self.get_init_state().is_acceptance(): return False
        else:                                       return True

    @staticmethod
    def Universal():
        """'Universal' <=> Matches everything      .------<-----------.
                                                 .===.                |
                                                 | A |--- any char ---'
                                                 '==='                 
        """
        result = DFA(AcceptanceF=True)
        result.add_transition(result.init_state_index, NumberSet_All(), 
                              result.init_state_index)
        return result

    def is_Universal(self):
        if len(self.states) != 1:                 
            return False
        else:
            return self.is_AcceptAllState(self.init_state_index)

    @staticmethod
    def Nothing():
        """'Nothing' <=> matches nothing, not having any transitions.
           (This DFA is inadmissible)
                                           .===.
                                           | A |
                                           '==='
                                               
        """
        return DFA(AcceptanceF=True)

    def is_Nothing(self):
        if   len(self.states) != 1:                           return False
        elif not self.get_init_state().target_map.is_empty(): return False
        elif not self.get_init_state().is_acceptance():       return False
        else:                                                 return True

    @staticmethod
    def Any():
        """'Any' <=> matches any character.
                                            .---.                 .===. 
                                            |   |--- any char --->| A |
                                            '---'                 '==='

        """
        result = DFA()
        result.add_transition(result.init_state_index, NumberSet_All(), AcceptanceF=True)
        return result

    @staticmethod
    def from_iterable(InitStateIndex, IterableStateIndexStatePairs):
        """IterableStateIndexStatePairs = list of (state_index, state) 
        """
        result = DFA(DoNothingF=True)
        result.init_state_index = InitStateIndex
        result.states = dict(IterableStateIndexStatePairs)
        return result

    @staticmethod
    def from_sequence(Sequence):
        """Sequence is a list of one of the following:
            -- NumberSet
            -- Number
            -- Character
        """
        assert type(Sequence) == list
        result = DFA()
        result.add_transition_sequence(result.init_state_index, Sequence)
        return result

    @staticmethod
    def from_character_set(CharacterSet, StateMachineId=None):
        result = DFA()
        result.add_transition(result.init_state_index, CharacterSet, AcceptanceF=True)
        if StateMachineId is not None: result.__id = StateMachineId
        return result

    @staticmethod
    def from_IncidenceIdMap(IncidenceIdMap, DfaId=None):
        """Generates a state machine that transits to states accepting specific
        incidence ids. That is from a list of (NumberSet, IncidenceId) pairs
        a state machine as the following is generated:

                        .----- set0 ---->( DFA_State 0: Accept Incidence0 )
                .-------.
                | init  |----- set1 ---->( DFA_State 1: Accept Incidence1 )
                | state |    
                '-------'                 ...

        IncidenceIdMap: 
                           incidence_id --> number set

        """
        def add(sm, StateIndex, TriggerSet, IncidenceId):
            if TriggerSet.is_empty(): return
            target_state_index = sm.add_transition(StateIndex, TriggerSet)
            target_state       = sm.states[target_state_index]
            target_state.set_acceptance()
            target_state.mark_acceptance_id(IncidenceId)

        sm = DFA(DfaId=DfaId)
        if IncidenceIdMap:
            for character_set, incidence_id in IncidenceIdMap:
                add(sm, sm.init_state_index, character_set, incidence_id)

        return sm

    def clone(self, ReplDbStateIndex=None, ReplDbPreContext=None, ReplDbAcceptance=None, 
              StateMachineId=None):
        """Clone state machine, i.e. create a new one with the same behavior,
        i.e. transitions, but with new unused state indices. This is used when
        state machines are to be created that combine the behavior of more
        then one state machine. E.g. see the function 'sequentialize'. Note:
        the state ids SUCCESS and TERMINATION are not replaced by new ones.

        RETURNS: cloned object if cloning successful
                 None          if cloning not possible due to external state references

        """
        def assert_transitivity(db):
            """Ids and their replacement remain in order, i.e. if x > y then db[x] > dv[y]."""
            if db is None: return
            prev_new = -1
            for old, new in sorted(db.iteritems(), key=itemgetter(0)): # x[0] = old value
                assert new > prev_new
                prev_new = new

        def assert_uniqueness(db):
            if db is None: return
            reference_set = set()
            for value in db.itervalues():
                assert value not in reference_set
                reference_set.add(value)

        assert_uniqueness(ReplDbStateIndex)
        assert_uniqueness(ReplDbPreContext)
        assert_uniqueness(ReplDbAcceptance)
        assert_transitivity(ReplDbAcceptance)

        if ReplDbStateIndex is None: 
            ReplDbStateIndex = dict(
                (si, state_machine_index.get())
                for si in sorted(self.states.iterkeys())
            )

        iterable = (
            (ReplDbStateIndex[si], state.clone(ReplDbStateIndex, 
                                               ReplDbPreContext=ReplDbPreContext,
                                               ReplDbAcceptance=ReplDbAcceptance))
            for si, state in self.states.iteritems()
        )
        
        result = DFA.from_iterable(ReplDbStateIndex[self.init_state_index], iterable)
        if StateMachineId is not None: result.set_id(StateMachineId)

        return result

    def normalized_clone(self, ReplDbPreContext=None):
        index_map, dummy, dummy  = self.get_state_index_normalization()
        acceptance_condition_db, \
        pattern_id_map           = self.get_pattern_and_pre_context_normalization()
        
        return self.clone(index_map, 
                          ReplDbPreContext=acceptance_condition_db, 
                          ReplDbAcceptance=pattern_id_map)

    def clone_subset(self, StartSi, StateSiSet, DfaId=None):
        """Should do the same as 'clone_from_state_subset()', replacement 
        can be made after unit tests.
        """
        correspondance_db = {
            si: state_machine_index.get() for si in StateSiSet
        }
        result = DFA(InitStateIndex=correspondance_db[StartSi], DfaId=DfaId)

        result.states = {
            # '.clone(correspondance_db)' only clones transitions to target states 
            # which are mentioned in 'correspondance_db'.
            correspondance_db[si]: self.states[si].clone(correspondance_db)
            for si in StateSiSet
        }
        
        return result

    def get_id(self):
        assert isinstance(self.__id, long) or self.__id in E_IncidenceIDs
        return self.__id  # core.id()

    def set_id(self, Value):
        assert isinstance(Value, long) or Value == E_IncidenceIDs.INDENTATION_HANDLER or Value == E_IncidenceIDs.INDENTATION_BAD
        self.__id = Value # core.set_id(Value)

    def get_init_state(self):
        return self.states[self.init_state_index]

    def get_orphaned_state_index_list(self):
        """Find list of orphan states.

        ORPHAN STATE: A state that is not connected to an init state. That is
                      it can never be reached from the init state.
        """
        work_set      = set([ self.init_state_index ])
        connected_set = set()
        while work_set:
            state_index = work_set.pop()
            # may be the 'state_index' is not even in state machine
            state       = self.states.get(state_index) 
            if state is None: continue
            connected_set.add(state_index)

            work_set.update((i for i in state.target_map.get_target_state_index_list()
                             if  i not in connected_set))

        # indices in 'connected_set' have a connection to the init state.
        # indice not in 'connected_set' do not. => Those are the orphans.

        return [ i for i in self.states.iterkeys() if i not in connected_set ]

    def get_hopeless_state_index_list(self):
        """Find list of hopeless states, i.e. states from one can never 
        reach an acceptance state. 
        
        HOPELESS STATE: A state that cannot reach an acceptance state.
                       (There is no connection forward to an acceptance state).
        """
        from_db = self.get_from_db()

        work_set     = set(  self.get_acceptance_state_index_list() 
                           + self.get_bad_lexatom_detector_state_index_list())
        reaching_set = set()  # set of states that reach acceptance states
        while len(work_set) != 0:
            state_index = work_set.pop()
            reaching_set.add(state_index)

            work_set.update((i for i in from_db[state_index] if  i not in reaching_set))

        # indices in 'reaching_set' have a connection to an acceptance state.
        # indice not in 'reaching_set' do not. => Those are the hopeless.
        return [ i for i in self.states.iterkeys() if i not in reaching_set ]

    def get_epsilon_closure_db(self):
        db = {}
        for index, state in self.states.items():
            # Do the first 'level of recursion' without function call, to save time
            index_list = state.target_map.get_epsilon_target_state_index_list()

            # Epsilon closure for current state
            ec = set([index]) 
            if len(index_list) != 0: 
                for target_index in ifilter(lambda x: x not in ec, index_list):
                    ec.add(target_index)
                    self.__dive_for_epsilon_closure(target_index, ec)

            db[index] = ec

        return db

    def get_epsilon_closure_of_state_set(self, TargetStateIndiceDb, EC_DB):
        """Returns the epsilon closure of a set of states, i.e. the union
           of the epsilon closures of the single states.
           
           StateIdxList: List of states to be considered.
           EC_DB:        Epsilon closure database, as computed once by
                         'get_epsilon_closure_db()'.
        """
        result = set()
        for index in TargetStateIndiceDb.iterkeys():
            result.update(EC_DB[index])
        return result

    def get_epsilon_closure(self, StateIdx):
        """Return all states that can be reached from 'StateIdx' via epsilon
           transition."""
        assert self.states.has_key(StateIdx)

        result = set([StateIdx])

        self.__dive_for_epsilon_closure(StateIdx, result)

        return result
 
    def acceptance_state_iterable(self):
        return [ 
            (si, state) 
            for si, state in self.states.iteritems() if state.is_acceptance() 
        ]

    def get_acceptance_state_list(self):
        return [ 
            state 
            for state in self.states.itervalues() if state.is_acceptance() 
        ]

    def acceptance_id_set(self):
        return set(flatten_it_list_of_lists( 
            state.acceptance_id_set() for state in self.states.itervalues() 
            if state.is_acceptance() 
        ))

    def is_plain_bad_lexatom_detector(self):
        init_state = self.get_init_state()
        if       init_state is None:                   return False
        if       init_state.has_transitions():         return False
        elif not init_state.is_bad_lexatom_detector(): return False
        else:                                          return True

    def get_bad_lexatom_detector_state_index_list(self):
        """At the time of this writing, BAD_LEXATOMs are implemented as states 
        accepting 'BAD_LEXATOM' and performing a transition upon drop-out.
        Bad-lexatom detector states are not 'hopeless' states, so this function
        is there to collect them.
        """
        return [ 
            index for index, state in self.states.iteritems() 
                  if state.is_bad_lexatom_detector() 
        ]

    def get_acceptance_state_index_list(self, AcceptanceID=None):
        if AcceptanceID is None:
            return [ 
                index for index, state in self.states.iteritems() 
                      if state.is_acceptance() 
            ]

        return [ 
            index for index, state in self.states.iteritems() 
                  if     state.is_acceptance() 
                     and state.single_entry.has_acceptance_id(AcceptanceID) 
        ]

    def get_to_db(self):
        """RETURNS:
                    map:    state_index --> states which it enters
        """
        return dict(
            (from_index, set(state.target_map.get_map().iterkeys()))
            for from_index, state in self.states.iteritems()
        )

    def get_from_db(self):
        """RETURNS:
                    map:     state_index --> states from which it is entered.
        """
        from_db = defaultdict(set)
        for from_index, state in self.states.iteritems():
            for to_index in state.target_map.get_target_state_index_list():
                from_db[to_index].add(from_index)
        return from_db

    def get_successors(self, SI):
        """RETURNS: State indices of all successor states of 'SI' 
                    including 'SI' itself.
        """
        work_set = set([SI])
        result   = set([SI])
        while work_set:
            state          = self.states[work_set.pop()]
            target_si_list = state.target_map.get_target_state_index_list()
            work_set.update(
                target_si 
                for target_si in target_si_list if target_si not in result
            )
            result.update(target_si_list)
        return result

    def get_predecessors(self, SI):
        """RETURNS: State indices of all predecessor states of 'SI' 
                    including 'SI' itself.
        HINT: If this function is to be called multiple times, better generate
              a 'predecessor_db' and interview the database.
        """
        predecessor_db = self.get_predecessor_db()
        return predecessor_db[SI] + [SI]
    
    def get_predecessor_db(self):
        """RETURNS:
        
            map:   state index ---> set of states that lie on the path to it.

        PROOF: 
            
        (1) Whenever a transition from B to A is entered, the predecessor set
        of A receives all known predecessors of B and B itself as predecessor.

        (2) Every predecessor set containing A is extended by the B and its 
        predecessors. Thus, ALL states containing A in their known predecessors
        receive the newly known predecessors of A.

        (3) Since, at the end all predecessor relationships are treated, all 
        known relationships are entered and all precessors are 'connected'.
        """
        def update(predecessor_db, StateIndex, PredecessorSet):
            """Enter into the 'predecessor_db' that all states in 'PredecessorSet'
            are predecessors of 'StateIndex'. Also, all states of which the 
            StateIndex is a predecessor, inherit its predecessors.
            """
            predecessor_db[StateIndex].update(PredecessorSet)
            for prev_predecessor_set in predecessor_db.itervalues():
                if StateIndex not in prev_predecessor_set: continue
                prev_predecessor_set.update(PredecessorSet)
                    
        predecessor_db = defaultdict(set)
        for si, state in self.states.iteritems():
            target_predecessor_set = copy(predecessor_db[si])
            target_predecessor_set.add(si)
            for target_si in state.target_map.get_map().iterkeys():
                update(predecessor_db, target_si, target_predecessor_set)

        return predecessor_db

    def get_successor_db(self, HintPredecessorDb=None):
        """RETURNS:

            map:   state index ---> set of states on the path from init state to this state.

        The algorithm takes the result from 'get_predecessor_db' and inverts it.
        """
        if not HintPredecessorDb:
            HintPredecessorDb = self.get_predecessor_db()

        successor_db = defaultdict(set)
        for si, predecessor_set in HintPredecessorDb.iteritems():
            for predecessor_si in predecessor_set:
                successor_db[predecessor_si].add(si)
        return successor_db

    def get_number_set(self):
        """Returns a number set that represents the state machine.
        If the state machine cannot be represented by a plain NumberSet,
        then it returns 'None'.

        Assumes: DFA is 'beautified'.
        """
        if len(self.states) != 2:
            return None

        # There can be only one target state from the init state
        target_map = self.get_init_state().target_map.get_map()
        if len(target_map) != 1:
            return None

        return target_map.itervalues().next()

    def get_beginning_character_set(self):
        """Return the character set union of all triggers in the init state.
        """
        return self.get_init_state().target_map.get_trigger_set_union()

    def get_ending_character_set(self):
        """Returns the union of all characters that trigger to an acceptance
           state in the given state machine. This is to detect whether the
           newline or suppressor end with an indentation character (grid or space).
        """
        result = NumberSet()
        for end_state_index in self.get_acceptance_state_index_list():
            for state in self.states.itervalues():
                if state.target_map.has_target(end_state_index) == False: continue
                result.unite_with(state.target_map.get_trigger_set_to_target(end_state_index))
        return result

    def get_state_index_normalization(self, NormalizeF=True):
        index_map         = {}
        inverse_index_map = {}

        index_sequence = self.__get_state_sequence_for_normalization()
        if NormalizeF:
            counter = -1L
            for state_i in index_sequence:
                counter += 1L
                index_map[state_i]         = counter
                inverse_index_map[counter] = state_i
        else:
            for state_i in index_sequence:
                index_map[state_i]         = state_i
                inverse_index_map[state_i] = state_i

        return index_map, inverse_index_map, index_sequence

    def get_pattern_and_pre_context_normalization(self, PreContextID_Offset=None, 
                                                  AcceptanceID_Offset=None):

        acceptance_condition_set_set = set()
        acceptance_id_set            = set()
        for state in self.states.itervalues():
            for cmd in state.single_entry.get_iterable(SeAccept):
                acceptance_condition_set_set.add(cmd.acceptance_condition_set())
                acceptance_id_set.add(cmd.acceptance_id())
                
        def enter(db, Value, TheEnum, NewId):
            if Value in TheEnum: db[Value] = Value; return NewId
            else:                db[Value] = NewId; return NewId + 1

        i = 1L
        repl_db_acceptance_condition_id = {}
        for acceptance_condition_set in sorted(acceptance_condition_set_set):
            for acceptance_condition_id in acceptance_condition_set:
                i = enter(repl_db_acceptance_condition_id, acceptance_condition_id, E_AcceptanceCondition, i)

        i = 1L
        repl_db_acceptance_id  = {}
        for acceptance_id in sorted(acceptance_id_set):
            i = enter(repl_db_acceptance_id, acceptance_id, E_IncidenceIDs, i)

        return repl_db_acceptance_condition_id, \
               repl_db_acceptance_id

    def get_string(self, NormalizeF=False, Option="utf8", OriginalStatesF=True):
        assert Option in ["utf8", "hex"]

        # (*) normalize the state indices
        index_map, inverse_index_map, index_sequence = self.get_state_index_normalization(NormalizeF)

        # (*) construct text 
        msg = "init-state = " + repr(index_map[self.init_state_index]) + "\n"
        for state_i in index_sequence:
            printed_state_i = index_map[state_i]
            state           = self.states[state_i]
            try:    state_str = "%05i" % printed_state_i
            except: state_str = "%s"   % printed_state_i
            msg += "%s%s" % (state_str, state.get_string(index_map, Option, OriginalStatesF))

        return msg

    def get_graphviz_string(self, NormalizeF=False, Option="utf8"):
        assert Option in ["hex", "utf8"]

        # (*) normalize the state indices
        index_map, inverse_index_map, index_sequence = self.get_state_index_normalization(NormalizeF)

        # (*) Border of plot block
        frame_txt  = "digraph state_machine_%i {\n" % self.get_id()
        frame_txt += "rankdir=LR;\n"
        frame_txt += "size=\"8,5\"\n"
        frame_txt += "node [shape = doublecircle]; $$ACCEPTANCE_STATES$$\n"
        frame_txt += "node [shape = circle];\n"
        frame_txt += "$$TRANSITIONS$$"
        frame_txt += "}\n"

        transition_str       = ""
        acceptance_state_str = ""
        for printed_state_i, state in sorted(imap(lambda i: (index_map[i], self.states[i]), index_sequence)):
            if state.is_acceptance(): 
                acceptance_state_str += "%i; " % int(printed_state_i)
            transition_str += state.get_graphviz_string(printed_state_i, index_map, Option)

        if acceptance_state_str != "": acceptance_state_str = acceptance_state_str[:-2] + ";"
        return blue_print(frame_txt, [["$$ACCEPTANCE_STATES$$", acceptance_state_str ],
                                      ["$$TRANSITIONS$$",       transition_str]])
        
    def __get_state_sequence_for_normalization(self):

        result     = []
        work_stack = [ self.init_state_index ]
        done_set   = set()
        while len(work_stack) != 0:
            i = work_stack.pop()
            if i in done_set: continue

            result.append(i)
            done_set.add(i)
            state = self.states[i]

            # Decide which target state is to be considered next.
            # sort by 'lowest trigger'
            def comparison_key(state_db, tm, A):
                trigger_set_to_A = tm.get(A)
                assert trigger_set_to_A is not None
                trigger_set_min = trigger_set_to_A.minimum()
                target_tm       = state_db[A].target_map.get_map()
                target_branch_n = len(target_tm)
                if len(target_tm) == 0: target_tm_min = -INTEGER_MAX
                else:                   target_tm_min = min(map(lambda x: x.minimum(), target_tm.itervalues()))
                return (trigger_set_min, target_branch_n, target_tm_min, A)

            tm = state.target_map.get_map()
            target_state_index_list = [ k for k in tm.iterkeys() if k not in done_set ]
            target_state_index_list.sort(key=lambda x: comparison_key(self.states, tm, x), reverse=True)

            work_stack.extend(target_state_index_list)
                                         
        # There might be 'orphans' which are not at all connected. Append them
        # sorted by a simple rule: by state index.
        if len(self.states) != len(result):
            for i in sorted(self.states.iterkeys()):
                if i in result: continue
                result.append(i)

        # DEBUG: double check that the sequence is complete
        x = self.states.keys(); x.sort()  # DEBUG
        y = deepcopy(result);   y.sort()  # DEBUG
        assert x == y                     # DEBUG

        return result

###    def has_cycles(self):
###        for si, predecessor_si_list in self.get_predecessor_db():
###            if si in predecessor_si_list: return True
###        return False

    def longest_path_to_first_acceptance(self):
        """Find the longest path to first acceptance state.

        'First acceptance state' is an acceptance state which can be
        reached without passing by another acceptance state.

        This function is useful for pre-contexts, where the arrival at
        the first acceptance state is sufficient. With the longest path
        possible to such a state a reasonable 'fallback number' can be
        determined, i.e. the number of lexatoms to maintain inside the
        buffer upon reload.

        RETURNS: Number of lexatoms to reach the first acceptance state.
                 None, if path is not unique.
        """
        worklist   = [(self.init_state_index, 0, set([self.init_state_index]))]
        max_length = -1
        while worklist:
            si, length, predecessor_set = worklist.pop()
            if self.states[si].is_acceptance():
                if length > max_length: max_length = length
                # NOT: si -> done_set, otherwise the acceptance could not be 
                #                      entered from elsewhere.
                # NOT: successors -> worklist, because anything behind the 
                #                              acceptance state is meaningless.
            else:
                new_predecessor_set = predecessor_set.copy()
                new_predecessor_set.add(si)
                for target_si in self.states[si].target_map.get_map().iterkeys():
                    if target_si in predecessor_set: return None
                    worklist.append((target_si, length+1, new_predecessor_set))

        if max_length == -1: return None
        else:                return max_length

    def iterable_init_state_transitions(self):
        for target_si, trigger_set in self.get_init_state().target_map:
            yield target_si, trigger_set

    def clean_up(self):
        # Delete states which are not connected from the init state.
        self.delete_orphaned_states()
        # Delete states from where there is no connection to an acceptance state.
        self.delete_hopeless_states() 

    def delete_orphaned_states(self):
        """Remove all orphan states.

        ORPHAN STATE: A state that is not connected to an init state. That is
                      it can never be reached from the init state.
        """
        for state_index in self.get_orphaned_state_index_list():
            if state_index == self.init_state_index: continue
            self.states.pop(state_index)

    def delete_hopeless_states(self):
        """Delete all hopeless states and transitions to them.

        HOPELESS STATE: A state that cannot reach an acceptance state.
                       (There is no connection forward to an acceptance state).
        """
        hopeless_si_set = set(self.get_hopeless_state_index_list())
        concerned_state_list = [
            state
            for si, state in self.states.iteritems()
            if si not in hopeless_si_set or si == self.init_state_index
        ]
        for hl_si in hopeless_si_set:
            for state in concerned_state_list:
                state.target_map.delete_transitions_to_target(hl_si)
            if hl_si == self.init_state_index: continue
            self.states.pop(hl_si)
        return 

    def delete_transitions_on_number(self, Number):
        """This function deletes any transition on 'Value' to another
           state. The resulting orphaned states are deleted. The operation
           may leave orphaned states! They need to be deleted manually.
        """
        for state in self.states.itervalues():
            # 'items()' not 'iteritems()' because 'delete_transitions_to_target()'
            # may change the dictionaries content.
            for target_state_index, trigger_set in state.target_map.get_map().items():
                assert not trigger_set.is_empty()
                if not trigger_set.contains(Number): continue

                trigger_set.cut_interval(Interval(Number))
                # If the operation resulted in cutting the path to the target state, 
                # => then delete it.
                if trigger_set.is_empty():
                    state.target_map.delete_transitions_to_target(target_state_index)

        return

    def delete_transitions_beyond_interval(self, MaskInterval):
        """Removes any transitions beyond the specified 'MaskInterval' from the DFA.
        """
        for from_si, state in self.states.items():
            target_map = state.target_map.get_map()
            for to_si, number_set in target_map.items():
                number_set.mask_interval(MaskInterval)
                if number_set.is_empty(): del target_map[to_si]

    def __dive_for_epsilon_closure(self, state_index, result):
        index_list = self.states[state_index].target_map.get_epsilon_target_state_index_list()
        for target_index in ifilter(lambda x: x not in result, index_list):
            result.add(target_index)
            self.__dive_for_epsilon_closure(target_index, result)

    def is_DFA_compliant(self):
        for state in self.states.values():
            if state.target_map.is_DFA_compliant() == False: 
                return False
        return True

    def is_AcceptAllState(self, StateIndex):
        """RETURNS: True,  if the state accepts and iterates on every character to
                           itself.
                    False, else.
        """
        state = self.states[StateIndex]
        if not state.is_acceptance():     return False

        tm = state.target_map.get_map()
        if len(tm) != 1:                  return False

        target_index, trigger_set = tm.iteritems().next()
        if   target_index != StateIndex:  return False
        elif not trigger_set.is_all():    return False
        else:                             return True

    def has_transition_to(self, TargetIndex):
        return any(state.target_map.has_target(TargetIndex)
                   for state in self.states.itervalues())

    def has_orphaned_states(self):
        """Detect whether there are states where there is no transition to them."""
        unique = set([])
        for state in self.states.values():
            unique.update(state.target_map.get_target_state_index_list())

        return any(state_index not in unique and state_index != self.init_state_index
                   for state_index in self.states.iterkeys())

    def has_acceptance_condition(self, AccConditionId):
        return any(AccConditionId in state.acceptance_condition_set()
                   for state in self.states.itervalues())

    def has_specific_acceptance_id(self):
        return any(state.single_entry.has_specific_acceptance_id()
                   for state in self.states.itervalues())

    def create_new_init_state(self, AcceptanceF=False):
        self.init_state_index = self.create_new_state()
        return self.init_state_index

    def create_new_state(self, AcceptanceF=False, StateIdx=None, RestoreInputPositionF=False, 
                         MarkAcceptanceId=None):
        """RETURNS: DFA_State index of the new state.
        """
        if StateIdx is None: new_si = state_machine_index.get()
        else:                new_si = StateIdx

        new_state = DFA_State(AcceptanceF or MarkAcceptanceId is not None)
        if MarkAcceptanceId is not None:
            new_state.mark_acceptance_id(MarkAcceptanceId)
            if RestoreInputPositionF:
                new_state.set_read_position_restore_f()

        self.states[new_si] = new_state
        return new_si
        
    @typed(StartStateIdx=long, AcceptanceF=bool)
    def add_transition(self, StartStateIdx, TriggerSet, TargetStateIdx = None, AcceptanceF = False):
        """Adds a transition from Start to Target based on a given Trigger.

           TriggerSet can be of different types: ... see add_transition()
           
           (see comment on 'DFA_State::add_transition)

           RETURNS: The target state index.
        """
        # NOTE: The Transition Constructor is very tolerant, so no tests on TriggerSet()
        #       assert TriggerSet.__class__.__name__ == "NumberSet"
        assert type(TargetStateIdx) == long or TargetStateIdx is None or TargetStateIdx in E_StateIndices

        # If target state is undefined (None) then a new one has to be created
        if TargetStateIdx is None:                       TargetStateIdx = state_machine_index.get()
        if self.states.has_key(StartStateIdx) == False:  self.states[StartStateIdx]  = DFA_State()        
        if self.states.has_key(TargetStateIdx) == False: self.states[TargetStateIdx] = DFA_State()
        if AcceptanceF:                                  self.states[TargetStateIdx].set_acceptance(True)

        self.states[StartStateIdx].add_transition(TriggerSet, TargetStateIdx)

        return TargetStateIdx
            
    def add_transition_sequence(self, StartIdx, Sequence, AcceptanceF=True):
        """Add a sequence of transitions which is ending with acceptance--optionally.
        """
        idx = StartIdx
        for x in Sequence:
            idx = self.add_transition(idx, x)
        if AcceptanceF:
            self.states[idx].set_acceptance(True)

    def add_epsilon_transition(self, StartStateIdx, TargetStateIdx=None, RaiseAcceptanceF=False):
        assert TargetStateIdx is None or type(TargetStateIdx) == long

        # create new state if index does not exist
        if not self.states.has_key(StartStateIdx):
            self.states[StartStateIdx] = DFA_State()
        if TargetStateIdx is None:
            TargetStateIdx = self.create_new_state(AcceptanceF=RaiseAcceptanceF)
        elif not self.states.has_key(TargetStateIdx):
            self.states[TargetStateIdx] = DFA_State()

        # add the epsilon target state
        self.states[StartStateIdx].target_map.add_epsilon_target_state(TargetStateIdx)     
        # optionally raise the state of the target to 'acceptance'
        if RaiseAcceptanceF: self.states[TargetStateIdx].set_acceptance(True)

        return TargetStateIdx

    def mark_state_origins(self, OtherStateMachineID=-1L):
        """Marks at each state that it originates from this state machine. This is
           important, when multiple patterns are combined into a single DFA and
           origins need to be traced down. In this case, each pattern (which is
           are all state machines) needs to mark the states with the state machine 
           identifier and the state inside this state machine.

           If OtherStateMachineID and StateIdx are specified other origins
              than the current state machine can be defined (useful for pre- and post-
              conditions).         
        """
        assert type(OtherStateMachineID) == long or OtherStateMachineID in E_IncidenceIDs

        if OtherStateMachineID == -1L: state_machine_id = self.__id
        else:                          state_machine_id = OtherStateMachineID

        for state_idx, state in self.states.items():
            state.mark_acceptance_id(state_machine_id)

    def mount_to_acceptance_states(self, MountedStateIdx, 
                                   CancelStartAcceptanceStateF=True):
        """Mount on any acceptance state the MountedStateIdx via epsilon transition.
        """
        for state_idx, state in self.acceptance_state_iterable():
            # -- only handle only acceptance states
            # -- only consider state other than the state to be mounted
            if state_idx == MountedStateIdx: continue
            # add the MountedStateIdx to the list of epsilon transition targets
            state.target_map.add_epsilon_target_state(MountedStateIdx)
            # if required (e.g. for sequentialization) cancel the acceptance status
            if CancelStartAcceptanceStateF: 
                # If there was a condition to acceptance => Cancel it first
                state.set_acceptance_condition_id(None) 
                state.set_acceptance(False)

    def replace_target_indices(self, ReplacementDict):
        for state in self.states.itervalues():
            state.target_map.replace_target_indices(ReplacementDict)

    def filter_dominated_origins(self):
        for state in self.states.values(): 
            state.single_entry.delete_dominated()

    @typed(Sequence=list)
    def apply_sequence(self, Sequence, StopAtBadLexatomF=True):
        """RETURNS: Resulting target state if 'Sequence' is applied on 
                    state machine.

           This works ONLY on DFA!
        """
        si = self.init_state_index
        for x in Sequence:
            si = self.states[si].target_map.get_resulting_target_state_index(x)
            if si is None: return None
            elif self.states[si].has_acceptance_id(E_IncidenceIDs.BAD_LEXATOM):
                break
        return self.states[si]

    def iterable_target_state_indices(self, StateIndex):
        return self.state_db[StateIndex].iterable_target_state_indices(StateIndex)

    def __repr__(self):
        return self.get_string(NormalizeF=True)

    def assert_consistency(self):
        """Check: -- whether each target state in contained inside the state machine.
        """
        state_indice_set = set(self.states.iterkeys())
        for state in self.states.itervalues():
            assert state_indice_set.issuperset(state.target_map.get_target_state_index_list())

    def assert_range(self, Range):
        for state in self.states.itervalues():
            for number_set in state.target_map.get_map().itervalues():
                number_set.assert_range(Range.minimum(), Range.least_greater_bound())
           
