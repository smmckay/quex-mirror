"""____________________________________________________________________________
(C) 2012-2013 Frank-Rene Schaefer
_______________________________________________________________________________
"""
import quex.engine.generator.base                   as     generator
from   quex.engine.generator.languages.variable_db  import variable_db
import quex.engine.analyzer.engine_supply_factory   as     engine
from   quex.engine.analyzer.door_id_address_label   import dial_db, \
                                                           DoorID, \
                                                           IfDoorIdReferencedCode
from   quex.engine.analyzer.commands                import CommandList, \
                                                           InputPToLexemeStartP

from   quex.blackboard import Lng, \
                              DefaultCounterFunctionDB, \
                              E_MapImplementationType, \
                              E_IncidenceIDs

def get(CounterDb, Name):
    """Implement the default counter for a given Counter Database. 

    In case the line and column number increment cannot be determined before-
    hand, a something must be there that can count according to the rules given
    in 'CounterDb'. This function generates the code for a general counter
    function which counts line and column number increments starting from the
    begin of a lexeme to its end.

    The implementation of the default counter is a direct function of the
    'CounterDb', i.e. the database telling how characters influence the
    line and column number counting. 
    
    Multiple modes may have the same character counting behavior. If so, 
    then there's only one counter implemented while others refer to it. 

    ---------------------------------------------------------------------------
    
    RETURNS: function_name, string --> Function name and the implementation 
                                       of the character counter.
             function_name, None   --> The 'None' implementation indicates that
                                       NO NEW counter is implemented. An 
                                       appropriate counter can be accessed 
                                       by the 'function name'.
    ---------------------------------------------------------------------------
    """
    assert CounterDb.covers(0, Setup.get_character_value_limit())

    function_name = DefaultCounterFunctionDB.get_function_name(CounterDb)
    if function_name is not None:
        return function_name, None # Implementation has been done before.

    function_name  = Lng.DEFAULT_COUNTER_FUNCTION_NAME(Name) 

    door_id_return = dial_db.new_door_id()
    code, \
    door_id_beyond = generator.do_loop(CounterDb, 
                                       DoorIdExit      = door_id_return,
                                       LexemeEndCheckF = True)

    implementation = __frame(function_name, Lng.INPUT_P(), code, door_id_return, 
                             door_id_beyond) 

    DefaultCounterFunctionDB.enter(CounterDb, function_name)

    return function_name, implementation

def __frame(FunctionName, IteratorName, CodeTxt, DoorIdReturn, DoorIdBeyond):
    

    txt = [  \
          "#ifdef __QUEX_OPTION_COUNTER\n" \
        + "static void\n" \
        + "%s(QUEX_TYPE_ANALYZER* me, QUEX_TYPE_CHARACTER* LexemeBegin, QUEX_TYPE_CHARACTER* LexemeEnd)\n" \
          % FunctionName \
        + "{\n" \
        + "#   define self (*me)\n" \
    ]

    # Following function refers to the global 'variable_db'
    txt.append(Lng.VARIABLE_DEFINITIONS(variable_db))
    txt.append(
        "    (void)me;\n"
        "    __QUEX_IF_COUNT_SHIFT_VALUES();\n"
        "    /* Allow LexemeBegin == LexemeEnd (e.g. END_OF_STREAM)\n"
        "     * => Caller does not need to check\n"
        "     * BUT, if so quit immediately after 'shift values'. */\n"
        "    __quex_assert(LexemeBegin <= LexemeEnd);\n"
        "    if(LexemeBegin == LexemeEnd) return;\n"
        "    %s = LexemeBegin;\n" % IteratorName
    )

    txt.extend(CodeTxt)

    door_id_failure = DoorID.incidence(E_IncidenceIDs.MATCH_FAILURE)
    txt.append(
        IfDoorIdReferencedCode(door_id_failure,
        [
            "%s\n" % Lng.LABEL(door_id_failure),
            "    %s\n" % Lng.GOTO(DoorIdBeyond),
        ])
    )
    txt.append(
         "%s:\n" % dial_db.get_label_by_door_id(DoorIdReturn) \
       + "    __quex_assert(%s == LexemeEnd); /* Otherwise, lexeme violates codec character boundaries. */\n" \
         % IteratorName \
       + "   return;\n" \
       + "#  undef self\n" \
       + "}\n" \
       + "#endif /* __QUEX_OPTION_COUNTER */\n" 
    )



    return "".join(Lng.GET_PLAIN_STRINGS(txt))

