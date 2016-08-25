#! /usr/bin/env python
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])

import quex.input.regular_expression.engine as regex
import quex.engine.state_machine.check.tail as tail

if "--hwut-info" in sys.argv:
    print "Tail Checker"
    sys.exit(0)
    
def test(A, B):
    def __core(A, TailCandidate):
        print ("Pattern = " + A).replace("\n", "\\n").replace("\t", "\\t")
        print ("Tail    = " + TailCandidate).replace("\n", "\\n").replace("\t", "\\t")
        sm0 = regex.do(A, {}).sm
        sm1 = regex.do(TailCandidate, {}).sm
        only_common_f, common_f = tail.do(sm0, sm1)
        print "commonality: %s; exclusive: %s; " % (common_f, only_common_f)
    print "---------------------------"
    __core(A, B)
    print
    __core(B, A)

test("b", "ab")
test("a", "a")
test("a", "ab")
test("a", "a{5}")
test("albert", "a(de)?lbert")
test("(alb)|(er)", "albert")
test("(alb)+|(er)", "albert")
test("[a-z]{1,3}", "albert")
test("(alfons)|(adelheid)|(adolf)|(arthur)|(arnheim)|(augsburg)|(frieda)", "albert")
test("(alfons)|(adelheid)|(adolf)|(arthur)|(arnheim)|(augsburg)|(frieda)", "arthurius")
test("(a+lfons)|(a{2}delheid)|(a+dolf)|(a+r+t+h{1,3}ur)|(a+r+n+heim)|(a{5,}ugsburg)|(f+rieda)", "arthurius")
test("alb|(albert(i?))", "albert")
test("alb|albertikus", "albert")
test("key", "[a-z]+")
