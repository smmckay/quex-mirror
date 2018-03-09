from quex.engine.misc.file_operations import open_file_or_die, \
                                             write_safely_and_close 
from quex.output.analyzer.core        import produce_include_statements
from quex.blackboard   import setup as Setup, \
                              Lng
from quex.DEFINITIONS  import QUEX_PATH

import os.path as path
import os

# Search for related files by:
dummy = """
find quex/code_base \
     -path "*.svn*"        -or -path "*TEST*" -or -name tags      \
     -or -name "TXT*"      -or -name "*.txt"  -or -name "*.sw?"   \
     -or -path "*DESIGN*"  -or -name "*.7z"   -or -name "*ignore" \
     -or -name "*DELETED*" -or -name .        -or -name "*_body"  \
     -or -name "[1-9]"     -or -name "circle" -or -name "*.o"     \
     -or -name "*.exe"     -prune  \
     -or -type f -print | sort
"""

base = """
asserts
lexeme
lexeme_base
lexeme.i
lexeme_base.i
definitions
include-guard-undef
bom
bom.i
MemoryManager
MemoryManager.i
single.i
multi.i
"""

base_compatibility = """
compatibility/iconv-argument-types.h
compatibility/stdint.h
compatibility/stdbool-pseudo.h
compatibility/stdbool.h
compatibility/win/borland_stdint.h
compatibility/win/msc_stdint.h
compatibility/win/msc_stdint.h
"""

base_buffer = """
buffer/asserts
buffer/asserts.i
buffer/Buffer
buffer/Buffer_print
buffer/Buffer_print.i
buffer/Buffer.i
buffer/BufferMemory.i
buffer/Buffer_navigation.i
buffer/Buffer_fill.i
buffer/Buffer_move.i
buffer/Buffer_load.i
buffer/Buffer_nested.i
buffer/Buffer_callbacks.i
buffer/Buffer_invariance.i
buffer/bytes/ByteLoader
buffer/bytes/ByteLoader.i
buffer/bytes/ByteLoader_FILE
buffer/bytes/ByteLoader_FILE.i
buffer/bytes/ByteLoader_POSIX
buffer/bytes/ByteLoader_POSIX.i
buffer/bytes/ByteLoader_stream
buffer/bytes/ByteLoader_stream.i
buffer/bytes/ByteLoader_wstream
buffer/bytes/ByteLoader_wstream.i
"""

base_analyzer = """
analyzer/C-adaptions.h
analyzer/Mode
analyzer/Mode.i
analyzer/asserts
analyzer/asserts.i
analyzer/configuration/derived
analyzer/configuration/undefine
analyzer/configuration/validation
analyzer/headers
analyzer/headers.i
analyzer/struct/constructor
analyzer/struct/constructor.i
analyzer/struct/reset
analyzer/struct/reset.i
analyzer/struct/include-stack
analyzer/struct/include-stack.i
analyzer/member/misc
analyzer/member/misc.i
analyzer/member/mode-handling
analyzer/member/mode-handling.i
analyzer/member/navigation
analyzer/member/navigation.i
analyzer/member/token-receiving
analyzer/member/token-receiving.i
"""

analyzer_accumulator = """
extra/accumulator/Accumulator
extra/accumulator/Accumulator.i
"""

analyzer_counter = """
analyzer/Counter
analyzer/Counter.i
"""

analyzer_post_categorizer = """
extra/post_categorizer/PostCategorizer
extra/post_categorizer/PostCategorizer.i
"""

analyzer_include_stack = """
analyzer/struct/include-stack
analyzer/struct/include-stack.i
"""

token_policy = "token/TokenPolicy"

token_queue = """
token/TokenQueue
token/TokenQueue.i
"""

token_default_C   = "token/CDefault.qx"
token_default_Cpp = "token/CppDefault.qx"

buffer_filler = """
buffer/lexatoms/LexatomLoader
buffer/lexatoms/LexatomLoader.i
buffer/lexatoms/LexatomLoader_navigation.i
buffer/lexatoms/LexatomLoader_Plain
buffer/lexatoms/LexatomLoader_Plain.i
buffer/lexatoms/LexatomLoader_Converter
buffer/lexatoms/LexatomLoader_Converter.i
buffer/lexatoms/LexatomLoader_Converter_RawBuffer.i
buffer/lexatoms/converter/Converter
buffer/lexatoms/converter/Converter.i
buffer/lexatoms/converter/iconv/Converter_IConv
buffer/lexatoms/converter/iconv/Converter_IConv.i
buffer/lexatoms/converter/iconv/special_headers.h
buffer/lexatoms/converter/icu/Converter_ICU
buffer/lexatoms/converter/icu/Converter_ICU.i
buffer/lexatoms/converter/icu/special_headers.h
"""

converter_helper = [
    "common.h",
    "identity",
    "identity.i",
    "generator/declarations.g",
    "generator/implementations.gi",
    "generator/string-converter.gi",
    "generator/character-converter-to-char-wchar_t.gi",
    "from-unicode-buffer",
    "from-unicode-buffer.i",
    "from-utf8",
    "from-utf8.i",
    "from-utf16",
    "from-utf16.i",
    "from-utf32",
    "from-utf32.i",
]

def do():
    # FSM base file list (required by any analyzer)
    txt =   base                   \
          + base_compatibility     \
          + base_buffer            \
          + base_analyzer          \
          + token_policy           \
          + token_queue

    txt += buffer_filler

    txt += " ".join("lexeme_converter/%s" % line for line in converter_helper)
    txt += "\n"

    if Setup.extern_token_class_file:
        if   Setup.language == "C":   txt += token_default_C
        elif Setup.language == "C++": txt += token_default_Cpp

    txt += analyzer_accumulator
    if Setup.count_column_number_f or Setup.count_line_number_f: txt += analyzer_counter 
    txt += analyzer_post_categorizer 
    if Setup.include_stack_support_f:                            txt += analyzer_include_stack

    __copy_files(txt)

def __copy_files(FileTxt):

    input_directory  = os.path.join(QUEX_PATH, Lng.CODE_BASE)
    output_directory = os.path.join(Setup.output_directory, "lib")

    file_list      = [ x.strip() for x in FileTxt.split() ]
    file_pair_list = [ 
        (os.path.join(input_directory, x), os.path.join(output_directory, x))
         for x in file_list 
    ]
    out_directory_set = set(
        path.dirname(drain) for source, drain in file_pair_list
    )

    # Sort directories according to length --> create parent directories before child
    for directory in sorted(out_directory_set, key=len):
        if os.access(directory, os.F_OK) == True: continue
        os.makedirs(directory) # create parents, if necessary

    for source_file, drain_file in file_pair_list:
        content = open_file_or_die(source_file, "rb").read()
        content = produce_include_statements(content)
        write_safely_and_close(drain_file, content)

