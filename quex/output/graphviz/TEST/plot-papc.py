#! /usr/bin/env python
import sys
import os

sys.path.append(os.environ["QUEX_PATH"])

from   quex.engine.mode                        import BasicMode
import quex.output.graphviz.core               as     plotter
import quex.input.regular_expression.engine    as     regex
from   quex.input.files.specifier.mode         import PatternActionPair
from   quex.input.code.base                    import CodeFragment

from   quex.blackboard import setup as Setup
Setup.normalize_f = True

if "--hwut-info" in sys.argv:
    print "Plot: Backward Detector (for pseudo-ambiguous post context)."
    sys.exit(0)

pattern = regex.do("a(((b+ee(fe)*)+(b+cd)?)|(b+cd))/bbb(cb)*(eebc)?de", {}).finalize(None)

pattern_list = [ 
    pattern
]

mode       = BasicMode("test-plot", pattern_list)
my_plotter = plotter.Generator(mode)

my_plotter.do()

# HWUT consideres '##' as comment
file_name_bipd = my_plotter.file_name_bipd_db.values()[0]
for line in open(file_name_bipd).readlines(): # .replace("#", "##")
    if line.find("digraph") != -1:
        print "digraph state_machine {"
    else:
        print "%s" % line,

os.remove("test-plot.dot")
os.remove(file_name_bipd)


