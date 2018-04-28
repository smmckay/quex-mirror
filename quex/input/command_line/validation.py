from   quex.DEFINITIONS              import QUEX_PATH
import quex.input.command_line.query as     query
from   quex.input.setup              import SETUP_INFO, DEPRECATED, \
                                            command_line_args_string, \
                                            command_line_args, \
                                            SetupParTypes
import quex.engine.codec_db.core     as     codec_db
import quex.engine.misc.error        as     error
from   quex.engine.misc.file_in      import is_identifier
import os.path

def do(setup, command_line, argv):
    """Does a consistency check for setup and the command line.
    """
    if setup.extern_token_id_file_show_f and not setup.extern_token_id_file:
        error.log("Option '--foreign-token-id-file-show' cannot be used without\n"
                  "option '--foreign-token-id-file'.")

    if os.path.isfile(setup.output_directory):
        error.log("The name '%s' is already a file and may not be used as output directory." 
                  % setup.output_directory)
    elif os.path.isdir(setup.output_directory):
        if os.access(setup.output_directory, os.W_OK) == False:
            error.log("The directory '%s' is not writeable." 
                      % setup.output_directory)
    else:
        os.mkdir(setup.output_directory)

    # if the mode is '--language dot' => check character display options. 
    if setup.character_display not in ["hex", "utf8"]:
        error.log("Character display must be either 'hex' or 'utf8'.\nFound: '%s'" % 
                  setup.character_display)

    # ensure that options are not specified twice
    for parameter, info in SETUP_INFO.items():
        if type(info) != list: continue
        occurence_n = 0 
        for option in info[0]:
            occurence_n += argv.count(option)
        if occurence_n > 1 and info[1] not in (SetupParTypes.LIST, SetupParTypes.INT_LIST):
            error.log("Received more than one of the following options:\n" + \
                      "%s" % repr(info[0])[1:-1])

    # (*) Check for 'Depraceted' Options ___________________________________________________
    for name, info in DEPRECATED.items():
        command_line_options = SETUP_INFO[name][0]
        comment                   = info[0]
        depreciated_since_version = info[1]
        for option in command_line_options:
            if command_line.search(option):
                error.log("Command line option '%s' is ignored.\n" % option + \
                          comment + "\n" + \
                          "Last version of Quex supporting this option is version %s. Please, visit\n" % \
                          depreciated_since_version + \
                          "http://quex.org for further information.")
                          
    # (*) Check for 'Straying' Options ___________________________________________________
    options = []
    for key, info in SETUP_INFO.items():
        if type(info) != list: continue
        if key in DEPRECATED: continue
        if info[1] is not None: options.extend(info[0])
    options.sort(lambda a,b: cmp(a.replace("-",""), b.replace("-","")))

    ufos = command_line.unidentified_options(options)
    if len(ufos) != 0:
        error.log("Unidentified option(s) = " +  repr(ufos) + "\n" + \
                  __get_supported_command_line_option_description(options))

    if setup.analyzer_derived_class_name != "" and \
       setup.analyzer_derived_class_file == "":
            error.log("Specified derived class '%s' on command line, but it was not\n" % \
                      setup.analyzer_derived_class_name + \
                      "specified which file contains the definition of it.\n" + \
                      "use command line option '--derived-class-file'.\n")

    if setup.lexatom.size_in_byte not in [-1, 1, 2, 4]:
        error.log("The setting of '--buffer-element-size' (or '-b') can only be\n" 
                  "1, 2, or 4 (found %s)." % repr(setup.lexatom.size_in_byte))

    if setup.buffer_byte_order not in ["<system>", "little", "big"]:
        error.log("Byte order (option --endian) must be 'little', 'big', or '<system>'.\n" + \
                  "Note, that this option is only interesting for cross plattform development.\n" + \
                  "By default, quex automatically chooses the endian type of your system.")

    # Manually written token class requires token class name to be specified
    if setup.extern_token_class_file and command_line.search("--token-class", "--tc") == False:
        error.log("The use of a manually written token class requires that the name of the class\n"
                  "is specified on the command line via the '--token-class' option.")

    if setup.converter_only_f and not setup.lexatom.type:
        error.log("Lexatom type must be specific for converter generation.")
    
    # Check that names are valid identifiers
    if setup.token_id_prefix_plain:
        __check_identifier(setup, "token_id_prefix_plain", "Token prefix")
    __check_identifier(setup, "analyzer_class_name", "Engine name")
    if setup.analyzer_derived_class_name != "": 
        __check_identifier(setup, "analyzer_derived_class_name", "Derived class name")
    
    __check_file_name(setup, "extern_token_class_file",                 "file containing token class definition")
    __check_file_name(setup, "analyzer_derived_class_file",      "file containing user derived lexer class")
    __check_file_name(setup, "extern_token_id_file", "file containing user token ids", 0,
                      CommandLineOption=SETUP_INFO["extern_token_id_file"])
    __check_file_name(setup, "input_mode_files", "quex source file")

    # Internal engine character encoding
    if setup.buffer_encoding.name != "unicode":
        if not setup.buffer_encoding_file:
            error.verify_word_in_list(setup.buffer_encoding_name,
                                      codec_db.get_supported_codec_list() + ["utf8", "utf16"],
                                      "Codec '%s' is not supported." % setup.buffer_encoding.name)
        # NOT: __check_codec_vs_buffer_lexatom_size_in_byte("utf8", 1)
        # BECAUSE: Code unit size is one. No type has a size of less than one byte!
        __check_codec_vs_buffer_lexatom_size_in_byte(setup, "utf16", 2)

