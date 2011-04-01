"""
Track Analysis

(C) 2011 Frank-Rene Schaefer
===============================================================================

The goal of track analysis is to profit from the static relations of 
states inside the state machine, so that the run-time effort can be 
reduced. At the end of the process, each state is decorated with a
set of attributes. They indicate how the state is to be implemented 
as source code.

The implementation of the state has the following basic elements:

*-----------------------------------------------------------------------------*

   Input:           Access the input character.

   SuccessorInfo:   [OPTIONAL] Store information to be used by successor states.

   TriggerMap:      All triggers that transit on a character to specific 
                    successor state.

   DropOut:         Handle the case that input character does not trigger in
                    trigger map.

*-----------------------------------------------------------------------------*

Accordingly, each state will be represented by a new 'state' consisting
of four objects:

    .input          <-- class Input
    .successor_info <-- class SuccessorInfo
    .trigger_map    <-- list of pairs (interval, target_state_index)
    .drop_out       <-- class DropOut

The following sections elaborate on the these objects and how they have
to perform. The classes 'Input', 'SuccessorInfo' and 'DropOut' allow
to access the information that resulted from the track analyzis. After
reading the following, review their class interfaces.
_____________________
                     |
Acceptance Detection |__________________________________________________________
---------------------'

The following discussion shows how these elements are configured. Consider
the simple state machine:

      ( 1 )-- 'a' -->( 2 )-- 'b' -->(( 3 ))
                                          "ab"

Is says that state 1 transits on 'a' to state 2. State 2 transits on 'b'
to state 3. State 3 is an acceptance state that indicates that pattern "ab" 
has been matched. This state machine can be implemented as follows:

        State1:
            /* Input */            input = *input_p;   
            /* TransitionBlock */  if( input == 'a' ) goto State2;
            /* DropOut */          goto Failure;

        State2:
            /* Input */            ++input_p;
                                   input = *input_p;   
            /* TransitionBlock */  if( input == 'b' ) goto State3;
            /* DropOut */          goto Failure;

        State2:
            /* Input */            ++input_p;
            /* DropOut */          goto Terminal('ab');

The following rules can already be derived:

*-----------------------------------------------------------------------------*

  Input:   (1) The init state does not increment the input_p,

           (2) If the state is the terminal of a post-context pattern
               without further transitions, then the input position
               is set to the end of the core pattern. Thus, it does
               not need to be incremented.

           (3) All other states increment/decrement the input position.

  DropOut: 
           (3) if no pattern ever matched the drop-out must be 'goto Failure'.

           (4) if the state is an acceptance state, then the drop-out must
               be 'goto Terminal;' where 'Terminal' is the address of the 
               action code that relates to the matching pattern.

  General: (5) When a terminal is reached, the input **must** point to the
               next character to be analyzed, i.e. one after the last
               character that matched!
*-----------------------------------------------------------------------------*

A somewhat more complicated state machine may be the following:

    ( 1 )-- 'a' -->(( 2 ))-- 'b' -->( 3 )-- 'c' -->(( 4 ))
                         "a"                             "abc"

Here, state 2 looks different since it is an acceptance state and contains a
transition on 'b' to state 3. However, with the above rules it still behaves as
expected. If something different from 'b' arrives, then the input pointer
stands on the position right after the matched character 'a' and we transit to
the terminal of pattern "a". 

State 3 is interesting. If no 'c' is detected then, still, pattern "a" has
matched already. So, state 3 can actually goto Terminal("a"), but the input
position must be decreased by 1 so that it points directly behind the matched
character "a". A new rule can be stated about the DropOut:

*-----------------------------------------------------------------------------*

   DropOut: (6) If a state itself is not an acceptance state, but some
                state before it is an acceptance state, then 
               
                  (6.1) set the input pointer back to the position 
                        where the last acceptance state matched.
                  (6.2) goto the terminal of the last acceptance
                        state.

*-----------------------------------------------------------------------------*

In the case above, the resetting of the input pointer is trivial. Now, 
consider the state machine
                                     'd'
                                    ,---.
                                    \   /
    ( 1 )-- 'a' -->(( 2 ))-- 'b' -->( 3 )-- 'c' -->(( 4 ))
                         "a"                             "abc"

Now, an arbitrary number of 'd's may occur before state 3 drops out.  This
requires, that state 2 must store the acceptance position and state 3 must
reset the acceptance position from a variable. Two new rules:

*-----------------------------------------------------------------------------*

  SuccessorInfo: (7) If there is a non-acceptance successor state 
                     that is reached via a path of arbitrary length 
                     (i.e. there is a loop somewhere), then the 
                     acceptance position must be stored in a variable
                     'last_acceptance_position'.

  DropOut: (8.1) For a non-acceptance state; If the path from the last 
                 acceptance state to this state is of arbitrary length, 
                 then the input position must be set to what 
                 'last_acceptance_position' indicated.

           (8.2) The same is true, if the state can be reached by multiple
                 acceptance states that have a different distance to this 
                 state.

*-----------------------------------------------------------------------------*

An even more complicated case may be mentioned here:

    ( 1 )-- 'a' -->(( 5 ))-- 'b' ---.
       \                 "a|abc"     \
        \                             \
         `-- 'b' -->(( 2 ))-- 'b' -->( 3 )-- 'c' -->(( 4 ))
                          "b"                             "a|abc"

The pattern "a|abc" wins in state 5 and state 4. Pattern "b" wins in state 2.
Now, it cannot be said upfront what pattern has matched if state 3 is reached.
Thus, the acceptance state must store information about the acceptance:

*-----------------------------------------------------------------------------*

    SuccessorInfo: (9) If there is a non-acceptance successor that
                       can be reached from different acceptance states,
                       then the state must store the information about
                       the acceptance in a variable 'last_acceptance'.

    DropOut: (10) For non-acceptance state; If the state can be reached
                  by different acceptance states, or if there are preceding 
                  acceptance states and a path without acceptance, then the 
                  terminal store in 'last_acceptance' must be entered.

*-----------------------------------------------------------------------------*

_____________________
                     |
Pre-Contexts         |__________________________________________________________
---------------------'

Note, that 'Acceptance' may be dependent on pre-contexts, that is the
acceptance of a state generally is determined by a sequence of checks:

    if     ( pre_context[...] ) acceptance X
    else if( pre_context[...] ) acceptance Y
    else                        acceptance Z

where X has higher priority than Y and Y has higher priority than Z. Z is the
highest priority pattern without pre-context. All pre-context dependent
acceptance states are neglected because they are dominated by Z. 

Pre-context flags, however, are constant as soon as the forward lexical
analysis starts. Thus, the comparison of two acceptance chains is enough to
judge whether the acceptance of two states is equivalent. Now, consider the
state machine:

      ( 1 )-- 'a' -->( 2 )-- 'b' -->( 3 )-- 'c' -->(( 4 ))
                                                         "xyz/abc/"

which means that pattern "abc" must be preceded by pattern "xyz" in order to
match. All successor acceptance states of state 1, though, depend on the
pre-context "xyz". Thus, state 1 could actually drop-out immediately if the
pre-context is not met. It is not necessary to transit through states 2, 3, and
4 to find out finally, that pattern "xyz/abc/" fails because of the
pre-context. A new rule can be defined

*-----------------------------------------------------------------------------*

   SuccessorInfo: (11) If all successor acceptance states depend on 
                       a certain pre-context flag being raised, then
                       the first state on that path can drop-out 
                       on the condition that the pre-context is not met.

   Terminal:      (12) When a terminal is reached where the pathes took 
                       care of the pre-context checks, then there is no
                       need to check it again in the terminal.

*-----------------------------------------------------------------------------*

_____________________
                     |
Post-Contexts        |__________________________________________________________
---------------------'

Post contexts are patterns that must be present after the core pattern.  When
the end of the post-context matches, then end of the lexeme must be set to the
end of the core pattern. Example:


      ( 1 )-- 'a' -->( 2 )-- 'b' -->( 3 )-- ':' -->(( 4 ))
                                      S("abc")           "abc/:"

That is pattern "abc" must be followed by ":". After the match, though, the
analysis starts with ':' not with what comes after it. If a post-contexted
patten is matched the position of the end of the core pattern must be 
restored. Similar to the acceptance discussion about new rules can 
be introduced:

*-----------------------------------------------------------------------------*

   SuccessorInfo: (13) If the length of the path from the end-of-core-pattern
                       to the final end-of-post context is arbitrary (due to
                       loops), then the input position of the end-of-core
                       pattern must be stored in a variable 'post_context_position[i]'.

   DropOut: (14) If the match is the end of a post context, then the position
                 of the core pattern needs to be restored.

               (14.1) If the distance to the end of the core pattern can be 
                      determined statically, then the input position is decremented
                      accordingly.

               (14.2) Else, the input position must be set to what is indicated
                      by variable 'post_context_position[i]'.
               
*-----------------------------------------------------------------------------*

Note, that it is not necessary to store what core pattern has matched, since
the fact that the end of the core pattern has been reached testifies what
core pattern is passed. Further, if there are multiple post-context
with the same core-patterns, then the 'post_context_position' can be shared,
if is stored in exactly the same states.

*-----------------------------------------------------------------------------*

    General: (15) post-constext that store their input positions in exactly
                  the same states can share their post_context_position 
                  variable.

*-----------------------------------------------------------------------------*

_____________________
                     |
Lexeme Start Pointer |__________________________________________________________
---------------------'

[[ This needs some clarification: What happens, if no acceptance state is
   reached then? OnFailure would expect that the input position is 
   lexeme_start_p + 1. This is impossible if it is reset at reload.
]]

On reload, in general, the current lexeme must be maintained so that is 
can be accessed in the pattern-action. However, if for a state it 
can be determined that no successor acceptance state cares about the lexeme,
then the lexeme start pointer can be set to the current input position. 
This allows to quickly skip large 'comment' section that span regions that
are even bigger than the current input buffer size. 

A new rule concerning the reload behavior can be defined:

    OnReload:

    (16) If no successor acceptance state 'cares' about the lexeme and
         a 'dont-care' acceptance state has been passed, then then reload
         can set the lexeme_start_p to the current input position and 
         reload the buffer from start.

    (17) All non-acceptance states that immediately follow a 'skipper
         state' must cause 'skip-failure' on drop-out.
"""
from quex.input.setup import setup as Setup
from copy import copy

