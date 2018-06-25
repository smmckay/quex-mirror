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
import quex.output.token.id_generator            as     token_id_maker
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

    content_table = _get_token_class()

    if Setup.token_class_only_f:
        _write_all(content_table)
        return

    else:
        content_table.append(
            (token_id_maker.do(Setup), Setup.output_token_id_file_ref)
        )
        ## class_token_implementation = content_table[-1][0]
        ## del content_table[-1]
        content_table.extend(_get_analyzers(mode_db))
        content_table.extend(lexeme_converter.do()) # [Optional]
        _write_all(content_table)

        source_package.do(Setup.output_directory)
        return

def analyzer_functions_get(ModeDB):
    # (*) Get list of modes that are actually implemented
    #     (abstract modes only serve as common base)
    mode_name_list = ModeDB.keys()  

    code = flatten_list_of_lists( 
        engine_generator.do_with_counter(mode, mode_name_list) for mode in ModeDB.itervalues() 
    )

    code.append(
        engine_generator.comment_match_behavior(ModeDB.itervalues())
    )

    # generate frame for analyser code
    return Lng.FRAME_IN_NAMESPACE_MAIN("".join(code))

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
    token_class = Lng.NAME_IN_NAMESPACE(Setup.token_class_name, Setup.token_class_name_space) 
    info_list = [
        ## "  --token-id-prefix  %s" % Setup.token_id_prefix,
        "  --token-class-file %s" % Setup.output_token_class_file,
        "  --token-class      %s" % token_class,
        "  --token-id-type    %s" % Setup.token_id_type,
        "  --lexatom-type     %s" % Setup.lexatom.type,
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

def _prepare_analyzers(mode_db): 
    # (*) implement the lexer mode-specific analyser functions
    function_analyzers_implementation \
                            = analyzer_functions_get(mode_db)

    # (*) Implement the 'quex' core class from a template
    # -- do the coding of the class framework
    configuration_header    = configuration.do(mode_db)
    analyzer_header, \
    member_function_signature_list = analyzer_class.do(mode_db, Epilog="") 
    analyzer_implementation = analyzer_class.do_implementation(mode_db, 
                                                               member_function_signature_list) 
    mode_implementation     = mode_classes.do(mode_db)

    # Engine (Source Code)
    engine_txt = "\n".join([Lng.ENGINE_TEXT_EPILOG(),
                            mode_implementation,
                            function_analyzers_implementation,
                            analyzer_implementation,
                            "\n"])

    return configuration_header, \
           analyzer_header, \
           engine_txt

def _get_token_class():
    """RETURNS: [0] List of (source code, file-name)
                [1] Source code for global lexeme null declaration
    """
    class_token_header,        \
    class_token_implementation = token_class.do()

    if Setup.token_class_only_f:
        class_token_header = do_token_class_info() + class_token_header

    return [
        (class_token_header,         token_db.token_type_definition.get_file_name()),
        (class_token_implementation, Setup.output_token_class_file_implementation),
    ]

def _get_analyzers(mode_db):
    configuration_header, \
    analyzer_header,      \
    engine_txt            = _prepare_analyzers(mode_db)

    return [
        (configuration_header, Setup.output_configuration_file),
        (analyzer_header,      Setup.output_header_file),
        (engine_txt,           Setup.output_code_file),
    ]

def _write_all(content_table):

    content_table = [
        (adapt.do(x[0], Setup.output_directory), x[1]) for x in content_table
    ]
    content_table = [
        (Lng.straighten_open_line_pragmas_new(x[0], x[1]), x[1]) for x in content_table
    ]

    for content, file_name in content_table:
        if not content: continue
        write_safely_and_close(file_name, content)

