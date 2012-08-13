# (C) 2012 Frank-Rene Schaefer
from quex.blackboard import E_Count

def do(ThePattern, EOF_ActionF):
    """Prepare additional actions which are required for line and column
    number counting. 
    
    The '.newline_n' and '.column_n' of a given 'Pattern' may be given by the
    pattern itself. For example the pattern "\n\n" increments the line number
    always by 2. The pattern "\n+" however increments the line number depending
    on how many '\n' it matches at runtime. These considerations where done
    by means of 

              quex.engine.state_machine.character_counter.do(...)

    at the time when the Pattern object was constructed in 

              class quex.input.regular_expression.construct.Pattern

    Depending on the newline_n and column_n increment being pre-determined,
    the counting behavior may be adapted. The following options exist:

        __QUEX_COUNT_END_OF_STREAM_EVENT(me)
        __QUEX_COUNT_VOID(me)
        __QUEX_COUNT_NEWLINE_N_FIXED_COLUMN_N_VOID(me, NewlineN) 
        __QUEX_COUNT_NEWLINE_N_ZERO_COLUMN_N_FIXED(me, ColumnN) 

    Their definition appears in 

             $QUEX_PATH/quex/code_base/definitions

    Where they are mapped to macros and functions which accomplish the job.

    """
    global LanguageDB

    if EOF_ActionF:
        return "__QUEX_COUNT_END_OF_STREAM_EVENT(self.counter);"

    if ThePattern is None:
        return "__QUEX_COUNT_VOID(self.counter);"

    newline_n   = ThePattern.newline_n
    character_n = ThePattern.character_n
    grid        = ThePattern.count.grid
    line_ipc    = ThePattern.count.increment_line_n_per_char
    column_ipc  = ThePattern.count.increment_column_n_per_char

    if   newline_n == E_Count.VOID:
        # Run the general algorithm, since not even the number of newlines in the 
        # pattern can be determined directly from the pattern
        return "__QUEX_COUNT_VOID(self.counter);"

    elif newline_n != 0:
        if ThePattern.sm.get_ending_character_set().contains_only(ord('\n')):
            # A pattern that ends with newline, lets the next column start at one.
            return "__QUEX_COUNT_NEWLINE_N_FIXED_COLUMN_N_ZERO(self.counter, %i);" % newline_n
        # TODO: Try to determine number of characters backwards to newline directly
        #       from the pattern state machine. (Those seldom cases won't bring much
        #       speed-up)
        return "__QUEX_COUNT_NEWLINE_N_FIXED_COLUMN_N_VOID(self.counter, %i);" % newline_n

    # Lexeme does not contain newline --> count only columns
    if character_n == E_Count.VOID: incr_str = "LexemeL"
    else:                           incr_str = "%i" % int(character_n)
    return "__QUEX_COUNT_NEWLINE_N_ZERO_COLUMN_N_FIXED(self.counter, %s);" % incr_str

def do(ThePattern, EOF_ActionF):
    return __new_do() \
           + "__quex_debug_counter();\n"

def __new_do(ThePattern, EOF_ActionF):

    if EOF_ActionF:
        return "__QUEX_COUNTER_SHIFT_VALUES(&self);\n" 

    counter = None

    if not counter.is_determined():
        if not counter.has_grid():
            return "QUEX_NAME(Counter_count)(&self.counter, LexemeBegin, LexemeEnd);\n"
        else:
            return "QUEX_NAME(Counter_count_with_grid)(&self.counter, LexemeBegin, LexemeEnd);\n"

    # (*) Column Number Increment Considerations
    if counter.grid != E_Count.NONE:
        if counter.grid > 0:
            if   counter.grid_step_n == 1:                     arg = None
            elif counter.grid_step_n == E_Count.LEXEME_LENGTH: arg = "LexemeL"
            else:                                              assert False

            core_txt = LanguageDB.GRID_STEP("self.counter._column_number_at_end", 
                                            counter.grid_width, arg)
            column_txt = "__QUEX_IF_COUNT_COLUMNS(%s);\n" % core_txt
        else:
            return "QUEX_NAME(Counter_count_with_grid)(&self.counter, LexemeBegin, LexemeEnd);\n"
    else:
        if   counter.column_n == 0:
            column_txt = ""
        else:
            if counter.column_n_proportional_to_lexeme_length():
                if counter.column_n == 1: arg = "LexemeL"
                else:                     arg = "LexemeL * %i" % counter.column_n
            else:                         arg = "%i" % counter.column_n
            column_txt = "__QUEX_IF_COUNT_COLUMNS_ADD(%s);\n" % arg


    # (*) Line Number Increment Considerations
    if   counter.newline_n == 0:
        line_txt = ""
    else:
        if counter.newline_n_proportional_to_lexeme_length():
            if counter.newline_n == 1: arg = "LexemeL"
            else:                      arg = "LexemeL * %i" % counter.newline_n
        else:                          arg = "%i" % counter.newline_n
        line_txt = "__QUEX_IF_COUNT_LINES_ADD(%s);\n" % arg

    return "__QUEX_COUNTER_SHIFT_VALUES(&self);\n" \
           + line_txt \
           + column_txt

