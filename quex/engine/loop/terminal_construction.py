from   quex.input.code.core                               import CodeTerminal
from   quex.engine.analyzer.terminal.core                 import Terminal
from   quex.engine.loop.loop_map                          import MiniTerminal, \
                                                                 LoopMap
from   quex.engine.misc.tools                             import typed

from   quex.blackboard import Lng

def do(loop_map, loop_config, appendix_cmd_list_db, ParallelMiniTerminalList, 
       DoorIdLoop):
    """RETURNS: list of all Terminal-s.
    """
    terminal_list_0 = _get_terminal_list_for_loop(loop_map, loop_config,
                                                  DoorIdLoop) 
    terminal_list_1 = _get_terminal_list_for_appendix_sms(loop_config, 
                                                          DoorIdLoop,
                                                          appendix_cmd_list_db)
    terminal_list_2 = _get_terminal_list_for_original_terminals(loop_config, 
                                                                ParallelMiniTerminalList)

    return terminal_list_0 + terminal_list_1 + terminal_list_2

@typed(loop_map=LoopMap)
def _get_terminal_list_for_loop(loop_map, loop_config, DoorIdLoop):
    """RETURNS: List of terminals of the loop state:

        (i)   Counting terminals: Count and return to loop entry.
        (ii)  Couple terminals:   Count and goto appendix state machine.
        (iii) Exit terminal:      Exit loop.

    The '<LOOP>' terminal serves as an address for the appendix state machines.
    If they fail, they can accept its incidence id and re-enter the loop from
    there.
    """
    # Terminal: Normal Loop Characters
    # (LOOP EXIT terminal is generated later, see below).
    result = []
    done   = set()
    for lme in loop_map:
        if   lme.iid_couple_terminal in done:                      continue
        elif lme.iid_couple_terminal == loop_config.iid_loop_exit: continue
        elif lme.code is None:                                     continue
        done.add(lme.iid_couple_terminal)

        result.append(
            Terminal(loop_config.CodeTerminal_without_Lazy_DoorIdLoop(lme.code, DoorIdLoop),
                     "<LOOP TERMINAL %s>" % lme.iid_couple_terminal, 
                     IncidenceId = lme.iid_couple_terminal,
                     dial_db     = loop_config.dial_db)
        )

    # Terminal: Re-enter Loop
    if loop_config.iid_loop_after_appendix_drop_out is not None:
        txt = Lng.COMMAND_LIST(
            loop_config.events.on_loop_after_appendix_drop_out(DoorIdLoop,
                                                               loop_config.column_number_per_code_unit),
            loop_config.dial_db
        )
        result.append(
            Terminal(CodeTerminal(txt),
                     "<LOOP>", loop_config.iid_loop_after_appendix_drop_out,
                     dial_db=loop_config.dial_db)
        )

    # Terminal: Exit Loop
    result.append(
        Terminal(CodeTerminal(loop_config.events.on_loop_exit_text(loop_config.dial_db)), 
                 "<LOOP EXIT>", loop_config.iid_loop_exit,
                 dial_db=loop_config.dial_db)
    )

    return result

def _get_terminal_list_for_appendix_sms(loop_config, DoorIdLoop, appendix_cmd_list_db):

    return [
        Terminal(loop_config.CodeTerminal_without_Lazy_DoorIdLoop(cmd_list, DoorIdLoop),
                 "<LOOP APPENDIX TERMINAL %s>" % appendix_sm_id, 
                 IncidenceId = appendix_sm_id,
                 dial_db     = loop_config.dial_db)
        for appendix_sm_id, cmd_list in appendix_cmd_list_db.iteritems()
    ]

@typed(ParallelMiniTerminalList=[MiniTerminal])
def _get_terminal_list_for_original_terminals(loop_config, 
                                              ParallelMiniTerminalList):
    """RETURNS: 
           [0] list of terminals of the appendix state machines.
    """
    return [
        mini.get_Terminal(PreCode            = [], 
                          dial_db            = loop_config.dial_db, 
                          LoopStateMachineId = loop_config.loop_state_machine_id)
        for mini in ParallelMiniTerminalList
    ]


