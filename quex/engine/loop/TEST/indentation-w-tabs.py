#! /usr/bin/env python
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])
from   quex.input.regular_expression.pattern       import Pattern
from   quex.input.code.base                        import SourceRef_VOID
from   quex.engine.pattern                         import Pattern
from   quex.engine.state_machine.core              import DFA
from   quex.engine.misc.interval_handling          import NumberSet, Interval
from   quex.engine.counter                         import IndentationCount_Pre
import quex.engine.analyzer.door_id_address_label  as     dial
from   quex.engine.misc.interval_handling          import NumberSet, Interval
from   quex.output.core.variable_db                import variable_db
from   quex.output.core.TEST.generator_test        import __Setup_init_language_database

from   helper import *

from   StringIO import StringIO
from   copy import deepcopy

if "--hwut-info" in sys.argv:
    print "Indentation Counting: With Tabulators;"
    print "CHOICES: Front, Back, InComment, Potpourri;"
    sys.exit(0)

if len(sys.argv) < 2: 
    print "Argument not acceptable, use --hwut-info"
    sys.exit(0)

def build(ISetup):
    Language = "ANSI-C"
    txt = create_indentation_handler_code(Language, "<by command line>", 
                                          ISetup, BufferSize=4)
    executable_name, \
    source           = compile(Language, txt, AssertsActionvation_str = "") 
    return executable_name, source

pattern_newline            = get_Pattern_Prep(DFA.from_character_set(NumberSet(ord('\n'))))
pattern_suppressed_newline = get_Pattern_Prep(DFA.from_sequence([ord(x) for x in "\\\n"]))
pattern_comment_w_newline  = regex.do("#[^\\n]*\\n", {})
pattern_comment_wo_newline = regex.do("\\([^\\)]*\\)", {})
whitespace                 = NumberSet([Interval(ord(x)) for x in " :\t"]) 

indent_setup = IndentationCount_Pre(SourceRef_VOID,  
                                WhiteSpaceCharacterSet   = whitespace,
                                BadSpaceCharacterSet     = None,
                                PatternNewline           = pattern_newline, 
                                PatternSuppressedNewline = pattern_suppressed_newline, 
                                PatternListComment       = [pattern_comment_w_newline,
                                                            pattern_comment_wo_newline])

if "FIRST" in sys.argv or len(sys.argv) <= 2:
    exe, tmp_file = build(indent_setup)

exe = "tmp.c.exe"

if "Front" in sys.argv:
    run(exe, 
        "0\n"
        "\t1\n"
        "\t 2\n"
        "\t  3\n"
        "\t   4\n"
        "\t  3\n"
        "\t 2\n"
        "\t1\n"
        "0\n")

if "Back" in sys.argv:
    run(exe, 
        "0\n"
        "\t1\n"
        " \t2\n"
        "  \t3\n"
        "   \t4\n"
        "    \t5\n"
        "   \t4\n"
        "  \t3\n"
        " \t2\n"
        "\t1\n"
        "0\n")

if "InComment" in sys.argv:
    run(exe, 
        "0\n"
        "(\t)1\n"
        " (\t)2\n"
        "  (\t)3\n"
        "   (\t)4\n"
        "  (\t)3\n"
        " (\t)2\n"
        "(\t)1\n"
        "0\n")

if "Potpourri" in sys.argv:
    run(exe, 
        "0\n"
        "\t \t\n"
        "\t  2\n"
        "\t   \t\\\n"
        "\t    4\n"
        "\t     #\t\n"
        "\t      6\n"
        "\t(\t)\t(\t)\t(\t)\t(\t)\t(\t)\n"
        "\t        8\n"
        "\t(\t)\t(\t)\t(\t)\t(\t)\t(\t)\n"
        "\t      6\n"
        "\t     #\t\n"
        "\t    4\n"
        "\t   \t\\\n"
        "\t  2\n"
        "\t \t\n"
        "0\n")


if "LAST" in sys.argv:
    try:    os.remove(exe)
    except: pass
