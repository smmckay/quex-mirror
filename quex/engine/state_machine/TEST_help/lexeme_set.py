import os
import sys
sys.path.insert(0, os.path.abspath("../../../../"))

from quex.engine.misc.interval_handling import NumberSet
from quex.engine.misc.enum              import Enum
from copy import copy
from collections import defaultdict, namedtuple

E_SubLexemeId = Enum("SEQUENCE", "NUMBER_SET")

def get_string_for_number_set(IntervalList):
    def do_interval(I):
        if I.end - I.begin == 1: return "%s"      % I.begin
        else:                    return "[%s-%s]" % (I.begin, I.end-1)

    txt = __representation(IntervalList, do_interval, "(", ")")

    return "".join(txt)

def get_immutable_for_number_set(N):
    def do_interval(I):
        if I.end - I.begin == 1: return I.begin
        else:                    return (I.begin, I.end - 1)

    interval_list = N.get_intervals(PromiseToTreatWellF=True)
    return tuple(__representation(interval_list, do_interval, 
                                  Prefix=E_SubLexemeId.NUMBER_SET)))

def __representation(interval_list, do_interval, Prefix=None, Suffix=None):
    if len(interval_list) == 1:
        return do_interval(interval_list[0])

    if Prefix is not None: result = [ Prefix ]
    else:                  result = []

    result.extend(
        do_interval(interval)
        for interval in N.get_intervals(PromiseToTreatWellF=True)
    )

    if Suffix is not None: result.append(Suffix)

    return result

class Line(SubLexeme):
    def __init__(self, TriggerSet):
        SubLexeme.__init__(self, [ TriggerSet ])

    def __repr__(self):
        return self.get_string("Line")

    @classmethod
    def clone_concatenation(cls, sub_lexeme_list, TriggerSet):
        result = copy(sub_lexeme_list)
        result[-1].lexeme.append(TriggerSet)
        return result

    def get_immutable(self):
        return tuple(self.lexeme)

class Loop(SubLexeme):
    def __init__(self, TrigerSetList):
        SubLexeme.__init__(self, TrigerSetList)

    def __repr__(self):
        return self.get_string("Loop")

    @classmethod
    def clone_concatenation(cls, sub_lexeme_list, TriggerSet):
        result = copy(sub_lexeme_list)
        result.append(TriggerSet)
        return result

    def get_immutable(self):
        return tuple([-1] + self.lexeme)

def get(Dfa):
    def straigthen_interval(N):
        if N.has_size_one(): return N.minimum()
        else:                return N

    def straigthen_lexeme(L):
        return tuple(straigthen_interval(interval)
                     for interval in L)

    lexeme_list = get_raw(Dfa)

    return set(straigthen_lexeme(lexeme) for lexeme in lexeme_list)

def get_interpretation(Dfa):
    """RETURNS: List of Lexemes that are matched by 'Dfa'.

    The lexemes are specified in terms of 'Interval' objects.
    """
    predecessor_db = Dfa.get_predecessor_db()
    successor_db   = Dfa.get_successor_db(HintPredecessorDb=predecessor_db)
    

Step = namedtuple("Step", ("by_trigger_set", "target_si"))

def get(Dfa):
    """RETURNS: 'set' of lexeme which are matched by 'Dfa'.

    The lexeme representation is suited for quick comparison. All
    elements are *immutables*, so they may also serve as hash keys
    or set elements.

    * 'set' => provides distinctness
               Two 'DFA's match the same set of lexemes if and only if 
               the return values of this functions are the same
            => set operations on the set of lexemes can directly be 
               applied.
    """
    path_list, \
    loop_db    = __find_paths(Dfa)

    return set(__expand(path, loop_db) for path in path_list)

def lexeme_set_to_string(LexemeSet):
    def __beatify(sub_lexeme):
        result = []
        for x in sub_lexeme:
            if type(x) == tuple:
                if x[0] == E_SubLexemeId.NUMBER_SET: 
                    sub_txt = get_string_for_number_set(x[1:])
                elif x[0] == E_SubLexemeId.SEQUENCE: 
                    sub_txt = __beatify(x[1:])
                else:
                    sub_txt = "[%s-%s]" % (x[0],x[1])
            else:
                sub_txt = "%s" % x

            result.append(sub_txt)
        return "".join(result)

    return [ __beatify(lexeme) for lexeme in sorted(LexemeSet) ]

def __expand(path, loop_db):
    if not path: return []

    if path[0].by_trigger_set is None: first_i = 1
    else:                              first_i = 0

    lexeme = [ E_SubLexemeId.SEQUENCE ]
    for trigger_set, si in path[first_i:]:
        loop_path_list = loop_db[si]
        for loop_path in loop_path_list:
            if len(loop_path) > 1:
                loop_lexeme = list(__expand(loop_path[:-1], loop_db))
            else:
                loop_lexeme = [ E_SubLexemeId.SEQUENCE ]
            last = get_immutable_for_number_set(loop_path[-1].by_trigger_set)
            loop_lexeme.append(last)
            lexeme.append(tuple(loop_lexeme))
        lexeme.append(get_immutable_for_number_set(trigger_set))
    return tuple(lexeme)

def __find_paths(Dfa):
    """RETURNS: [0] List of paths
                [1] LoopDb: si --> path that comes back to 'si'

    where each 'path' is a sequence of (state index, trigger), representing the
    path through a Dfa. '(state index, trigger)' represents a transition to
    'state index' via the 'trigger'.
    """
    def is_on_path(path, si):
        """RETURNS: Index 'i' with path[i].si == si, if exists.
                    None, if 'si' is not on path. 
        """
        for i, step in enumerate(path):
            if step.target_si == si: return i
        return None

    loop_db   = defaultdict(list)
    path_list = []
    #             from where:  with what trigger:
    path      = [ Step(None,       Dfa.init_state_index) ]
    work_list = [ path ]
    while work_list:
        path = work_list.pop()
        si   = path[-1].target_si
            
        state = Dfa.states[si]
        if state.is_acceptance(): path_list.append(path)

        for target_si, trigger_set in state.target_map:
            prev_pos = is_on_path(path, target_si)
            if prev_pos is not None:
                loop_db[si].append(path[prev_pos:])
            else:
                work_list.append(path + [ Step(trigger_set, target_si) ])

    print "#Dfa:", Dfa.get_string(NormalizeF=False)
    print "#loop_db:", loop_db
    return path_list, loop_db

if "__main__" == __name__: 
    import quex.input.regular_expression.engine as regex
    re_str     = "x[c-dx-z]+z+(ab)+"
    dfa        = regex.do(re_str, {}).sm
    lexeme_set = get_lexemes(dfa)
    for lexeme in lexeme_set:
        print lexeme
