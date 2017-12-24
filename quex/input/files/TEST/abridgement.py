#! /usr/bin/env python
import sys
import os

sys.path.insert(0, os.environ["QUEX_PATH"])
import quex.input.files.TEST.helper    as helper

if "--hwut-info" in sys.argv:
    print "Pattern-Action Pairs: abridgement;"
    sys.exit()

def test(Txt):
    helper.test("abridgement", Txt)

test('{ "+" PLUS; }')
test('(N) { "+" PLUS; "-" MINUS; }')
test('(L) { "+" PLUS; "-" MINUS; }')
test('(i)  { "+"+ MANY_PLUS; }')
