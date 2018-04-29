import quex.output.languages.cpp.source_package  as     source_package
#
import quex.input.files.core                     as     quex_file_parser
#                                                
from   quex.engine.misc.tools                    import flatten_list_of_lists
from   quex.engine.misc.file_operations          import write_safely_and_close
#
import quex.output.core.engine                   as     engine_generator
import quex.output.analyzer.core                 as     analyzer_class
import quex.output.analyzer.adapt                as     adapt
import quex.output.analyzer.configuration        as     configuration 
import quex.output.analyzer.lexeme_converter     as     lexeme_converter 
import quex.output.token.core                    as     token_class
import quex.output.analyzer.modes                as     mode_classes
import quex.output.languages.graphviz.core       as     grapviz_generator

import quex.token_db   as     token_db
from   quex.blackboard import setup as Setup, \
                              Lng

def do():
    """Generates state machines for all modes. Each mode results into 
       a separate state machine that is stuck into a virtual function
       of a class derived from class 'quex_mode'.
    """
    if Setup.language == "DOT": 
        return do_plot()

    if not Setup.converter_only_f:
        mode_db = quex_file_parser.do(Setup.input_mode_files)
    else:
        mode_db = None

    _generate(mode_db)

def _generate(mode_db):
    if Setup.converter_only_f:
        content_table = lexeme_converter.do()
        do_converter_info(content_table[0][1], content_table[1][1])
        _write_all(content_table)
        return

    elif Setup.token_class_only_f:
        content_table, global_lexeme_null_declaration = _get_token_class()
        class_token_header  = content_table[1][0]
        content_table[1][0] = do_token_class_info() + class_token_header
        _straighten_line_pragmas_token_class()
    else:
        content_table, global_lexeme_null_declaration = _get_token_class()
        class_token_implementation = content_table[-1][0]
        content_table.extend(_get_analyzers(mode_db, 
                                            class_token_implementation, 
                                            global_lexeme_null_declaration))
        content_table.extend(lexeme_converter.do()) # [Optional]

    _write_all(content_table)
    _straighten_open_line_pragmas_all()
    source_package.do(Setup.output_directory)

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
        engine_generator.comment_match_behavior(ModeDB.itervalues())
    )

    # generate frame for analyser code
    return engine_generator.frame_this("".join(code))

def do_plot():
    mode_db = quex_file_parser.do(Setup.input_mode_files)

    for mode in mode_db.itervalues():        
        plotter = grapviz_generator.Generator(mode)
        plotter.do(Option=Setup.character_display)

def do_converter_info(HeaderFileName, SourceFileName):
    print "  Generate character and string converter functions"
    print
    print "     from encoding: %s;" % Setup.buffer_encoding.name
    print "          type:     %s;" % Setup.lexatom.type
    print "     to:            utf8, utf16, utf32, 'char', and 'wchar_t'."
    print
    print "     header: %s" % HeaderFileName
    print "     source: %s" % SourceFileName
    print

def do_token_class_info():
    info_list = [
        "  --token-id-prefix       %s" % Setup.token_id_prefix,
        "  --token-class-file      %s" % Setup.output_token_class_file,
        "  --token-class           %s" % Setup.token_class,
        "  --token-id-type         %s" % Setup.token_id_type,
        "  --buffer-element-type   %s" % Setup.lexatom.type,
        "  --foreign-token-id-file %s" % Setup.output_token_id_file,
    ]
    if token_db.support_repetition():
        info_list.append("  --token-class-support-repetition")
    if token_db.support_take_text():
        info_list.append("  --token-class-support-take-text")

    print "info: Analyzers using this token class must be generated with"
    print "info:"
    for line in info_list:
        print "info:    %s" % line
    print "info:"
    print "info: Header: \"%s\"" % token_db.token_type_definition.get_file_name() 
    print "info: Source: \"%s\"" % Setup.output_token_class_file_implementation

    comment = ["<<<QUEX-OPTIONS>>>\n"]
    for line in info_list:
        if line.find("--token-class-file") != -1: continue
        comment.append("%s\n" % line)
    comment.append("<<<QUEX-OPTIONS>>>")
    return Lng.ML_COMMENT("".join(comment), IndentN=0)

def _prepare_analyzers(mode_db, class_token_implementation, 
                       global_lexeme_null_declaration): 
    # (*) implement the lexer mode-specific analyser functions
    function_analyzers_implementation \
                            = analyzer_functions_get(mode_db)

    # (*) Implement the 'quex' core class from a template
    # -- do the coding of the class framework
    configuration_header    = configuration.do(mode_db)
    analyzer_header, \
    member_function_signature_list = analyzer_class.do(mode_db, 
                                                       Epilog=global_lexeme_null_declaration) 
    analyzer_implementation = analyzer_class.do_implementation(mode_db, 
                                                               member_function_signature_list) 
    mode_implementation     = mode_classes.do(mode_db)

    # Engine (Source Code)
    engine_txt = "\n".join([Lng.ENGINE_TEXT_EPILOG(),
                            mode_implementation,
                            function_analyzers_implementation,
                            analyzer_implementation,
                            class_token_implementation, "\n"])

    return configuration_header, \
           analyzer_header, \
           engine_txt

def _get_token_class():
    """RETURNS: [0] List of (source code, file-name)
                [1] Source code for global lexeme null declaration
    """
    token_id_header,                \
    global_lexeme_null_declaration, \
    class_token_header,             \
    class_token_implementation      = token_class.do()

    return [
        (token_id_header,            Setup.output_token_id_file),
        (class_token_header,         token_db.token_type_definition.get_file_name()),
        (class_token_implementation, Setup.output_token_class_file_implementation),
    ], global_lexeme_null_declaration

def _get_analyzers(mode_db, class_token_implementation, global_lexeme_null_declaration):
    configuration_header, \
    analyzer_header,      \
    engine_txt            = _prepare_analyzers(mode_db, 
                                               class_token_implementation,
                                               global_lexeme_null_declaration)

    return [
        (configuration_header, Setup.output_configuration_file),
        (analyzer_header,      Setup.output_header_file),
        (engine_txt,           Setup.output_code_file),
    ]

def _write_all(content_table):

    content_table = [
        (adapt.do(x[0], Setup.output_directory), x[1]) for x in content_table
    ]

    for content, file_name in content_table:
        if content is None: continue
        write_safely_and_close(file_name, content)


def _straighten_line_pragmas_token_class():
    Lng.straighten_open_line_pragmas(token_db.token_type_definition.get_file_name())
    Lng.straighten_open_line_pragmas(Setup.output_token_class_file_implementation)
    if token_id_header is not None:
        Lng.straighten_open_line_pragmas(Setup.output_token_id_file)

def _straighten_open_line_pragmas_all():
    Lng.straighten_open_line_pragmas(Setup.output_header_file)
    Lng.straighten_open_line_pragmas(Setup.output_code_file)
    if not token_db.token_type_definition.manually_written():
        Lng.straighten_open_line_pragmas(token_db.token_type_definition.get_file_name())


