import quex.input.command_line.validation            as     validation
from   quex.input.setup                              import global_extension_db,      \
                                                            global_character_type_db, \
                                                            command_line_args_defined, \
                                                            command_line_arg_position, \
                                                            E_Files
from   quex.input.files.token_type                   import TokenTypeDescriptorManual
from   quex.input.files.token_id_file                import parse as token_id_file_parse
from   quex.output.languages.core                   import db as output_language_db
from   quex.engine.misc.file_in                      import read_namespaced_name
import quex.engine.misc.error                        as     error 
import quex.engine.state_machine.transformation.core as     bc_factory


from   quex.blackboard import setup as Setup
import quex.blackboard as     blackboard
from   quex.constants  import E_Compression

from   operator import itemgetter
import re
import sys
import os

def prepare(command_line, argv):
    """RETURN:  True, if process needs to be started.
                False, if job is done.
    """
    global Setup

    # (*) Classes and their namespace
    __setup_analyzer_class(Setup)
    __setup_token_class(Setup)
    __setup_token_id_prefix(Setup)
    # __setup_lexeme_null(Setup)       # Requires 'token_class_name_space'

    # (*) Output programming language        
    Setup.language = Setup.language.upper()
    error.verify_word_in_list(Setup.language, output_language_db.keys(),
                              "Programming language '%s' is not supported." % Setup.language)
    Setup.language_db  = output_language_db[Setup.language]()
    Setup.extension_db = global_extension_db[Setup.language]

    # Is the output file naming scheme provided by the extension database
    # (Validation must happen immediately)
    if Setup.extension_db.has_key(Setup.output_file_naming_scheme) == False:
        error.log("File extension scheme '%s' is not provided for language '%s'.\n" \
                  % (Setup.output_file_naming_scheme, Setup.language) + \
                  "Available schemes are: %s." % repr(Setup.extension_db.keys())[1:-1])

    if Setup.buffer_byte_order == "<system>": 
        Setup.buffer_byte_order                      = sys.byteorder 
        Setup.byte_order_is_that_of_current_system_f = True
    else:
        Setup.byte_order_is_that_of_current_system_f = False

    lexatom_size_in_byte = __prepare_buffer_element_specification(Setup)

    buffer_codec = bc_factory.do(Setup.buffer_codec_name, 
                                 Setup.buffer_codec_file)
    Setup.buffer_codec_set(buffer_codec, lexatom_size_in_byte)

    type_info = global_character_type_db.get(Setup.buffer_lexatom_type)
    if     type_info is not None and len(type_info) >= 4 \
       and type_info[3] != -1 and Setup.buffer_lexatom_size_in_byte != -1 \
       and type_info[3] != Setup.buffer_lexatom_size_in_byte:
        error.log("\nBuffer element type ('--bet' or '--buffer-element-type') was set to '%s'.\n" \
                  % Setup.buffer_lexatom_type \
                  + "It is well known to be of size %s[byte]. However, the buffer element size\n" \
                  % type_info[3] \
                  + "('-b' or '--buffer-element-type') was specified as '%s'.\n\n" \
                  % Setup.buffer_lexatom_size_in_byte \
                  + "Quex can continue, but the result is questionable.\n", \
                  DontExitF=True)

    if Setup.converter_ucs_coding_name == "": 
        if global_character_type_db.has_key(Setup.buffer_lexatom_type):
            if Setup.buffer_byte_order == "little": index = 1
            else:                                   index = 2
            Setup.converter_ucs_coding_name = global_character_type_db[Setup.buffer_lexatom_type][index]

    if Setup.extern_token_id_specification: 
        if len(Setup.extern_token_id_specification) > 3: 
            error.log("Option '--foreign-token-id-file' received > 3 followers.\n"
                      "Found: %s" % str(Setup.extern_token_id_specification)[1:-1])
        if len(Setup.extern_token_id_specification) > 1:
            Setup.token_id_foreign_definition_file_region_begin_re = \
                    __compile_regular_expression(Setup.extern_token_id_specification[1], "token id region begin")
        if len(Setup.extern_token_id_specification) > 2:
            Setup.token_id_foreign_definition_file_region_end_re = \
                    __compile_regular_expression(Setup.extern_token_id_specification[2], "token id region end")
        Setup.extern_token_id_file = \
                Setup.extern_token_id_specification[0]

        CommentDelimiterList = [["//", "\n"], ["/*", "*/"]]
        token_id_file_parse(Setup.extern_token_id_file, 
                            CommentDelimiterList)

    # AFTER: Setup.extern_token_id_file !!!
    if Setup.language not in ["DOT"]:
        prepare_file_names(Setup)

    # (*) Compression Types
    compression_type_list = []
    for name, ctype in [("compression_template_f",         E_Compression.TEMPLATE),
                        ("compression_template_uniform_f", E_Compression.TEMPLATE_UNIFORM),
                        ("compression_path_f",             E_Compression.PATH),
                        ("compression_path_uniform_f",     E_Compression.PATH_UNIFORM)]:
        if command_line_args_defined(command_line, name):
            compression_type_list.append((command_line_arg_position(name), ctype))

    compression_type_list.sort(key=itemgetter(0))
    Setup.compression_type_list = map(lambda x: x[1], compression_type_list)

    validation.do(Setup, command_line, argv)

    # (*) return Setup ___________________________________________________________________
    return True

