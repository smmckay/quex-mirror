# (C) Frank Rene Schaefer
import quex.output.core.state_machine_coder       as     state_machine_coder
import quex.output.core.state_router              as     state_router_generator
from   quex.output.core.variable_db               import variable_db
from   quex.engine.analyzer.door_id_address_label import DoorID, \
                                                         DialDB
import quex.output.core.reload_state              as     reload_state_coder
import quex.engine.analyzer.engine_supply_factory as     engine
from   quex.engine.analyzer.terminal.core         import Terminal
import quex.engine.analyzer.core                  as     analyzer_generator

from   quex.engine.misc.tools import typed
from   quex.blackboard        import E_IncidenceIDs, \
                                     setup as Setup, \
                                     Lng

# MAIN:      sm --> analyzer
#            sm_txt --> code_analyzer
#            terminal_txt --> code_terminals
#
# PRE_SM:    pre_sm --> analyzer
#            pre_sm_txt --> code_analyzer
#            terminal = begin of core
#
# BIPD_SM-s: bipd_sm -> analyzer
#            bipd_sm_txt -> code_analyzer
#            termina = terminal for which BIPD operated
#
# COUNT_SM:  count_db --> count_sm
#            analyzer  = get_analyzer
#            modify analyzer
#            terminal = exit_door_id
#
# SKIPER_SM:
#
# RANGE_SKIPPER_SM:
#
# NESTER_RANGE_SKIPPER_SM:
#
# INDENTATION_DETECTOR_SM:

def do_main(SM, ReloadStateForward, dial_db):
    """Main pattern matching state machine (forward).
    ---------------------------------------------------------------------------
    Micro actions are: line/column number counting, position set/reset,
    last acceptance setting/reset, lexeme start pointer set/reset, setting
    terminating zero for lexeme/reset, setting last character. 

            DropOut     --> FAILURE
            BLC         --> ReloadStateForward
            EndOfStream --> END_OF_STREAM

    Variables (potentially) required:

            position, PositionRegisterN, last_acceptance, input.
    """
    txt, analyzer = __do_state_machine(SM, engine.Class_FORWARD(), ReloadStateForward, 
                                       dial_db)

    if analyzer.last_acceptance_variable_required():
        variable_db.require("last_acceptance")

    # Treat the external reload state the same way as if it was generated
    # along the process.
    analyzer.reload_state_extern_f = False

    return txt, analyzer

def do_pre_context(SM, PreContextSmIdList, dial_db):
    """Pre-context detecting state machine (backward).
    ---------------------------------------------------------------------------
    Micro actions are: pre-context fullfilled_f

            DropOut     --> Begin of 'main' state machine.
            BLC         --> ReloadStateBackward
            EndOfStream --> 'error'

    Variables (potentially) required:

            pre_context_fulfilled_f[N] --> Array of flags for pre-context
                                           indication.
    RETURNS: [0] generated code text
             [1] reload state BACKWARD, to be generated later.
    """

    if SM is None: 
        return [], None

    txt, analyzer = __do_state_machine(SM, engine.BACKWARD_PRE_CONTEXT) 

    txt.append("\n%s" % Lng.LABEL(DoorID.global_end_of_pre_context_check(dial_db)))
    # -- set the input stream back to the real current position.
    #    during backward lexing the analyzer went backwards, so it needs to be reset.
    txt.append("    %s\n" % Lng.INPUT_P_TO_LEXEME_START())

    for sm_id in PreContextSmIdList:
        variable_db.require("pre_context_%i_fulfilled_f", Index = sm_id)

    variable_db.require("input") 

    return txt, analyzer

def do_backward_read_position_detectors(BipdDb):
    """RETURNS: [0] Code for BIPD analyzer
                [1] map: acceptance_id --> DoorID of entry into BIPD

    The 'bipd_entry_door_id_db' is used by 'do_main()' later.
    """
    result = []
    for incidence_id, bipd_sm in BipdDb.iteritems():
        txt, analyzer = __do_state_machine(bipd_sm, 
                                           engine.Class_BACKWARD_INPUT_POSITION(incidence_id)) 
        result.extend(txt)
    return result

def do_reload_procedure(TheAnalyzer):
    """Lazy (delayed) code generation of the forward and backward reloaders. 
    Any state who needs reload may 'register' in a reloader. This registering may 
    happen after the code generation of forward or backward state machine.
    """
    # Variables that tell where to go after reload success and reload failure
    if   TheAnalyzer is None:                             return []
    elif not TheAnalyzer.engine_type.subject_to_reload(): return []
    elif TheAnalyzer.reload_state is None:                return []
    elif TheAnalyzer.reload_state_extern_f:               return []

    variable_db.require("target_state_else_index")  # upon reload failure
    variable_db.require("target_state_index")       # upon reload success

    require_position_registers(TheAnalyzer)

    return reload_state_coder.do(TheAnalyzer.reload_state)

