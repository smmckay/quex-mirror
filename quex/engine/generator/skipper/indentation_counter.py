import quex.engine.state_machine.index              as     sm_index
from   quex.engine.state_machine.engine_state_machine_set import CharacterSetStateMachine
import quex.engine.analyzer.engine_supply_factory   as     engine
from   quex.engine.analyzer.door_id_address_label   import DoorID
from   quex.engine.analyzer.transition_map          import TransitionMap
from   quex.engine.analyzer.commands.core           import CommandList, \
                                                           IndentationHandlerCall, \
                                                           ColumnCountSet, \
                                                           LineCountAdd, \
                                                           GotoDoorId
from   quex.engine.analyzer.door_id_address_label   import dial_db, \
                                                           IfDoorIdReferencedLabel
from   quex.engine.analyzer.terminal.core           import Terminal
from   quex.engine.counter                          import CountCmdFactory
from   quex.engine.generator.code.core              import CodeTerminal
import quex.engine.generator.loop                   as     loop
import quex.engine.generator.state.transition.core  as     relate_to_TransitionCode
from   quex.engine.generator.state.transition.code  import TransitionCode
from   quex.engine.generator.languages.variable_db  import variable_db
from   quex.engine.misc.string_handling             import blue_print
from   quex.blackboard                              import Lng, \
                                                           E_StateIndices, \
                                                           E_IncidenceIDs, \
                                                           setup as Setup
import quex.blackboard                              as     blackboard

def do(Data, TheAnalyzer):
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
    global variable_db
    counter_db            = Data["counter_db"]
    isetup                = Data["indentation_setup"]
    incidence_db          = Data["incidence_db"]
    default_ih_f          = Data["default_indentation_handler_f"]
    mode_name             = Data["mode_name"]
    sm_suppressed_newline = Data["sm_suppressed_newline"]

    # -- 'on_indentation' == 'on_beyond': 
    #     A handler is called as soon as an indentation has been detected.
    after_beyond = [
        IndentationHandlerCall(default_ih_f, mode_name),
        GotoDoorId(DoorID.continue_without_on_after_match())
    ]

    # -- 'on_bad_indentation' is invoked if a character appeared that has been
    #    explicitly disallowed to be used as indentation.
    bad_indentation_iid = dial_db.new_incidence_id() 

    if Setup.buffer_based_analyzis_f: reload_state = None
    else:                             reload_state = TheAnalyzer.reload_state

    sm_terminal_list = _get_state_machine_vs_terminal_list(sm_suppressed_newline, 
                                                           isetup.sm_newline.get(),
                                                           isetup.sm_comment.get())

    # 'whitespace' --> normal counting
    # 'bad'        --> goto bad character indentation handler
    # else         --> non-whitespace detected => handle indentation
    ccfactory = CountCmdFactory.from_ParserDataIndentation(isetup, 
                                                           counter_db, 
                                                           Lng.INPUT_P(), 
                                                           DoorID.incidence(bad_indentation_iid))

    # (*) Generate Code
    code,          \
    door_id_beyond = loop.do(ccfactory, 
                             AfterBeyond       = after_beyond,
                             EngineType        = TheAnalyzer.engine_type,
                             ReloadStateExtern = reload_state,
                             LexemeMaintainedF = True,
                             ParallelSmTerminalPairList = sm_terminal_list)

    code = [IfDoorIdReferencedLabel(DoorID.incidence(E_IncidenceIDs.INDENTATION_HANDLER))] + code

    _code_terminal_on_bad_indentation_character(code, isetup, mode_name, incidence_db, 
                                                bad_indentation_iid)

    return code

