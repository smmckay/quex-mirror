from   quex.input.code.core                               import CodeTerminal
from   quex.engine.analyzer.terminal.core                 import Terminal
from   quex.engine.loop.loop_map                          import MiniTerminal, \
                                                                 LoopMap
from   quex.engine.misc.tools                             import typed

from   quex.blackboard import Lng

def do(loop_map, loop_config, appendix_lcci_db, ParallelMiniTerminalList, 
       DoorIdLoop):
    """RETURNS: list of all Terminal-s.
    """
    loop_terminal_list           = _get_terminal_list_for_loop(loop_map, loop_config,
                                                               DoorIdLoop) 

    run_time_counter_required_f, \
    parallel_terminal_list       = _get_terminal_list_for_appendices(loop_config, 
                                                                     appendix_lcci_db,
                                                                     ParallelMiniTerminalList)

    return loop_terminal_list + parallel_terminal_list, \
           run_time_counter_required_f

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

        code = [ 
            loop_config.replace_Lazy_DoorIdLoop(cmd, DoorIdLoop) 
            for cmd in lme.code 
        ]
        result.append(
            Terminal(CodeTerminal(Lng.COMMAND_LIST(code, loop_config.dial_db)), 
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

@typed(ParallelMiniTerminalList=[MiniTerminal])
def _get_terminal_list_for_appendices(loop_config, appendix_lcci_db, 
                                      ParallelMiniTerminalList):
    """RETURNS: [0] True, default counter is required.
                    False, else.
                [1] list of terminals of the appendix state machines.
    """
    run_time_counter_required_f = False
    terminal_list               = []
    for mini_terminal in ParallelMiniTerminalList:
        rtcr_f, cmd_list = loop_config.get_count_code(
            appendix_lcci_db.get(mini_terminal.incidence_id)
        )
        count_code = Lng.COMMAND_LIST(cmd_list, loop_config.dial_db)
        run_time_counter_required_f |= rtcr_f

        terminal_list.append(
            mini_terminal.get_Terminal(count_code, 
                                       loop_config.dial_db, 
                                       loop_config.loop_state_machine_id)
        )

    return run_time_counter_required_f, terminal_list