class Input:
    def __init__(self, AcceptanceInfo):
        self.__move_input_position = None
        self.__immediate_drop_out_if_not_pre_context_list = None

    def move_input_position(self):
        """ 1   --> increment by one before dereferencing
           -1   --> decrement by one before dereferencing
            0 --> neither increment nor decrement.
        """
        return self.__move_input_position

    def immediate_drop_out_if_not_pre_context_list(self):
        """If all successor states require the list of given
           pre-contexts, then the state can check whether 
           at least one of them is hit. Otherwise, it 
           could immediately drop out.
        """
        return self.__immediate_drop_out_if_not_pre_context_list

    def set_move_input_position(self, Value):
        self.__move_input_position = Value


class SuccessorInfo:
    def __init__(self):
        self.__store_acceptance_f          = None
        self.__store_acceptance_position_f = False

    def store_acceptance_f(self):
        """Acceptance to be stored upon entry in this function.
           True  --> store acceptance information
           False  --> no acceptance is to be stored.
        """
        return self.__store_acceptance

    def store_acceptance_position_f(self):
        """True  --> position needs to be stored in last_acceptance.
           False --> position does not need to be stored in last_acceptance.

           This may influence, the way that the acceptance object is
           interpreted. For example, if the acceptance requires a pre-context
           to be fulfilled, the last_acceptance is stored inside the 
           pre-context if-block.
        """
        return self.__store_acceptance_position_f

    def store_post_context_position_list(self):
        """[]   --> No post contexts related to the state.
           List --> list of integers that indicate that the current state needs 
                    to store

                            post_context_position[i] = input_p

                    for all 'i' in List.
        """
        return self.__post_context_index_list

    def set_store_acceptance_f(self, Value):
        assertt type(Value) == AcceptanceCondition
        self.__store_acceptance_f = Value

    def set_store_acceptance_position_f(self)
        self.__store_acceptance_position_f = True

