import quex.engine.analyzer.core                   as     core
from   quex.engine.analyzer.door_id_address_label  import DialDB
import quex.input.regular_expression.engine        as     regex
import quex.engine.analyzer.optimizer              as     optimizer
import quex.engine.analyzer.track_analysis         as     track_analysis
from   quex.engine.analyzer.position_register_map  import print_this
import quex.engine.analyzer.engine_supply_factory  as     engine
import quex.engine.state_machine.construction.combination  as     combination
from   quex.constants  import E_InputActions, E_StateIndices, E_AcceptanceCondition, E_Op
from   quex.blackboard import setup as Setup

import sys
import os
from   operator import itemgetter

def if_DRAW_in_sys_argv(sm):
    if "DRAW" not in sys.argv: return
    fh = open("tmp.dot", "wb")
    fh.write( sm.get_graphviz_string() )
    fh.close()
    os.system("cat tmp.dot | awk ' ! /circle/ { print; }' > tmp1.dot")
    os.system("graph-easy --input=tmp1.dot --as boxart > tmp2.txt")
    os.system("awk '{ print \"   #   \", $0; }' tmp2.txt > tmp3.txt")
    os.system('echo "   #____________________________________________________________________" >> tmp3.txt')
    print "##", sys.argv[1]
    os.system('cat tmp3.txt')
    os.remove("tmp.dot")
    os.remove("tmp1.dot")
    sys.exit()

def prepare(PatternStringList, GetPreContextSM_F=False):
    pattern_list = map(lambda x: regex.do(x, {}).finalize(None), PatternStringList)

    if GetPreContextSM_F:
        state_machine_list = [ pattern.sm_pre_context for pattern in pattern_list ]
    else:
        state_machine_list = [ pattern.sm for pattern in pattern_list ]

    sm = combination.do(state_machine_list, False) # May be 'True' later.
    return sm.normalized_clone()

def test_track_analysis(SM, EngineType = engine.FORWARD, PrintPRM_F = False):
    print SM.get_string(NormalizeF=True, OriginalStatesF=False)
    to_db   = SM.get_to_db()
    from_db = SM.get_from_db()

    trace_db,       \
    path_element_db = track_analysis.do(SM, to_db)

    for state_index, paths_to_state in sorted(trace_db.iteritems(),key=itemgetter(0)):
        print "#State %i" % state_index
        for accept_sequence in paths_to_state:
            print accept_sequence.get_string(Indent=1)
        print

def get_drop_out_string(analyzer, StateIndex):
    txt = ".drop_out:\n"
    if_str = "if"
    for cmd in analyzer.drop_out.entry.get_command_list(E_StateIndices.DROP_OUT, StateIndex):
        if cmd.id == E_Op.IfPreContextSetPositionAndGoto:
            if   E_AcceptanceCondition.BEGIN_OF_LINE in cmd.content.acceptance_condition_set: 
                txt += "%s BeginOfLine: " % (if_str)
            if E_AcceptanceCondition.BEGIN_OF_STREAM in cmd.content.acceptance_condition_set: 
                txt += "%s BeginOfLine: " % (if_str)
            for acceptance_condition_id in cmd.content.acceptance_condition_set:
                txt += "%s PreContext_%s: " % (if_str, acceptance_condition_id)

            if if_str == "if": if_str = "else if"
            txt += cmd.content.router_element.get_string() + "\n"
        elif cmd.id == E_Op.GotoDoorId:
            txt += "GotoDoorId: %s" % str(cmd.content.door_id)
        else:
            txt += str(cmd) + "\n"
    return txt

def get_state_text(TheAnalyzer, state):
    txt = state.get_string(InputF=False, TransitionMapF=False)
    return txt + get_drop_out_string(TheAnalyzer, state.index)

def print_analyzer(TheAnalyzer):
    states_txt_db = {}
    for state in TheAnalyzer:
        #if EngineType.is_FORWARD():
        #    # if state.index == SM.init_state_index: assert state.input == E_InputActions.DEREF
        #    # else: assert state.input == E_InputActions.INCREMENT_THEN_DEREF
        txt = get_state_text(TheAnalyzer, state)
        print txt
        states_txt_db[state.index] = txt
    return states_txt_db

def test(SM, EngineType = engine.FORWARD, PrintPRM_F = False):
    
    print SM.get_string(NormalizeF=True, OriginalStatesF=False)

    plain = core.FSM.from_DFA(SM, EngineType, dial_db=DialDB())

    # Print plain analyzer, note down what changed during optimization
    states_txt_db = print_analyzer(plain)

    if PrintPRM_F:
        print_this(plain)

    diff_txt_db = {}
    optimized = optimizer.do(plain)
    for state in optimized:
        optimized_txt = get_state_text(optimized, optimized.state_db[state.index])
        if states_txt_db[state.index] != optimized_txt:
            diff_txt_db[state.index] = optimized_txt

    # Print the results of optimization
    if len(diff_txt_db):
        print 
        print "--- Optimized States ---"
        print 
        for state_index, state_txt in sorted(diff_txt_db.iteritems(), key=itemgetter(0)):
            print state_txt
