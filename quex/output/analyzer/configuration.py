
from   quex.engine.misc.string_handling import blue_print
import quex.output.analyzer.adapt       as     adapt

from   quex.blackboard  import setup as Setup, Lng
import quex.token_db    as     token_db
import quex.blackboard  as     blackboard
from   quex.DEFINITIONS import QUEX_VERSION

import time

def do(Mode_PrepPrepDB):
    LexerClassName = Setup.analyzer_class_name

    txt = Lng.open_template(Lng.analyzer_configuration_file())

    token_descr = token_db.token_type_definition

    if Setup.analyzer_derived_class_name != "":
        analyzer_derived_class_name = Setup.analyzer_derived_class_name
    else:
        analyzer_derived_class_name = Setup.analyzer_class_name

    include_guard_extension = Lng.INCLUDE_GUARD(Lng.NAMESPACE_REFERENCE(Setup.analyzer_name_space) 
                                                + "__" + Setup.analyzer_class_name)

    def namespace(NameSpaceList):
        return Lng.NAMESPACE_REFERENCE(NameSpaceList, TrailingDelimiterF=False)

    txt = blue_print(txt, 
            [
             ["$$BUFFER_LIMIT_CODE$$",          "%s" % Setup.buffer_limit_code],
             ["$$INCLUDE_GUARD_EXTENSION$$",    include_guard_extension],
             ["$$QUEX_SETTING_MODE_INITIAL_P$$",  Lng.NAME_IN_NAMESPACE_MAIN(blackboard.initial_mode.get_pure_text())],
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
             ["$$QUEX_VERSION$$",               QUEX_VERSION],
             ["$$TOKEN_CLASS$$",                token_descr.class_name],
             ["$$TOKEN_CLASS_NAME_SAFE$$",      token_descr.class_name_safe],
             ["$$TYPE_DEFINITIONS$$",           Lng.type_definitions()],
             ["$$TOKEN_PREFIX$$",               Setup.token_id_prefix],
             ["$$TOKEN_QUEUE_SIZE$$",           repr(Setup.token_queue_size)],
             ["$$USER_LEXER_VERSION$$",         Setup.user_application_version_id],
             ])

    return adapt.do(txt, Setup.output_directory)

