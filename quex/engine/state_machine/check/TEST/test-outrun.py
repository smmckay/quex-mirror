#! /usr/bin/env python
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])

import quex.input.regular_expression.engine   as regex
import quex.engine.state_machine.check.outrun as outrun_check

if "--hwut-info" in sys.argv:
    print "Outrun - Matching Same and More"
    # print "CHOICES: True, False, Pre-Post-Contexts-True, Pre-Post-Contexts-False;"
    sys.exit(0)
    
def test(A, B):
    def __core(Pattern0, Pattern1):
        print ("Pattern A = " + Pattern0).replace("\n", "\\n").replace("\t", "\\t")
        print ("Pattern B = " + Pattern1).replace("\n", "\\n").replace("\t", "\\t")
        sm0 = regex.do(Pattern0, {}).extract_sm()
        sm1 = regex.do(Pattern1, {}).extract_sm()
        print "claim     = ", outrun_check.do(sm0, sm1)
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
