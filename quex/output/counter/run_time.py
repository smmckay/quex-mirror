"""____________________________________________________________________________
(C) 2012-2013 Frank-Rene Schaefer
_______________________________________________________________________________
"""
import quex.output.core.base                        as     generator
import quex.engine.loop.core                        as     loop
import quex.engine.analyzer.engine_supply_factory   as     engine

from   quex.output.core.variable_db                 import variable_db
from   quex.engine.analyzer.door_id_address_label   import DoorID, DialDB
from   quex.engine.misc.tools                       import typed
from   quex.engine.counter                          import CountActionMap

import quex.condition  as     condition
from   quex.blackboard import Lng, \
                              DefaultCounterFunctionDB, \
                              E_IncidenceIDs

@typed(CaMap=CountActionMap)
def get(CaMap, ModeName):
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

    mode_with_same_counter = DefaultCounterFunctionDB.get_mode_name(CaMap)
    if mode_with_same_counter is not None:
        # Use previously done implementation for this 'CaMap'
        return __frame(Lng.DEFAULT_COUNTER_FUNCTION_NAME(ModeName), 
                       [ Lng.DEFAULT_COUNTER_CALL(mode_with_same_counter) ], 
                       None, None, None)

    door_id_return = dial_db.new_door_id()

    analyzer_list,           \
    terminal_list,           \
    dummy_loop_map,          \
    dummy_door_id_loop,      \
    required_register_set,   \
    dummy_run_time_counter_f = loop.do(CaMap, 
                                       OnLoopExitDoorId = door_id_return,
                                       LexemeEndCheckF  = True,
                                       EngineType       = engine.CHARACTER_COUNTER, 
                                       dial_db          = dial_db,
                                       ModeName         = ModeName)

    code = generator.do_analyzer_list(analyzer_list)

    code.extend(
        generator.do_terminals(terminal_list, TheAnalyzer=None, dial_db=dial_db)
    )

    variable_db.require_registers(required_register_set)
    implementation = __frame(Lng.DEFAULT_COUNTER_FUNCTION_NAME(ModeName), code, 
                             Lng.INPUT_P(), door_id_return, dial_db) 

    DefaultCounterFunctionDB.enter(CaMap, ModeName)

    return implementation

def __frame(FunctionName, CodeTxt, IteratorName, DoorIdReturn, dial_db):

    txt = [  \
          "static void\n" \
        + "%s(QUEX_TYPE_ANALYZER* me, QUEX_TYPE_LEXATOM* LexemeBegin, QUEX_TYPE_LEXATOM* LexemeEnd)\n" % FunctionName \
        + "{\n" \
    ]

    if IteratorName:
        state_router_adr   = DoorID.global_state_router(dial_db).related_address
        state_router_label = Lng.LABEL_STR_BY_ADR(state_router_adr)
        txt.extend([
            "#   define self (*me)\n",
            "/*  'QUEX_GOTO_STATE' requires 'QUEX_LABEL_STATE_ROUTER' */\n",
            "#   define QUEX_LABEL_STATE_ROUTER %s\n" % state_router_label
        ])

        # Following function refers to the global 'variable_db'
        txt.append(Lng.VARIABLE_DEFINITIONS(variable_db))

        txt.extend([
            "    (void)me;\n",
             Lng.COUNTER_SHIFT_VALUES(),
            "%s" % Lng.ML_COMMENT("Allow LexemeBegin == LexemeEnd (e.g. END_OF_STREAM)\n"
                                  "=> Caller does not need to check\n"
                                  "BUT, if so quit immediately after 'shift values'."),
            "    __quex_assert(LexemeBegin <= LexemeEnd);\n",
            "    %s" % Lng.IF("LexemeBegin", "==", "LexemeEnd"), 
            "        %s\n" % Lng.PURE_RETURN,
            "    %s\n" % Lng.END_IF,
            "    %s = LexemeBegin;\n" % IteratorName
        ])

    txt.extend(CodeTxt)

    if IteratorName:
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
        )

    txt.append("}\n")

    return "".join(Lng.GET_PLAIN_STRINGS(txt, dial_db))

