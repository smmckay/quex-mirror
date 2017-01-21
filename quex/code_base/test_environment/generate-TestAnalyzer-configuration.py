import os
import sys

sys.path.insert(0, os.environ["QUEX_PATH"])

import quex.input.command_line.core     as command_line
import quex.input.files.core            as quex_file_parser
from   quex.engine.misc.file_operations import open_file_or_die
from   quex.output.core.dictionary      import db
import quex.output.cpp.configuration    as configuration
import quex.output.cpp.analyzer_class   as analyzer_class
import quex.core                        as core

from   quex.blackboard                  import Lng, setup as Setup
import quex.blackboard as blackboard

def code(Language):
    global tail_str
    command_line.do(["-i", "nothing.qx", "-o", "TestAnalyzer", "--token-policy", 
                     "single", "--no-include-stack", "--language", Language])
    mode_db = quex_file_parser.do(Setup.input_mode_files)

    core._generate(mode_db)

    return mode_db

def add_engine_stuff(mode_db, FileName, TokenClassImplementationF=False):
    # Analyzer class implementation
    #
    analyzer_class_implementation = analyzer_class.do_implementation(mode_db)
    with open(FileName, "a") as fh:
        fh.write(analyzer_class_implementation)

    if not TokenClassImplementationF:
        return

    # Token class implementation (In C++ it is pasted into header)
    #
    dummy,                                 \
    map_token_id_to_string_implementation, \
    dummy,                                 \
    token_class_implementation             = core._prepare_token_class()

    with open(FileName, "a") as fh:
        fh.write("%s\n%s" % (token_class_implementation,
                             map_token_id_to_string_implementation))
    
    Lng.straighten_open_line_pragmas(FileName)

if sys.argv[1] == "C++":
    mode_db = code("C++")
    add_engine_stuff(mode_db, "TestAnalyzer")
    os.remove("TestAnalyzer.cpp")

elif sys.argv[1] == "C":
    mode_db = code("C")
    add_engine_stuff(mode_db, "TestAnalyzer.h",
                     TokenClassImplementationF=True)
    os.remove("TestAnalyzer.c")

else:
    print "pass 'C' or C++' as first command line argument"
