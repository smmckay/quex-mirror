#! /usr/bin/env python
import os
import sys
sys.path.append(os.environ["QUEX_PATH"])
import quex.input.command_line.core          as command_line
import quex.core                             as core
import quex.output.analyzer.lexeme_converter as lexeme_converter
import quex.output.analyzer.adapt            as adapt
import quex.output.languages.core            as languages
from   quex.engine.state_machine.transformation.table import EncodingTrafoByTable
import quex.blackboard

import shutil

quex.blackboard.setup.analyzer_class_name = "TestAnalyzer"

if "--hwut-info" in sys.argv:
    print "Converter: Determine UTF-8 Range Map for Codec"
    print "CHOICES:   cp037, cp737, cp866, cp1256;"
    sys.exit()

def test(CodecName):
    stdout = sys.stdout
    sys.stdout = open(os.devnull, "w")
    command_line.do(["--co", "--encoding", CodecName, "--csn", "lexeme", 
                     "--language", "C++", "--bet", "uint8_t", "--odir", "Conv"])
    core.do()
    sys.stdout = stdout

    define_str = " ".join(["-DQUEX_TYPE_LEXATOM='unsigned char'",
                           "-DQUEX_OPTION_DISABLE_STD_STRING_USAGE_EXT",
                           "-DQUEX_INLINE=inline", 
                           "-D__QUEX_CODEC=%s " % CodecName,
                           "-DQUEX_OPTION_LITTLE_ENDIAN_EXT"])

    compile_str = "g++ -ggdb -I./ %s converter-tester.cpp -o converter-tester" % define_str
    print "##", compile_str
    os.system(compile_str)

    os.system("./converter-tester")
    if True:
        os.remove("./converter-tester")
        shutil.rmtree("./Conv")
    else:
        print "#TODO delete temporary files"

quex.blackboard.setup.language_db = languages.db["C"]()

test(sys.argv[1])

