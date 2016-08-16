#! /usr/bin/env python
import sys
import os
sys.path.insert(0, os.getcwd())
from helper import *

if "--hwut-info" in sys.argv:
    print "Skip-Range: Varrying DelimiterLength (Buffer=length+3)"
    print "CHOICES: 1, 2, 3, 4;"
    sys.exit(0)

DL = sys.argv[1]
if   DL == "1": SEP = "."
elif DL == "2": SEP = ".-"
elif DL == "3": SEP = ".-="
elif DL == "4": SEP = ".-=>"
else:
    print "Delimiter length argument '%s' not acceptable, use --hwut-info" % DL
    sys.exit(0)

buffer_size = len(SEP) + 2

def build(Language, CloserStr, BufferSize):
    code = create_range_skipper_code(Language, "", CloserStr, BufferSize, CounterPrintF="short")
    exe, tmp_file_name = compile(Language, code)
    return exe, tmp_file_name

exe, tmp_file = build("ANSI-C", map(ord, SEP), buffer_size)

# List of strings that are almost the complete seperator, but miss something
SEP_with_missing_tail = [ SEP[:i] for i in range(len(SEP)) if i != 0 ]


for i in range(26):
    print "--( %i )---------------------------------------------------" % i
    head = "".join(chr(ord('a') + k) for k in range(i))
    run(exe, head + SEP + "X", FilterF=True)
    for NOT_SEP in SEP_with_missing_tail:
        run(exe, head + NOT_SEP + SEP + "X", FilterF=True)
    if len(SEP_with_missing_tail) > 1: 
        run(exe, head + "".join(SEP_with_missing_tail) + SEP + "X", FilterF=True)

try: os.remove(exe)
except: pass



