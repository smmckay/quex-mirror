import os
import sys
sys.path.insert(0, os.path.abspath("../../../../"))

from quex.engine.misc.interval_handling import NumberSet
from quex.engine.misc.enum              import Enum
from copy import copy
from collections import defaultdict, namedtuple

from itertools import tee, takewhile

E_SubLexemeId = Enum("SEQUENCE", "NUMBER_SET", "LOOP")

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

    result = [ __expand(Dfa.init_state_index, path, loop_db) for path in path_list ]
    return result

def lexeme_set_to_string(LexemeSet):
    class Interpreter:
        @staticmethod
        def do(I):
            if I[0] == I[1]: return "%s" % I[0]
            else:            return "[%s-%s]" % (I[0], I[1])
        seperator     = ","
        right_bracket = "("
        left_bracket  = "("

    return [ __beautify(lexeme, Interpreter) for lexeme in sorted(LexemeSet) ]

def lexeme_set_to_characters(LexemeSet):
    class Interpreter:
        @staticmethod
        def do(I):
            print "#I:", I
            if I[0] == I[1]: return "%s" % unichr(I[0])
            else:            return "[%s-%s]" % (unichr(I[0]), unichr(I[1]))
        seperator     = ""
        right_bracket = ""
        left_bracket  = ""

    return [ __beautify(lexeme, Interpreter) for lexeme in sorted(LexemeSet) ]

def get_immutable_for_number_set(N):
    def do_interval(I):
        return (I.begin, I.end - 1)

    interval_list = N.get_intervals(PromiseToTreatWellF=True)
    return tuple(__representation(interval_list, do_interval, 
                                  Prefix=E_SubLexemeId.NUMBER_SET))

def __representation(interval_list, do_interval, Prefix=None, Suffix=None):

    result = []

    if Prefix is not None: result.append(Prefix)

    result.extend(
        do_interval(interval) for interval in interval_list
    )

    if Suffix is not None: result.append(Suffix)

    return result

def __beautify(SubLexeme, Interpreter):
    print "#SubLexeme:", SubLexeme
    return "".join(__beautify_sequence(SubLexeme, Interpreter))

def __beautify_sequence(SubLexeme, Interpreter):

    def next_tuple(sub_lexeme, i, L):
        if i == L - 1: return None, L
        else:          i += 1; return sub_lexeme[i], i

    txt = []
    L   = len(SubLexeme)
    print "#SubLexeme:", SubLexeme
    i   = 0
    tpl = SubLexeme[i]
    while tpl is not None:
        while tpl is not None and tpl[0] == E_SubLexemeId.NUMBER_SET:
            txt.append(
                "".join(__representation(tpl[1:], Interpreter.do,
                        Interpreter.right_bracket, Interpreter.left_bracket))
            )
            tpl, i = next_tuple(SubLexeme, i, L)

        loop_txt = []
        while tpl is not None and tpl[0] == E_SubLexemeId.LOOP:
            loop_txt.append(
                "".join(__beautify_sequence(tpl[1:], Interpreter))
            )
            tpl, i = next_tuple(SubLexeme, i, L)

        if loop_txt:
            txt.append("(%s)*" % "|".join(loop_txt))

    return txt

def __expand(StartSi, path, loop_db):
    def loop_lexeme(StartSi, loop_path, loop_db):
        loop_lexeme = [ E_SubLexemeId.LOOP ]
        if len(loop_path) > 1:
            # sub_path = loop_path[:-1]
            sub_path = __expand(StartSi, loop_path[:-1], loop_db)
            loop_lexeme.extend(sub_path)

        last = get_immutable_for_number_set(loop_path[-1].by_trigger_set)
        loop_lexeme.append(last)
        return tuple(loop_lexeme)

    if not path: return []

    lexeme     = []
    current_si = StartSi
    for trigger_set, target_si in path:
        lexeme.extend(loop_lexeme(StartSi, loop_path, loop_db)
                      for loop_path in loop_db[current_si])
        lexeme.append(get_immutable_for_number_set(trigger_set))
        current_si = target_si

    lexeme.extend(loop_lexeme(StartSi, loop_path, loop_db)
                  for loop_path in loop_db[current_si])

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
    #           from where:  with what trigger:
    work_list = [ (Step(None,   Dfa.init_state_index), []) ]

    while work_list:
        step, path = work_list.pop()
            
        path  = path + [step]
        si    = step.target_si

        prev_pos = is_on_path(path[:-1], si)
        if prev_pos is not None:
            loop_db[si].append(path[prev_pos+1:])
            continue

        state = Dfa.states[si]
        if state.is_acceptance(): 
            path_list.append(path[1:])

        for target_si, trigger_set in state.target_map:
            work_list.append((Step(trigger_set, target_si), path))

    return path_list, loop_db

if "__main__" == __name__: 
    import quex.input.regular_expression.engine as regex
    re_str     = "x((ab*c|cd)*y)"
    # re_str     = "x(ab*c)*"
    dfa        = regex.do(re_str, {}, AllowNothingIsNecessaryF=True).sm
    lexeme_set = get(dfa)
    for i, lexeme in enumerate(lexeme_set_to_characters(lexeme_set)):
    # for i, lexeme in enumerate(lexeme_set):
        print "[%i] %s " % (i, lexeme)
