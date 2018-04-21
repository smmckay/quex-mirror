#! /usr/bin/env python
import os
import sys
sys.path.append(os.environ["QUEX_PATH"])
import quex.output.analyzer.lexeme_converter as lexeme_converter
import quex.output.analyzer.adapt            as adapt
import quex.output.languages.core as languages
from   quex.engine.state_machine.transformation.table import EncodingTrafoByTable
import quex.blackboard

quex.blackboard.setup.analyzer_class_name = "TestAnalyzer"

if "--hwut-info" in sys.argv:
    print "Converter: Determine UTF-8 Range Map for Codec"
    print "CHOICES:   cp037, cp737, cp866, cp1256;"
    sys.exit()

def test(CodecName):
    trafo_info          = EncodingTrafoByTable(CodecName)
    code_str, code0_str = lexeme_converter._do(trafo_info)
    fh = open("converter-tester.h", "w")
    fh.write(adapt.do(code_str + "\n" + code0_str, "ut"))
    fh.close()
    define_str = "-DQUEX_TYPE_LEXATOM='unsigned char' " + \
                 "-DQUEX_INLINE=inline " + \
                 ("-D__QUEX_CODEC=%s " % CodecName) + \
                 "-D__QUEX_OPTION_LITTLE_ENDIAN " 

    compile_str = "g++ -ggdb -I./ -I../../../../code_base/ %s converter-tester.cpp -o converter-tester" % define_str
    print "##", compile_str
    os.system(compile_str)

    os.system("./converter-tester")
    if True:
        os.remove("./converter-tester.h")
        os.remove("./converter-tester")
    else:
        print "#TODO delete temporary files"

quex.blackboard.setup.language_db = languages.db["C"]()
def tiny(miniSelf):
    return "converter-tester.h", "" 

quex.blackboard.setup.language_db.lexeme_converter_file_names = tiny
quex.blackboard.setup.output_directory                        = "test_environment"

test(sys.argv[1])

