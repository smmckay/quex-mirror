"""____________________________________________________________________________
(C) 2012-2013 Frank-Rene Schaefer
_______________________________________________________________________________
"""
import quex.output.core.base                        as     generator
import quex.output.core.loop.action_map             as     action_map
from   quex.output.core.variable_db                 import variable_db
from   quex.engine.analyzer.door_id_address_label   import DoorID, DialDB
import quex.engine.analyzer.engine_supply_factory   as     engine
from   quex.engine.misc.tools                       import typed
from   quex.engine.counter                          import CountActionMap

from   quex.blackboard import Lng, \
                              DefaultCounterFunctionDB, \
                              E_IncidenceIDs

@typed(CaMap=CountActionMap)
def get(CaMap, Name):
    """Implement the default counter for a given Counter Database. 

    In case the line and column number increment cannot be determined before-
    hand, a something must be there that can count according to the rules given
    in 'CaMap'. This function generates the code for a general counter
    function which counts line and column number increments starting from the
    begin of a lexeme to its end.

    The implementation of the default counter is a direct function of the
    'CaMap', i.e. the database telling how characters influence the
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
    dial_db = DialDB()

    function_name = DefaultCounterFunctionDB.get_function_name(CaMap)
    if function_name is not None:
        # Use previously done implementation for this 'CaMap'
        return function_name, None 

    door_id_return = dial_db.new_door_id()

    analyzer_list,        \
    terminal_list,        \
    required_register_set = action_map.do(CaMap, 
                                          DoorIdLoopExit  = door_id_return, 
                                          LexemeEndCheckF = True,
                                          dial_db         = dial_db)

    code = generator.do_analyzer_list(analyzer_list)

    code.extend(
        generator.do_terminals(terminal_list, TheAnalyzer=None, dial_db=dial_db)
    )

    variable_db.require_registers(required_register_set)
    implementation = __frame(function_name, Lng.INPUT_P(), code, door_id_return, 
                             dial_db) 

    function_name  = Lng.DEFAULT_COUNTER_FUNCTION_NAME(Name) 
    DefaultCounterFunctionDB.enter(CaMap, function_name)

    return function_name, implementation

def __frame(FunctionName, IteratorName, CodeTxt, DoorIdReturn, dial_db):
    
    state_router_adr   = DoorID.global_state_router(dial_db).related_address
    state_router_label = Lng.LABEL_STR_BY_ADR(state_router_adr)
    txt = [  \
          "#ifdef __QUEX_OPTION_COUNTER\n" \
        + "static void\n" \
        + "%s(QUEX_TYPE_ANALYZER* me, QUEX_TYPE_LEXATOM* LexemeBegin, QUEX_TYPE_LEXATOM* LexemeEnd)\n" \
          % FunctionName \
        + "{\n" \
        + "#   define self (*me)\n" \
        + "/*  'QUEX_GOTO_STATE' requires 'QUEX_LABEL_STATE_ROUTER' */\n"
        + "#   define QUEX_LABEL_STATE_ROUTER %s\n" % state_router_label
    ]

    # Following function refers to the global 'variable_db'
    txt.append(Lng.VARIABLE_DEFINITIONS(variable_db))
    txt.extend([
        "    (void)me;\n",
        "    __QUEX_IF_COUNT_SHIFT_VALUES();\n",
        "%s" % Lng.ML_COMMENT("Allow LexemeBegin == LexemeEnd (e.g. END_OF_STREAM)\n"
                              "=> Caller does not need to check\n"
                              "BUT, if so quit immediately after 'shift values'."),
        "    __quex_assert(LexemeBegin <= LexemeEnd);\n",
        "    %s" % Lng.IF("LexemeBegin", "==", "LexemeEnd"), 
        "        %s\n" % "return;", # TODO: Replace with Lng.PURE_RETURN
        "    %s\n" % Lng.END_IF(),
        "    %s = LexemeBegin;\n" % IteratorName
    ])

    txt.extend(CodeTxt)

    door_id_failure     = DoorID.incidence(E_IncidenceIDs.MATCH_FAILURE, dial_db)
    door_id_bad_lexatom = DoorID.incidence(E_IncidenceIDs.BAD_LEXATOM, dial_db)

    txt.append(
          "%s /* TERMINAL: BAD_LEXATOM */\n;\n"  % Lng.LABEL(door_id_bad_lexatom)
        # BETTER: A lexeme that is 'counted' has already matched!
        #         => FAILURE is impossible!
        # "%s /* TERMINAL: FAILURE     */\n%s\n" % Lng.UNREACHABLE
        + "%s /* TERMINAL: FAILURE     */\n%s\n" % (Lng.LABEL(door_id_failure), 
                                                    Lng.GOTO(DoorIdReturn, dial_db))
    )
    txt.append(
         "%s\n" % Lng.LABEL(DoorIdReturn)
       + "%s\n" % Lng.COMMENT("Assert: lexeme in codec's character boundaries.") \
       + "     __quex_assert(%s == LexemeEnd);\n" % IteratorName \
       + "    return;\n" \
       + "".join(generator.do_state_router(dial_db)) \
       + "%s\n" % Lng.UNDEFINE("self")
       + "%s\n" % Lng.UNDEFINE("QUEX_LABEL_STATE_ROUTER")
       # If there is no MATCH_FAILURE, then DoorIdBeyond is still referenced as 'gotoed',
       # but MATCH_FAILURE is never implemented, later on, because its DoorId is not 
       # referenced.
       + "#    if ! defined(QUEX_OPTION_COMPUTED_GOTOS)\n"
       + "     %s /* in QUEX_GOTO_STATE       */\n" % Lng.GOTO(DoorID.global_state_router(dial_db), dial_db)
       + "     %s /* to BAD_LEXATOM           */\n" % Lng.GOTO(DoorID.incidence(E_IncidenceIDs.BAD_LEXATOM, dial_db), dial_db)
       + "#    endif\n"
       + "    %s\n" % Lng.COMMENT("Avoid compiler warning: 'Unused labels'") \
       + "    %s\n" % Lng.GOTO(door_id_failure, dial_db) \
       + "    (void)target_state_index;\n"
       + "    (void)target_state_else_index;\n"
       + "}\n" \
       + "#endif /* __QUEX_OPTION_COUNTER */\n" 
    )

    return "".join(Lng.GET_PLAIN_STRINGS(txt, dial_db))