class DropOut:
    def modify_input_position(self):
        """Integer --> move input position forward/backward
                       according to integer.
           None    --> restore 'last_acceptance_position'.
                       or, goto 'post_context_position[i]'
                       where 'i' is returned by 
                       'post_context_index()'
        """
        pass

    def post_context_index(self):
        """None    --> State has nothing to do with post contexts
           Integer --> Index of the post context that is to
                       be used for 'post_context_position[i]' when
                       the end of the core pattern is restored.
        """
        pass

    def goto_terminal(self):
        """None          --> goto 'last_acceptance'.
           AcceptanceObj --> ...
        """
        pass


class AcceptanceCondition:
    def __init__(self, PatternID, PreContextID, PreContextBeginOfLineF):
        # PatternID                   => ID of the pattern that accepts.
        # PreContextID                => pre-context that must be fulfilled so that 
        #                                pattern id is the winner. 
        #                   == -1     => no pre-context
        # PreContextBeginOfLineF      
        #                   == True   => For the acceptance PatternID
        #                                The begin of line must be fulfilled
        #                   == False  => no begin of line condition
        #
        # The normal case of a pattern without pre-context and begin-of-line 
        # condition is the (N, -1, False), where N is some integer.
        self.pattern_id                  = PatternID
        self.pre_context_id              = PreContextID
        self.pre_context_begin_of_line_f = PreContextBeginOfLineF

