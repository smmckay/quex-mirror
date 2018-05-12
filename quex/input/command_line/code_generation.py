import quex.input.command_line.validation            as     validation
from   quex.input.setup                              import global_character_type_db,  \
                                                            command_line_args_defined, \
                                                            command_line_arg_position
from   quex.input.files.token_type                   import TokenTypeDescriptorManual
from   quex.input.files.token_id_file                import parse as token_id_file_parse
from   quex.output.languages.core                    import db as output_language_db
from   quex.engine.misc.file_in                      import read_namespaced_name
import quex.engine.misc.error                        as     error 

import quex.token_db   as     token_db
from   quex.blackboard import setup as Setup
from   quex.constants  import E_Compression

from   operator import itemgetter
import re
import sys


def prepare(command_line, argv):
    """RETURN:  True, if process needs to be started.
                False, if job is done.
    """

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

    # Is the output file naming scheme provided by the extension database
    # (Validation must happen immediately)
    Setup.language_db.extension_db = Setup.language_db.all_extension_db.get(Setup.output_file_naming_scheme)
    if Setup.language_db.extension_db is None:
        error.log("File extension scheme '%s' is not provided for language '%s'.\n" \
                  % (Setup.output_file_naming_scheme, Setup.language) + \
                  "Available schemes are: %s." % repr(sorted(Setup.language_db.all_extension_db.keys()))[1:-1])

    if Setup.buffer_byte_order == "<system>": 
        Setup.buffer_byte_order                      = sys.byteorder 
        Setup.byte_order_is_that_of_current_system_f = True
    else:
        Setup.byte_order_is_that_of_current_system_f = False

    if Setup.__buffer_lexatom_size_in_byte == "wchar_t":
        error.log("Since Quex version 0.53.5, 'wchar_t' can no longer be specified\n"
                  "with option '--buffer-element-size' or '-bes'. Please, specify\n"
                  "'--buffer-element-type wchar_t' or '--bet'.")

    if Setup.__buffer_lexatom_type == "wchar_t":
        Setup.converter_ucs_coding_name = "WCHAR_T"

    Setup.buffer_setup(Setup.__buffer_lexatom_type,
                       Setup.__buffer_lexatom_size_in_byte,
                       Setup.buffer_encoding_name, 
                       Setup.buffer_encoding_file) 

    type_info = global_character_type_db.get(Setup.lexatom.type)
    if     type_info is not None and len(type_info) >= 4 \
       and type_info[3] != -1 and Setup.lexatom.size_in_byte != -1 \
       and type_info[3] != Setup.lexatom.size_in_byte:
        error.log("\nBuffer element type ('--bet' or '--buffer-element-type') was set to '%s'.\n" \
                  % Setup.lexatom.type \
                  + "It is well known to be of size %s[byte]. However, the buffer element size\n" \
                  % type_info[3] \
                  + "('-b' or '--buffer-element-type') was specified as '%s'.\n\n" \
                  % Setup.lexatom.size_in_byte \
                  + "Quex can continue, but the result is questionable.\n", \
                  DontExitF=True)

    if Setup.converter_ucs_coding_name == "": 
        if global_character_type_db.has_key(Setup.lexatom.type):
            if Setup.buffer_byte_order == "little": index = 1
            else:                                   index = 2
            Setup.converter_ucs_coding_name = global_character_type_db[Setup.lexatom.type][index]

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

        token_id_file_parse(Setup.extern_token_id_file)

    # AFTER: Setup.extern_token_id_file !!!
    if Setup.language not in ["DOT"]: Setup.prepare_all_file_names()

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
        ClassName --> analyzer_class_name = ClassName
                      analyzer_name_space = []
    """
    Setup.analyzer_class_name, \
    Setup.analyzer_name_space, \
    Setup.analyzer_name_safe   = \
         read_namespaced_name(Setup.analyzer_class, 
                              "analyzer class (options -o, --analyzer-class)")

    if Setup.show_name_spaces_f:
        print "FSM: {"
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
    """
    if not Setup.token_class:
        default_name = "Token"
        if Setup.analyzer_class_name:
            Setup.token_class = "%s_%s" % (Setup.analyzer_class_name, default_name)
        else:
            Setup.token_class = default_name

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
        token_db.token_type_definition = \
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

