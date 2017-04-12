import os
import sys

sys.path.insert(0, os.environ["QUEX_PATH"])

import quex.input.command_line.core     as command_line
import quex.input.files.core            as quex_file_parser
import quex.output.cpp.templates        as templates
import quex.output.cpp.analyzer_class   as analyzer_class
import quex.output.cpp.token_class_maker as token_class_maker
import quex.core                        as core

from   quex.blackboard                  import Lng, setup as Setup
import quex.blackboard                  as     blackboard
from   quex.input.code.base             import CodeFragment

blackboard.header = CodeFragment(
"""
extern bool UserConstructor_UnitTest_return_value;
extern bool UserReset_UnitTest_return_value;
extern bool UserMementoPack_UnitTest_return_value;
""")
blackboard.class_constructor_extension = CodeFragment("return UserConstructor_UnitTest_return_value;")
blackboard.reset_extension             = CodeFragment("return UserReset_UnitTest_return_value;")
blackboard.memento_pack_extension      = CodeFragment("return UserMementoPack_UnitTest_return_value;")

def code(Language):
    global tail_str
    command_line.do(["-i", "nothing.qx", "-o", "TestAnalyzer",
                     "--no-include-stack", "--language", Language])
    mode_db = quex_file_parser.do(Setup.input_mode_files)

    core._generate(mode_db)

    return mode_db

def add_engine_stuff(mode_db, FileName, TokenClassImplementationF=False):

    # Analyzer class implementation
    #
    analyzer_class_implementation  = "#ifndef QUEX_OPTION_UNIT_TEST_NO_IMPLEMENTATION_IN_HEADER\n"
    analyzer_class_implementation += analyzer_class.do_implementation(mode_db)
    analyzer_class_implementation += "\n"
    analyzer_class_implementation += templates.get_implementation_header(Setup)
    analyzer_class_implementation += "\n"
    analyzer_class_implementation += "bool UserConstructor_UnitTest_return_value = true;\n"
    analyzer_class_implementation += "bool UserReset_UnitTest_return_value       = true;\n"
    analyzer_class_implementation += "bool UserMementoPack_UnitTest_return_value = true;\n"
    analyzer_class_implementation += "#endif /* QUEX_OPTION_UNIT_TEST_NO_IMPLEMENTATION_IN_HEADER */\n"

    with open(FileName, "a") as fh:
        fh.write(analyzer_class_implementation)


    if not TokenClassImplementationF:
        return

    dummy,                     \
    dummy,                     \
    dummy,                     \
    token_class_implementation = token_class_maker.do()

    with open(FileName, "a") as fh:
        fh.write("#ifndef QUEX_OPTION_UNIT_TEST_NO_IMPLEMENTATION_IN_HEADER\n")
        fh.write(token_class_implementation)

        # fh.write("#else  /* QUEX_OPTION_UNIT_TEST_NO_IMPLEMENTATION_IN_HEADER */\n")
        # fh.write("bool UserConstructor_UnitTest_return_value = true;\n")
        # fh.write("bool UserReset_UnitTest_return_value       = true;\n")
        # fh.write("bool UserMementoPack_UnitTest_return_value = true;\n")
        fh.write("#endif /* QUEX_OPTION_UNIT_TEST_NO_IMPLEMENTATION_IN_HEADER */\n")

    Lng.straighten_open_line_pragmas(FileName)

def append_variable_definitions(FileName):
    fh = open(FileName)
    content = fh.read()
    fh.close()
    fh = open(FileName, "wb")
    fh.write(content)
    fh.write("\n")
    fh.write("bool UserConstructor_UnitTest_return_value = true;\n")
    fh.write("bool UserReset_UnitTest_return_value       = true;\n")
    fh.write("bool UserMementoPack_UnitTest_return_value = true;\n")
    fh.close()

if sys.argv[1] == "C++":
    mode_db = code("C++")
    add_engine_stuff(mode_db, "TestAnalyzer", TokenClassImplementationF=True)
    os.rename("TestAnalyzer.cpp", "TestAnalyzer-dummy.cpp")
    append_variable_definitions("TestAnalyzer-dummy.cpp")

elif sys.argv[1] == "C":
    mode_db = code("C")
    add_engine_stuff(mode_db, "TestAnalyzer.h",
                     TokenClassImplementationF=True)
    os.rename("TestAnalyzer.c", "TestAnalyzer-dummy.c")
    append_variable_definitions("TestAnalyzer-dummy.c")

else:
    print "pass 'C' or C++' as first command line argument"
