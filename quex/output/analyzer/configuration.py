
from   quex.engine.misc.string_handling import blue_print

from   quex.blackboard  import setup as Setup, Lng
import quex.blackboard  as     blackboard
from   quex.constants   import E_IncidenceIDs
from   quex.DEFINITIONS import QUEX_VERSION

import time

def do(Mode_PrepPrepDB):
    IndentationSupportF = blackboard.required_support_indentation_count()
    BeginOfLineSupportF = blackboard.required_support_begin_of_line()

    LexerClassName = Setup.analyzer_class_name

    txt = Lng.open_template(Lng.analyzer_configuration_file())

    # -- check if exit/entry handlers have to be active
    entry_handler_active_f = any(
        mode.incidence_db.has_key(E_IncidenceIDs.MODE_ENTRY)
        for mode in Mode_PrepPrepDB.values()
    )
    exit_handler_active_f = any(
        mode.incidence_db.has_key(E_IncidenceIDs.MODE_EXIT)
        for mode in Mode_PrepPrepDB.values()
    )

    # token_repetition_token_id_list empty => token_repetition_support_txt = ""
    token_repetition_support_txt = (" %s " % Lng.OR).join(
        Lng.EQUAL("TokenID", token_id_str)
        for token_id_str in blackboard.token_repetition_token_id_list
    )

    if Setup.analyzer_derived_class_name != "":
        analyzer_derived_class_name = Setup.analyzer_derived_class_name
    else:
        analyzer_derived_class_name = Setup.analyzer_class_name

    txt = Lng.SWITCH(txt, "QUEX_OPTION_COUNTER_COLUMN",        Setup.count_column_number_f)        
    txt = Lng.SWITCH(txt, "QUEX_OPTION_COMPUTED_GOTOS",                False)
    txt = Lng.SWITCH(txt, "QUEX_OPTION_INCLUDE_STACK",                 Setup.include_stack_support_f)
    txt = Lng.SWITCH(txt, "QUEX_OPTION_COUNTER_LINE",          Setup.count_line_number_f)      
    txt = Lng.SWITCH(txt, "QUEX_OPTION_RUNTIME_MODE_TRANSITION_CHECK", Setup.mode_transition_check_f)
    txt = Lng.SWITCH(txt, "QUEX_OPTION_TOKEN_REPETITION_SUPPORT",      token_repetition_support_txt) 
    txt = Lng.SWITCH(txt, "QUEX_OPTION_INDENTATION_TRIGGER",           IndentationSupportF)     
    txt = Lng.SWITCH(txt, "QUEX_OPTION_ENDIAN_BIG",                  Setup.buffer_byte_order == "big")
    txt = Lng.SWITCH(txt, "QUEX_OPTION_ENDIAN_LITTLE",               Setup.buffer_byte_order == "little")
    txt = Lng.SWITCH(txt, "__QUEX_OPTION_ON_ENTRY_HANDLER_PRESENT",    entry_handler_active_f)
    txt = Lng.SWITCH(txt, "__QUEX_OPTION_ON_EXIT_HANDLER_PRESENT",     exit_handler_active_f)
    txt = Lng.SWITCH(txt, "__QUEX_OPTION_PLAIN_C",                     Setup.language.upper() == "C")
    txt = Lng.SWITCH(txt, "__QUEX_OPTION_SUPPORT_BEGIN_OF_LINE_PRE_CONDITION", BeginOfLineSupportF)
    txt = Lng.SWITCH(txt, "QUEX_OPTION_ENDIAN_SYSTEM",               Setup.byte_order_is_that_of_current_system_f)
    txt = Lng.SWITCH(txt, "__QUEX_OPTION_ENGINE_RUNNING_ON_CODEC",     Setup.buffer_codec.name != "unicode")

    token_descr = blackboard.token_type_definition
    codec_name  = Lng.SAFE_IDENTIFIER(Setup.buffer_codec.name)
    include_guard_extension = Lng.INCLUDE_GUARD(Lng.NAMESPACE_REFERENCE(Setup.analyzer_name_space) 
                                                + "__" + Setup.analyzer_class_name)

    def namespace(NameSpaceList):
        return Lng.NAMESPACE_REFERENCE(NameSpaceList, TrailingDelimiterF=False)

    if not token_repetition_support_txt:
        token_repetition_support_txt = Lng.FALSE

    txt = blue_print(txt, 
            [
             ["$$BUFFER_LIMIT_CODE$$",          "%s" % Setup.buffer_limit_code],
             ["$$QUEX_SETTING_CHARACTER_CODEC$$", codec_name],
             ["$$INCLUDE_GUARD_EXTENSION$$",    include_guard_extension],
             ["$$INITIAL_LEXER_MODE_ID$$",      Lng.NAME_IN_NAMESPACE_MAIN("ModeID_%s" % blackboard.initial_mode.get_pure_text())],
             ["$$LEXER_BUILD_DATE$$",           time.asctime()],
             ["$$LEXER_CLASS_NAME$$",           LexerClassName],
             ["$$LEXER_CLASS_NAME_SAFE$$",      Setup.analyzer_name_safe],
             ["$$LEXER_DERIVED_CLASS_NAME$$",   analyzer_derived_class_name],
             ["$$MAX_MODE_CLASS_N$$",           repr(len(Mode_PrepPrepDB))],
             ["$$NAMESPACE_MAIN$$",             namespace(Setup.analyzer_name_space)],
             ["$$NAMESPACE_MAIN_CLOSE$$",       Lng.NAMESPACE_CLOSE(Setup.analyzer_name_space)],
             ["$$NAMESPACE_MAIN_OPEN$$",        Lng.NAMESPACE_OPEN(Setup.analyzer_name_space)],
             ["$$NAMESPACE_TOKEN$$",            namespace(token_descr.name_space)],
             ["$$NAMESPACE_TOKEN_CLOSE$$",      Lng.NAMESPACE_CLOSE(token_descr.name_space)],
             ["$$NAMESPACE_TOKEN_OPEN$$",       Lng.NAMESPACE_OPEN(token_descr.name_space)],
             ["$$PATH_TERMINATION_CODE$$",      "%s" % Setup.path_limit_code],
             ["$$QUEX_TYPE_LEXATOM$$",          Setup.buffer_lexatom_type],
             ["$$QUEX_VERSION$$",               QUEX_VERSION],
             ["$$TOKEN_CLASS$$",                token_descr.class_name],
             ["$$TOKEN_CLASS_NAME_SAFE$$",      token_descr.class_name_safe],
             ["$$TOKEN_COLUMN_N_TYPE$$",        token_descr.column_number_type.get_pure_text()],
             ["$$TOKEN_ID_TYPE$$",              token_descr.token_id_type.get_pure_text()],
             ["$$TOKEN_LINE_N_TYPE$$",          token_descr.line_number_type.get_pure_text()],
             ["$$TOKEN_PREFIX$$",               Setup.token_id_prefix],
             ["$$TOKEN_QUEUE_SAFETY_BORDER$$",  repr(Setup.token_queue_safety_border)],
             ["$$TOKEN_QUEUE_SIZE$$",           repr(Setup.token_queue_size)],
             ["$$TOKEN_REPEAT_TEST$$",          token_repetition_support_txt],
             ["$$USER_LEXER_VERSION$$",         Setup.user_application_version_id],
             ])

    return txt

