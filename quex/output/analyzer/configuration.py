
from   quex.engine.misc.string_handling import blue_print
import quex.output.analyzer.adapt       as     adapt

import quex.blackboard  as     blackboard
from   quex.blackboard  import setup as Setup, Lng
import quex.token_db    as     token_db
import quex.blackboard  as     blackboard
from   quex.DEFINITIONS import QUEX_VERSION

import time
from   itertools import chain

def do(Mode_PrepPrepDB):
    txt = Lng.open_template(Lng.analyzer_configuration_file())

    lexatom_loader_seek_buffer_size = 512
    indentation_stack_size          = 64
    buffer_size                     = 131072
    buffer_size_min                 = 32768
    converter_buffer_size           = 65536
    mode_stack_size                 = 64
    if   buffer_size_min >= 1024: fallback_n = 256
    elif buffer_size_min >= 16:   fallback_n = buffer_size >> 4
    else:                         fallback_n = 0


    adaptable_list = [
        ("BUFFER_FALLBACK_N",                    "%s" % fallback_n),
        ("BUFFER_SIZE",                          "%s" % buffer_size),
        ("BUFFER_SIZE_MIN",                      "%s" % buffer_size_min),
        ("INDENTATION_STACK_SIZE",               "%s" % indentation_stack_size),
        ("BUFFER_LEXATOM_LOADER_CONVERTER_BUFFER_SIZE", "(size_t)%s" % converter_buffer_size),
        ("BUFFER_LEXATOM_LOADER_SEEK_BUFFER_SIZE", lexatom_loader_seek_buffer_size),
        ("MODE_STACK_SIZE",                      "(size_t)%s" % mode_stack_size), 
        ("TOKEN_QUEUE_SIZE",                     "(size_t)%s" % repr(Setup.token_queue_size)),
    ]
    immutable_list = [
        ("VERSION",                           '"%s"' % QUEX_VERSION),
        ("ANALYZER_VERSION",                  '"%s"' % Setup.user_application_version_id),
        ("BUILD_DATE",                        '"%s"' % time.asctime()),
        ("MODE_INITIAL_P",                    '&%s'  % Lng.NAME_IN_NAMESPACE_MAIN(blackboard.initial_mode.get_pure_text())),
        ("BUFFER_LEXATOM_BUFFER_BORDER",      "0x%X" % Setup.buffer_limit_code),
        ("BUFFER_LEXATOM_NEWLINE",            _lexatom_newline_in_engine_encoding()),
        ("BUFFER_LEXATOM_PATH_TERMINATION",  "0x%X" % Setup.path_limit_code),

    ]
    adaptable_txt = [ Lng.QUEX_SETTING_DEF(name, value) for name, value in adaptable_list ]
    immutable_txt = [ Lng.QUEX_SETTING_DEF(name, value) for name, value in immutable_list ]

    setting_list = [ name for name, dummy in chain(adaptable_list, immutable_list) ]

    txt = blue_print(txt, [
         ["$$ADAPTABLE$$",        "\n".join(adaptable_txt)],
         ["$$IMMUTABLE$$",        "\n".join(immutable_txt)],
         ["$$TYPE_DEFINITIONS$$", _type_definitions()],
         ["$$ERROR_IF_NO_CONFIGURATION_BY_MACRO$$", Lng.ERROR_IF_DEFINED_AND_NOT_CONFIGURATION_BY_MACRO(setting_list)],
     ])

    return adapt.do(txt, Setup.output_directory)

def _type_definitions():
    token_descr = token_db.token_type_definition
    if Setup.computed_gotos_f: type_goto_label  = "void*"
    else:                      type_goto_label  = "int32_t"

    type_def_list = [
        ("lexatom_t",         Setup.lexatom.type),
        ("token_id_t",        token_descr.token_id_type),
        ("token_line_n_t",    token_descr.line_number_type.get_pure_text()),
        ("token_column_n_t",  token_descr.column_number_type.get_pure_text()),
        ("acceptance_id_t",   "int"),
        ("indentation_t",     "int"),
        ("stream_position_t", "intmax_t"),
        ("goto_label_t",      type_goto_label)
    ]

    excluded = ""
    if not blackboard.required_support_indentation_count():
        excluded = "indentation_t"

    def_str = "\n".join(Lng.QUEX_TYPE_DEF(original, customized_name) 
                        for customized_name, original in type_def_list 
                        if customized_name != excluded)

    return Lng.FRAME_IN_NAMESPACE_MAIN(def_str)

def _lexatom_newline_in_engine_encoding():
    if not blackboard.required_support_begin_of_line():
        return ord("\n")  # Anyway, the value is unused

    lexatom_sequence = Setup.buffer_encoding.do_single(ord('\n')) 
    # Any misfit must be caught at pattern definition time.
    if not len(lexatom_sequence) == 1:
        return ord("\n")

    return lexatom_sequence[0]


