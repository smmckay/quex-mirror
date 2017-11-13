#! /usr/bin/env python
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])

import quex.input.regular_expression.engine           as regex
import quex.engine.state_machine.cut.stem_and_branches   as stem_and_branches
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
    print "    " + clean(stem_and_branches.stem(orig)).replace("\n", "\n    ")
    print 
    tails = stem_and_branches.branches(orig)
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

