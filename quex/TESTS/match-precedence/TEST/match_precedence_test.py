import os
import sys
sys.path.append(os.environ["QUEX_PATH"])
sys.path.insert(0, os.getcwd())


#from   quex.core                        import blackboard_mode_db_setup
import quex.input.files.mode        as     mode
from   quex.input.code.base         import SourceRef
from   quex.input.code.core         import CodeUser
import quex.output.core.dictionary  as     languages

import quex.blackboard              as     blackboard

blackboard.setup.language_db = languages.db["C++"]

from   StringIO import StringIO

def do(TxtList, DELETED_Op):
    blackboard.mode_prep_prep_db.clear()
    for txt in TxtList:
        sh = StringIO(txt)
        sh.name = "<string>"
        mode.parse(sh)

    blackboard.initial_mode = CodeUser("X", SourceRef.from_FileHandle(sh))

    mode_prep_db = mode.__finalize_modes_prep(blackboard.mode_prep_prep_db)
    for x in sorted(mode_prep_db.itervalues(), key=lambda x: x.name):
        print "Mode: '%s'" % x.name
        for i, pattern in enumerate(x.pattern_list):
            terminal = x.terminal_db[pattern.incidence_id]
            print "(%i) %s {%s}" % (i, pattern.pattern_string(), "".join(terminal.pure_code()).strip())


