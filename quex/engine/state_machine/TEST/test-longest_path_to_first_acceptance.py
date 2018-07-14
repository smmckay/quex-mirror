#! /usr/bin/env python
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])

import quex.input.regular_expression.engine as     core
from   StringIO                             import StringIO

if "--hwut-info" in sys.argv:
    print "Longest path to first acceptance;"
    print "CHOICES: Sequences, Alternatives, Repetitions, Wild;"
    sys.exit(0)
    
def test(TestString):
    TestString = TestString.replace("\n", "\\n").replace("\t", "\\t")
    TestString = "%s" % TestString
    print ("RE:     " + TestString).replace("\n", "\\n").replace("\t", "\\t")
    sm = core.do(TestString, {}, AllowNothingIsNecessaryF=True).sm
    # print "#sm:", sm
    print ("result: %s" % sm.longest_path_to_first_acceptance())

if "Sequences" in sys.argv:
    test('A')
    test('AB')
    test('ABC')
    test('[0-9]')
    test('[0-9]B')
    test('[0-9]BC')
    test('A[0-9]')
    test('A[0-9]C')
    test('AB[0-9]')

elif "Alternatives" in sys.argv:
    test('A|B')
    test('AA|A')
    test('AA|B')
    test('AA|AB')
    test('AB|B')
    test('AB|BA')
    test('AAA|A')
    test('AAA|B')
    test('AAA|AB')
    test('AAB|B')
    test('AAA|AA')
    test('AAA|AB')
    test('AAA|AAB')
    test('AAB|AB')

elif "Repetitions" in sys.argv:
    test('A*')
    test('A(A*)')   
    test('B(A*)')   
    test('(A*)A')
    test('(A*)B')
    test('A(B*)C')
    
    test('"AB"*')
    test('"AB"("AB"*)')   
    test('"CD"("AB"*)')   
    test('("AB"*)"AB"')
    test('("AB"*)"CD"')
    test('"AB"("CD"*)"EF"')

elif "Wild" in sys.argv:
    test('X"123"?')
    test('"123"?X')
    test('"123"*X')

    test('abc("123"|"ABC")xyz')
    test('abc("123"|"ABCD")xyz')
    test('abc("123"|"ABC")+xyz')
    test('abc("123"|"ABC")?xyz')
    test('abc("123"|"ABC")*xyz')

    test('X("a"|"x"?|"e"|"g")')
    test('"a"|"x"+|"e"|"g"')
    test('X("a"|"x"*|"e"|"g")')

    test('abc("123"|("ABC"|"XYZ"))"123"("AAA"|"BBB"|"CCC")xyz')
    test('abc("123"|("ABCD"|"XYZ"))"123"("AAA"|"BBB"|"CCC")xyz')