def __new_do(ThePattern, EOF_ActionF):
    """Prepare additional actions around a pattern action which are required 
    for line and column number counting. 
    
    The '.newline_n' and '.column_n' of a given 'Pattern' may be given by the
    pattern itself. For example the pattern "\n\n" increments the line number
    always by 2. The pattern "\n+" however increments the line number depending
    on how many '\n' it matches at runtime. These considerations where done
    by means of 

         quex.engine.state_machine.character_counter.do(...)

    at the time when the patterns were absorbed into a 'real' mode in

         quex.input.files.mode.Mode.__init__(...)

    which calls

         quex.input.regular_expression.construct.Pattern.do_count(CounterDB)

    Depending on the newline_n and column_n increment being pre-determined,
    the counting behavior may be adapted. A set of counting functions try
    to profit from such pre-determinations:

            __QUEX_COUNT_NEWLINE_*_COLUMN_*_GRID_*

    where '*' may have one of the following values:

        * = 0: Increment = Zero.
        * = S: Not increment, instead set to a particular value 
               (may be derived from LexemeL).
        * = N: Fixed, increment passed as argument.
        * = X: Increment = Undetermined.

    'Homogenous':
        All characters have the same with (except grid characters). That is
        the column number increment can be determined by 'LexemeL * X' 
        -- where X is some constant.

    For NEWLINE: 0, N, X

    For COLUMN:  X, N, S

    For GRID:    0, X
                 Not 'N', because A fixed number of grid triggers does not 
                 provide any computational advantage.

    Option NEWLINE_N only makes sense with GRID_0, because only then, the
    column number can be determined by counting backwards to the last 
    newline. 
    
    Option COLUMN_N cannot appear with GRID_X, because any grid makes the
    column number increment un-pre-determined.

    If parameters are only 'N' and '0' then everything is pre-determined.

    __QUEX_COUNT_NEWLINE_0_COLUMN_X_GRID_0 --> Counter_count_homogenously_to_newline_backwards(...)
    __QUEX_COUNT_NEWLINE_0_COLUMN_X_GRID_X --> Counter_count_with_grid(...)
    __QUEX_COUNT_NEWLINE_N_COLUMN_X_GRID_0 --> Counter_count_homogenously_to_newline_backwards(...)
                                               line_n += Fixed Value
    __QUEX_COUNT_NEWLINE_X_COLUMN_X_GRID_0 --> Counter_count(...)
    __QUEX_COUNT_NEWLINE_X_COLUMN_X_GRID_X --> Counter_count_with_grid(...)
    __QUEX_COUNT_NEWLINE_X_COLUMN_N_GRID_0 --> Counter_count_newlines(...)
                                               column += Fixed Value

             $QUEX_PATH/quex/code_base/definitions

    Where they are mapped to macros and functions which accomplish the job.
    """
    global LanguageDB

    if EOF_ActionF:
        return "__QUEX_COUNT_END_OF_STREAM_EVENT(self.counter);"

    if ThePattern is None:
        return "__QUEX_COUNT_NEWLINE_X_COLUMN_X_GRID_X(self.counter);"

    if ThePattern.count.line_n == 0:
        return __pattern_without_newline(ThePattern.count)
    else:
        return __pattern_with_newline(ThePattern.count)

def __pattern_with_newline(Count):
    columns_involved_f       = (Count.column_n != 0 or Count.grid != E_Count.NONE)
    line_n_increment_fixed_f = (Count.increment_line_n_per_char != E_Count.VOID)

    if Count.line_n == E_Count.VOID:
        if columns_involved_f:
            # Column and line numbers appear in the pattern and nothing can
            # be determined beforehand. Thus, run the general count algorithm.
            return "__QUEX_COUNT_VOID(self.counter);"
        else:
            # There are solely newline characters involved in the pattern.
            # Thus, the line number increment can be determined by the number
            # of newline characters, IF all have the same increment.
            if line_n_increment_fixed_f:
                assert isinstance(Count.increment_line_n_per_char, (int, long))
                return "__QUEX_COUNT_NEWLINE_N_FIXED_COLUMN_N_ZERO(self.counter, LexemeL * %i);" \
                       % Count.increment_line_n_per_char
            else:
                return "__QUEX_COUNT_VOID(self.counter);"
    else:
        isinstance(Count.line_n, (int, long))
        # Line numbers do not have to be counted.
        if not columns_involved_f:
            if line_n_increment_fixed_f:
                return "__QUEX_COUNT_NEWLINE_N_FIXED_COLUMN_N_ZERO(self.counter, %i);" \
                       % (Count.line_n * Count.increment_line_n_per_char)
            elif grid == E_Count.NONE:
                return "__QUEX_COUNT_NEWLINE_N_FIXED_COLUMN_N_VOID(self.counter);"
            else:
                return "__QUEX_COUNT_NEWLINE_N_FIXED_COLUMN_N_VOID(self.counter);"

def __pattern_without_newline(Count):
        


    assert isinstance(Count.line_n, (int, long))
    # line_n == integer means, that the number of newlines in the pattern is fixed.

    if ThePattern.sm.get_ending_character_set().contains_only(ord('\n')):
        # A pattern that ends with newline, lets the next column start at one.
        return "__QUEX_COUNT_NEWLINE_N_FIXED_COLUMN_N_ZERO(self.counter, %i);" % Count.line_n

    # TODO: Try to determine number of characters backwards to newline directly
    #       from the pattern state machine. (Those seldom cases won't bring much
    #       speed-up)
    return "__QUEX_COUNT_NEWLINE_N_FIXED_COLUMN_N_VOID(self.counter, %i);" % Count.line_n

def __pattern_without_newline(Count):
    # Lexeme does not contain newline --> count only columns
    if Count.column_n == E_Count.VOID: incr_str = "LexemeL"
    else:                              incr_str = "%i" % int(character_n)
    return "__QUEX_COUNT_NEWLINE_N_ZERO_COLUMN_N_FIXED(self.counter, %s);" % incr_str