def __compile_regular_expression(Str, Name):
    tmp = Str.replace("*", "\\*")
    tmp = tmp.replace("?", "\\?")
    tmp = tmp.replace("{", "\\{")
    tmp = tmp.replace("}", "\\}")
    try:
        return re.compile(tmp)
    except:
        error.log("Invalid %s: %s" % (Name, Str))

def __setup_analyzer_class(Setup):
    """ X0::X1::X2::ClassName --> analyzer_class_name = ClassName
                                  analyzer_name_space = ["X0", "X1", "X2"]
        ::ClassName --> analyzer_class_name = ClassName
                        analyzer_name_space = []
        ClassName --> analyzer_class_name = ClassName
                      analyzer_name_space = ["quex"]
    """
    if Setup.analyzer_class.find("::") == -1:
        Setup.analyzer_class = "quex::%s" % Setup.analyzer_class

    Setup.analyzer_class_name, \
    Setup.analyzer_name_space, \
    Setup.analyzer_name_safe   = \
         read_namespaced_name(Setup.analyzer_class, 
                              "analyzer class (options -o, --analyzer-class)")

    if Setup.show_name_spaces_f:
        print "Analyzer: {"
        print "     class_name:  %s;" % Setup.analyzer_class_name
        print "     name_space:  %s;" % repr(Setup.analyzer_name_space)[1:-1]
        print "     name_prefix: %s;" % Setup.analyzer_name_safe   
        print "}"

    Setup.analyzer_derived_class_name,       \
    Setup.analyzer_derived_class_name_space, \
    Setup.analyzer_derived_class_name_safe = \
         read_namespaced_name(Setup.analyzer_derived_class_name, 
                              "derived analyzer class (options --derived-class, --dc)",
                              AllowEmptyF=True)

def __setup_token_class(Setup):
    """ X0::X1::X2::ClassName --> token_class_name = ClassName
                                  token_name_space = ["X0", "X1", "X2"]
        ::ClassName --> token_class_name = ClassName
                        token_name_space = []
        ClassName --> token_class_name = ClassName
                      token_name_space = analyzer_name_space
    """
    if Setup.token_class.find("::") == -1:
        # By default, Setup the token in the analyzer's namespace
        if len(Setup.analyzer_name_space) != 0:
            analyzer_name_space = reduce(lambda x, y: "%s::%s" % (x, y), Setup.analyzer_name_space)
        else:
            analyzer_name_space = ""
        Setup.token_class = "%s::%s" % (analyzer_name_space, Setup.token_class)

    # Token classes and derived classes have the freedom not to open a namespace,
    # thus no check 'if namespace == empty'.
    Setup.token_class_name,       \
    Setup.token_class_name_space, \
    Setup.token_class_name_safe = \
         read_namespaced_name(Setup.token_class, 
                              "token class (options --token-class, --tc)")

    if Setup.show_name_spaces_f:
        print "Token: {"
        print "     class_name:  %s;" % Setup.token_class_name
        print "     name_space:  %s;" % repr(Setup.token_class_name_space)[1:-1]
        print "     name_prefix: %s;" % Setup.token_class_name_safe   
        print "}"

    if Setup.extern_token_class_file:
        blackboard.token_type_definition = \
                TokenTypeDescriptorManual(Setup.extern_token_class_file,
                                          Setup.token_class_name,
                                          Setup.token_class_name_space,
                                          Setup.token_class_name_safe,
                                          Setup.token_id_type)

    #if len(Setup.token_class_name_space) == 0:
    #    Setup.token_class_name_space = deepcopy(Setup.analyzer_name_space)

def __setup_token_id_prefix(Setup):
    Setup.token_id_prefix_plain,      \
    Setup.token_id_prefix_name_space, \
    dummy                           = \
         read_namespaced_name(Setup.token_id_prefix, 
                              "token prefix (options --token-id-prefix)", 
                              AllowEmptyF=True)

    if len(Setup.token_id_prefix_name_space) != 0 and Setup.language.upper() == "C":
         error.log("Token id prefix cannot contain a namespaces if '--language' is set to 'C'.")

