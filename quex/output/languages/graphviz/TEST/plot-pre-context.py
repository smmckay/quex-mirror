#! /usr/bin/env python
import sys
import os

sys.path.append(os.environ["QUEX_PATH"])

from   quex.engine.mode                     import BasicMode
import quex.output.languages.graphviz.core            as     plotter
import quex.input.regular_expression.engine as     regex

from   quex.blackboard import setup as Setup

Setup.normalize_f = True

if "--hwut-info" in sys.argv:
    print "Plot: Pre-Context."
    sys.exit(0)


pattern = regex.do("[Hh]ello/a((b+ee(fe)*)+(b+cd)?)/", {}).finalize(None)

pattern_list = [
    pattern
]

my_plotter = plotter.Generator(BasicMode("test-plot", pattern_list))

my_plotter.do()

# HWUT consideres '##' as comment
for line in open(my_plotter.file_name_pre_context).readlines(): # .replace("#", "##")
    if line.find("digraph") != -1:
        print "digraph state_machine {"
    else:
        print "%s" % line,
os.remove(my_plotter.file_name_pre_context)
os.remove("test-plot.dot")


