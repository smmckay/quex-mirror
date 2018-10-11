import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])

from   quex.engine.counter                        import CountAction, \
                                                         CountActionMap
from   quex.engine.state_machine.core             import DFA  
from   quex.engine.misc.interval_handling         import NumberSet, Interval, \
                                                         NumberSet_All
import quex.engine.analyzer.door_id_address_label as     dial
from   quex.engine.analyzer.door_id_address_label import DialDB
import quex.engine.state_machine.transformation.core as  bc_factory
import quex.engine.loop.core                      as     loop
from   quex.engine.loop.parallel_state_machines   import combine_intersecting_character_sets
import quex.engine.analyzer.engine_supply_factory as     engine
from   quex.blackboard                            import setup as Setup
from   quex.constants                             import E_CharacterCountType
import quex.output.languages.core                 as     languages
                                                         

from   operator import attrgetter
from   collections import namedtuple

if "--hwut-info" in sys.argv:
    print "Loop: combine_intersecting_character_sets;"
    sys.exit()

# Define heavily-self intersecting character sets.
## The intersection of a character set with another shall 
## still have intersections with the character set
def test(TL):
    print "#======================================"
    result = combine_intersecting_character_sets(TL)

    for x in result:
        print x[0], [sm.get_id() for sm in x[2]]


SM0 = DFA()
SM1 = DFA()
SM2 = DFA()
CA0 = CountAction(E_CharacterCountType.COLUMN, 0)

test_list = [
    (NumberSet(Interval(0, 100)), CA0, SM0),
    (NumberSet(Interval(10, 90)), CA0, SM1),
    (NumberSet(Interval(20, 80)), CA0, SM2),
]
test(test_list)

test_list = [
    (NumberSet(Interval(20, 80)), CA0, SM2),
    (NumberSet(Interval(10, 90)), CA0, SM1),
    (NumberSet(Interval(0, 100)), CA0, SM0),
]
test(test_list)

##test_list = [
    ##(NumberSet(20, 80), CA0, SM2),
    ##(NumberSet(10, 90), CA0, SM1),
    ##(NumberSet(0, 100), CA0, SM0),
##]