class AcceptanceConditionList:
    def __init__(self, OriginList=None):
        LanguageDB = Setup.language_db

        if OriginList == None:  # Acceptance = Failure
            self.__info = []
            return

        origin_list = OriginList.get_list()
        origin_list.sort()
        # Store information about the 'acceptance behavior' of a state.
        # 
        #    len(self.__info) == 0 --> state is not an acceptance state at all
        #    self.__info[i]
        self.__info = []
        for origin in origin_list:
            if not origin.is_acceptance(): continue

            info = AcceptanceCondition(origin.state_machine_id,
                                       origin.pre_context_id(),
                                       origin.pre_context_begin_of_line_f())
            
            self.__info.append(info)

            # If an unconditioned acceptance occurred, then no further consideration
            # is necessary.
            if     origin.pre_context_id()              == -1 \
               and origin.pre_context_begin_of_line_f() == False:
                break

    def is_failure(self):
        return len(self.__info) == 0

    def is_unconditioned_acceptance(self):
        if   len(self.__info) != 1:                 return False
        elif self.__info[0].pre_context_id != -1:   return False
        elif self.__info[0].pre_context_id == True: return False
        return True

    def __eq__(self, Other):
        if not isinstance(Other, AcceptanceConditionList): return False
        return self.__info == Other.__info

    def __repr__(self):
        if len(self.__info) == 0: return "Failure"
        txt = []
        for acceptance in self.__info:
            txt.append("(A = %i; pre-context = %i, begin_of_line=%s), " % 
                       (acceptance.pattern_id, acceptance.pre_context_id, 
                        repr(acceptance.pre_context_begin_of_line_f)))
        return "".join(txt)


