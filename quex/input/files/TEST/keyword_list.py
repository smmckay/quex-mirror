#! /usr/bin/env python
import sys
import os

sys.path.insert(0, os.environ["QUEX_PATH"])
import quex.input.files.TEST.helper    as helper


if "--hwut-info" in sys.argv:
    print "Pattern-Action Pairs: keyword_list;"
    sys.exit()

def test(Txt):
    helper.test("keyword_list", Txt)

test("{ a; }")
test("(u)  { x; }")
test("(u)  { Z; }")
test("(l)  { x; }")
test("(l)  { Z; }")
test("(Nl) { Z; }")
test("(Nu) { x; }")
test("(i)  { x; }")
test("(i)  { Z; }")
test(" PREFIX_{ a; }")
test("(u)PREFIX_ { x; }")