def _get_state_machine_vs_terminal_list(SmSuppressedNewline, SmNewline, SmComment): 
    """Get a list of pairs (state machine, terminal) for the newline, suppressed
    newline and comment:

    newline --> 'eat' newline state machine, then RESTART counting the
                columns of whitespace.
    newline_suppressor + newline --> 'eat' newline suppressor + newline
                     then CONTNIUE with column count of whitespace.
    comment --> 'eat' anything until the next newline, then RESTART
                 counting columns of whitespace.
    """
    result = []
    _add_suppressed_newline(result, SmNewline, SmSuppressedNewline)
    _add_newline(result, SmNewline)
    _add_comment(result, SmComment)
    return result

def _add_suppressed_newline(psml, SmNewline, SmSuppressedNewline):
    """Add a pair (suppressed newline, terminal on suppressed newline to 'psml'.

    A suppresed newline is not like a newline--the next line is considered as 
    being appended to the current line. Nevertheless the line number needs to
    incremented, just the column number is not reset to 1. Then, it continues
    with indentation counting.
    """
    if SmSuppressedNewline is None:
        return

    # The parser MUST ensure that if there is a newline suppressor, there MUST
    # be a newline being defined.
    assert SmNewline is not None

    cl = [
        LineCountAdd(1),
        GotoDoorId(DoorID.incidence(E_IncidenceIDs.INDENTATION_HANDLER)),
    ]
    terminal = Terminal(CodeTerminal(Lng.COMMAND_LIST(cl)), "<INDENTATION SUPPRESSED NEWLINE>")
    terminal.set_incidence_id(SmNewline.get_id())

    psml.append((SmSuppressedNewline, terminal))

def _add_newline(psml, SmNewline):
    """Add a pair (newline state machine, terminal on newline) to 'psml'.

    When a newline occurs, the column count can be set to 1 and the line number
    is incremented. Then the indentation counting restarts.
    """
    assert SmNewline is not None

    cl = [
        ColumnCountSet(1),
        LineCountAdd(1),
        GotoDoorId(DoorID.incidence(E_IncidenceIDs.INDENTATION_HANDLER))
    ]
    terminal = Terminal(CodeTerminal(Lng.COMMAND_LIST(cl)), "<INDENTATION NEWLINE>")
    terminal.set_incidence_id(SmNewline.get_id())

    psml.append((SmNewline, terminal))


def _add_comment(psml, SmComment):
    """On matching the comment state machine goto a terminal that does the 
    following:
    """
    if SmComment is None: return

    comment_skip_iid = dial_db.new_incidence_id()
    door_id_comment  = DoorID.incidence(comment_skip_iid)

    if SmComment.last_character_set().contains_only(ord('\n')):
        code = Lng.COMMAND_LIST([
            ColumnCountSet(1),
            LineCountAdd(1),
        ])
    else:
        count_info = CountInfo.from_StateMachine(SmComment, 
                                                 CounterDb,
                                                 CodecTrafoInfo=Setup.buffer_codec_transformation_info)
        code = [
            Lng.COMMAND(Assign(E_R.ReferenceP, E_R.LexemeStartP)),
            counter.do_CountInfo(count_info),
            Lng.COMMAND(Assign(E_R.LexemeStartP, E_R.ReferenceP))
        ]
        variable_db.require("reference_p")

    code.append(Lng.GOTO(DoorID.incidence(E_IncidenceIDs.INDENTATION_HANDLER)))

    terminal = Terminal(CodeTerminal(code), "INDENTATION COMMENT")
    terminal.set_incidence_id(comment_skip_iid)

    psml.append((SmComment, terminal))

def _code_terminal_on_bad_indentation_character(code, ISetup, ModeName, incidence_db, BadIndentationIid):
    if ISetup.bad_character_set.get() is None:
        return
    on_bad_indentation_txt = incidence_db[E_IncidenceIDs.INDENTATION_BAD].get_text()
    code.extend([
        "%s\n" % Lng.LABEL(DoorID.incidence(BadIndentationIid)),
        "#define BadCharacter (me->buffer._input_p[-1])\n",
        "%s\n" % on_bad_indentation_txt,
        "#undef  BadCharacter\n",
        "%s\n" % Lng.GOTO(DoorID.global_reentry())
    ])

