from   quex.engine.misc.file_operations import open_file_or_die, \
                                               write_safely_and_close 
from   quex.engine.misc.tools           import flatten_list_of_lists
import quex.output.analyzer.adapt       as     adapt
from   quex.blackboard                  import Lng, setup as Setup
from   quex.DEFINITIONS                 import QUEX_PATH

import os.path as path
import os

def do(OutputDir, DirList=None):
    file_set = __collect_files(DirList)
    __copy_files(OutputDir, file_set)

dir_db = {
    "": [
        "asserts",
        "lexeme_base",
        "lexeme_base.i",
        "definitions",
        "include-guard-undef",
        "declarations",
        "implementations.i",
        "implementations-inline.i",
    ],
    "token/": [
        "receiving",
        "receiving.i",
        "TokenQueue",
        "TokenQueue.i",
        "CDefault.qx",
        "CppDefault.qx" 
    ],
    "extra/post_categorizer/": [
        "PostCategorizer",
        "PostCategorizer.i",
    ],
    "extra/accumulator/": [
        "Accumulator",
        "Accumulator.i",
    ],
    "extra/strange_stream/": [
        "StrangeStream",
    ],
    "buffer/lexatoms/": [
        "LexatomLoader", 
        "LexatomLoader.i",
        "LexatomLoader_navigation.i",
        "LexatomLoader_Plain",
        "LexatomLoader_Plain.i",
        "LexatomLoader_Converter",
        "LexatomLoader_Converter.i",
        "LexatomLoader_Converter_RawBuffer.i",
        "converter/Converter",
        "converter/Converter.i",
        "converter/iconv/Converter_IConv",
        "converter/iconv/Converter_IConv.i",
        "converter/iconv/special_headers.h",
        "converter/icu/Converter_ICU",
        "converter/icu/Converter_ICU.i",
        "converter/icu/special_headers.h",
        "converter/recode/Converter_Recode",
        "converter/recode/Converter_Recode.i",
    ],
    "buffer/": [
        "asserts",
        "asserts.i",
        "Buffer",
        "Buffer_print",
        "Buffer_print.i",
        "Buffer.i",
        "BufferMemory.i",
        "Buffer_navigation.i",
        "Buffer_fill.i",
        "Buffer_move.i",
        "Buffer_load.i",
        "Buffer_nested.i",
        "Buffer_callbacks.i",
        "Buffer_invariance.i",
    ],
    "buffer/bytes/": [
        "ByteLoader",
        "ByteLoader.i",
        "ByteLoader_FILE",
        "ByteLoader_FILE.i",
        "ByteLoader_POSIX",
        "ByteLoader_POSIX.i",
        "ByteLoader_stream",
        "ByteLoader_stream.i",
        "ByteLoader_wstream",
        "ByteLoader_wstream.i",
        "ByteLoader_Memory",
        "ByteLoader_Memory.i",
        "ByteLoader_Probe",
        "ByteLoader_Probe.i",
    ],
    "analyzer/": [
        "C-adaptions.h",
        "Mode",
        "Mode.i",
        "asserts",
        "asserts.i",
        "configuration/derived",
        "configuration/undefine",
        "configuration/validation",
        "Counter",
        "Counter.i",
        "struct/include-stack",
        "struct/include-stack.i",
        "struct/constructor",
        "struct/constructor.i",
        "struct/reset",
        "struct/reset.i",
        "struct/include-stack",
        "struct/include-stack.i",
        "member/misc",
        "member/misc.i",
        "member/mode-handling",
        "member/mode-handling.i",
        "member/navigation",
        "member/navigation.i",
        "adaptors/Feeder",
        "adaptors/Feeder.i",
        "adaptors/Gavager",
        "adaptors/Gavager.i",
        "Statistics",
        "Statistics.i"
    ],
    "quex/": [
        "bom",            "bom.i",  
        "MemoryManager",  "MemoryManager.i"
    ],
    "quex/compatibility/": [
        "iconv-argument-types.h",
        "stdint.h",
        "stdbool-pseudo.h",
        "stdbool.h",
        "win/borland_stdint.h",
        "win/msc_stdint.h",
        "win/msc_stdint.h",
    ],
    # "lexeme_converter/": [ ], DEPRECATED ...
}

def dir_db_get_files(Dir):
    global dir_db

    if   not Dir: return []
    elif Dir[-1] != "/": Dir += "/"

    return [
        os.path.join(directory, path)
        for directory, file_list in dir_db.iteritems() if directory.startswith(Dir)
        for path in file_list
    ]

def __collect_files(DirList):
    if DirList is None: dir_list = dir_db.keys() 
    else:               dir_list = DirList

    result = set(flatten_list_of_lists(
        dir_db_get_files(d) for d in dir_list
    ))
    result.update(dir_db[""])
    return result

def __copy_files(OutputDir, FileSet):
    include_db = [
        ("declarations",      "$$INCLUDE_TOKEN_CLASS_DEFINITION$$",     Lng.INCLUDE(Setup.output_token_class_file)),
        ("implementations.i", "$$INCLUDE_TOKEN_CLASS_IMPLEMENTATION$$", Lng.INCLUDE(Setup.output_token_class_file_implementation)),
        ("implementations-inline.i", "$$INCLUDE_TOKEN_CLASS_IMPLEMENTATION$$", Lng.INCLUDE(Setup.output_token_class_file_implementation)),
        ("token/TokenQueue",  "$$INCLUDE_TOKEN_CLASS_DEFINITION$$",     Lng.INCLUDE(Setup.output_token_class_file)),
        ("token/TokenQueue",  "$$INCLUDE_LEXER_CLASS_DEFINITION$$",     Lng.INCLUDE(Setup.output_header_file)),
    ]
    for path, dummy, dummy in include_db:
        directory, basename = os.path.split(path)
        assert (not directory and basename in dir_db[""]) \
               or (basename in dir_db["%s/" % directory])

    file_pair_list,   \
    out_directory_set = __get_source_drain_list(OutputDir, FileSet)

    # Make directories
    # Sort according to length => create parent directories before child.
    for directory in sorted(out_directory_set, key=len):
        if os.access(directory, os.F_OK) == True: continue
        os.makedirs(directory) # create parents, if necessary

    # Copy
    for source_file, drain_file in file_pair_list:
        content = open_file_or_die(source_file, "rb").read()
        for path, origin, replacement in include_db:
            if not source_file.endswith(path): continue
            content = content.replace(origin, replacement)

        content = adapt.do(content, OutputDir, OriginalPath=source_file)
        write_safely_and_close(drain_file, content)

def __get_source_drain_list(OutputDir, FileSet):
    input_directory          = os.path.join(QUEX_PATH, Lng.CODE_BASE)
    output_directory         = os.path.join(OutputDir, "lib")

    file_pair_list = [ 
        (os.path.join(input_directory, source), 
         os.path.join(output_directory, source))
         for source in FileSet 
    ]
    out_directory_set = set(
        path.dirname(drain) for source, drain in file_pair_list
    )

    return file_pair_list, out_directory_set
