# PURPOSE: 
#
# This file generates DOCUMENTATION for command line arguments of quex. For this,
# it considers the setup definitions in $QUEX_PATH/input/setup.py and the content
# of this file. Any update on the command line options is directly reflected in
# the documentation. 
#
# There is a test in $QUEX_PATH/quex/TEST/ which tests for the consistency of the
# generated documentation with the current command line setup information.
#
# FILES:
#  
# The output files are defined in the variables:
#  
#   'sphinx_file' = file where the sphinx documentation is written.
#   'man_file'    = file where the man page is written.
#
# (C) Frank-Rene Schaefer
#______________________________________________________________________________
import os
import sys
sys.path.insert(0, os.environ["QUEX_PATH"])
#______________________________________________________________________________
sphinx_file = os.environ["QUEX_PATH"] + "/doc/source/appendix/command-line/intro.rst"
man_file    = os.environ["QUEX_PATH"] + "/doc/manpage/quex.1"
#______________________________________________________________________________


from quex.input.command_line.doc_generator import SectionHeader, Option, Item, \
                                                  List, Block, Note, \
                                                  VisitorSphinx, VisitorManPage
from quex.DEFINITIONS import QUEX_VERSION

content = [
SectionHeader("Code Generation"),
"""
This section lists the command line options to control code generation.
""",
Option("input_mode_files", "[file name]+",
    """
    The names following \\v{-i} designate the files containing quex source
    code to be used as input.
    """),
Option("analyzer_class", "[name ::]* name",
    """
    This option defines the name (and possibly name space) of the lexical
    analyser class that is to be created.  The name space can be specified
    by means of a sequence where names are separated by \\v{::}.  At the same time, this
    name also determines the file stem of the output files generated by
    quex. For example, the invocation
    """,
    Block("> quex ... -o MySpace::MySubSpace::MySubSubSpace::Lexer"),
    """
    specifies that the lexical analyzer class is \\v{Lexer} and that it is located
    in the name space \\v{MySubSubSpace} which in turn is located \\v{MySubSpace} which
    it located in \\v{MySpace}.

    If no name space is specified, the analyzer is placed in name space
    \\v{quex} for C++ and the root name space for C. If the analyzer shall be
    placed in the root name space a \\v{::} must be proceeding
    the class name. For example, the invocation
    """,
    Block("> quex ... -o ::Lexer", "bash"),
    """sets up the lexical analyzer in the root name space and
    """,
    Block("> quex ... -o Lexer", "bash"),
    """generates a lexical analyzer class \\v{Lexer} in default name space \\v{quex}.
    """
    ),
Option("insight_f", None,
    """
    Prints insights on construction process together with time stamps. This
    option is usefule for large, complex, and time consuming lexical
    analyzer specifications.
    """),
Option("output_directory", "directory",
    """
     \\v{directory} = name of the output directory where generated files are 
     to be written. This does more than merely copying the sources to another
     place in the file system. It also changes the include file references
     inside the code to refer to the specified \\v{directory} as a base.
    """),
Option("output_file_naming_scheme", "scheme",
    """
    Specifies the file stem and extensions of the output files. The provided
    argument identifies the naming scheme. The possible values for \\v{scheme}
    and their result is mentioned in the list below.
    """,
    Item("C++", 
     List("No extension for header files that contain only declarations.",
     " \\v{.i} for header files containing inline function implementation.",
     " \\v{.cpp} for source files.")),
    Item("C", 
     List("\\v{.h} for header files.",
     "\\v{.c} for source files.")),
    Item("++",
     List("\\v{.h++} for header files.",
     "\\v{.c++} for source files.")),
    Item("pp",
     List("\\v{.hpp} for header files.",
     "\\v{.cpp} for source files.")),
    Item("cc",
     List("\\v{.hh} for header files.",
     "\\v{.cc} for source files.")),
    Item("xx",
     List("\\v{.hxx} for header files.",
          "\\v{.cxx} for source files.")),
    """
    If the option is not provided, then the naming scheme depends on the 
    \\v{--language} command line option.  For \\v{C} there is currently no 
    different naming scheme supported.
    """),
Option("language", "name",
     "Defines the programming language of the output. \\v{name} can be",
     List("\\v{C} for plain C code.",
          "\\v{C++} for C++ code.",
          "\\v{dot} for plotting information in graphviz format.")),

Option("character_display", "hex|utf8",
     """Specifies how the character of the state transition are to be displayed
     when `--language dot` is used.
     """,
     List("\\v{hex} displays the Unicode code point in hexadecimal notation.",
          "\\v{utf8} is specified the character will be displayed 'as is' in UTF8 notation."),
      ),
Option("normalize_f", None,
    """
    If this option is set, the output of '--language dot' will be a normalized
    state machine. That is, the state numbers will start from zero. If this flag 
    is not set, the state indices are the same as in the generated code.
    """),
Option("user_application_version_id", "string",
    """
    \\v{string} = arbitrary name of the version that was generated. This string
    is reported by the `version()` member function of the lexical analyser. 
    """),
Option("mode_transition_check_f", None,
    """
    Turns off the mode transition check and makes the engine a little faster.
    During development this option should not be used. But the final lexical
    analyzer should be created with this option set. 
    """),
Option("single_mode_analyzer_f",  None,
    """
    In case that there is only one mode, this flag can be used to inform quex
    that it is not intended to refer to the mode at all. In that case no
    instance of the mode is going to be implemented. This reduces memory 
    consumption a little and may possibly increase performance slightly.
    """),
Option("string_accumulator_f",  None,
     """
     Turns the string accumulator option off. This disables the use of the string 
     accumulator to accumulate lexemes.
     """),
Option("include_stack_support_f", None,
     """
     Disables the support of include stacks where the state of the lexical 
     analyzer can be saved and restored before diving into included files.
     Setting this flag may speed up a bit compile time
     """),
Option("post_categorizer_f", None, 
     """
     Turns the post categorizer option on. This allows a 'secondary'
     mapping from lexemes to token ids based on their name. See 
     ':ref:`PostCategorizer`'.
     """),
Option("count_line_number_f", None,
     """
     Lets quex generate an analyzer without internal line counting.
     """),
Option("count_column_number_f", None,
     """
     Lets quex generate an analyzer without internal column counting.
     """),
"""
If an independent source package is required that can be compiled without an 
installation of quex, the following option may be used
""",
Option("source_package_directory",  "directory",
     """
     Creates all source code that is required to compile the produced
     lexical analyzer. Only those packages are included which are actually
     required. Thus, when creating a source package the same command line
     'as usual' must be used with the added `--source-package` option.

     The directory name following the option  specifies the place where
     the source package is to be located.
     """),
"""
For the support of derivation from the generated lexical analyzer class the
following command line options can be used.
""",
Option("analyzer_derived_class_name", "name",
    """
    \\v{name} = If specified, the name of the derived class that the user intends to provide
    (see section <<sec-formal-derivation>>). Note, specifying this option
    signalizes that the user wants to derive from the generated class. If this
    is not desired, this option, and the following, have to be left out. The 
    name space of the derived analyzer class is specified analogously to the
    specification for `--analyzer-class`, as mentioned above.
    """),
Option("analyzer_derived_class_file", "file name",
    """
    \\v{file-name} = If specified, the name of the file where the derived class is
    defined.  This option only makes sense in the context of option
    \\v{--derived-class}. 
    """),
Option("token_id_prefix", "prefix",
     """
     \\v{prefix} = Name prefix to prepend to the name
     given in the token-id files. For example, if a token section contains
     the name \\v{COMPLEX} and the token-prefix is \\v{TOKEN_PRE_}
     then the token-id inside the code will be \\v{TOKEN_PRE_COMPLEX}. 

     The token prefix can contain name space delimiters, i.e. \\v{::}. In
     the brief token senders the name space specifier can be left out.
     """),
Option("token_policy", "single|queue",
     """
     Determines the policy for passing tokens from the analyzer to the user. 
     It can be either 'single' or 'queue'.
     """), 

Option("token_memory_management_by_user_f", None,
     """
     Enables the token memory management by the user. This command line
     option is equivalent to the compile option
     """,
     Block("QUEX_OPTION_USER_MANAGED_TOKEN_MEMORY"),
     """
     It provides the functions \\v{token_queue_memory_switch(...)} for
     token policy 'queue' and \\v{token_p_swap(...)} for token policy
     'single'.
     """),
Option("token_queue_size", "number", 
     """
     In conjunction with token passing policy 'queue', \\v{number} specifies
     the number of tokens in the token queue. This determines the maximum
     number of tokens that can be send without returning from the analyzer
     function.
     """), 

Option("token_queue_safety_border", "number", 
     """
     Specifies the number of tokens that can be sent at maximum as reaction to
     one single pattern match. More precisely, it determines the number of 
     token slots that are left empty when the token queue is detected to be
     full.
     """),

Option("token_id_counter_offset", "number",
     """
     \\v{number} = Number where the numeric values for the token ids start
     to count. Note, that this does not include the standard token ids
     for termination, uninitialized, and indentation error.
     """),
"""
Certain token ids are standard, in a sense that they are required for a
functioning lexical analyzer. Namely they are \\v{TERMINATION} and
\\v{UNINITIALIZED}. The default values of those do not follow the token id
offset, but are 0 and 1. If they need to be different, they must be defined
in the \\v{token { ... }} section, e.g.""",
Block("""
    token {
        TERMINATION   = 10001;
        UNINITIALIZED = 10002;
        ...
    }
"""),
"""
A file with token ids can be provided by the option
""",
Option("token_id_foreign_definition", "file name [[begin-str] end-str]",
       """
       \\v{file-name} = Name of the file that contains an alternative definition
       of the numerical values for the token-ids.
        
       Note, that quex does not reflect on actual program code. It extracts the
       token ids by heuristic. The optional second and third arguments allow
       to restrict the region in the file to search for token ids. It starts
       searching from a line that contains \\v{begin-str} and stops at the first
       line containing \\v{end-str}. For example
       """,
       Block("""
           > quex ... --foreign-token-id-file my_token_ids.hpp   \\
                                              yytokentype   '};' \\
                      --token-prefix          Bisonic::token::
       """, "bash"),
       """
       reads only the token ids from the enum in the code fragment \\v{yytokentype}.
       """),
Option("token_id_foreign_definition_file_show_f", None,
     """
     If this option is specified, then Quex prints out the token ids which have
     been found in a foreign token id file.
     """),
"""
The following options support the definition of a independently customized token class:
""",
Option("token_class_file", "file name",
     """
     \\v{file name} = Name of file that contains the definition of the
     token class. The setting provided here is possibly 
     overwritten if the \\v{token_type} section defines a file name
     explicitly.
     """),
Option("token_class", "[name ::]+ name",
     """
     \\v{name} is the name of the token class. Using '::'-separators it is possible
     to defined the exact name space as mentioned for the `--analyzer-class` command
     line option.
     """),
Option("token_id_type", "type name",
     """
     \\v{type-name} defines the type of the token id. This defines internally the 
     macro \\v{QUEX_TYPE_TOKEN_ID}. This macro is to be used when a customized
     token class is defined. The types of Standard C99 'stdint.h' are encouraged.
     """),
Option("token_class_only_f", None,
     """
     When specified, quex only creates a token class. This token class differs
     from the normally generated token classes in that it may be shared between
     multiple lexical analyzers.
     """,
     Note("""
     When this option is specified, then the LexemeNull is implemented along 
     with the token class. In this case all analyzers that use the token class, 
     shall define \\v{--lexeme-null-object} according the token name space.
     """),
),
Option("external_lexeme_null_object", "name [:: name]+", 
     """
     This option specifies the name and name space of the \\v{LexemeNull} object. If the option is
     not specified, then this object is created along with the analyzer
     automatically. When using a shared token class, then this object must
     have been created along with the token class. Announcing the name of
     the lexeme null object prevents quex from generating a lexeme null
     inside the engine itself.
     """),
"""
There may be cases where the characters used to indicate buffer limit needs to
be redefined, because the default value appear in a pattern.  For most codecs,
such as ASCII and Unicode, the buffer limit codes do not intersect with valid
used code points of characters. Theoretically however, the user may define 
buffer codecs that require a different definition of the limiting codes.
The following option allows modification of the buffer limit code:
""",
Option("buffer_limit_code", "number", 
     """Defines the value used to mark buffer borders. This should be a number that
     does not occur as an input character."""),
"""
On several occasions quex produces code related to 'newline'. The coding of 
newline has two traditions: The Unix tradition which codes it plainly as 0x0A, 
and the DOS tradition which codes it as 0x0D followed by 0x0A. To be on the 
safe side by default, quex codes newline as an alternative of both. In case,
that the DOS tradition is not relevant, some performance improvements might
be achieved, if the '0x0D, 0x0A' is disabled. This can be done by the 
following flag.
""",
Option("dos_carriage_return_newline_f", None, 
     """If specified, the DOS newline (0x0D, 0x0A) is not considered whenever
     newline is required."""),
"""
Input codecs other than ASCII or UTF32 (which map 1:1 to Unicode code points)
can be used in two ways. Either on uses a converter that converts the file
content into Unicode and the engine still runs on Unicode, or the engine itself
is adapted to the require codec. 

Currently quex-generated lexers can interact with GNU IConv and IBM's ICU library
as input converters. Using one of those requires, of course, that  
the correspondent library is installed and available. On Unix systems, the iconv library
is usually present. ICU is likely required to be installed but also freely
available. Using input converters, such as IConv or ICU is a flexible solution.
The converter can be adapted dynamically while the internal engine remains
running on Unicode.
""",
Option("converter_iconv_f", None, 
     """
     Enable the use of the IConv library for character stream decoding.
     This is equivalent to defining '-DQUEX_OPTION_CONVERTER_ICONV'
     as a compiler flag. Depending on the compiler setup the '-liconv' flag 
     must be set explicitly in order to link against the IConv
     library.
     """),
Option("converter_icu_f", None,
     """
     Enable the use of IBM's ICU library for character stream decoding.
     This is equivalent to defining '-DQUEX_OPTION_CONVERTER_ICU'
     as a compiler flag. There are a couple of libraries that are required
     for ICU. You can query those using the ICU tool 'icu-config'. A command 
     line call to this tool with '--ldflags' delivers all libraries that need
     to be linked. A typical list is '-lpthread -lm -L/usr/lib -licui18n -licuuc 
     -licudata'."""),
"""
Alternatively, the engine can run directly on a specific codec, i.e. without a conversion
to Unicode. This approach is less flexible, but may be faster.
""",
Option("buffer_codec_name", "codec name",
     """
     Specifies a codec for the generated engine. The codec name specifies
     the codec of the internal analyzer engine. An engine generated for 
     a specific codec can only analyze input of this particular codec. 
     """,
     Note("""
     When \\v{--codec} is specified the command line flag \\v{-b} or
     \\v{--buffer-element-size} does not represent the number of bytes
     per character, but *the number of bytes per code element*. The
     codec UTF8, for example, is of dynamic length and its code elements
     are bytes, thus only \\v{-b 1} makes sense. UTF16 triggers on elements
     of two bytes, while the length of an encoding for a character varies.
     For UTF16, only \\v{-b 2} makes sense.
     """),
),
Option("buffer_codec_file", "file name", 
     """
     By means of this option a freely customized codec can be defined. The
     \\v{file name} determines at the same time the file where
     the codec mapping is described and the codec's name. The codec's name
     is the directory-stripped and extension-less part of the given
     follower.  Each line of such a file must consist of three numbers, that
     specify 'source interval begin', 'source interval length', and 'target
     interval end. Such a line specifies how a cohesive Unicode character
     range is mapped to the number range of the customized codec. For
     example, the mapping for codec iso8859-6 looks like the following.
     """,
     Block("""
                    0x000 0xA1 0x00
                    0x0A4 0x1  0xA4
                    0x0AD 0x1  0xAD
                    0x60C 0x1  0xAC
                    0x61B 0x1  0xBB
                    0x61F 0x1  0xBF
                    0x621 0x1A 0xC1
                    0x640 0x13 0xE0
     """),
     """
     Here, the Unicode range from 0 to 0xA1 is mapped one to one from Unicode to 
     the codec. 0xA4 and 0xAD are also the same as in Unicode. The remaining
     lines describe how Unicode characters from the 0x600-er page are mapped 
     inside the range somewhere from 0xAC to 0xFF.
     """,
     Note("""
     This option is only to be used, if quex does not support the codec
     directly. The options \\v{--codec-info} and \\v{--codec-for-language} help to
     find out whether Quex directly supports a specific codec. If a \\v{--codec-file}
     is required, it is advisable to use \\v{--codec-file-info  file-name.dat} to
     see if the mapping is in fact as desired.""")),
Option("bad_lexatom_detection_f", None, 
       """If present, the encoding error detection is turned off. That also 
       means, that the 'on_bad_lexatom' handler is never possibly be called.
       """),
"""The buffer on which a generated analyzer runs is characterized by its size 
(macro QUEX_SETTING_BUFFER_SIZE), by its element's size, and their type. The latter
two can be specified on the command line.

In general, a buffer element contains what causes a state transition 
in the analyzer. In ASCII code, a state transition happens on one byte 
which contains a character. If converters are used, the internal buffer
runs on plain Unicode. Here also, a character occupies a fixed number
of bytes. The check mark in 4 byte Unicode is coded as as 0x00001327.
It is treated as one chunk and causes a single state transition.

If the internal engine runs on a specific codec (\\v{--codec}) which is
dynamic, e.g. UTF8, then state transitions happen on parts of a character.
The check mark sign is coded in three bytes 0xE2, 0x9C, and 0x93. Each
byte is read separately and causes a separate state transition.
""",
Option("buffer_lexatom_size_in_byte", "1|2|4",
     """
     With this option the number of bytes is specified that a buffer 
     element occupies. 
        
     The size of a buffer element should be large enough so that it can
     carry the Unicode value of any character of the desired input coding
     space.  When using Unicode, to be safe '-b 4' should be used except that
     it is inconceivable that any code point beyond 0xFFFF ever appears. In
     this case '-b 2' is enough.

     When using dynamic sized codecs, this option is better not used. The
     codecs define their chunks themselves. For example, UTF8 is built upon
     one byte chunks and UTF16 is built upon chunks of two bytes. 
     """,
     Note("""
        If a character size different from one byte is used, the 
        \\v{.get_text()} member of the token class does contain an array
        that particular type. This means, that \\v{.text().c_str()}
        does not result in a nicely printable UTF8 string. Use
        the member \\v{.utf8_text()} instead."""),
      ),
Option("buffer_lexatom_type", "type name",
     """
     A flexible approach to specify the buffer element size and type is by
     specifying the name of the buffer element's type, which is the purpose
     of this option. Note, that there are some 'well-known' types such as
     \\v{uint*_t} (C99 Standard), \\v{u*} (Linux Kernel), \\v{unsigned*} (OSAL)
     where the \\v{*} stands for 8, 16, or 32. Quex can derive its size 
     automatically.

     Quex tries to determine the size of the buffer element type. This size is
     important to determine the target codec when converters are used. That
     is, if the size is 4 byte a different Unicode codec is used then if it
     was 2 byte. If quex fails to determine the size of a buffer element from
     the given name of the buffer element type, then the Unicode codec must
     be specified explicitly by '--converter-ucs-coding-name'.

     By default, the buffer element type is determined by the buffer element 
     size.
     """),

Option("buffer_byte_order", "little|big|<system>",
       """
        There are two types of byte ordering for integer number depending on the CPU.
        For creating a lexical analyzer engine on the same CPU type as quex runs
        then this option is not required, since quex finds this out by its own.
        If you create an engine for a different platform, you must know its byte ordering
        scheme, i.e. little endian or big endian, and specify it after \\v{--endian}. 
        """,
        """
        According to the setting of this option one of the three macros is defined 
        in the header files:
        """,
        List(
        "__QUEX_OPTION_SYSTEM_ENDIAN",
        "__QUEX_OPTION_LITTLE_ENDIAN",
        "__QUEX_OPTION_BIG_ENDIAN",
        ),
        """
        Those macros are of primary use for character code converters. The
        converters need to know what the analyser engines number representation
        is. However, the user might want to use them for his own special
        purposes (using \\v{#ifdef __QUEX_OPTION_BIG_ENDIAN ... #endif}).
        """),
"""
The implementation of customized converters is supported by the following options.
""",
Option("converter_ucs_coding_name", "name", 
     """
     Determines what string is passed to the converter so that it converters
     a codec into Unicode. In general, this is not necessary. But, if a 
     unknown user defined type is specified via '--buffer-element-type' then
     this option must be specified.

     By default it is defined based on the buffer element type.
     """),
"""
Template and Path Compression ore methods to combine multiple states into one
'mega state'. The mega state combines in itself the common actions of the states
that it represents. The result is a massive reduction in code size.
The compression can be controlled with the following command line options:
""",
Option("compression_template_f", None, 
     """
     If this option is set, then template compression is activated.
     """),
Option("compression_template_uniform_f", None, 
     """
     This flag enables template compression. In contrast to the previous flag it 
     compresses such states into a template state which are uniform. Uniform means,
     that the states do not differ with respect to the actions performed at their
     entry. In some cases this might result in smaller code size and faster execution 
     speed.
     """),
Option("compression_template_min_gain", "number", 
     """
     The number following this option specifies the template compression coefficient.
     It indicates the relative cost of routing to a target state compared to a simple
     'goto' statement. The optimal value, with respect to code size and speed, may 
     vary from processor platform to processor platform, and from compiler to compiler.
     """), 
Option("compression_path_f", None, 
     """
     This flag activates path compression. By default, it compresses any sequence
     of states that can be lined up as a 'path'.
     """),
Option("compression_path_uniform_f", None, 
     """
     Same as uniform template compression, only for path compression. 
     """),
Option("path_limit_code", "number",
     """
     Path compression requires a 'pathwalker' to determine quickly the end of 
     a path. For this, each path internally ends with a signal character, the
     'path termination code'. It must be different from the buffer limit code
     in order to avoid ambiguities. 
       
     Modification of the 'path termination code' makes only sense if the input
     stream to be analyzed contains the default value.
     """),
"""
The following options control the output of comment which is added to the generated code:
""",
Option("comment_state_machine_f", None, 
     """
     With this option set a comment is generated that shows all state transitions
     of the analyzer in a comment at the begin of the analyzer function. The format
     follows the scheme presented in the following example
     """,
     Block("""
            /* BEGIN: STATE MACHINE
             ...
             * 02353(A, S) <- (117, 398, A, S)
             *       <no epsilon>
             * 02369(A, S) <- (394, 1354, A, S), (384, 1329)
             *       == '=' ==> 02400
             *       <no epsilon>
             ...
             * END: STATE MACHINE
             */
     """, "cpp"),
     """
     It means that state 2369 is an acceptance state (flag 'A') and it should store
     the input position ('S'), if no backtrack elimination is applied. It originates
     from pattern '394' which is also an acceptance state and '384'. It transits to
     state 2400 on the incidence of a '=' character.
     """),
Option("comment_transitions_f", None, 
     """
     Adds to each transition in a transition map information about the characters 
     which trigger the transition, e.g. in a transition segment implemented in a 
     C-switch case construct
     """,
     Block("""
           ...
           case 0x67: 
           case 0x68: goto _2292;/* ['g', 'h'] */
           case 0x69: goto _2295;/* 'i' */
           case 0x6A: 
           case 0x6B: goto _2292;/* ['j', 'k'] */
           case 0x6C: goto _2302;/* 'l' */
           case 0x6D:
           ...
     """),
     """
     The output of the characters happens in UTF8 format.
     """),
Option("comment_mode_patterns_f", None, 
     """
     If this option is set a comment is printed that shows what pattern is present 
     in a mode and from what mode it is inherited. The comment follows the following
     scheme:
     """,
     Block("""
           /* BEGIN: MODE PATTERNS 
            ...
            * MODE: PROGRAM
            * 
            *     PATTERN-ACTION PAIRS:
            *       (117) ALL:     [ \r\n\t]
            *       (119) CALC_OP: "+"|"-"|"*"|"/"
            *       (121) PROGRAM: "//"
            ...
            * END: MODE PATTERNS
            */
     """, "cpp"),
     """
     This means, that there is a mode \\v{PROGRAM}. The first three pattern are related
     to the terminal states '117', '119', and '121'. The white space pattern of 117 was
     inherited from mode `ALL`. The math operator pattern was inherited from mode
     \\v{CALC_OP} and the comment start pattern "//" was implemented in \\v{PROGRAM} 
     itself.
     """),
"""
The comment output is framed by \\v{BEGIN:} and \\v{END:} markers. These markers facilitate the extraction
of the comment information for further processing. For example, the Unix command 'awk' can be used to
extract what appears in between \\v{BEGIN:} and \\v{END:} the following way:
""",
Block("""
   awk 'BEGIN {w=0} /BEGIN:/ {w=1;} // {if(w) print;} /END:/ {w=0;}' MyLexer.c
""", "bash"),
"""When using multiple lexical analyzers it can be helpful to get precise 
information about all related name spaces. Such short reports on the standard
output are triggered by the following option.
""",
Option("show_name_spaces_f", None, 
     """
     If specified short information about the name space of the analyzer and the
     token are printed on the console. 
     """),
SectionHeader("Errors and Warnings"),
"""
When the analyzer behaves unexpectedly, it may make sense to ponder over low-priority
patterns outrunning high-priority patterns. The following flag supports these considerations.
""",
Option("warning_on_outrun_f", None, 
     """
     When specified, each mode is investigated whether there are patterns of lower
     priority that potentially outrun patterns of higher priority. This may happen
     due to longer length of the matching lower priority pattern. 
     """),
"""
Some warnings, notes, or error messages might not be interesting or even
be disturbing. For such cases, quex provides an interface to 
prevent messages on the standard output.
""",
Option("suppressed_notification_list", "[integer]+", 
    """
    By this option, errors, warnings, and notes may be suppressed. The 
    option is followed by a list of integers--each integer represents
    a suppressed message.
    """),
"""
The following enumerates suppress codes together with their associated messages.
""",
Item("0", 
     """
     Warning if quex cannot find an included file while        
     diving into a 'foreign token id file'.                    
     """),
Item("1",
     """
    A token class file (\\v{--token-class-file}) may           
    contain a section with extra command line arguments       
    which are reported in a note.                             
     """),
Item("2",
     """
    Error check on dominated patterns,                        
    i.e. patterns that may never match due to higher          
    precedence patterns which cover a super set of lexemes.    
     """),
Item("3",
     """
    Error check on special patterns (skipper, indentation,    
    etc.) whether they are the same.                          
     """),
Item("4",
     """
    Warning or error on 'outrun' of special patterns due to   
    lexeme length. Attention: To allow this opens the door to 
    very confusing situations. For example, a comment skipper 
    on "/*" may not trigger because a lower precedence pattern
    matches on "/**" which is longer and therefore wins.      
     """),
Item("5",
     """
    Detect whether higher precedence patterns match on a      
    subset of lexemes that a special pattern (skipper,        
    indentation, etc.) matches. Attention: Allowing such      
    behavior may cause confusing situations. If this is       
    allowed a pattern may win against a skipper, for example. 
    It is the expectation, though, that a skipper shall skip  
    --which it cannot if such scenarios are allowed.          
     """),
Item("6",
     """
    Warning if no token queue is used while some              
    functionality might not work properly.                    
     """),
Item("7",
     """
    Warning if token ids are used without being explicitly    
    defined.                                                  
     """),
Item("8",
     """
    Warning if a token id is mentioned as a 'repeated token'  
    but has not been defined.                                 
     """),
Item("9",
     """
    Warning if a prefix-less token name starts with the       
    token prefix.                                             
     """),
Item("10",
     """
    Warning if there is no 'on_bad_lexatom' handler while a   
    codec different from Unicode is used.                     
     """),
Item("11",
     """
    Warning a counter setup is defined without specifying a   
    newline behavior.                                         
     """),
Item("12",
     """
    Warning if a counter setup is defined without an          
    \\v{\\else} section.                                        
     """),
Item("13",
     """
    Warning if a default newline is used upon missing newline definition
    in a counter definition section.
     """),
Item("14",
     """
    Same as 13, except with hexadecimal '0D'.                 
     """),
Item("15",
     """
    Warning if a token type has no 'take_text' member         
    function. It means, that the token type has no interface  
    to automatically accept a lexeme or an accumulated       
    string.                                                   
     """),
Item("16",
     """
    Warning if there is a string accumulator while            
    '--suppress 15' has been used.                            
     """),
SectionHeader("Queries"),
"""
The former command line options influenced the procedure of code generation.
The options to solely query quex are listed in this section. First of all the two
traditional options for help and version information are
""",
Option("query_help_f", None,
       """Reports some help about the usage of quex on the console.
       """),
Option("query_version_f", None,
       """Prints information on the version of quex.
       """),
"""
The following options allow to query on character sets and the result
of regular expressions.
""",
Option("query_codec", "name",
       """
   Displays the characters that are covered by the given codec's name. If the
   name is omitted, a list of all supported codecs is printed. 
       """),
Option("query_codec_list", None,
       """
   Displays all character encodings that can be implemented directly in the
   analyzer state machine without using a converter. Additionally, the encodings 
   'utf8' and 'utf16' are always supported.
       """),
Option("query_codec_file", "file name", 
       """
   Displays the characters that are covered by the codec provided in the
   given file. This makes sense in conjunction with \\v{--codec-file} where 
   customized codecs can be defined.
       """),
Option("query_codec_language", "language", 
       """
   Displays the codecs that quex supports for the given human language. If the
   language argument is omitted, all available languages are listed.
       """),
Option("query_property", "property", 
       """
   Displays information about the specified Unicode property.
   The \\v{property} can also be a property alias. If \\v{property}
   is not specified, then brief information about all available Unicode
   properties is displayed.
       """),
Option("query_set_by_property", "setting", 
       """
   Displays the set of characters for the specified Unicode property setting. 
   For query on binary properties only the name is required. All other
   properties require a term of the form \\v{name=value}.
       """),
Option("query_property_match", "wildcard-expression", 
       """
       Displays property settings that match the given wildcard expression. This
       helps to find correct identifiers in the large list of Unicode settings.
       For example, the wildcard-expression \\v{Name=*LATIN*} gives all settings
       of property \\v{Name} that contain the string \\v{LATIN}.
       """),
Option("query_set_by_expression", "regular expression", 
       """
       Displays the resulting character set for the given regular expression.
   Larger character set expressions that are specified in \\v{[: ... :]} brackets.
       """),
Option("query_numeric_f", None, 
       """
   If this option is specified the numeric character codes are displayed rather
   then the characters.
       """),
Option("query_interval_f", None, 
       """
       If this option is set, adjacent characters are displayed as intervals, i.e.
       in terms of begin and end of domains of adjacent character codes.
       This provides a concise display.
       """),
Option("query_unicode_names_f", None, 
       """
       If this option is given, resulting characters are displayed by their
       (lengthy) Unicode name.
       """),
]

def doc(Formatter, TemplateFile, OutFile):
    global content
    content_txt = Formatter.do(content)
    page = open(TemplateFile, "rb").read()
    page = page.replace("$$OPTIONS$$", content_txt)
    page = page.replace("$$VERSION$$", "%s" % QUEX_VERSION)
    open(OutFile, "wb").write(page)
    print "Written: '%s'" % OutFile

doc(VisitorSphinx(), 
    "%s/doc/source/appendix/command-line/intro.template" % os.environ["QUEX_PATH"], 
    sphinx_file)

doc(VisitorManPage(), 
    "%s/doc/manpage/quex.template" % os.environ["QUEX_PATH"], 
    man_file) 


