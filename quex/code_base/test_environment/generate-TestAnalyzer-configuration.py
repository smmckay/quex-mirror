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


def code(Language, Suffix):
    Setup.language_db = db[Language]

    core.do()

    if False:
        if Language == "C++":
            clean("TestAnalyzer", Suffix)
            clean("TestAnalyzer-configuration", Suffix)
            clean("TestAnalyzer-token_ids", Suffix)
            clean("TestAnalyzer-token", Suffix)
        else:
            clean("TestAnalyzer", Suffix)
            clean("TestAnalyzer-configuration", Suffix)
            clean("TestAnalyzer-token_ids", Suffix)
            clean("TestAnalyzer-token", Suffix)

def clean(FileName, Suffix):
    result = []
    fh = open(FileName)
    for line in fh.readlines():
        line = line.replace("TestAnalyzer-configuration",
                            "TestAnalyzer%s-configuration" % Suffix)
        line = line.replace("TestAnalyzer-token_ids",
                            "TestAnalyzer%s-token_ids" % Suffix)
        line = line.replace("TestAnalyzer-token",
                            "TestAnalyzer%s-token" % Suffix)
        result.append(line)
    fh.close()
    fh = open(FileName, "wb")
    fh.write("".join(result))
    fh.close()

if sys.argv[1] == "C++":
    command_line.do(["-i", "nothing.qx", "-o", "TestAnalyzer", "--token-policy", 
                     "single", "--no-include-stack", "--language", "C++"])
    code("C++", "Cpp")
    os.remove("TestAnalyzer.cpp")
elif sys.argv[1] == "C":
    command_line.do(["-i", "nothing.qx", "-o", "TestAnalyzer", "--token-policy", 
                     "single", "--no-include-stack", "--language", "C"])
    code("C", "C")
    os.remove("TestAnalyzer.c")

else:
    print "pass 'C' or C++' as first command line argument"
