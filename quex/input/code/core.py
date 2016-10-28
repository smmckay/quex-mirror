from   quex.input.code.base   import SourceRef, CodeFragment, SourceRef_VOID
from   quex.engine.misc.tools import typed

from   copy import deepcopy

class CodeUser(CodeFragment):
    """User code as it is taken from some input file. It contains:

          .get_code() -- list of strings or text formatting instructions
                         (including possibly annotations about its source code origin)
          .sr         -- the source reference where it was taken from
          .mode_name  -- Mode where the code was defined
    """
    def __init__(self, Code, SourceReference):
        CodeFragment.__init__(self, Code, SourceReference)

    def clone(self):
        assert False, "UNUSED"
        result = CodeUser(deepcopy(self.get_code()), self.sr)
        return result

CodeUser_NULL = CodeUser([], SourceRef())

class CodeTerminal(CodeFragment):
    __slots__ = ("__requires_lexeme_terminating_zero_f", 
                 "__requires_lexeme_begin_f", 
                 "__pure_code")

    @typed(Code=list, SourceReference=SourceRef, PureCode=list)
    def __init__(self, Code, SourceReference=SourceRef_VOID, 
                 PureCode=None):
        CodeFragment.__init__(self, Code, SourceReference)

        if PureCode is not None: self.__pure_code = PureCode
        else:                    self.__pure_code = Code

    @staticmethod
    def from_CodeFragment(CF):
        return CodeTerminal(CF.get_code(), CF.sr)

    def get_pure_code(self):
        return self.__pure_code

CodeTerminal_NULL = CodeTerminal([])

