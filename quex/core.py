from   quex.engine.misc.file_in                 import write_safely_and_close

from   quex.blackboard                          import setup as Setup, \
                                                       Lng
import quex.output.cpp.source_package           as source_package
import quex.blackboard                          as blackboard
#
import quex.input.files.core                    as quex_file_parser
#
import quex.output.cpp.core                     as cpp_generator
import quex.output.cpp.token_id_maker           as token_id_maker
import quex.output.cpp.token_class_maker        as token_class_maker
import quex.output.cpp.analyzer_class           as analyzer_class
import quex.output.cpp.configuration            as configuration 
import quex.output.cpp.mode_classes             as mode_classes
import quex.output.cpp.codec_converter_helper   as codec_converter_helper 
import quex.output.graphviz.core                as grapviz_generator

def do():
    """Generates state machines for all modes. Each mode results into 
       a separate state machine that is stuck into a virtual function
       of a class derived from class 'quex_mode'.
    """
    if Setup.language == "DOT": 
        return do_plot()

    mode_db = quex_file_parser.do(Setup.input_mode_files)

    # (*) [Optional] Generate a converter helper
    codec_converter_helper_header, \
    codec_converter_helper_implementation = codec_converter_helper.do()
    
    # (*) Generate the token ids
    #     (This needs to happen after the parsing of mode_db, since during that
    #      the token_id_db is developed.)
    if Setup.external_lexeme_null_object != "":
        # Assume external implementation
        token_id_header                        = None
        function_map_id_to_name_implementation = ""
    else:
        token_id_header                        = token_id_maker.do(Setup, mode_db) 
        function_map_id_to_name_implementation = token_id_maker.do_map_id_to_name_function()

    # (*) [Optional] Make a customized token class
    class_token_header, \
    class_token_implementation = token_class_maker.do(function_map_id_to_name_implementation)

    if Setup.token_class_only_f:
        write_safely_and_close(blackboard.token_type_definition.get_file_name(), 
                                 do_token_class_info() \
                               + class_token_header)
        write_safely_and_close(Setup.output_token_class_file_implementation,
                               class_token_implementation)
        write_safely_and_close(Setup.output_token_id_file, token_id_header)
        return

    # (*) Implement the 'quex' core class from a template
    # -- do the coding of the class framework
    configuration_header    = configuration.do(mode_db)
    analyzer_header         = analyzer_class.do(mode_db)
    analyzer_implementation = analyzer_class.do_implementation(mode_db) + "\n"
    mode_implementation     = mode_classes.do(mode_db)

    # (*) implement the lexer mode-specific analyser functions
    function_analyzers_implementation = analyzer_functions_get(mode_db)

    # Implementation (Potential Inline Functions)
    if class_token_implementation is not None:
         analyzer_implementation += class_token_implementation + "\n" 

    # Engine (Source Code)
    engine_txt =   mode_implementation                    + "\n" \
                 + function_analyzers_implementation      + "\n" \
                 + function_map_id_to_name_implementation + "\n" 

    # (*) Write Files ___________________________________________________________________
    if codec_converter_helper_header is not None:
        write_safely_and_close(Setup.output_buffer_codec_header,   
                               codec_converter_helper_header) 
        write_safely_and_close(Setup.output_buffer_codec_header_i, 
                               codec_converter_helper_implementation) 

    if token_id_header is not None:
        write_safely_and_close(Setup.output_token_id_file, token_id_header)

    write_safely_and_close(Setup.output_configuration_file, configuration_header)

    if Setup.language == "C":
        engine_txt     += analyzer_implementation
    else:
        analyzer_header = analyzer_header.replace("$$ADDITIONAL_HEADER_CONTENT$$", 
                                                  analyzer_implementation)

    write_safely_and_close(Setup.output_header_file, analyzer_header)
    write_safely_and_close(Setup.output_code_file,   engine_txt)

    if class_token_header is not None:
        write_safely_and_close(blackboard.token_type_definition.get_file_name(), 
                               class_token_header)

    Lng.straighten_open_line_pragmas(Setup.output_header_file)
    Lng.straighten_open_line_pragmas(Setup.output_code_file)
    if not blackboard.token_type_definition.manually_written():
        Lng.straighten_open_line_pragmas(blackboard.token_type_definition.get_file_name())

    if Setup.source_package_directory != "":
        source_package.do()

def analyzer_functions_get(ModeDB):
    IndentationSupportF = blackboard.required_support_indentation_count()
    BeginOfLineSupportF = blackboard.required_support_begin_of_line()

    inheritance_info_str = ""
    analyzer_code        = []

    # (*) Get list of modes that are actually implemented
    #     (abstract modes only serve as common base)
    mode_list      = [ mode for mode in ModeDB.itervalues() if not mode.abstract_f() ]
    mode_name_list = [ mode.name for mode in mode_list ] 

    for mode in mode_list:        
        # -- some modes only define event handlers that are inherited
        if len(mode.pattern_list) == 0: continue

        analyzer_code.extend(cpp_generator.do(mode, mode_name_list))

        if Setup.comment_mode_patterns_f:
            inheritance_info_str += mode.get_documentation()

    # Bring the info about the patterns first
    if Setup.comment_mode_patterns_f:
        comment = []
        Lng.ML_COMMENT(comment, 
                                     "BEGIN: MODE PATTERNS\n" + \
                                     inheritance_info_str     + \
                                     "\nEND: MODE PATTERNS")
        comment.append("\n") # For safety: New content may have to start in a newline, e.g. "#ifdef ..."
        analyzer_code.append("".join(comment))

    # generate frame for analyser code
    return cpp_generator.frame_this("".join(analyzer_code))

def do_plot():
    mode_db = quex_file_parser.do(Setup.input_mode_files)

    for mode in mode_db.values():        
        # -- some modes only define event handlers that are inherited
        pattern_action_pair_list = mode.get_pattern_action_pair_list()
        if len(pattern_action_pair_list) == 0: continue

        plotter = grapviz_generator.Generator(pattern_action_pair_list,
                                              StateMachineName = mode.name)
        plotter.do(Option=Setup.character_display)

def do_token_class_info():
    info_list = [
        "  --token-id-prefix       %s" % Setup.token_id_prefix,
        "  --token-class-file      %s" % Setup.output_token_class_file,
        "  --token-class           %s" % Setup.token_class,
        "  --token-id-type         %s" % Setup.token_id_type,
        "  --buffer-element-type   %s" % Setup.buffer_element_type,
        "  --lexeme-null-object    %s" % Setup.lexeme_null_full_name_cpp,
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
    txt = []
    Lng.ML_COMMENT(txt, "".join(comment), IndentN=0)
    return "".join(txt) + "\n"


