from   quex.input.code.core             import CodeFragment
from   quex.engine.analyzer.door_id_address_label import DoorID
from   quex.engine.analyzer.state.core  import Processor
from   quex.engine.analyzer.state.entry import Entry
import quex.engine.state_machine.index  as     index
from   quex.engine.misc.tools           import typed

from   quex.blackboard import E_IncidenceIDs

from   copy  import copy

#__________________________________________________________________________
#
# TerminalState:
#                    .-------------------------------------------------.
#  .-----.           |                                                 |
#  | 341 |--'accept'--> input_p = position[2]; --->---+---------.      |
#  '-----'           |  set terminating zero;         |         |      |
#  .-----.           |                                |    .---------. |
#  | 412 |--'accept'--> column_n += length  ------>---+    | pattern | |
#  '-----'           |  set terminating zero;         |    |  match  |--->
#  .-----.           |                                |    | actions | |
#  | 765 |--'accept'--> line_n += 2;  ------------>---'    '---------' |
#  '-----'           |  set terminating zero;                          |
#                    |                                                 |
#                    '-------------------------------------------------'
# 
# A terminal state prepares the execution of the user's pattern match 
# actions and the start of the next analysis step. For this, it computes
# line and column numbers, sets terminating zeroes in strings and resets
# the input pointer to the position where the next analysis step starts.
#__________________________________________________________________________
class Terminal(Processor):
    @typed(Name=(str,unicode), Code=CodeFragment)
    def __init__(self, Code, Name, IncidenceId=None, RequiredRegisterSet=None,
                 RequiresLexemeBeginF=False, RequireLexemeTerminatingZeroF=False, 
                 dial_db=None):
        assert dial_db is not None
        assert    isinstance(IncidenceId, long) \
               or IncidenceId is None \
               or IncidenceId in E_IncidenceIDs
        Processor.__init__(self, index.get(), Entry(dial_db))
        if IncidenceId is not None: 
            self.__incidence_id = IncidenceId
            self.__door_id      = DoorID.incidence(IncidenceId, dial_db)
        else:                       
            self.__incidence_id = None
            self.__door_id      = None
        self.__code         = Code
        self.__name         = Name
        self.__requires_goto_loop_entry_f = False
        if RequiredRegisterSet is not None:
            self.__required_register_set = RequiredRegisterSet
        else:
            self.__required_register_set = set()
        self.__requires_lexeme_terminating_zero_f = RequireLexemeTerminatingZeroF
        self.__requires_lexeme_begin_f            = RequiresLexemeBeginF

    @property
    def door_id(self):
        assert self.__incidence_id is not None
        assert self.__door_id is not None
        return self.__door_id

    def clone(self, NewIncidenceId=None):
        # TODO: clone manually
        result = Terminal(Code        = copy(self.__code),
                          Name        = self.__name,
                          IncidenceId = NewIncidenceId if NewIncidenceId is None \
                                                       else self.__incidence_id,
                          RequiredRegisterSet           = self.__required_register_set,
                          RequiresLexemeBeginF          = self.__requires_lexeme_begin_f,
                          RequireLexemeTerminatingZeroF = self.__requires_lexeme_terminating_zero_f,
                          dial_db                       = self.entry.dial_db)
        result.__door_id = self.__door_id

        if NewIncidenceId is not None:
            result.set_incidence_id(NewIncidenceId, ForceF=True)
        return result

    def incidence_id(self):
        return self.__incidence_id

    def set_incidence_id(self, IncidenceId, ForceF=False):
        assert ForceF or self.__incidence_id is None
        self.__incidence_id = IncidenceId
        self.__door_id      = DoorID.incidence(IncidenceId, self.entry.dial_db)

    def name(self):
        return self.__name

    def code(self, TheAnalyzer):
        return self.__code.get_code()

    def pure_code(self):
        return self.__code.get_pure_code()

    def requires_lexeme_terminating_zero_f(self):
        return self.__requires_lexeme_terminating_zero_f

    def requires_lexeme_begin_f(self):
        return self.__requires_lexeme_begin_f

    def required_register_set(self):
        return self.__required_register_set

