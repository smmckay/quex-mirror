#! /usr/bin/env python
import sys
import os

sys.path.append(os.environ["QUEX_PATH"])

from   quex.engine.mode                     import BasicMode
import quex.output.languages.graphviz.core            as plotter
import quex.input.regular_expression.engine as regex
from   quex.blackboard import setup as Setup
Setup.normalize_f = True

if "--hwut-info" in sys.argv:
    print "Plot: Core state machine."
    sys.exit(0)

pattern_list = [
    regex.do("a(((b+ee(fe)*)+(b+cd)?)|(b+cd))", {}).finalize(None)
]

# HWUT consideres '##' as comment
my_plotter = plotter.Generator(BasicMode("test-plot", pattern_list))

my_plotter.do()
for line in open("test-plot.dot").readlines(): # .replace("#", "##")
    if line.find("digraph") != -1:
        print "digraph state_machine {"
    else:
        print "%s" % line,
os.remove("test-plot.dot")



