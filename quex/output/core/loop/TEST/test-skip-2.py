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
    code = create_character_set_skipper_code(Language, "", TriggerSet, QuexBufferSize=BufferSize+2,
                                             CounterPrintF="short")
    exe_name, tmp_file_name = compile(Language, code)
    return exe_name, tmp_file_name

def run(Executable, TestStr):
    fh = open("test.txt", "wb")
    fh.write(TestStr)
    fh.close()
    run_this("./%s test.txt" % Executable)
    if REMOVE_FILES:
        os.remove("test.txt")

if "FIRST" in sys.argv:
    exe, tmp_file = build(trigger_set, buffer_size)
else:
    exe = "tmp.c.exe"

run(exe, "_X")
run(exe, "a_X")
run(exe, "ab_X")
run(exe, "abc_X")
run(exe, "abcd_X")
run(exe, "abcde_X")
run(exe, "abcdef_X")
run(exe, "abcdefg_X")
run(exe, "abcdefgh_X")
run(exe, "abcdefghi_X")
run(exe, "abcdefghij_X")
run(exe, "abcdefghijk_X")
run(exe, "abcdefghijkl_X")
run(exe, "abcdefghijklm_X")
run(exe, "abcdefghijklmn_X")
run(exe, "abcdefghijklmno_X")
run(exe, "abcdefghijklmnop_X")
run(exe, "abcdefghijklmnopq_X")
run(exe, "abcdefghijklmnopqr_X")
run(exe, "abcdefghijklmnopqrs_X")
run(exe, "abcdefghijklmnopqrst_X")
run(exe, "abcdefghijklmnopqrstu_X")
run(exe, "abcdefghijklmnopqrstuv_X")
run(exe, "abcdefghijklmnopqrstuvw_X")
run(exe, "abcdefghijklmnopqrstuvwx_X")
run(exe, "abcdefghijklmnopqrstuvwxy_X")
run(exe, "abcdefghijklmnopqrstuvwxyz_X")

if "LAST" in sys.argv:
    try: os.remove(exe)
    except: pass
    try: os.remove(tmp_file)
    except: pass

