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
    StrangeStream_str = " -DQUEX_OPTION_STRANGE_ISTREAM_IMPLEMENTATION_EXT "
    Language = "Cpp"


def build(Opener, Closer):
    open_sequence  = map(ord, Opener)
    close_sequence = map(ord, Closer)
    code_str = create_nested_range_skipper_code(Language, "<by command line>", 
                                                open_sequence, 
                                                close_sequence, 
                                                QuexBufferSize=len(close_sequence)+3)
    executable_name, \
    source           = compile(Language, code_str, 
                               AssertsActionvation_str = "", 
                               StrangeStream_str       = StrangeStream_str)
    return executable_name, source

def my_run(executable, Name, TestStr):
    print
    print "--( %s )------------" % Name
    print
    sys.stdout.flush()

    # The TestStr needs one more 'closer' since 'nesting counter = 1'
    # upon entry. The main loop detects the first 'opener'.
    run(executable, TestStr, FilterF=True)

    sys.stdout.flush()

def clean(executable, source):
    if REMOVE_FILES:
        try: os.remove(executable)
        except: pass
        try: os.remove(source)
        except: pass

def wild_str_core(N):
    """Generate a random configuration of opener/closers.
    IDEA: At any position between the outest brackets a '()' may be inserted
          resulting in a well defines nested expression. Repeating this process
          results in large tree of valid nested expressions.
    """
    seed = 17 # seed of 'pseudo randomness'
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
    # The first opener is omitted, since the first opener is detected by 
    # main analyzer
    txt = txt[1:]
    txt = txt.replace("(", "OPENER").replace("OPENER", Opener)
    txt = txt.replace(")", "CLOSER").replace("CLOSER", Closer)
    return txt

# TODO: Compile once, run multiple times.
#       The tests are already setup for that, but it requires some 
#       slight adaptions.
if choice == "one":
    exe, source = build("(", ")")
    my_run(exe, "OPEN-CLOSE", "a)X")
    my_run(exe, "OPEN-OPEN-CLOSE-CLOSE", "a())X")
    my_run(exe, "OPEN-OPEN-CLOSE-OPEN-CLOSE-CLOSE", "a()())X")
    my_run(exe, "OPEN-OPEN-OPEN-CLOSE-OPEN-CLOSE-CLOSE-CLOSE", "a(()()))X")
    my_run(exe, "WILD", wild_str(10000, "(", ")"))
    clean(exe, source)

elif choice == "two":
    exe, source = build("(-", "-)")
    my_run(exe, "OPEN-CLOSE", "a-)X")
    my_run(exe, "OPEN-OPEN-CLOSE-CLOSE", "a(--)-)X")
    my_run(exe, "OPEN-OPEN-CLOSE-OPEN-CLOSE-CLOSE", "a(--)(--)-)X")
    my_run(exe, "OPEN-OPEN-OPEN-CLOSE-OPEN-CLOSE-CLOSE-CLOSE", "a(-(--)(--)-)-)X")
    my_run(exe, "WILD", wild_str(50000, "(-", "-)"))
    clean(exe, source)

elif choice == "three":
    exe, source = build("((-", "-))")
    my_run(exe, "OPEN-CLOSE", "a-))X")
    my_run(exe, "OPEN-OPEN-CLOSE-CLOSE", "a((--))-))X")
    my_run(exe, "OPEN-OPEN-CLOSE-OPEN-CLOSE-CLOSE", "a((--))((--))-))X")
    my_run(exe, "OPEN-OPEN-OPEN-CLOSE-OPEN-CLOSE-CLOSE-CLOSE", "a((-((--))((--))-))-))X")
    my_run(exe, "WILD", wild_str(50000, "((-", "-))"))
    clean(exe, source)

elif choice == "same-head":
    exe, source = build("same(", "same)")
    my_run(exe, "OPEN-CLOSE", "same)X")
    my_run(exe, "OPEN-OPEN-CLOSE-CLOSE", "asame(same)same)X")
    my_run(exe, "OPEN-OPEN-CLOSE-OPEN-CLOSE-CLOSE", "asame(same)same(same)same)X")
    my_run(exe, "OPEN-OPEN-OPEN-CLOSE-OPEN-CLOSE-CLOSE-CLOSE", "asame(same(same)same(same)same)same)X")
    my_run(exe, "WILD", wild_str(50000, "same(", "same)"))
    clean(exe, source)

