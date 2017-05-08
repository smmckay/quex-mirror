# TODO: Draw relation to Powerset Construction: 
#       "https://en.wikipedia.org/wiki/Powerset_construction"
#
# (C) Frank-Rene Schaefer
#from   quex.engine.state_machine.core                 import DFA
#from   quex.engine.state_machine.state.core           import DFA_State
from   quex.engine.state_machine.state.target_map_ops import get_elementary_trigger_sets
from   quex.engine.state_machine.index                import map_state_combination_to_index

def do(SM, Class_StateMachine=None, Class_State=None):
    """Creates a deterministic finite automaton (DFA) from a state machine 
    - which may be a NFA (non-deterministic finite automaton). 
    
    This is a generalized version of the 'subset construction' algorithm. Where
    subsection construction focuses on letters of an alphabet for the
    investigation of transitions, this algorithm focuses on elementary trigger
    sets. A very good description of the subset construction algorithm can be
    found in 'Engineering a Compiler' by Keith Cooper.
    """
    Class_StateMachine = SM.__class__
    Class_State        = SM.get_init_state().__class__

    # (*) create the result state machine
    initial_state_epsilon_closure = SM.get_epsilon_closure(SM.init_state_index) 

    # (*) initial state of resulting DFA = epsilon closure of initial state of NFA
    #     -- add the command list of all states in the epsilon closure
    InitState = Class_State.from_state_iterable(
                           SM.states[i] for i in initial_state_epsilon_closure)

    # NOTE: 
    # DFAs with an initial acceptance state are conceivable!  In a
    # 'define' section building bricks of patterns may be defined that 'accept
    # nothing'. Those 'building bricks' may use nfa_to_dfa here, too.  
    #
    # (A pattern state machine for pattern matching, of course, has to disallow 
    #  'accept nothing'.)
    result = Class_StateMachine(InitState=InitState)
                          
    # (*) prepare the initial worklist
    worklist = [ ( result.init_state_index, initial_state_epsilon_closure) ]

    epsilon_closure_db = SM.get_epsilon_closure_db()

    while worklist:
        # 'start_state_index' is the index of an **existing** state in the state machine.
        # It was either created above, in DFA's constructor, or as a target
        # state index.
        start_state_index, start_state_combination = worklist.pop()
 
        # (*) compute the elementary trigger sets together with the 
        #     epsilon closure of target state combinations that they trigger to.
        #     In other words: find the ranges of characters where the state triggers to
        #     a unique state combination. E.g:
        #                Range        Target DFA_State Combination 
        #                [0:23]   --> [ State1, State2, State10 ]
        #                [24:60]  --> [ State1 ]
        #                [61:123] --> [ State2, State10 ]
        #
        elementary_trigger_set_infos = get_elementary_trigger_sets(start_state_combination,
                                                                   SM, epsilon_closure_db)
        ## DEBUG_print(start_state_combination, elementary_trigger_set_infos)

        # (*) loop over all elementary trigger sets
        for epsilon_closure_of_target_state_combination, trigger_set in elementary_trigger_set_infos.iteritems():
            #  -- if there is no trigger to the given target state combination, then drop it
            if trigger_set.is_empty(): continue

            # -- add a new target state representing the state combination
            #    (if this did not happen yet)
            target_state_index = \
                 map_state_combination_to_index(epsilon_closure_of_target_state_combination)

            # -- if target state combination was not considered yet, then create 
            #    a new state in the state machine
            if not result.states.has_key(target_state_index):
                # create the new target state in the state machine
                result.states[target_state_index] = \
                    Class_State.from_state_iterable(
                        SM.states[i] 
                        for i in epsilon_closure_of_target_state_combination)

                worklist.append((target_state_index, 
                                 epsilon_closure_of_target_state_combination))  

            # -- add the transition 'start state to target state'
            result.add_transition(start_state_index, trigger_set, target_state_index)

    return result 


if False:
    # TODO: NFA-To-DFA: Use DFA +  Epsilon Transition Database.
    # 
    #       => Results are ONLY DFAs.
    #       => No epsilon transition in states and/or state machines.
    #
    def new_do(StateDb, EpsilonTranstionDb):
        """StateDb:             state index --> DFA_State
        
               Describes DFA states and their indices.

           EpsilonTranstionDb:  source state index --> target state index

               Describes added epsilon transitions between the states give by source
               and target.
        """

    def new_get_epsilon_closure_db(StateDb, EpsilonTranstionDb):
        db = {}
        for si, state in StateDb.items():
            # Do the first 'level of recursion' without function call, to save time
            index_list = EpsilonTranstionDb[si] 

            # Epsilon closure for current state
            ec = set([si]) 
            if len(index_list) != 0: 
                for target_index in filter(lambda x: x not in ec, index_list):
                    ec.add(target_index)
                    state.__dive_for_epsilon_closure(EpsilonTranstionDb, target_index, ec)

            db[si] = ec

        return db

    def new_dive_for_epsilon_closure(EpsilonTranstionDb, StateIndex, result):
        index_list = EpsilonTranstionDb[StateIndex]
        for target_index in filter(lambda x: x not in result, index_list):
            result.add(target_index)
            result.new_dive_for_epsilon_closure(target_index, result)

