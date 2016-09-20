#! /usr/bin/env python
import sys
import os

sys.path.append(os.environ["QUEX_PATH"])

from   quex.engine.mode                     import BasicMode
import quex.output.graphviz.core            as     plotter
import quex.input.regular_expression.engine as     regex
from   quex.input.files.mode                import PatternActionPair

from   quex.blackboard import setup as Setup

Setup.normalize_f = True

if "--hwut-info" in sys.argv:
    print "Plot: Pre-Context."
    sys.exit(0)


pattern = regex.do("[Hh]ello/a((b+ee(fe)*)+(b+cd)?)/", {})
pattern.mount_pre_context_sm()

pattern_list = [
    pattern
]

my_plotter = plotter.Generator(BasicMode("test-plot", pattern_list))

my_plotter.do()

# HWUT consideres '##' as comment
for line in open(my_plotter.pre_context_file_name).readlines(): # .replace("#", "##")
    if line.find("digraph") != -1:
        print "digraph state_machine {"
    else:
        print "%s" % line,
os.remove(my_plotter.pre_context_file_name)
os.remove("test-plot.dot")


