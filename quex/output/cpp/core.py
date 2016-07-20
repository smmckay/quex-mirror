# (C) Frank-Rene Schaefer
#______________________________________________________________________________
from   quex.engine.analyzer.door_id_address_label         import get_plain_strings
from   quex.engine.analyzer.terminal.core                 import Terminal
from   quex.output.core.variable_db                       import variable_db
import quex.output.core.base                              as     generator
from   quex.engine.counter                                import CountActionMap
from   quex.engine.pattern                                import Pattern
from   quex.engine.misc.tools                             import all_isinstance, \
                                                                 typed, \
                                                                 flatten_list_of_lists
import quex.output.cpp.run_time_counter                   as     run_time_counter
from   quex.blackboard                                    import setup as Setup, \
                                                                 E_IncidenceIDs, \
                                                                 Lng

@typed(ModeNameList = [(str, unicode)])
def do(Mode, ModeNameList):
    """RETURNS: The analyzer code for a mode defined in 'Mode'.
    """
    variable_db.init() 

    function_body,       \
    variable_definitions = do_core(Mode) 

    function_txt = wrap_up(Mode.name, function_body, variable_definitions, 
                           ModeNameList, Mode.dial_db)

    return function_txt

def do_core(Mode):
    """Produces main code for an analyzer function which can detect patterns given in
    the 'PatternList' and has things to be done mentioned in 'TerminalDb'. 

    RETURN: Code implementing the lexical analyzer.

    The code is not embedded in a function and required definitions are not provided.
    This happens through function 'wrap_up()'.
    """
    # Prepare the combined state machines and terminals 
    esms = Mode
    TerminalDb         = Mode.terminal_db
    ReloadStateForward = Mode.reload_state_forward
    OnAfterMatchCode   = Mode.incidence_db.get_CodeTerminal(E_IncidenceIDs.AFTER_MATCH)
    dial_db            = Mode.dial_db

    variable_db.require_registers(flatten_list_of_lists(
        terminal.required_register_set()
        for terminal in TerminalDb.itervalues()
    ))

    # (*) Pre Context State Machine
    #     (If present: All pre-context combined in single backward analyzer.)
    pre_context, \
    pre_analyzer = generator.do_pre_context(esms.pre_context_sm,
                                            esms.pre_context_sm_id_list,
                                            dial_db)
    # assert all_isinstance(pre_context, (IfDoorIdReferencedCode, int, str, unicode))

    # (*) Backward input position detection
    #     (Seldomly present -- only for Pseudo-Ambiguous Post Contexts)
    bipd                 = generator.do_backward_read_position_detectors(esms.bipd_sm_db,
                                                                         dial_db)
    # assert all_isinstance(bipd, (IfDoorIdReferencedCode, int, str, unicode))

    # (*) Main State Machine -- try to match core patterns
    #     Post-context handling is webbed into the main state machine.
    main, \
    main_analyzer        = generator.do_main(esms.sm, ReloadStateForward, 
                                             dial_db)
    # assert all_isinstance(main, (IfDoorIdReferencedCode, int, str, unicode))

    # (*) Terminals
    #     (BEFORE 'Reload procedures' because some terminals may add entries
    #      to the reloader.)
    terminals            = generator.do_terminals(TerminalDb.values(), 
                                                  main_analyzer, 
                                                  dial_db)

    # (*) Reload procedures
    reload_procedure_fw  = generator.do_reload_procedure(main_analyzer)
    reload_procedure_bw  = generator.do_reload_procedure(pre_analyzer)

    # assert all_isinstance(reload_procedures, (IfDoorIdReferencedCode, int, str, unicode))

    # (*) Re-entry preparation
    reentry_preparation  = generator.do_reentry_preparation(esms.pre_context_sm_id_list,
                                                            OnAfterMatchCode, 
                                                            dial_db)

    # (*) State Router
    #     (Something that can goto a state address by an given integer value)
    state_router         = generator.do_state_router(dial_db)
    # assert all_isinstance(state_router, (IfDoorIdReferencedCode, int, str, unicode))

    # (*) Variable Definitions
    #     (Code that defines all required variables for the analyzer)
    variable_definitions = generator.do_variable_definitions()
    # assert all_isinstance(variable_definitions, (IfDoorIdReferencedCode, int, str, unicode))

    # (*) Putting it all together
    function_body = []
    function_body.extend(pre_context)         # implementation of pre-contexts (if there are some)
    function_body.extend(main)                # main pattern matcher
    function_body.extend(bipd)                # (seldom != empty; only for pseudo-ambiguous post contexts)
    function_body.extend(terminals)           
    function_body.extend(state_router)        # route to state by index (only if no computed gotos)
    function_body.extend(reload_procedure_fw)
    function_body.extend(reload_procedure_bw)
    function_body.extend(reentry_preparation)   

    return function_body, variable_definitions

def wrap_up(ModeName, FunctionBody, VariableDefs, ModeNameList, dial_db):
    txt_function = Lng.ANALYZER_FUNCTION(ModeName, Setup, VariableDefs, 
                                         FunctionBody, dial_db, ModeNameList) 
    txt_header   = Lng.HEADER_DEFINITIONS(dial_db) 
    assert isinstance(txt_header, (str, unicode))

    txt_analyzer = get_plain_strings(txt_function, dial_db)
    assert all_isinstance(txt_analyzer, (str, unicode))

    return [ txt_header ] + txt_analyzer

def do_run_time_counter(Mode):
    assert Mode.run_time_counter_db is not None
    assert isinstance(Mode.run_time_counter_db, CountActionMap)

    variable_db.init()

    # May be, the default counter is the same as for another mode. In that
    # case call the default counter of the other mode with the same one and
    # only macro.
    function_name, \
    code           = run_time_counter.get(Mode.run_time_counter_db, 
                                          Mode.name)

    txt = [ Lng.RUN_TIME_COUNTER_PROLOG(function_name) ]

    if code is not None:
        txt.append(code)

    return txt

def frame_this(Code):
    return Lng["$frame"](Code, Setup)

