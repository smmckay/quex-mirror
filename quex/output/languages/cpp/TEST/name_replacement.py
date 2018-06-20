#! /usr/bin/env python
import sys
import os
from StringIO import StringIO
sys.path.append(os.environ["QUEX_PATH"])

import quex.output.languages.core as languages
import quex.blackboard            as blackboard

if "--hwut-info" in sys.argv:
    print "Name and Namespace Replacement;"
    print "CHOICES: C, C++;"
    sys.exit()

choice = sys.argv[1]
blackboard.setup.language_db = languages.db[choice]()


def test(txt, N, NSP):
    txt0 = {
        0: "None",
        1: "Empty String",
        2: "String Size 1",
        3: "String Size > 1",
    }[N]
    txt1 = {
        0: "None",
        1: "Empty List",
        2: "List Size 1",
        3: "List Size > 1",
    }[NSP]

    print "___ Prefix: %s; Namespace: %s; __________________________________" \
          % (txt0, txt1)

    blackboard.setup.analyzer_class_name       = { 0: None, 1: "", 2: "L",     3: "Lexy"         }[N]
    blackboard.setup.analyzer_name_space       = { 0: None, 1: [], 2: ["LN0"], 3: ["LN0", "LN1"] }[NSP]

    blackboard.setup.token_class_name          = { 0: None, 1: "", 2: "T",     3: "Toky"         }[N]
    blackboard.setup.token_class_name_space    = { 0: None, 1: [], 2: ["TN0"], 3: ["TN0", "TN1"] }[NSP]

    blackboard.setup._quex_lib_prefix          = { 0: None, 1: "", 2: "Q",     3: "Quex"         }[N]
    blackboard.setup._quex_lib_name_space      = { 0: None, 1: [], 2: ["QN0"], 3: ["QN0", "QN1"] }[NSP]

    result = blackboard.setup.language_db.replace_naming(txt)

    for line in result.splitlines():
        print "    %s" % line

    print

txt = """
QUEX_NAME()       --> QUEX_NAME(Something);  QUEX_GNAME()       --> QUEX_GNAME(Something);
QUEX_NAME_TOKEN() --> QUEX_NAME_TOKEN(Something);  QUEX_GNAME_TOKEN() --> QUEX_GNAME_TOKEN(Something);
QUEX_NAME_LIB()   --> QUEX_NAME_LIB(Something);  QUEX_GNAME_LIB()   --> QUEX_GNAME_LIB(Something);
"""

for n in [0, 1, 2, 3]:
    for nsp in [0, 1, 2, 3]:
        test(txt, n, nsp)
