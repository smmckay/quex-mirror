
#include "Dumlyzer"

QUEX_NAMESPACE_MAIN_OPEN

QUEX_NAME(Mode) QUEX_NAME(M) = {
    /* id                */ QUEX_NAME(ModeID_M),
    /* name              */ "M",
#   if      defined(QUEX_OPTION_INDENTATION_TRIGGER) \
       && ! defined(QUEX_OPTION_INDENTATION_DEFAULT_HANDLER)
    /* on_indentation    */ QUEX_NAME(Mode_on_indentation_null_function),
#   endif
    /* on_entry          */ QUEX_NAME(Mode_on_entry_exit_null_function),
    /* on_exit           */ QUEX_NAME(Mode_on_entry_exit_null_function),
#   if      defined(QUEX_OPTION_RUNTIME_MODE_TRANSITION_CHECK)
    /* has_base          */ QUEX_NAME(M_has_base),
    /* has_entry_from    */ QUEX_NAME(M_has_entry_from),
    /* has_exit_to       */ QUEX_NAME(M_has_exit_to),
#   endif
    /* analyzer_function */ QUEX_NAME(M_analyzer_function)
};

QUEX_NAME(Mode)* (QUEX_NAME(mode_db)[__QUEX_SETTING_MAX_MODE_CLASS_N]) = {
    &QUEX_NAME(M)
};

void QUEX_NAME(M_on_entry)(QUEX_TYPE_ANALYZER* me, const QUEX_NAME(Mode)* FromMode) { }
void QUEX_NAME(M_on_exit)(QUEX_TYPE_ANALYZER* me, const QUEX_NAME(Mode)* ToMode)    { }
bool QUEX_NAME(M_has_base)(const QUEX_NAME(Mode)* Mode)                             { return false; }
bool QUEX_NAME(M_has_entry_from)(const QUEX_NAME(Mode)* Mode)                       { return false; }
bool QUEX_NAME(M_has_exit_to)(const QUEX_NAME(Mode)* Mode)                          { return false; } 

__QUEX_TYPE_ANALYZER_RETURN_VALUE  
QUEX_NAME(M_analyzer_function)(QUEX_TYPE_ANALYZER* me)   { return (__QUEX_TYPE_ANALYZER_RETURN_VALUE)0; }
bool QUEX_NAME(user_constructor)(QUEX_TYPE_ANALYZER* me) { return false; }
void QUEX_NAME(user_destructor)(QUEX_TYPE_ANALYZER* me)  { }
bool QUEX_NAME(user_reset)(QUEX_TYPE_ANALYZER* me)       { return true; }

#ifdef QUEX_OPTION_INCLUDE_STACK

bool
QUEX_NAME(user_memento_pack)(QUEX_TYPE_ANALYZER* me, 
                             const char*         InputName, 
                             QUEX_NAME(Memento)* memento) 
{ (void)me; (void)memento; (void)InputName; return true; }

void
QUEX_NAME(user_memento_unpack)(QUEX_TYPE_ANALYZER*  me, 
                               QUEX_NAME(Memento)*  memento)
{ (void)me; (void)memento; }
#endif /* QUEX_OPTION_INCLUDE_STACK */

QUEX_NAMESPACE_MAIN_CLOSE


QUEX_NAMESPACE_TOKEN_OPEN

const char*
QUEX_NAME_TOKEN(map_id_to_name)(const QUEX_TYPE_TOKEN_ID TokenID)
{  return ""; }

QUEX_NAMESPACE_TOKEN_CLOSE



bool UserConstructor_UnitTest_return_value = false;
bool UserReset_UnitTest_return_value = false;
bool UserMementoPack_UnitTest_return_value = false;
