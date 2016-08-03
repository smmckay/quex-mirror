from   quex.input.code.core                         import CodeTerminal
from   quex.engine.analyzer.door_id_address_label   import DoorID
from   quex.engine.operations.operation_list        import Op
import quex.engine.analyzer.door_id_address_label   as     dial
from   quex.engine.analyzer.terminal.core           import Terminal
from   quex.engine.counter                          import IndentationCount, \
                                                           CountActionMap, \
                                                           LineColumnCount
import quex.output.core.loop                        as     loop
from   quex.blackboard                              import Lng, \
                                                           E_IncidenceIDs, \
                                                           E_R, \
                                                           setup as Setup

def do(Data, ReloadState):
    """________________________________________________________________________
    Counting whitespace at the beginning of a line.

                   .-----<----+----------<--------------+--<----.
                   |          | count                   |       | count = 0
                   |          | whitespace              |       |
                 .---------.  |                         |       |
       --------->|         +--'                         |       |
                 |         |                            |       |
                 |         |                            |       |
                 |         |          .------------.    |       |
                 |         +----->----| suppressor |----'       |
                 |         |          | + newline  |            | 
                 | COUNTER |          '------------'            |
                 |         |          .---------.               |
                 |         +----->----| newline |---------------'
                 |         |          '---------'
                 |         |          .----------------.
                 |         |----->----| on_indentation |---------> RESTART
                 '---------'   else   '----------------'
                                           

    Generate an indentation counter. An indentation counter is entered upon 
    the detection of a newline (which is not followed by a newline suppressor).
    
    Indentation Counter:

                indentation = 0
                column      = 0
                       |
                       |<------------------------.
                .-------------.                  |
                | INDENTATION |       indentation += count
                | COUNTER     |       column      += count
                '-------------'                  |
                       |                         |
                       +-------- whitspace -->---'
                       |
                   Re-Enter 
                   Analyzer
                                            
    An indentation counter is a single state that iterates to itself as long
    as whitespace occurs. During that iteration the column counter is adapted.
    There are two types of adaption:

       -- 'normal' adaption by a fixed delta. This adaption happens upon
          normal space characters.

       -- 'grid' adaption. When a grid character occurs, the column number
          snaps to a value given by a grid size parameter.

    When a newline occurs the indentation counter exits and restarts the
    lexical analysis. If the newline is not followed by a newline suppressor
    the analyzer will immediately be back to the indentation counter state.
    ___________________________________________________________________________
    """
    ca_map                = Data["ca_map"]
    isetup                = Data["indentation_setup"]
    incidence_db          = Data["incidence_db"]
    mode_name             = Data["mode_name"]
    dial_db               = Data["dial_db"]

    whitespace_set        = isetup.whitespace_character_set
    bad_space_set         = isetup.bad_space_character_set
    sm_newline            = isetup.get_sm_newline()
    sm_comment            = isetup.get_sm_comment()
    sm_suppressed_newline = isetup.get_sm_suppressed_newline()
    default_ih_f          = incidence_db.default_indentation_handler_f()

    assert isinstance(ca_map, CountActionMap)
    assert isinstance(isetup, IndentationCount)
    assert sm_suppressed_newline  is None or sm_suppressed_newline.is_DFA_compliant()
    assert sm_newline is None             or sm_newline.is_DFA_compliant()
    assert sm_comment is None             or sm_comment.is_DFA_compliant()

    # -- 'on_indentation' == 'on_beyond': 
    #     A handler is called as soon as an indentation has been detected.
    loop_exit_door_id, \
    ih_call_terminal   = _get_indentation_handler_terminal(default_ih_f, 
                                                           mode_name,
                                                           dial_db)
    sm_terminal_list    = _get_state_machine_vs_terminal_list(sm_suppressed_newline, 
                                                              sm_newline,
                                                              sm_comment) 
    if bad_space_set is not None:
        sm_terminal_list.append(
            _get_state_machine_vs_terminal_bad_indentation(bad_space_set,
                                                           incidence_db, dial_db)
        )

    # 'whitespace' --> normal counting
    # 'bad'        --> goto bad character indentation handler
    # else         --> non-whitespace detected => handle indentation

    engine_type = None # Default
    if ReloadState: engine_type = ReloadState.engine_type

    # (*) Generate Code
    code,                 \
    terminal_list,        \
    loop_map,             \
    door_id_beyond,       \
    required_register_set = loop.do(ca_map, 
                                    OnLoopExitDoorId  = loop_exit_door_id,
                                    EngineType        = engine_type,
                                    ReloadStateExtern = ReloadState,
                                    LexemeMaintainedF = True,
                                    ParallelSmTerminalPairList = sm_terminal_list, 
                                    dial_db           = dial_db,
                                    LoopCharacterSet  = whitespace_set) 

    return code, terminal_list, required_register_set

