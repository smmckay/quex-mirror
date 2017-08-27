import os
import sys
sys.path.insert(0, os.environ["QUEX_PATH"])

import quex.constants as constants

if "--hwut-info" in sys.argv:
    print "Check that there are no trailing unused Enum Values;"
    sys.exit()

enum_list = [ x for x in dir(constants) if x.startswith("E_") ]

enum_db = dict(
    (enum_name, [ x for x in dir(constants.__dict__[enum_name]) if x[0] != "_" ])
    for enum_name in enum_list
    if not enum_name.endswith("_string") and not enum_name.endswith("_corresponance")
)

for enum_name, value_list in enum_db.iteritems():
    search_list = [ "%s\\.%s" % (enum_name, value) for value in value_list ]
    os.system("./no-unused-enum-values-helper.sh %s %s" % (enum_name, " ".join(sorted(search_list))))
print "<terminated>"

