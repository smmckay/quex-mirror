import quex.output.languages.cpp.source_package          as     source_package
#
import quex.input.files.core                             as     quex_file_parser
#                                                        
from   quex.engine.misc.tools                            import flatten_list_of_lists
from   quex.engine.misc.file_operations                  import write_safely_and_close
#
import quex.output.core.engine                           as     engine_generator
import quex.output.analyzer.core                         as     analyzer_class
import quex.output.analyzer.configuration                as     configuration 
import quex.output.analyzer.lexeme_converter             as     lexeme_converter 
import quex.output.languages.cpp.token_class             as     token_class
import quex.output.languages.cpp.mode_classes            as     mode_classes
import quex.output.languages.graphviz.core               as     grapviz_generator

import quex.blackboard as     blackboard
from   quex.blackboard import setup as Setup, \
                              Lng

from   operator import attrgetter

def do():
    """Generates state machines for all modes. Each mode results into 
       a separate state machine that is stuck into a virtual function
       of a class derived from class 'quex_mode'.
    """
    if Setup.language == "DOT": 
        return do_plot()

    mode_db = quex_file_parser.do(Setup.input_mode_files)

    _generate(mode_db)

def _generate(mode_db):
    token_id_header,                \
    global_lexeme_null_declaration, \
    class_token_header,             \
    class_token_implementation      = token_class.do()

    if Setup.token_class_only_f:
        class_token_header =   do_token_class_info() \
                             + class_token_header
        _write_token_class(class_token_header, 
                           class_token_implementation, 
                           token_id_header)
        return

    configuration_header,                 \
    analyzer_header,                      \
    engine_txt,                           \
    lexeme_converter_header,        \
    lexeme_converter_implementation = _prepare_all(mode_db, 
                                                         class_token_implementation,
                                                         global_lexeme_null_declaration)

    _write_all(configuration_header, analyzer_header, engine_txt, 
               class_token_header, token_id_header,
               lexeme_converter_header, 
               lexeme_converter_implementation)

    if Setup.source_package_directory != "":
        source_package.do()

def analyzer_functions_get(ModeDB):
    # (*) Get list of modes that are actually implemented
    #     (abstract modes only serve as common base)
    mode_name_list = ModeDB.keys()  

    def code_for_mode(mode):
        if mode.run_time_counter_db is not None:
            txt = engine_generator.do_run_time_counter(mode) 
        else:
            txt = []

        txt.extend(engine_generator.do(mode, mode_name_list))
        return txt

    code = flatten_list_of_lists( 
        code_for_mode(mode) for mode in ModeDB.itervalues() 
    )

    code.append(
        do_comment_pattern_action_pairs(ModeDB.itervalues())
    )

    # generate frame for analyser code
    return engine_generator.frame_this("".join(code))

def do_plot():
    mode_db = quex_file_parser.do(Setup.input_mode_files)

    for mode in mode_db.itervalues():        
        plotter = grapviz_generator.Generator(mode)
        plotter.do(Option=Setup.character_display)

def do_token_class_info():
    info_list = [
        "  --token-id-prefix       %s" % Setup.token_id_prefix,
        "  --token-class-file      %s" % Setup.output_token_class_file,
        "  --token-class           %s" % Setup.token_class,
        "  --token-id-type         %s" % Setup.token_id_type,
        "  --buffer-element-type   %s" % Setup.buffer_lexatom_type,
        "  --foreign-token-id-file %s" % Setup.output_token_id_file,
    ]
    print "info: Analyzers using this token class must be generated with"
    print "info:"
    for line in info_list:
        print "info:    %s" % line
    print "info:"
    print "info: Header: \"%s\"" % blackboard.token_type_definition.get_file_name() 
    print "info: Source: \"%s\"" % Setup.output_token_class_file_implementation

    comment = ["<<<QUEX-OPTIONS>>>\n"]
    for line in info_list:
        if line.find("--token-class-file") != -1: continue
        comment.append("%s\n" % line)
    comment.append("<<<QUEX-OPTIONS>>>")
    return Lng.ML_COMMENT("".join(comment), IndentN=0)

