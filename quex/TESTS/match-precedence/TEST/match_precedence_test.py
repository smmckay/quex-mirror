import os
import sys
sys.path.append(os.environ["QUEX_PATH"])
sys.path.insert(0, os.getcwd())

import quex.input.files.mode       as     mode
from   quex.input.code.base        import SourceRef
from   quex.input.code.core        import CodeUser
import quex.output.languages.core  as     languages

import quex.blackboard             as     blackboard

blackboard.setup.language_db = languages.db["C++"]()

from   StringIO import StringIO

def do(TxtList, DELETED_Op):
    mode_prep_prep_db = {}
    for txt in TxtList:
        sh = StringIO(txt)
        sh.name = "<string>"
        mode.parse(sh, mode_prep_prep_db)

    blackboard.initial_mode = CodeUser("X", SourceRef.from_FileHandle(sh))

    mode_prep_db = mode.__finalize_modes_prep(mode_prep_prep_db)
    for x in sorted(mode_prep_db.itervalues(), key=lambda x: x.name):
        print "Mode: '%s'" % x.name
        for i, pattern in enumerate(x.pattern_list):
            terminal = x.terminal_db[pattern.incidence_id]
            print "(%i) %s {%s}" % (i, pattern.pattern_string(), "".join(terminal.pure_code()).strip())


