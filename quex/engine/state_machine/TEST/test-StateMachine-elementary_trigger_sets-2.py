#! /usr/bin/env python
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])


from quex.engine.misc.interval_handling import *
from quex.engine.state_machine.core import *
from quex.engine.state_machine.state.target_map_ops import get_elementary_trigger_sets

if "--hwut-info" in sys.argv:
    print "NFA: Get elementary trigger sets II"
    sys.exit(0)

# (*) Special case that caused trouble before: two states
#     trigger on the same trigger to the same target state.
sm = DFA()
sm.add_transition(36L, 98, 100L)
sm.add_transition(37L, 98, 100L)

print "states machine = ", sm

def show(ETS):
    result = repr(ETS)
    result = result.replace("(", "[")
    result = result.replace(",)", ")")
    result = result.replace(")", "]")
    return result

# (*) compute the elementary trigger set
epsilon_closure_db = sm.get_epsilon_closure_db()
ets = get_elementary_trigger_sets([36, 37], sm, epsilon_closure_db).items()
print "elementary trigger sets = ", show(ets)
i = 10
for target_indices, trigger_set in ets:
    i += 1
    print trigger_set.gnuplot_string(i)


# (*) Another special case
sm = DFA()
sm.add_transition(36L, Interval(98, 100), 100L)
sm.add_transition(37L, 98, 100L)

print "states machine = ", sm

# (*) compute the elementary trigger set
epsilon_closure_db = sm.get_epsilon_closure_db()
ets = get_elementary_trigger_sets([36, 37], sm, epsilon_closure_db).items()
print "elementary trigger sets = ", show(ets)
i = 10
for target_indices, trigger_set in ets:
    i += 1
    print trigger_set.gnuplot_string(i)
            