def _get_indentation_handler_terminal(DefaultIndentationHanderF,
                                      ModeName, dial_db):
    code = [
        Op.IndentationHandlerCall(DefaultIndentationHanderF, ModeName),
        Op.GotoDoorId(DoorID.continue_without_on_after_match(dial_db))
    ]
    incidence_id = dial.new_incidence_id()
    terminal = Terminal(CodeTerminal(code),
                                     "CALL INDENTATION HANDLER", 
                                     incidence_id,
                                     dial_db=dial_db)

    return DoorID.incidence(incidence_id, dial_db), terminal

def _get_state_machine_vs_terminal_list(SmSuppressedNewline, SmNewline, 
                                        SmComment): 
    """Get a list of pairs (state machine, terminal) for the newline, suppressed
    newline and comment:

    newline --> 'eat' newline state machine, then RESTART counting the
                columns of whitespace.
    newline_suppressor + newline --> 'eat' newline suppressor + newline
                     then CONTNIUE with column count of whitespace.
    comment --> 'eat' anything until the next newline, then RESTART
                 counting columns of whitespace.

    RETURNS: list of pairs: [0] state machine
                            [1] terminal
    """
    result = []
    # If nothing is to be done, nothing is appended
    _add_pair(result, SmSuppressedNewline, "<INDENTATION SUPPRESSED NEWLINE>")
    _add_pair(result, SmNewline, "<INDENTATION NEWLINE>")
    _add_pair(result, SmComment, "<INDENTATION COMMENT>")

    for sm, terminal in result:
        assert isinstance(terminal, loop.MiniTerminal)
        assert sm.get_id() == terminal.incidence_id
    return result

def _get_state_machine_vs_terminal_bad_indentation(BadSpaceCharacterSet,
                                                   incidence_db, dial_db):
    """Generate state machine that detects the 'bad indentation character'.
    Generate terminal that emboddies the defined 'bad indentation character
    handler' from the incidence_dab.

    RETURNS: [0] state machine
             [1] terminal
    """

    sm = StateMachine.from_character_set(BadSpaceCharacterSet,
                                         E_IncidenceIDs.INDENTATION_BAD)

    on_bad_indentation_txt = Lng.SOURCE_REFERENCED(
        incidence_db[E_IncidenceIDs.INDENTATION_BAD]
    )
    code = [
        Lng.ON_BAD_INDENTATION(on_bad_indentation_txt, 
                               dial.new_incidence_id(),
                               dial_db)
    ]
    terminal = loop.MiniTerminal(code, "<INDENTATION BAD INDENTATION CHARACTER>", 
                                 E_IncidenceIDs.INDENTATION_BAD)

    return sm, terminal


def _add_pair(psml, SmOriginal, Name):
    """Add a state machine-terminal pair to 'psml'. A terminal is generated
    which transits to 'INDENTATION_HANDLER'. The state machine is cloned
    for safety.
    """
    if SmOriginal is None: return

    incidence_id = dial.new_incidence_id()

    # Disconnect from machines being used elsewhere.
    sm = SmOriginal.clone(StateMachineId=incidence_id)

    code = [ 
        Lng.GOTO(DoorID.incidence(E_IncidenceIDs.INDENTATION_HANDLER, dial_db)) 
    ]

    terminal = loop.MiniTerminal(code, Name, incidence_id)
    # TRY:     terminal.set_requires_goto_loop_entry_f()
    # INSTEAD: GOTO 'INDENTATION_HANDLER'

    psml.append((sm, terminal))