class TrackInfo:
    def __init__(self, DSM):
        """SM -- state machine to be investigated.  """
        self.__sm = DSM.sm()

        # (1) Analyze recursively in the state machine:
        #     -- Collect states that are part of a loop in the state machine.
        #        If a path from state A to state B contains one of those states,
        #        then the number of transitions that appear between A and B 
        #        can only be determined at run-time.
        self.__loop_states = set([])
        #     -- Acceptance Database.
        #        Store for each state the information about what acceptance 
        #        states lie on the way to it. Further store the path, so
        #        that later on it can be determined whether the number of 
        #        transitions can be determined beforehand.
        self.__acceptance_db = {}
        #     -- post context configurations
        #        If multiple post-contexts share the same core pattern, then they
        #        can share the 'post_context_position[i]' variable. The following
        #        data structure stores pairs of 
        #
        #         (state index list that store input position) , (list of related post contexts)
        self.__post_context_configurations = self.__post_context_storage_configurations()

        #     Dive to get the information above.
        self.__dive(self.__sm.init_state_index, []) 

        # (2) Acceptance Determination
        #     -- The database that maps:  state_index --> (Acceptance, TransitionsNSinceAcceptance)
        #
        #        Acceptance --> An object carrying information about the 
        #                       acceptance of the state.
        #
        #        TransitionsNSinceAcceptance --> Number of transitions (passed characters) since 
        #                                        the last acceptance state.
        #                                        == None --> undetermined
        #                                        == -1   --> new input position = 1 after lexeme begin
        #                                        == int  --> number of characters since acceptance
        self.__db = {}

        #     -- Sets that keep track of necessity to store acceptance and/or acceptance position
        self.__acceptance_states_with_necessity_to_store_last_acceptance          = set([])
        self.__acceptance_states_with_necessity_to_store_last_acceptance_position = set([])

        #     Analyze to build the databases mentioned above.
        self.__determine_database()

        # (3) Adorn each state in the state machine with acceptance information
        for state_index, state in self.__sm.states.iteritems():

            acceptance = self.__acceptance_db[state_index]

            # -- On State Entry (before any transition)
            input = Input()
            if state_index in self.__acceptance_states_with_necessity_to_store_last_acceptance:
                assert state.is_acceptance()
                info = self.__acceptance_db[state_index]
                assert len(info) == 1
                input.set_store_acceptance_f(self.__db[state_index][0])

            if state_index in self.__acceptance_states_with_necessity_to_store_last_acceptance_position:
                input.set_store_acceptance_position_f(True)
            
            on_entry_begin_of_post_context_list = []
            for origin in state.origins().get_list(): 
                if not origin.is_end_of_post_contexted_core_pattern(): continue
                # Assumption about origin based on assumption about single pattern state machine:
                #
                #    According to 'setup_post_context.py' (currently line 121) no acceptance
                #    state of a post context can store the input position. This has been made 
                #    impossible! Otherwise, the post context would have zero length.
                #
                #    Post-conditions via backward search, i.e. pseudo ambiguous post conditions,
                #    are a different ball-game.
                assert origin.is_acceptance() == False

                # Store current input position, to be restored when post condition really matches
                post_context_index = DSM.get_post_context_index(origin.state_machine_id)
                on_entry_begin_of_post_context_list.append(post_context_index)

            # -- On Drop-Out (no transition triggered)
            on_drop_out_acceptance, on_drop_out_adjust_input_position = self.__db[state_index]

            state.acceptance_tracer = AcceptanceInfo(on_entry_store_acceptance, 
                                                     on_entry_store_acceptance_position_f,
                                                     on_entry_begin_of_post_context_list,
                                                     on_drop_out_acceptance,
                                                     on_drop_out_adjust_input_position)

    def __acceptance_db_add(self, LastAcceptanceStateInde, PathSinceLastAcceptance):
        self.__acceptance_db.setdefault(StateIndex, []).append((LastAcceptanceStateIndex, 
                                                                copy(PathSinceLastAcceptance)))

    def __dive(self, StateIndex, path, last_acceptance_state_index=-1, path_since_last_acceptance=[]):
        assert type(path) == list

        state = self.__sm.states[StateIndex]
        if state.is_acceptance(): 
            last_acceptance_state_index = StateIndex
            path_since_last_acceptance  = []

        for origin in state.origins().get_list():
            if origin.is_end_of_post_contexted_core_pattern():
                post_context_id = origin.post_context_id()
                last_post_context_id[post_context_id]   = True
                last_post_context_path[post_context_id] = []

        if StateIndex in path:
            # All states in the detected loop must be marked as being part of
            # a recursion. Thus, if a path contains any one of those states the
            # distance cannot be determined.
            idx = path.index(StateIndex)
            self.__loop_states.update(path[idx:])
            return

        # Add the information that the current state has a path where the last acceptance
        # lies n transitions backward.
        self.__acceptance_db_add(last_acceptance_state_index, path_since_last_acceptance)

        path.append(StateIndex)
        path_since_last_acceptance.append(StateIndex)

        for state_index in state.transitions().get_target_state_index_list():
            self.__dive(state_index, path, last_acceptance_state_index, path_since_last_acceptance)

    def __determine_database(self):
        def _get_transition_n_since_last_acceptace(InfoList):
            # If any state on the path is element of a recursive cycle, then
            # the distance to the last acceptance is not definite
            n = None
            for info in InfoList:
                path_from_last_acceptance_state = info[1]
                for state_index in path_from_last_acceptance_state:
                    if state_index in self.__loop_states:
                        return None

                if   n == None:                                 n = len(path_from_last_acceptance_state) 
                elif n != len(path_from_last_acceptance_state): return None

            return n

        def _get_common_acceptance(InfoList):
            acceptance = None
            for info in InfoList:
                acceptance_state_index = info[0]

                if acceptance_state_index == -1: # Failure
                    acceptance_obj = AcceptanceConditionList()
                else:
                    state = self.__sm.states[acceptance_state_index]
                    acceptance_obj = AcceptanceConditionList(state.origins())

                if   acceptance == None:           acceptance = acceptance_obj
                elif acceptance != acceptance_obj: return None

            return acceptance
                   
        # Determine for each state whether the acceptance is definite
        for state_index, state in self.__sm.states.iteritems():
            if state.is_acceptance(): 
                # The last acceptance state is the state itself and the last 
                # acceptance position lies zero characters backward.
                self.__db[state_index] = (AcceptanceConditionList(state.origins()), 0)
                continue

            info = self.__acceptance_db[state_index]
            #    = list of pairs (AcceptanceStateIndex, Path from AcceptanceStateIndex to state_index)

            acceptance = _get_common_acceptance(info)
            if acceptance == None:
                # Note, for any acceptance state involved, that there is a successor that 
                # has undetermined acceptance. Thus, this acceptance state needs to be stored.
                self.__acceptance_states_with_necessity_to_store_last_acceptance.update(map(lambda x: x[0], info))

                # Acceptance can only be determined at run-time. It cannot be determined
                # by the transition structure.
                transition_n_since_last_acceptance = None

            elif acceptance.is_failure():
                # If acceptance == Failure, then the new input position is one behind
                # the current lexeme start.
                transition_n_since_last_acceptance = -1

            else:
                # All information about acceptance points to the same pattern.
                # Thus, try to determine if distance to those states backward is
                # all the same.
                transition_n_since_last_acceptance = _get_transition_n_since_last_acceptace(info)

            if transition_n_since_last_acceptance == None:
                self.__acceptance_states_with_necessity_to_store_last_acceptance_position.update(map(lambda x: x[0], info))

            self.__db[state_index] = (acceptance, transition_n_since_last_acceptance)

    def __post_context_position_store_conifigurations(self):
        """Determine the groups of post contexts that store their input
           positions at the same set of states.
        """

        # post context id --> list of states where the input position is to be stored.
        db = {}
        for index, state in self.__sm.iteritems():
            for origin in state.origins().get_list():
                if origin.store_input_position_f():
                    db.setdefault(origin.origin.post_context_id(), []).append(index)

        # Combine those post contexts that share the same set of states where 
        # positions are to be stored.
        group_list = []
        for post_context_id, state_index_list in db.iteritems():
            # See whether there is already a group with the same state index list
            for group in group_list:
                if db[group[0]] == state_index_list: 
                    group.append(post_constex_id)
                    break
            else:
                # Build your own group
                group_list.append([post_context_id])

        self.__post_context_group_list = group_list




