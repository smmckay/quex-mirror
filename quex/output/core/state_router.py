from   quex.engine.analyzer.door_id_address_label  import DoorID, DialDB

from   quex.engine.misc.tools                      import typed
from   quex.blackboard import Lng

from   operator import itemgetter

def do(StateRouterInfoList, dial_db):
    """Create code that allows to jump to a state based on an integer value.
    """

    # NOTE: Do not use 'IfDoorIdReferencedCode' because the state router may 
    #       possibly not be tagged as 'gotoed', event if it is used.
    prolog = "#   ifndef QUEX_OPTION_COMPUTED_GOTOS\n" \
             "    __quex_assert_no_passage();\n"       \
             "%s\n" % Lng.LABEL(DoorID.global_state_router(dial_db), dial_db) 
    epilog = "#   endif /* QUEX_OPTION_COMPUTED_GOTOS */\n"
    
    if len(StateRouterInfoList) == 0: code = []
    else:                             code = __get_code(StateRouterInfoList)

    result = [ prolog ] 
    result.extend(code)
    result.append(epilog)
    return result

def __get_code(StateRouterInfoList):
    # It is conceivable, that 'last_acceptance' is never set to a valid 
    # terminal. Further, there might be solely the init state. In this
    # case the state router is void of states. But, the terminal router
    # requires it to be defined --> define a dummy state router.
    if len(StateRouterInfoList) == 0:
        return ["    QUEX_NAME(error_code_set_if_first)(&self, E_Error_StateRouter_Empty);\n    return;\n"]

    variable = "target_state_index"
    case_code_list = sorted(StateRouterInfoList, key=itemgetter(0))
    default  = [
        "        default:\n"
        "            QUEX_NAME(error_code_set_if_first)(&self, E_Error_StateRouter_UnkownStateIndex);\n"
        "            return;\n"
        "    }\n"
    ]
    txt = Lng.CASE_SELECT(variable, case_code_list, default)

    return txt

@typed(dial_db=DialDB)
def get_info(StateIndexList, dial_db):
    """
    NOTE: At least a 'dummy' state router is always equired so that 'goto
    QUEX_STATE_ROUTER;' does not reference a non-existing label. Then, we
    return an empty text array.

    <fschaef9/13y10m15d: "Still true with current dial_db implementation?">
    """
    if len(StateIndexList) == 0: return []

    # Make sure, that for every state the 'drop-out' state is also mentioned
    result = [None] * len(StateIndexList)
    for i, index in enumerate(StateIndexList):
        assert type(index) != str
        if index >= 0:
            # Transition to state entry
            adr = index
        else:
            assert False, "Is this still an issue?"
            # Transition to a templates 'drop-out'
            adr = DoorID.drop_out(- index, dial_db).related_address

        result[i] = (index, Lng.GOTO_ADDRESS(adr, dial_db))

    return result
