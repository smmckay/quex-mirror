#! /usr/bin/env python
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])

import quex.input.regular_expression.engine           as regex
import quex.engine.state_machine.cut.head_and_tails   as head_and_tails
import quex.engine.state_machine.algorithm.beautifier as beautifier

if "--hwut-info" in sys.argv:
    print "Stem and Branches;"
    print "CHOICES: repetition, optional;"
    sys.exit(0)

def clean(SM):
    result = beautifier.do(SM)
    result.clean_up()
    return repr(result)
    
def test(Original):
    print "---------------------------------------------------------"
    print ("Original = " + Original).replace("\n", "\\n").replace("\t", "\\t")
    orig   = regex.do(Original, {}, AllowNothingIsNecessaryF=True).sm
    print
    print "Head"
    print "    " + clean(head_and_tails.head(orig)).replace("\n", "\n    ")
    print 
    tails = head_and_tails.tails(orig)
    if not tails:
        print "<no tails>"
    else:
        for i, tail in enumerate(tails):
            print "Tail[%i]" % i
            print "    " + clean(tail).replace("\n", "\n    ")

if "repetition" in sys.argv:
    test("x*")
    test("x+")
    test("(ax*)(c*)")
    test("(ax*|bx*)")
    test("(ax*|by*)")
    test("(ax*|by*)c")
    test("(ax*|by*)(c*)")

if "optional" in sys.argv:
    test("x?")
    test("xx?")
    test("(ax?)(c?)")
    test("(ax?|bx?)")
    test("(ax?|by?)")
    test("(ax?|by?)c")
    test("(ax?|by?)(c?)")

