import os
import sys

sys.path.insert(0, os.environ["QUEX_PATH"])

import quex.input.command_line.core     as command_line
import quex.input.files.core            as quex_file_parser
from   quex.engine.misc.file_operations import open_file_or_die
from   quex.output.core.dictionary      import db
import quex.output.cpp.configuration    as configuration
import quex.output.cpp.analyzer_class   as analyzer_class

from   quex.blackboard                  import Lng, setup as Setup

Setup.language_db = db[Setup.language]

command_line.do(["-i", "nothing.qx", "-o", "TestAnalyzer", "--token-policy", "single", "--no-include-stack"])

# Parse default token file
fh = open_file_or_die(os.environ["QUEX_PATH"] 
                      + Lng["$code_base"] 
                      + Lng["$token-default-file"])
mode_db = quex_file_parser.do(Setup.input_mode_files)
fh.close()

BeginOfLineSupportF = True
IndentationSupportF = False     

txt = configuration.do({})
result = []
for line in txt.splitlines():
    if line.find("__QUEX_SETTING_MAX_MODE_CLASS_N") != -1: 
        line = line.replace("(0)", "(64)")
    result.append("%s\n" % line)

open("TestAnalyzer-configuration", "w").write("".join(result))

result = [
    "namespace quex {\n"
    "class Token { public: int _id; int type_id() { return _id; } };\n"
    "}\n"
]
for line in analyzer_class.do(mode_db).splitlines():
    if line.find("include") != -1 and line.find("#") != -1: 
        if line.find("-token_id") != -1: continue
        if line.find("-token") != -1: continue
    if line.find("$$ADDITIONAL_HEADER_CONTENT$$") != -1: continue
    result.append("%s\n" % line)

result.extend([
    "namespace quex {\n"
    "bool TestAnalyzer::user_constructor() { return true; }\n",
    "void TestAnalyzer::user_destructor() {}\n",
    "bool TestAnalyzer::user_reset() { return true; }\n",
    "}"
])
open("TestAnalyzer", "w").write("".join(result))