def __check_identifier(setup, Candidate, Name):
    value = setup.__dict__[Candidate]
    if is_identifier(value): return

    CommandLineOption = ""
    if type(SETUP_INFO) == list:
        CommandLineOption = " (%s)" % str(SETUP_INFO[Candidate][0])[-1:1]

    error.log("%s must be a valid identifier%s.\n" % (Name, CommandLineOption) + \
              "Received: '%s'" % value)

def __get_supported_command_line_option_description(NormalModeOptions):
    txt = "OPTIONS:\n"
    for option in NormalModeOptions:
        txt += "    " + option + "\n"

    txt += "\nOPTIONS FOR QUERY MODE:\n"
    txt += query.get_supported_command_line_option_description()
    return txt

def __check_file_name(setup, Candidate, Name, Index=None, CommandLineOption=None):
    value             = setup.__dict__[Candidate]
    if len(value) == 0: return

    if CommandLineOption is None:
        CommandLineOption = command_line_args(Candidate)

    if Index is not None:
        if type(value) != list or len(value) <= Index: value = ""
        else:                                          value = value[Index]

    if type(value) == list:
        for name in value:
            if name.startswith("-"):
                error.log("Quex refuses to work with file names that start with '-' (minus).\n"  + \
                          "Received '%s' for %s (%s)" % (value, name, repr(CommandLineOption)[1:-1]))
            if os.access(name, os.F_OK) == False:
                # error.log("File %s (%s)\ncannot be found." % (name, Name))
                error.log_file_not_found(name, Name)
    else:
        if value == "" or value[0] == "-":              return
        if os.access(value, os.F_OK):                   return
        if os.access(QUEX_PATH + "/" + value, os.F_OK): return
        if     os.access(os.path.dirname(value), os.F_OK) == False \
           and os.access(QUEX_PATH + "/" + os.path.dirname(value), os.F_OK) == False:
            error.log("File '%s' is supposed to be located in directory '%s' or\n" % \
                      (os.path.basename(value), os.path.dirname(value)) + \
                      "'%s'. No such directories exist." % \
                      (QUEX_PATH + "/" + os.path.dirname(value)))
        error.log_file_not_found(value, Name)

def __check_codec_vs_buffer_lexatom_size_in_byte(setup, CodecName, RequiredBufferElementSize):
    if   setup.buffer_encoding.name != CodecName:                  return
    elif setup.lexatom.size_in_byte >=  RequiredBufferElementSize: return

    if setup.lexatom.size_in_byte == -1: 
        msg_str = "undetermined (found type '%s')" % setup.lexatom.type
    else:
        msg_str = "is not %i (found %i)" % (RequiredBufferElementSize, setup.lexatom.size_in_byte)

    error.log("Using encoding '%s' while buffer element size is %s.\n" % (CodecName, msg_str) + 
              "Consult command line argument %s" \
              % command_line_args_string("__buffer_lexatom_size_in_byte"))

