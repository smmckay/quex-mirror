from   quex.input.code.base   import SourceRef, CodeFragment, SourceRef_VOID
from   quex.engine.misc.tools import typed
from   quex.blackboard        import Lng

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
        result = CodeUser(deepcopy(self.get_code()), self.sr)
        return result

CodeUser_NULL = CodeUser([], SourceRef())

class CodeTerminal(CodeFragment):
    __slots__ = ("__requires_lexeme_terminating_zero_f", "__requires_lexeme_begin_f", "__pure_code")

    @typed(Code=list, SourceReference=SourceRef, 
           LexemeRelevanceF=bool, LexemeTerminatingZeroF=bool, LexemeBeginF=bool,
           PureCode=list)
    def __init__(self, Code, SourceReference=SourceRef_VOID, 
                 LexemeRelevanceF=False, LexemeTerminatingZeroF=False, LexemeBeginF=False,
                 PureCode=None):
        CodeFragment.__init__(self, Code, SourceReference)
        if LexemeRelevanceF:
            self.__requires_lexeme_terminating_zero_f = None
            self.__requires_lexeme_begin_f            = None
        else:
            self.__requires_lexeme_terminating_zero_f = LexemeTerminatingZeroF
            self.__requires_lexeme_begin_f            = LexemeBeginF

        if PureCode is not None: self.__pure_code = PureCode
        else:                    self.__pure_code = Code

    @staticmethod
    def from_CodeFragment(CF, LexemeRelevanceF=False):
        return CodeTerminal(CF.get_code(), CF.sr, LexemeRelevanceF=LexemeRelevanceF)

    def requires_lexeme_begin_f(self):            
        # NOT: if self.__requires_lexeme_begin_f is None: ...
        #      The construction is too dynamic.
        self.__requires_lexeme_begin_f =    self.requires_lexeme_terminating_zero_f() \
                                         or self.contains_string(Lng.Match_LexemeBegin)
        return self.__requires_lexeme_begin_f

    def requires_lexeme_terminating_zero_f(self): 
        # NOT: if self.__requires_lexeme_terminating_zero_f is None: ...
        #      The construction is too dynamic.
        self.__requires_lexeme_terminating_zero_f = self.contains_string(Lng.Match_Lexeme) 
        return self.__requires_lexeme_terminating_zero_f

    def get_pure_code(self):
        return self.__pure_code

CodeTerminal_NULL = CodeTerminal([])

class CodeTerminalOnMatch(CodeTerminal):
    @typed(Code=CodeFragment)
    def __init__(self, CodeFrag):
        code           = CodeFrag.get_code() 
        self.mode_name = CodeFrag.sr.mode_name
        CodeTerminal.__init__(self, code, CodeFrag.sr, LexemeRelevanceF=True)


    
