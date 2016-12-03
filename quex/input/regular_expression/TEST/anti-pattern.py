#! /usr/bin/env python
import sys
import os
import StringIO

sys.path.insert(0, os.environ["QUEX_PATH"])
import quex.input.regular_expression.exception as exception
import quex.input.regular_expression.engine as engine
from   quex.blackboard import setup as Setup
from   quex.constants  import INTEGER_MAX

Setup.set_all_character_set_UNIT_TEST(-INTEGER_MAX, INTEGER_MAX)

if "--hwut-info" in sys.argv:
    print "Anti-Patterns"
    sys.exit(0)
    
def test(TestString):
    print
    print "expression = \"" + TestString + "\""
    stream = StringIO.StringIO(TestString)
    try:
        result = engine.do(stream, {})
        print "result     = " + result.get_string(NormalizeF=True) 
    except exception.RegularExpressionException, x:
        print x.message

test("\\A{for}")    
test("\\A{[ab][cd][de]}")    
test("\\A{x+y+}")    
