#! /usr/bin/env python
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])
from   quex.input.code.base                        import SourceRef_VOID
from   quex.engine.pattern                         import Pattern
from   quex.input.regular_expression.pattern       import Pattern_Prep
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
    print "Indentation Counting: Without Tabulators;"
    print "CHOICES: InAndOut, EmptyLines, NoDents, SuppressedNewline, CloseMultiple;"
    sys.exit(0)

if len(sys.argv) < 2: 
    print "Argument not acceptable, use --hwut-info"
    sys.exit(0)

def build(ISetup):
    Language = "ANSI-C"
    txt = create_indentation_handler_code(Language, "<by command line>", 
                                          ISetup, BufferSize=3)
    executable_name, \
    source           = compile(Language, txt, AssertsActionvation_str = "") 
    return executable_name, source

pattern_newline            = get_Pattern_Prep(DFA.from_character_set(NumberSet(ord('\n'))))
pattern_suppressed_newline = get_Pattern_Prep(DFA.from_sequence([ord(x) for x in "\\\n"]))

indent_setup = IndentationCount_Pre(SourceRef_VOID,  
                                WhiteSpaceCharacterSet   = NumberSet([Interval(ord(x)) for x in " :"]), 
                                BadSpaceCharacterSet     = None,
                                PatternNewline           = pattern_newline, 
                                PatternSuppressedNewline = pattern_suppressed_newline, 
                                PatternListComment       = [])

if "FIRST" in sys.argv or len(sys.argv) <= 2:
    exe, tmp_file = build(indent_setup)

exe = "tmp.c.exe"

if "InAndOut" in sys.argv:
    run(exe, 
        "0\n"
        " 1\n"
        " :2\n"
        " : 3\n"
        " : :4\n"
        " : 3\n"
        " :2\n"
        " 1\n"
        "0\n")

if "EmptyLines" in sys.argv:
    run(exe, 
        "0\n"
        "  \n"
        " :2\n"
        " :  \n"
        " : :4\n"
        " : :  \n"
        " : : :6\n"
        " : : :  \n"
        " : : : :8\n"
        " : : :  \n"
        " : : :6\n"
        " : :  \n"
        " : :4\n"
        " :  \n"
        " :2\n"
        "  \n"
        "0\n")

if "NoDents" in sys.argv:
    run(exe, 
        "0\n"
        "0\n"
        " :2\n"
        " :2\n"
        " : :4\n"
        " : :4\n"
        " :2\n"
        " :2\n"
        "0\n"
        "0\n")

if "CloseMultiple" in sys.argv:
    run(exe, 
        "\n"
        "0\n"
        " 1\n"
        "  2\n"
        "0\n"
        " 1\n"
        "  2\n"
        "   3\n"
        "0\n"
        " 1\n"
        "  2\n"
        "   3\n"
        "    4\n"
        "0\n")

if "SuppressedNewline" in sys.argv:
    run(exe, 
        "a\n"
        " : b\n"   
        "\\\n"
        " : c\n"   
        " \\\n"
        " : d\n"   
        " :\\\n"
        " : e\n"     
        " : \\\n"
        " : f\n"      
        " : :\\\n"
        " : g\n"   # 3 columns
        "h\n")

if "Comments" in sys.argv:
    run(exe, 
        "a\n"
        " : b\n"   
        "#\n"
        " : c\n"   
        " #\n"
        " : d\n"   
        " :#\n"
        " : e\n"     
        " : #\n"
        " : f\n"      
        " : :#\n"
        " : g\n"   # 3 columns
        " : : #\n"
        " : h\n"   # 3 columns
        "i\n")

if "LAST" in sys.argv:
    try:    os.remove(exe)
    except: pass
