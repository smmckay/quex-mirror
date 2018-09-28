import quex.engine.state_machine.algebra.reverse as reverse
from   quex.engine.misc.file_operations import write_safely_and_close
from   quex.blackboard                  import setup as Setup

class Generator:
    def __init__(self, Mode):
        self.mode = Mode
        self.file_name_main        = "%s.dot"             % self.mode.name
        self.file_name_pre_context = "%s-pre-context.dot" % self.mode.name
        self.file_name_bipd_db     = dict( 
            (sm.get_id(), "%s_%s\.dot" % (Mode.name, sm.get_id()))
            for sm in Mode.bipd_sm_to_be_reversed_db.itervalues()
        )

    def do(self, Option="utf8"):
        """Prepare output in the 'dot' language, that graphviz uses."""
        assert Option in ["utf8", "hex"]

        self.__do(self.mode.sm, self.file_name_main, Option)

        if self.mode.pre_context_sm is not None:
            self.__do(self.mode.pre_context_sm, self.file_name_pre_context, Option)

        if len(self.mode.bipd_sm_to_be_reversed_db) != 0:
            for sm in self.mode.bipd_sm_to_be_reversed_db.itervalues():
                file_name = self.file_name_bipd_db[sm.get_id()] 
                reversed_sm = reverse.do(sm)
                self.__do(reversed_sm, file_name, Option)

    def __do(self, state_machine, FileName, Option="utf8"):
        dot_code = state_machine.get_graphviz_string(NormalizeF=Setup.normalize_f, Option=Option)
        write_safely_and_close(FileName, dot_code)

