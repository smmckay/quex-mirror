import quex.token_db          as     token_db
import quex.engine.misc.error as     error
from   quex.constants         import E_IncidenceIDs
import quex.blackboard        as     blackboard
from   quex.blackboard        import setup as Setup, \
                                     required_support_indentation_count, \
                                     required_support_begin_of_line

def do(Condition):
    """Determines whether a condition for code generation holds."""
    if   not Condition:                                                        
        return True
    elif Condition.startswith("not-"):
        return not do(Condition[4:])
    elif "&&" in Condition:
        return all(do(x.strip()) for x in Condition.split("&&"))
    elif "||" in Condition:
        return any(do(x.strip()) for x in Condition.split("||"))
    elif Condition == "lexeme-null":
        return Setup.implement_lexeme_null_f
    elif Condition == "count-line":
        return bool(Setup.count_line_number_f)
    elif Condition == "count-column":
        return bool(Setup.count_column_number_f) or bool(required_support_indentation_count())
    elif Condition == "token-stamp-line":
        return do("count-line")                      # NEEDS REWORK
    elif Condition == "token-stamp-column":
        return do("count-column")                    # NEEDS REWORK
    elif Condition == "token-take-text":
        return token_db.support_take_text()
    elif Condition == "token-repetition":
        return token_db.support_repetition()
    elif Condition == "token-class-only":
        return Setup.token_class_only_f
    elif Condition == "count":
        return Setup.count_line_number_f or Setup.count_column_number_f or bool(required_support_indentation_count())
    elif Condition == "indentation":
        return bool(required_support_indentation_count())
    elif Condition == "lib-quex":
        return bool(Setup.implement_lib_quex_f)
    elif Condition == "lib-lexeme":
        return Setup.implement_lib_lexeme_f
    elif Condition == "std-lib":
        return Setup.standard_library_usage_f
    elif Condition == "mode-on-entry-handler":
        return True                                  # NEEDS REWORK
        return any(
            mode.incidence_db.has_key(E_IncidenceIDs.MODE_ENTRY)
            for mode in blackboard.mode_db.values()
        )
    elif Condition == "mode-on-exit-handler":
        return True                                  # NEEDS REWORK
        return any(
            mode.incidence_db.has_key(E_IncidenceIDs.MODE_EXIT)
            for mode in blackboard.mode_db.values()
        )
    elif Condition == "C":
        return Setup.language == "C"
    elif Condition == "Cpp":
        return Setup.language == "C++"
    elif Condition == "begin-of-line-context":
        return required_support_begin_of_line()
    elif Condition == "computed-gotos":
        return Setup.computed_gotos_f
    elif Condition == "memory-management-extern":
        return Setup.memory_management_extern_f
    elif Condition == "unit-test":
        return Setup.unit_test_f
    else:                                                                      
        error.log("Code generation: found unknown condition '<%s>'." % Condition)