def prepare_file_names(Setup):
    # BEFORE file names can be prepared, determine the output directory!
    #
    # If 'source packaging' is enabled and no output directory is specified
    # then take the directory of the source packaging.
    if Setup.source_package_directory and not Setup.output_directory:
        Setup.output_directory = Setup.source_package_directory

    #__________________________________________________________________________
    if Setup.language in ["DOT"]:
        return

    Setup.output_file_stem = ""
    if Setup.analyzer_name_space != ["quex"]:
        for name in Setup.analyzer_name_space:
            Setup.output_file_stem += name + "_"
    Setup.output_file_stem += Setup.analyzer_class_name

    Setup.output_code_file          = __prepare_file_name("",               E_Files.SOURCE) 
    Setup.output_header_file        = __prepare_file_name("",               E_Files.HEADER)
    Setup.output_configuration_file = __prepare_file_name("-configuration", E_Files.HEADER)
    Setup.output_token_id_file      = __prepare_file_name("-token_ids",     E_Files.HEADER)
    if Setup.extern_token_id_file:
        Setup.output_token_id_file_ref = Setup.extern_token_id_file
    else:
        Setup.output_token_id_file_ref = __prepare_file_name("-token_ids",     E_Files.HEADER, 
                                                             BaseNameF=True)
    Setup.output_token_class_file   = __prepare_file_name("-token",         E_Files.HEADER)
    if Setup.token_class_only_f == False:
        Setup.output_token_class_file_implementation = __prepare_file_name("-token",     E_Files.HEADER_IMPLEMTATION)
    else:
        Setup.output_token_class_file_implementation = __prepare_file_name("-token",     E_Files.SOURCE)

    lexeme_converter_dir = "quex/code_base/lexeme_converter"
    if   Setup.buffer_codec.name == "utf8":
        Setup.output_buffer_codec_header   = "%s/from-utf8"    % lexeme_converter_dir
        Setup.output_buffer_codec_header_i = "%s/from-utf8.i"  % lexeme_converter_dir

    elif Setup.buffer_codec.name == "utf16":
        Setup.output_buffer_codec_header   = "%s/from-utf16"   % lexeme_converter_dir
        Setup.output_buffer_codec_header_i = "%s/from-utf16.i" % lexeme_converter_dir

    elif Setup.buffer_codec.name == "utf32":
        Setup.output_buffer_codec_header   = "%s/from-utf32"   % lexeme_converter_dir
        Setup.output_buffer_codec_header_i = "%s/from-utf32.i" % lexeme_converter_dir

    elif Setup.buffer_codec.name != "unicode":
        # Note, that the name may be set to 'None' if the conversion is utf8 or utf16
        # See Internal engine character encoding'
        Setup.output_buffer_codec_header = \
            __prepare_file_name("-converter-%s" % Setup.buffer_codec.name, E_Files.HEADER)
        Setup.output_buffer_codec_header_i = \
            __prepare_file_name("-converter-%s" % Setup.buffer_codec.name, E_Files.HEADER_IMPLEMTATION)
    else:
        Setup.output_buffer_codec_header   = "%s/from-unicode-buffer"   % lexeme_converter_dir
        Setup.output_buffer_codec_header_i = "%s/from-unicode-buffer.i" % lexeme_converter_dir

def __prepare_file_name(Suffix, ContentType, BaseNameF=False):
    global Setup
    assert ContentType in E_Files

    # Language + Extenstion Scheme + ContentType --> name of extension
    ext = Setup.extension_db[Setup.output_file_naming_scheme][ContentType]

    file_name = Setup.output_file_stem + Suffix + ext

    if not Setup.output_directory or BaseNameF:       
        return file_name
    else:                                
        return os.path.normpath(Setup.output_directory + "/" + file_name)

def __prepare_buffer_element_specification(setup):
    global global_character_type_db
    if Setup.buffer_lexatom_size_in_byte == "wchar_t":
        error.log("Since Quex version 0.53.5, 'wchar_t' can no longer be specified\n"
                  "with option '--buffer-element-size' or '-bes'. Please, specify\n"
                  "'--buffer-element-type wchar_t' or '--bet'.")

    if Setup.buffer_lexatom_type == "wchar_t":
        Setup.converter_ucs_coding_name = "WCHAR_T"

    # (*) Determine buffer element type and size (in bytes)
    lexatom_size_in_byte = Setup.buffer_lexatom_size_in_byte
    if lexatom_size_in_byte == -1:
        if global_character_type_db.has_key(Setup.buffer_lexatom_type):
            lexatom_size_in_byte = global_character_type_db[Setup.buffer_lexatom_type][3]
        elif Setup.buffer_lexatom_type == "":
            lexatom_size_in_byte = 1
        else:
            # Buffer element type is not identified in 'global_character_type_db'.
            # => here Quex cannot know its size on its own.
            lexatom_size_in_byte = -1

    if Setup.buffer_lexatom_type == "":
        if lexatom_size_in_byte in [1, 2, 4]:
            Setup.buffer_lexatom_type = { 
                1: "uint8_t", 2: "uint16_t", 4: "uint32_t",
            }[lexatom_size_in_byte]
        elif lexatom_size_in_byte == -1:
            pass
        else:
            error.log("Buffer element type cannot be determined for size '%i' which\n" \
                      % lexatom_size_in_byte + 
                      "has been specified by '-b' or '--buffer-element-size'.")

    return lexatom_size_in_byte

