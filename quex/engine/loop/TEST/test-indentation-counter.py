#! /usr/bin/env python
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])
from   quex.input.regular_expression.pattern       import Pattern
from   quex.input.code.base                        import SourceRef_VOID
from   quex.engine.pattern                         import Pattern
from   quex.engine.state_machine.core              import StateMachine
from   quex.engine.misc.interval_handling          import NumberSet, Interval
from   quex.engine.counter                         import IndentationCount
import quex.engine.analyzer.door_id_address_label  as     dial
from   quex.engine.misc.interval_handling          import NumberSet, Interval
from   quex.output.core.variable_db                import variable_db
from   quex.output.core.TEST.generator_test        import __Setup_init_language_database

from   helper import *

from   StringIO import StringIO
from   copy import deepcopy

if "--hwut-info" in sys.argv:
    print "Indentation Counting"
    print "CHOICES: WithoutTab, WithTab, WithTab-2, Comment, Bad;"
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

def get_Pattern(ValueList):
    sm = StateMachine.from_character_set(NumberSet([ Interval(ord(x)) for x in ValueList ]))
    return Pattern(sm.get_id(), sm, None, None, None, "", SourceRef_VOID)

if "WithoutTab" in sys.argv:
    pattern_newline = get_Pattern("\n")
    pattern_suppressed_newline = get_Pattern("\n")
    indent_setup = IndentationCount(SourceRef_VOID,  
                                    WhiteSpaceCharacterSet   = NumberSet([Interval(ord(x)) for x in " :"]), 
                                    BadSpaceCharacterSet     = None,
                                    PatternNewline           = pattern_newline, 
                                    PatternSuppressedNewline = pattern_suppressed_newline, 
                                    PatternComment           = None)

    exe, tmp_file = build(indent_setup)

    run(exe, 
        "\n"
        "a\n"
        " b\n"
        " :c\n"
        " : d\n"
        " : :e\n"
        " : : f\n"
        " : : :g\n"
        " : : : h\n"
        " : : : :i\n"
        " : : : h\n"
        " : : :g\n"
        " : : f\n"
        " : :e\n"
        " : d\n"
        " :c\n"
        " b\n"
        "a\n")

    run(exe, 
        "\n"
        "a\n"
        "  \n"
        " :c\n"
        " :  \n"
        " : :e\n"
        " : :  \n"
        " : : :g\n"
        " : : :  \n"
        " : : : :i\n"
        " : : :  \n"
        " : : :g\n"
        " : :  \n"
        " : :e\n"
        " :  \n"
        " :c\n"
        "  \n"
        "a\n")

    my_run(exe, 
        "\n"
        "\n"
        "a\n"
        "a\n"
        " :c\n"
        " :c\n"
        " : :e\n"
        " : :e\n"
        " : : :g\n"
        " : : :g\n"
        " : : : :i\n"
        " : : : :i\n"
        " : : :g\n"
        " : : :g\n"
        " : :e\n"
        " : :e\n"
        " :c\n"
        " :c\n"
        "a\n"
        "a\n"
        "\n"
        "\n")

    run(exe, 
        "\n"
        "a\n"
        " \\n"
        " :c\n"
        " : \\n"
        " : :e\n"
        " : : \\n"
        " : : :g\n"
        " : : : \\n"
        " : : : :i\n"
        " : : : \\n"
        " : : :g\n"
        " : : \\n"
        " : :e\n"
        " : \\n"
        " :c\n"
        " \\n"
        "a\n")


elif "Uniform-Reloaded" in sys.argv:
    indent_setup.specify("whitespace", get_Pattern(" :"), SourceRef_VOID)

    test("\n"
         "  a\n"
         "                                     \n"
         "       b\n"
         "         c\n"
         "       d\n"
         "       e\n"
         "       h\n"
         "  i\n"
         "  j\n"
         , indent_setup, BufferSize=10)

elif "NonUniform" in sys.argv:
    indent_setup.specify("whitespace", get_Pattern(" :\t"), SourceRef_VOID)

    test("\n"
         "    a\n"     # 4 spaces
         "\tb\n"       # 0 space  + 1 tab = 4
         " \tc\n"      # 1 spaces + 1 tab = 4
         "  \td\n"     # 2 spaces + 1 tab = 4
         "   \te\n"    # 3 spaces + 1 tab = 4
         "    \tf\n"   # 4 spaces + 1 tab = 8
         "        g\n" # 8 spaces         = 8
         , indent_setup)


elif "NonUniform-2" in sys.argv:
    indent_setup.specify("whitespace", get_Pattern(" :\t"), SourceRef_VOID)

    test("\n"
         "        a\n" # 8 spaces
         "\t \tb\n"    # tab + 1 + tab = 8
         "\t  \tc\n"   # tab + 2 + tab = 8
         "\t   \td\n"  # tab + 3 + tab = 8
         "\t    e\n"   # tab + 4       = 8
         , indent_setup)


elif "Comment" in sys.argv:
    indent_setup.specify("whitespace", get_Pattern(" :\t"), SourceRef_VOID)
    indent_setup.specify("comment",    get_Pattern("\"%%\"(\"\\\\\n\"|[^\\n])+"), SourceRef_VOID)

    test("\n"
         "        a\n" # 8 spaces
         "\t \tb\n"    # tab + 1 + tab = 8
         "\t  \tc\n"   # tab + 2 + tab = 8
         "\t   \td\n"  # tab + 3 + tab = 8
         "\t    e\n"   # tab + 4       = 8
         , indent_setup)
