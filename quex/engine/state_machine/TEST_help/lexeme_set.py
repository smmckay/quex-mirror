import os
import sys
sys.path.insert(0, os.path.abspath("../../../../"))

from quex.engine.state_machine.core import DFA

def get(Dfa, IterationMaxN=1):
    def check_loop(iteration_db, target_si, IterationMaxN):
        print "#iteration_db:", target_si, iteration_db
        if target_si in iteration_db:
            if iteration_db[target_si] >= IterationMaxN:
                return iteration_db, False
            else:
                consider_db = copy(iteration_db) # disconnect
                consider_db[target_si] += 1
                return consider_db, True
        else:
            consider_db = copy(iteration_db) # disconnect
            consider_db[target_si] = 1
            return consider_db, True

    work_list = [ (Dfa.init_state_index, [], { Dfa.init_state_index: 1 }) ]
    result    = []

    while work_list:
        entry = work_list.pop()
        print "#entry:", entry
        si, lexeme_list, iteration_db = entry
        state = Dfa.states[si]
        if state.is_acceptance():
            print "#good:", lexeme_list
            result.extend(lexeme_list)

        for target_si, trigger_set in state.target_map.get_map().iteritems():
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
             

if "__main__" == __name__: 
    import quex.input.regular_expression.engine as regex
    dfa = regex.do("xy+z", {}).sm
    print get(dfa)
