from   quex.input.regular_expression.pattern             import Pattern_Prep           
from   quex.input.code.core                              import CodeTerminal
from   quex.engine.incidence_db                          import IncidenceDB
from   quex.engine.analyzer.terminal.core                import Terminal
from   quex.engine.analyzer.terminal.factory             import TerminalFactory
from   quex.engine.analyzer.door_id_address_label        import DoorID
import quex.engine.state_machine.check.superset          as     superset_check
import quex.engine.state_machine.check.identity          as     identity_checker
import quex.engine.state_machine.construction.sequentialize           as     sequentialize
import quex.engine.state_machine.algorithm.beautifier    as     beautifier

from   quex.engine.misc.tools import typed
import quex.engine.misc.error as     error

import quex.blackboard as blackboard
from   quex.blackboard import setup as Setup, \
                              standard_incidence_db_is_immutable, \
                              Lng, \
                              E_IncidenceIDs, \
                              E_TerminalType
from   copy        import deepcopy
from   collections import namedtuple
from   operator    import attrgetter

def get(BaseModeSequence, OptionsDb, CounterDb, IncidenceDb, ReloadState):
    """Priority, Pattern, Terminal List: 'ppt_list'
    -----------------------------------------------------------------------
    The 'ppt_list' is the list of eXtended Pattern Action Pairs.
    Each element in the list consist of
    
        .priority 
        .pattern
        .terminal
    
    The pattern priority allows to keep the list sorted according to its
    priority given by the mode's position in the inheritance hierarchy and
    the pattern index itself.
    -----------------------------------------------------------------------
    """ 
    mode_name        = BaseModeSequence[-1].name

    # -- Evaluate the DELETE and PRIORITY-MARK commands

    # -- Setup the pattern list and the terminal db
    pattern_list, \
    terminal_db   = finalize(ppt_list, IncidenceDb, extra_terminal_list, terminal_factory)

    return pattern_list, \
           terminal_db, \
           history_deletion, \
           history_reprioritization

def finalize_terminal_db(ppt_list, IncidenceDb, ExtraTerminalList, terminal_factory):
    """This function MUST be called after 'finalize_pattern_list()'!
    """
    terminal_list = [
        terminal for priority, pattern, terminal in ppt_list
                 if terminal is not None
    ]

    # Some incidences have their own terminal
    # THEIR INCIDENCE ID REMAINS FIXED!
    terminal_list.extend(
        IncidenceDb.extract_terminal_db(terminal_factory, ReloadRequiredF=True).itervalues()
    )

    terminal_list.extend(ExtraTerminalList)

    # Consistency check
    # (i) Incidence Ids are either integers or 'E_IncidenceIDs'
    assert all((   isinstance(t.incidence_id(), (int, long)) 
                or t.incidence_id() in E_IncidenceIDs)
               for t in terminal_list)
    # (ii) Every incidence id appears only once.
    assert    len(set(t.incidence_id() for t in terminal_list)) \
           == len(terminal_list)

    return dict((t.incidence_id(), t) for t in terminal_list)

