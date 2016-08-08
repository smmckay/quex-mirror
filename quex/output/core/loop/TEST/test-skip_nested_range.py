#! /usr/bin/env python
import sys
import os
sys.path.insert(0, os.getcwd())
from helper import *

if "--hwut-info" in sys.argv:
    print "Skip-NestedRange: Delimiters of different sizes;"
    print "CHOICES: one, two, three, same-head;"
    sys.exit(0)

choice = sys.argv[1]

Language          = "ANSI-C"
StrangeStream_str = ""
if sys.argv[1].find("StrangeStream") != -1:
    StrangeStream_str = " -DQUEX_OPTION_STRANGE_ISTREAM_IMPLEMENTATION "
    Language = "Cpp"


def test(Name, TestStr, Opener="/*", Closer="*/"):
    print
    print "--( %s )------------" % Name
    print
    open_sequence  = map(ord, Opener)
    close_sequence = map(ord, Closer)
    code_str = create_nested_range_skipper_code(Language, TestStr, 
                                                open_sequence, 
                                                close_sequence, 
                                                QuexBufferSize=len(close_sequence)+2)
    compile_and_run(Language, code_str,
                    StrangeStream_str=StrangeStream_str)
    if "X" in TestStr: 
        print "column_number_at_end(expected): %i;\n" % (TestStr.find("X")+1)

def wild_str_core(N, Seed=17):
    """Generate a random configuration of opener/closers.
    IDEA: At any position between the outest brackets a '()' may be inserted
          resulting in a well defines nested expression. Repeating this process
          results in large tree of valid nested expressions.
    """
    seed = Seed # seed of 'pseudo randomness'
    pos  = 0
    txt  = "()"
    for i in range(N):
        # seed *= 513  % 65521 --> all 'odd'
        seed = (seed * 51)  % 65521
        pos  = seed % len(txt)

        txt = txt[:pos] + "()" + txt[pos:]
    return "(%s)X" % txt

def wild_str(N, Opener, Closer):
    # Avoid 'dangerous' cases where opener and closer patterns intersect.
    txt = wild_str_core(N)
    txt = txt.replace("(", "OPENER").replace("OPENER", Opener)
    txt = txt.replace(")", "CLOSER").replace("CLOSER", Closer)
    return txt

# TODO: Compile once, run multiple times.
#       The tests are already setup for that, but it requires some 
#       slight adaptions.
if choice == "one":
    test("CLOSE",                            
         "a)",         "(", ")")
    test("OPEN-CLOSE",                       
         "a()X",       "(", ")")
    test("OPEN-OPEN-CLOSE-CLOSE",            
         "a(())X",     "(", ")")
    test("OPEN-OPEN-CLOSE-OPEN-CLOSE-CLOSE", 
         "a(()())X",   "(", ")")
    test("OPEN-OPEN-OPEN-CLOSE-OPEN-CLOSE-CLOSE-CLOSE", 
         "a((()()))X", "(", ")")
    test("WILD", 
         wild_str(20000, "(", ")"), "(", ")")

elif choice == "two":
    test("CLOSE",                            
         "a-)",                "(-", "-)")
    test("OPEN-CLOSE",                       
         "a(--)X",             "(-", "-)")
    test("OPEN-OPEN-CLOSE-CLOSE",            
         "a(-(--)-)X",         "(-", "-)")
    test("OPEN-OPEN-CLOSE-OPEN-CLOSE-CLOSE", 
         "a(-(--)(--)-)X",     "(-", "-)")
    test("OPEN-OPEN-OPEN-CLOSE-OPEN-CLOSE-CLOSE-CLOSE", 
         "a(-(-(--)(--)-)-)X", "(-", "-)")
    test("WILD", 
         wild_str(50000, "(-", "-)"), "(-", "-)")


elif choice == "three":
    if False:
        test("CLOSE",                            
             "a-))",                        "((-", "-))")
        test("OPEN-CLOSE",                       
             "a((--))X",                    "((-", "-))")
        test("OPEN-OPEN-CLOSE-CLOSE",            
             "a((-((--))-))X",              "((-", "-))")
        test("OPEN-OPEN-CLOSE-OPEN-CLOSE-CLOSE", 
             "a((-((--))((--))-))X",        "((-", "-))")
        test("OPEN-OPEN-OPEN-CLOSE-OPEN-CLOSE-CLOSE-CLOSE", 
             "a((-((-((--))((--))-))-))X",  "((-", "-))")

    for seed in range(1, 1023, 3):
        txt = wild_str_core(10, Seed=seed)
        txt = txt.replace("(", "OPENER").replace("OPENER", "((-")
        txt = txt.replace(")", "CLOSER").replace("CLOSER", "-))")
        test("WILD", 
             txt, "((-", "-))")

elif choice == "same-head":
    test("CLOSE",                            
         "asame)",                                     "same(", "same)")
    test("OPEN-CLOSE",                       
         "asame(same)X",                               "same(", "same)")
    test("OPEN-OPEN-CLOSE-CLOSE",            
         "asame(same(same)same)X",                     "same(", "same)")
    test("OPEN-OPEN-CLOSE-OPEN-CLOSE-CLOSE", 
         "asame(same(same)same(same)same)X",           "same(", "same)")
    test("OPEN-OPEN-OPEN-CLOSE-OPEN-CLOSE-CLOSE-CLOSE", 
         "asame(same(same(same)same(same)same)same)X", "same(", "same)")
    test("WILD", 
         wild_str(20000, "same(", "same)"),            "same(", "same)")