def do_comment_pattern_action_pairs(ModeIterable):
    """Write some comment on the pattern action pairs of all modes.
    """
    if not Setup.comment_mode_patterns_f:
        return ""

    txt = "".join(
        mode.documentation.get_string()
        for mode in sorted(ModeIterable, key=attrgetter("name"))
    )
    comment = Lng.ML_COMMENT("BEGIN: MODE PATTERNS\n" + \
                             txt                      + \
                             "\nEND: MODE PATTERNS")
    return comment 

    # (*) [Optional] Make a customized token class

def _prepare_all(mode_db, class_token_implementation, 
                 global_lexeme_null_declaration): 
    # (*) implement the lexer mode-specific analyser functions
    function_analyzers_implementation \
                            = analyzer_functions_get(mode_db)

    # (*) Implement the 'quex' core class from a template
    # -- do the coding of the class framework
    configuration_header    = configuration.do(mode_db)
    analyzer_header         = analyzer_class.do(mode_db, 
                                                Epilog=global_lexeme_null_declaration) 
    analyzer_implementation = analyzer_class.do_implementation(mode_db) 
    mode_implementation     = mode_classes.do(mode_db)

    # (*) [Optional] Generate a converter helper
    lexeme_converter_header, \
    lexeme_converter_implementation = lexeme_converter.do()
    
    # Engine (Source Code)
    engine_txt = "\n".join([Lng.ENGINE_TEXT_EPILOG(),
                            mode_implementation,
                            function_analyzers_implementation,
                            analyzer_implementation,
                            class_token_implementation, "\n"])

    return configuration_header, \
           analyzer_header, \
           engine_txt, \
           lexeme_converter_header, \
           lexeme_converter_implementation

def _write_all(configuration_header, analyzer_header, engine_txt, 
               class_token_header, token_id_header, 
               lexeme_converter_header, 
               lexeme_converter_implementation):

    if lexeme_converter_header is not None:
        write_safely_and_close(Setup.output_buffer_codec_header,   
                               lexeme_converter_header) 
        write_safely_and_close(Setup.output_buffer_codec_header_i, 
                               lexeme_converter_implementation) 

    if token_id_header is not None:
        assert not Setup.extern_token_id_file
        write_safely_and_close(Setup.output_token_id_file, token_id_header)

    write_safely_and_close(Setup.output_configuration_file, configuration_header)


    write_safely_and_close(Setup.output_header_file, analyzer_header)
    write_safely_and_close(Setup.output_code_file,   engine_txt)

    if class_token_header:
        write_safely_and_close(blackboard.token_type_definition.get_file_name(), 
                               class_token_header)

    _straighten_open_line_pragmas_all()

def _write_token_class(class_token_header, class_token_implementation, 
                       token_id_header):
    write_safely_and_close(blackboard.token_type_definition.get_file_name(), 
                           class_token_header) 
    Lng.straighten_open_line_pragmas(blackboard.token_type_definition.get_file_name())
    write_safely_and_close(Setup.output_token_class_file_implementation,
                           class_token_implementation)
    Lng.straighten_open_line_pragmas(Setup.output_token_class_file_implementation)

    if token_id_header is not None:
        write_safely_and_close(Setup.output_token_id_file, token_id_header)
        Lng.straighten_open_line_pragmas(Setup.output_token_id_file)

def _straighten_open_line_pragmas_all():
    Lng.straighten_open_line_pragmas(Setup.output_header_file)
    Lng.straighten_open_line_pragmas(Setup.output_code_file)
    if not blackboard.token_type_definition.manually_written():
        Lng.straighten_open_line_pragmas(blackboard.token_type_definition.get_file_name())


