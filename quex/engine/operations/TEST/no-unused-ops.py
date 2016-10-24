import os
import sys
sys.path.insert(0, os.environ["QUEX_PATH"])

from quex.blackboard import E_Op

if "--hwut-info" in sys.argv:
    print "Check that there are no trailing unused Ops;"
    sys.exit()

value_list = [ x for x in dir(E_Op) if x[0] != "_" ]

os.system("./no-unused-ops-helper.sh %s" % " ".join(sorted(value_list)))
print "<terminated>"

