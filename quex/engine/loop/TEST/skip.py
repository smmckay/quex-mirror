#! /usr/bin/env python
import sys
import os
sys.path.insert(0, os.getcwd())
from helper import *
from quex.engine.misc.interval_handling import NumberSet, Interval
from quex.output.core.TEST.generator_test   import __Setup_init_language_database, REMOVE_FILES

if "--hwut-info" in sys.argv:
    print "Skip-Characters: Varrying Buffer Size"
    print "CHOICES: 3, 4, 5, 6, 7, 8;"
    print "SAME;"
    sys.exit(0)

if len(sys.argv) < 2: 
    print "Argument not acceptable, use --hwut-info"
    sys.exit(0)

buffer_size = int(sys.argv[1])

if buffer_size not in [3, 4, 5, 6, 7, 8]:
    print "Argument not acceptable, use --hwut-info"
    sys.exit(0)

trigger_set = NumberSet([Interval(ord('a'), ord('z') + 1), 
                         Interval(ord('A'), ord('Z') + 1)])

Language = "Cpp"
__Setup_init_language_database(Language)

trigger_set = NumberSet([Interval(ord('a'), ord('z') + 1), 
                         Interval(ord('A'), ord('Z') + 1)])

def build(TriggerSet, BufferSize):
    Language = "ANSI-C"
    code = create_character_set_skipper_code(Language, "", TriggerSet, 
                                             QuexBufferSize=BufferSize+2,
                                             CounterPrintF="short")
    exe_name, tmp_file_name = compile(Language, code)
    return exe_name, tmp_file_name

if "FIRST" in sys.argv or len(sys.argv) == 2:
    exe, tmp_file = build(trigger_set, buffer_size)
else:
    exe = "tmp.c.exe"

run(exe, "_X", FilterF=True, NextLetter="_")
run(exe, "a_X", FilterF=True, NextLetter="_")
run(exe, "ab_X", FilterF=True, NextLetter="_")
run(exe, "abc_X", FilterF=True, NextLetter="_")
run(exe, "abcd_X", FilterF=True, NextLetter="_")
run(exe, "abcde_X", FilterF=True, NextLetter="_")
run(exe, "abcdef_X", FilterF=True, NextLetter="_")
run(exe, "abcdefg_X", FilterF=True, NextLetter="_")
run(exe, "abcdefgh_X", FilterF=True, NextLetter="_")
run(exe, "abcdefghi_X", FilterF=True, NextLetter="_")
run(exe, "abcdefghij_X", FilterF=True, NextLetter="_")
run(exe, "abcdefghijk_X", FilterF=True, NextLetter="_")
run(exe, "abcdefghijkl_X", FilterF=True, NextLetter="_")
run(exe, "abcdefghijklm_X", FilterF=True, NextLetter="_")
run(exe, "abcdefghijklmn_X", FilterF=True, NextLetter="_")
run(exe, "abcdefghijklmno_X", FilterF=True, NextLetter="_")
run(exe, "abcdefghijklmnop_X", FilterF=True, NextLetter="_")
run(exe, "abcdefghijklmnopq_X", FilterF=True, NextLetter="_")
run(exe, "abcdefghijklmnopqr_X", FilterF=True, NextLetter="_")
run(exe, "abcdefghijklmnopqrs_X", FilterF=True, NextLetter="_")
run(exe, "abcdefghijklmnopqrst_X", FilterF=True, NextLetter="_")
run(exe, "abcdefghijklmnopqrstu_X", FilterF=True, NextLetter="_")
run(exe, "abcdefghijklmnopqrstuv_X", FilterF=True, NextLetter="_")
run(exe, "abcdefghijklmnopqrstuvw_X", FilterF=True, NextLetter="_")
run(exe, "abcdefghijklmnopqrstuvwx_X", FilterF=True, NextLetter="_")
run(exe, "abcdefghijklmnopqrstuvwxy_X", FilterF=True, NextLetter="_")
run(exe, "abcdefghijklmnopqrstuvwxyz_X", FilterF=True, NextLetter="_")

if "LAST" in sys.argv:
    try: os.remove(exe)
    except: pass
    try: os.remove(tmp_file)
    except: pass