class AcceptanceInfo:
    def __init__(self, 
                 OnEntryAcceptance,   
                 OnEntryStoreInputPositionF,
                 OnEntryBeginOfPostContextList, 
                 OnDropOutAcceptance, 
                 OnDropOutAdjustInputPosition):

        assert    OnEntryAcceptance == None \
               or isinstance(OnEntryAcceptance, AcceptanceConditionList)
        assert type(OnEntryStoreInputPositionF) == bool
        assert    OnDropOutAcceptance == None \
               or isinstance(OnDropOutAcceptance, AcceptanceConditionList)
        assert    OnDropOutAdjustInputPosition       == None \
               or type(OnDropOutAdjustInputPosition) == int
        assert type(OnEntryBeginOfPostContextList) == list

        self.__on_entry_store_acceptance           = OnEntryAcceptance
        self.__on_entry_store_input_position_f     = OnEntryStoreInputPositionF
        self.__on_entry_begin_of_post_context_list = OnEntryBeginOfPostContextList
        #
        self.__on_drop_out_acceptance              = OnDropOutAcceptance
        self.__on_drop_out_adjust_input_position   = OnDropOutAdjustInputPosition

    def on_entry_store_acceptance(self):
        """None                    -- Do not store any acceptance.
           AcceptanceConditionList -- Object containing information about how to store
                                      acceptance.
        """
        return self.__on_entry_store_acceptance

    def on_entry_store_input_position_f(self):
        """True,  if all successor states have a distinct acceptance
                  that can be determined from the state machine structure.
                  Then, no storage of the acceptance in an acceptance
                  variable is necessary.
           False, if there are subsequent states that are of void 
                  acceptance that can only be determined at run-time.
                  Then, the 'last_acceptance' variable is required.
        """
        return self.__on_entry_store_input_position_f

    def on_entry_store_begin_of_post_context_position_list(self):
        return self.__on_entry_store_begin_of_post_condition_list

    def on_drop_out_acceptance(self):
        """None                 -- Acceptance cannot be determined based on the
                                   structure of the state machine. At run-time 
                                   it must be restored what is saved in variable
                                   'last_acceptance'.
           AcceptanceConditionList -- Object containing information about acceptance.
        """
        return self.__on_drop_out_acceptance

    def on_drop_out_adjust_input_position(self):
        """None    -- Acceptance position undetermined. Restore what is 
                      stored in 'last_acceptance_position'.
           integer -- number of characters to go forward/backward to set 
                      the input right after the last acceptance position.

           NOTE: This function is not to be called if the drop-out acceptance
                 is FAILURE. In that case, the input position is always set
                 to lexeme start + 1.
        """
        assert    self.__on_drop_out_acceptance              == None \
               or self.__on_drop_out_acceptance.is_failure() == False

        return self.__on_drop_out_adjust_input_position

    def on_reload_maintain_lexeme_start_pointer(self, StateIndex):
        """If an acceptance has been passed, that does not care about the
           lexeme and if all subsequent possible acceptance states do not care
           about the lexeme, the lexeme start pointer bended. On reload, the
           lexeme start does not have to lie inside the buffer and, therefore are
           larger section can be reloaded.
        """
        return True

    def __repr__(self):
        txt = []
        txt.append("OnEntry:   store acceptance      = %s;\n" % repr(self.on_entry_store_acceptance()))
        txt.append("           store input position  = %s;\n" % repr(self.on_entry_store_input_position_f()))
        txt.append("OnDropOut: acceptance            = %s;\n" % repr(self.on_drop_out_acceptance()))
        if      self.on_drop_out_acceptance() != None \
            and self.on_drop_out_acceptance().is_failure():
            txt.append("           adjust input position = <set to lexeme start + 1>;\n")
        else:
            txt.append("           adjust input position = %s;\n" % repr(self.on_drop_out_adjust_input_position()))
        return "".join(txt)
