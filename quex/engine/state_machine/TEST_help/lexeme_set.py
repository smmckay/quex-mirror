import os
import sys
sys.path.insert(0, os.path.abspath("../../../../"))

from copy import copy

def get(Dfa, IterationMaxN=2):
    """RETURNS: 'set' of lexeme which are matched by 'Dfa'.

    Rather than providing a raw list of 'Intervals', lexemes are
    represented as *immutables*, namely:  
        
         1) numerical value of the lexatom,
            if the interval size is 1
         2) tuple of the form (front, back)
            where 'front' is the first and 'back' is 
            the last lexatom of the interval.

    * The representation provided by this function is suited for
      quick comparison and verification of lexeme set operations.

    * The 'set' container is chosen to provide 'distinctness'.
      => Two 'Dfa' match the same set of lexemes if and only if
         'get(Dfa, *)' returns the same set of lexemes. 

    NOTE: The 'IterationMaxN' determines how many iterations in 
          a loop are expanded. This is an element that might 
          influence the precision of the identity condition.
    """
    def straigthen_interval(I):
        if I.end - I.begin == 1: return I.begin
        else:                    return (I.begin, I.end - 1)

    def straigthen_lexeme(L):
        return tuple(straigthen_interval(interval)
                     for interval in L)

    lexeme_list = get_raw(Dfa, IterationMaxN)

    return set(straigthen_lexeme(lexeme) for lexeme in lexeme_list)

def get_raw(Dfa, IterationMaxN):
    """RETURNS: List of Lexemes that are matched by 'Dfa'.

    The lexemes are specified in terms of 'Interval' objects.
    """
    def check_loop(iteration_db, target_si, IterationMaxN):
        if target_si not in iteration_db:
            consider_db = copy(iteration_db) # disconnect
            consider_db[target_si] = 1
            return consider_db, True
        elif iteration_db[target_si] <= IterationMaxN:
            consider_db = copy(iteration_db) # disconnect
            consider_db[target_si] += 1
            return consider_db, True
        else:
            return iteration_db, False

    work_list = [ (Dfa.init_state_index, [], { Dfa.init_state_index: 1 }) ]
    result    = []

    while work_list:
        entry = work_list.pop()
        si, lexeme_list, iteration_db = entry
        state = Dfa.states[si]
        if state.is_acceptance():
            result.extend(lexeme for lexeme in lexeme_list if lexeme)

        for target_si, trigger_set in state.target_map.get_map().iteritems():
            assert target_si in Dfa.states
            interval_list  = trigger_set.get_intervals()
            if not lexeme_list:
                new_lexeme_set = [ 
                    [ interval ] for interval in interval_list 
                ]
            else:
                new_lexeme_set = [
                    lexeme + [ interval ] 
                    for interval in interval_list
                    for lexeme in lexeme_list
                ]

            considered_iteration_db, \
            pass_f                   = check_loop(iteration_db, target_si,
                                                  IterationMaxN)
            if not pass_f: continue

            work_list.append((target_si, new_lexeme_set, 
                              considered_iteration_db))
    return result


    """RETURNS: List of Lexemes that are matched by 'Dfa'.

    The lexemes are specified in terms of 'Interval' objects.
    """
    def check_loop(path, target_si):
        """RETURNS: Number of transitions backwards so that target state 
                           is reached.
                    None, else; no loop.
        """
        for i, info in reversed(enumerate(path)):
            si, interval = info
            if si != target_si: continue
            return i
        return None
            

    work_list = [ (Dfa.init_state_index, [], [ Dfa.init_state_index ]) ] 
    result    = []

    while work_list:
        entry    = work_list.pop()
        si, path = entry
        state    = Dfa.states[si]

        if state.is_acceptance():
            result.append(lexeme_from_path(path))

        for target_si, trigger_set in state.target_map.get_map().iteritems():
            assert target_si in Dfa.states
            considered_iteration_db, \
            pass_f                   = check_loop(iteration_db, si, target_si,
                                                  IterationMaxN)
            if not pass_f: continue

            work_list.append((target_si, new_lexeme_set, 
                              considered_iteration_db))
    return result
             
def concatenate(Set0, Set1):
    return set(
        lexeme0 + lexeme1
        for lexeme0, lexeme1 in permutate(Set0, Set1, 2)
    )

if "__main__" == __name__: 
    import quex.input.regular_expression.engine as regex
    dfa = regex.do("x[cd]+z+(ab)+", {}).sm
    lexeme_set = get(dfa, 2)
    for lexeme in lexeme_set:
        print lexeme
