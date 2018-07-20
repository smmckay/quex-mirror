"""____________________________________________________________________________
(C) 2013 Frank-Rene Schaefer
_______________________________________________________________________________
"""
import quex.engine.state_machine.character_counter as character_counter
from   quex.engine.misc.tools import typed
from   quex.constants         import E_Count
from   quex.blackboard        import Lng, setup as Setup

@typed(lcci=(None, character_counter.SmLineColumnCountInfo))
def map_SmLineColumnCountInfo_to_code(lcci, ShiftF=True, ModeName=None):
    """RETURN: [0] Verdict
               [1] CounterCode

    Verdict == True  --> Run-time counter implementation required!!
                         Pattern's length cannot be determined beforehand.
                         
               False --> No run-time counting is necessary!!
                         It was possible to determine the increments
                         based on the pattern's structure. 
                             
    """
    if not (Setup.count_line_number_f or Setup.count_column_number_f):
        return False, ""

    if lcci is None:
        return  True, Lng.DEFAULT_COUNTER_CALL(ModeName)

    # (*) Default Character Counter ___________________________________________
    #
    #     Used when the increments and/or setting cannot be derived from the 
    #     pattern itself. That is, if one of the following is VOID:
    if lcci.run_time_counter_required_f:
        return True, [ Lng.DEFAULT_COUNTER_CALL(ModeName) ]

    # (*) Determine Line and Column Number Count ______________________________
    #    
    #     Both, for line and column number considerations the same rules hold.
    #     Those rules are defined in 'get_increment()' as shown below.
    #
    def get_increment(txt, Increment, IncrementByLexemeLength, AddFunction):
        if IncrementByLexemeLength == 0 or Increment == 0:
            return 
        elif Increment != E_Count.VOID:
            arg = Lng.VALUE_STRING(Increment)
        else:
            arg = Lng.MULTIPLY_WITH(Lng.LEXEME_LENGTH(), IncrementByLexemeLength)

        txt.append("%s\n" % AddFunction(arg))

    # Column and line counts must be shifted (begin=end) even if only
    # columns are counted. For example, even if only columns are modified
    # the old line_number_at_begin must be adapted to the current.
    if ShiftF: txt = [ Lng.COUNTER_SHIFT_VALUES() ]
    else:      txt = []

    # -- Line Number Count
    get_increment(txt, lcci.line_n_increment, 
                  lcci.line_n_increment_by_lexeme_length, 
                  Lng.COUNTER_LINE_ADD)

    # -- Column Number Count
    if  lcci.column_index != E_Count.VOID:
        txt.append(Lng.COUNTER_COLUM_SET(lcci.column_index + 1))

    elif lcci.column_n_increment_by_lexeme_length != E_Count.VOID:
        get_increment(txt, lcci.column_n_increment, 
                      lcci.column_n_increment_by_lexeme_length, 
                      Lng.COUNTER_COLUM_ADD)

    else:
        # Following assert results from entry check against 'VOID'
        assert lcci.grid_step_size_by_lexeme_length != E_Count.VOID

        if   lcci.grid_step_n == E_Count.VOID: 
            grid_step_n = Lng.LEXEME_LENGTH()
        elif lcci.grid_step_n != 0:
            grid_step_n = lcci.grid_step_n
        else:
            grid_step_n = None

        if grid_step_n is not None:
            txt.extend(Lng.COUNTER_COLUMN_GRID_STEP(lcci.grid_step_size_by_lexeme_length, 
                                                    grid_step_n)) 
            txt.append("\n")

    return False, txt

