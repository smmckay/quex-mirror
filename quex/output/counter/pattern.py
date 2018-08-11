"""____________________________________________________________________________
(C) 2013 Frank-Rene Schaefer
_______________________________________________________________________________
"""
import quex.engine.state_machine.character_counter as character_counter
from   quex.engine.operations.operation_list       import Op
from   quex.engine.misc.tools                      import typed
from   quex.constants                              import E_Count
from   quex.blackboard                             import Lng, setup as Setup

@typed(lcci=(None, character_counter.SmLineColumnCountInfo))
def map_SmLineColumnCountInfo_to_code(lcci, ShiftF=True, ModeName=None):
    run_time_counter_required_f, cmd_list = map_SmLineColumnCountInfo_to_CmdList(lcci, ShiftF, ModeName)
    return run_time_counter_required_f, Lng.COMMAND_LIST(cmd_list)

@typed(lcci=(None, character_counter.SmLineColumnCountInfo))
def map_SmLineColumnCountInfo_to_CmdList(lcci, ShiftF=True, ModeName=None):
    """RETURN: [0] Verdict
               [1] CounterCode

    Verdict == True  --> Run-time counter implementation required!!
                         Pattern's length cannot be determined beforehand.
                         
               False --> No run-time counting is necessary!!
                         It was possible to determine the increments
                         based on the pattern's structure. 
                             
    """
    if not (Setup.count_line_number_f or Setup.count_column_number_f):
        return False, []
    elif lcci is None:
        return True, [ Op.PasspartoutCounterCall(ModeName) ]

    # (*) Default Character Counter ___________________________________________
    #
    #     Used when the increments and/or setting cannot be derived from the 
    #     pattern itself. That is, if one of the following is VOID:
    if lcci.run_time_counter_required_f:
        return True, [ Op.PasspartoutCounterCall(ModeName) ]

    # (*) Determine Line and Column Number Count ______________________________
    #    
    #     Both, for line and column number considerations the same rules hold.
    #     Those rules are defined in 'get_offset()' as shown below.
    #
    def get_offset(Increment, IncrementByLexemeLength):
        if IncrementByLexemeLength == 0 or Increment == 0:
            return None, None
        elif Increment != E_Count.VOID:
            return Increment, 1
        else:
            return Lng.LEXEME_LENGTH(), IncrementByLexemeLength

    # Column and line counts must be shifted (begin=end) even if only
    # columns are counted. For example, even if only columns are modified
    # the old line_number_at_begin must be adapted to the current.
    if ShiftF: cmd_list = [ Op.ColumnCountShift() , Op.LineCountShift() ]
    else:      cmd_list = []

    # -- Line Number Count
    offset, factor = get_offset(lcci.line_n_increment, 
                                lcci.line_n_increment_by_lexeme_length) 
    if offset is not None:
        cmd_list.append(Op.LineCountAdd(offset, factor))

    # -- Column Number Count
    if  lcci.column_index != E_Count.VOID:
        cmd_list.append(Op.ColumnCountSet(lcci.column_index + 1))

    elif lcci.column_n_increment_by_lexeme_length != E_Count.VOID:
        offset, factor = get_offset(lcci.column_n_increment, 
                                    lcci.column_n_increment_by_lexeme_length) 
        if offset is not None:
            cmd_list.append(Op.ColumnCountAdd(offset, factor))

    else:
        # Following assert results from entry check against 'VOID'
        assert lcci.grid_step_size_by_lexeme_length != E_Count.VOID

        if   lcci.grid_step_n == E_Count.VOID: grid_step_n = Lng.LEXEME_LENGTH()
        elif lcci.grid_step_n != 0:            grid_step_n = lcci.grid_step_n
        else:                                  grid_step_n = None

        if grid_step_n is not None:
            cmd_list.append(Op.ColumnCountGridAdd(lcci.grid_step_size_by_lexeme_length, 
                                                  grid_step_n)) 

    return False, cmd_list