def require_position_registers(TheAnalyzer):
    """Require an array to store input positions. This has later to be 
    implemented as 'variables'. Position registers are exclusively used
    for post-context restore. No other engine than FORWARD would require
    those.
    """
    if not TheAnalyzer.engine_type.is_FORWARD(): 
        return

    if TheAnalyzer.position_register_map is None:
        position_register_n = 0
    else:
        position_register_n = len(set(TheAnalyzer.position_register_map.itervalues()))

    if position_register_n != 0:
        initial_array  = "{ " + ("0, " * (position_register_n - 1) + "0") + "}"
    else:
        # Implement a dummy array (except that there is no reload)
        initial_array = "(void*)0"

    variable_db.require_array("position", ElementN = position_register_n,
                              Initial = initial_array)
    variable_db.require("PositionRegisterN", 
                        Initial = "(size_t)%i" % position_register_n)

@typed(dial_db=DialDB)
def do_state_router(dial_db):
    routed_address_set = dial_db.routed_address_set()
    # If there is only one address subject to state routing, then the
    # state router needs to be implemented.
    #if len(routed_address_set) == 0:
    #    return []

    # Add the address of 'terminal_end_of_file()' if it is not there, already.
    # (It should not be there, if we are working on a fixed chunk, as in 'counting'.
    #  When counting is webbed into analysis:: assert address_eof in routed_address_set)
    if False:
        address_eof = DoorID.incidence(E_IncidenceIDs.END_OF_STREAM, dial_db).related_address 
        routed_address_set.add(address_eof)
        dial_db.mark_address_as_gotoed(address_eof)

    routed_state_info_list = state_router_generator.get_info(routed_address_set, dial_db)
    return state_router_generator.do(routed_state_info_list, dial_db) 

def do_variable_definitions():
    # Following function refers to the global 'variable_db'
    return Lng.VARIABLE_DEFINITIONS(variable_db)

def __do_state_machine(sm, EngineType, ReloadStateForward=None, dial_db=None): 
    """Generates code for state machine 'sm' and the 'EngineType'.

    RETURNS: list of strings
    """
    assert len(sm.get_orphaned_state_index_list()) == 0

    txt = []
    # -- [optional] comment state machine transitions 
    if Setup.comment_state_machine_f: 
        Lng.COMMENT_STATE_MACHINE(txt, sm)

    # -- Analyze state machine --> optimized version
    analyzer = analyzer_generator.do(sm, EngineType, 
                                     ReloadStateExtern = ReloadStateForward, 
                                     dial_db           = dial_db)

    # -- Generate code for analyzer
    txt.extend(
        do_analyzer(analyzer)
    )

    return txt, analyzer

def do_analyzer(analyzer): 
    state_machine_code = state_machine_coder.do(analyzer)
    Lng.REPLACE_INDENT(state_machine_code)
    # Variable to store the current input
    variable_db.require("input") 
    return state_machine_code

@typed(TerminalList=[Terminal])
def do_terminals(TerminalList, TheAnalyzer, dial_db):
    return Lng.TERMINAL_CODE(TerminalList, TheAnalyzer, dial_db)

def do_reentry_preparation(PreContextSmIdList, OnAfterMatchCode, dial_db):
    return Lng.REENTRY_PREPARATION(PreContextSmIdList, OnAfterMatchCode, dial_db)

_increment_actions_for_utf8 = [
     1, "if     ( ((*iterator) & 0x80) == 0 ) { iterator += 1; } /* 1byte character */\n",
     1, "/* NOT ( ((*iterator) & 0x40) == 0 ) { iterator += 2; }    2byte character */\n",
     1, "else if( ((*iterator) & 0x20) == 0 ) { iterator += 2; } /* 2byte character */\n",
     1, "else if( ((*iterator) & 0x10) == 0 ) { iterator += 3; } /* 3byte character */\n",
     1, "else if( ((*iterator) & 0x08) == 0 ) { iterator += 4; } /* 4byte character */\n",
     1, "else if( ((*iterator) & 0x04) == 0 ) { iterator += 5; } /* 5byte character */\n",
     1, "else if( ((*iterator) & 0x02) == 0 ) { iterator += 6; } /* 6byte character */\n",
     1, "else if( ((*iterator) & 0x01) == 0 ) { iterator += 7; } /* 7byte character */\n",
     1, "else                                 { iterator += 1; } /* default 1       */\n",
]
    
_increment_actions_for_utf16 = [
     1, "if( *iterator >= 0xD800 && *iterator < 0xE000 ) { iterator += 2; }\n",
     1, "else                                            { iterator += 1; }\n", 
]
    
