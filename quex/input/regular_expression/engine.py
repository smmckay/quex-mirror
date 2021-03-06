# The 'grammar' of quex's regular expressions:
#
#  complete expression: expression
#                       expression / expression              = post conditioned expression
#                       expression / expression /            = pre conditioned expression
#                       expression / expression / expression = pre and post conditioned expression
# 
#  expression: term
#              term | expression
#  
#  term:  primary
#         primary term
#  
#  primary:  " non_double_quote *  "              = character string
#            [ non_rect_bracket_close ]           = set of characters
#            { identifier }                       = pattern replacement
#            ( expression )
#            non_control_character+               = lonely characters
#            primary repetition_cmd
#  
#  non_double_quote: 'anything but an unbackslashed double quote, i.e. \" is ok, 
#                     but " is not.'      
#  non_rect_bracket_close: 'anything but an unbackslashed rectangular bracket, i.e.
#                           \] is ok, but ] is not.'               
#  non_control_character: 'anything but (, ", [, or {'
#       
#  repetition_cmd: 'a repetition command such as +, *, {2}, {,2}, {2,5}'        
#
#########################################################################################       
import quex.engine.codec_db.core                              as codec_db
from   quex.engine.state_machine.core                         import DFA
import quex.engine.state_machine.algorithm.beautifier         as beautifier
import quex.engine.state_machine.algorithm.nfa_to_dfa         as nfa_to_dfa
import quex.engine.state_machine.algebra.sanitizer            as sanitizer
import quex.engine.state_machine.algebra.complement           as complement
import quex.engine.state_machine.algebra.reverse              as reverse
import quex.engine.state_machine.algebra.intersection         as intersection
import quex.engine.state_machine.algebra.difference           as difference
import quex.engine.state_machine.algebra.symmetric_difference as symmetric_difference
import quex.engine.state_machine.algebra.union                as union
import quex.engine.state_machine.cut.operations_on_sets       as derived
import quex.engine.state_machine.cut.stem_and_branches        as stem_and_branches
import quex.engine.state_machine.cut.operations_on_lexemes    as cut
from   quex.input.code.base                                   import SourceRef

import quex.input.regular_expression.traditional_character_set  as traditional_character_set
import quex.input.regular_expression.property                   as property
from   quex.input.regular_expression.pattern                    import Pattern_Prep
import quex.input.regular_expression.snap_backslashed_character as snap_backslashed_character
import quex.input.regular_expression.snap_character_string      as snap_character_string
from   quex.input.regular_expression.auxiliary                  import __snap_until, \
                                                                       __debug_entry, \
                                                                       __debug_exit, \
                                                                       __debug_print, \
                                                                       snap_replacement

import quex.engine.state_machine.construction.sequentialize    as sequentialize
import quex.engine.state_machine.construction.parallelize      as parallelize
import quex.engine.state_machine.construction.repeat           as repeat
import quex.engine.codec_db.unicode.case_fold_parser           as ucs_case_fold

from   quex.engine.misc.interval_handling  import Interval, NumberSet
import quex.engine.misc.error              as     error
from   quex.engine.misc.file_in            import check, \
                                                  check_whitespace, \
                                                  skip_whitespace, \
                                                  read_identifier, \
                                                  optional_flags
import quex.engine.misc.utf8               as utf8
from   quex.blackboard import setup as Setup
from   quex.constants  import INTEGER_MAX
from   quex.input.regular_expression.exception import RegularExpressionException

from   StringIO import StringIO
       

CONTROL_CHARACTERS = [ "+", "*", "\"", "/", "(", ")", "{", "}", "|", "[", "]", "$"] 
SPECIAL_TERMINATOR = None

def do(UTF8_String_or_Stream, PatternDict, 
       AllowNothingIsNecessaryF = False, SpecialTerminator=None):
    global SPECIAL_TERMINATOR 
    assert type(AllowNothingIsNecessaryF) == bool
    assert type(PatternDict) == dict

    # SPECIAL_TERMINATOR --> if string is not only to be terminated by ' '
    SPECIAL_TERMINATOR = SpecialTerminator

    def __ensure_whitespace_follows(InitialPos, stream):
        tmp = stream.read(1)
        if tmp == "" or tmp.isspace() or tmp == SPECIAL_TERMINATOR:
            stream.seek(-1, 1)
            return

        end_position = stream.tell() - 1
        stream.seek(InitialPos)
        pattern_str = stream.read(end_position - InitialPos)
        error.log("Pattern definition '%s' not followed by whitespace.\n" % pattern_str + \
                  "Found subsequent character '%s'." % tmp, 
                  stream)

    if type(UTF8_String_or_Stream) == str: stream = StringIO(UTF8_String_or_Stream)
    else:                                  stream = UTF8_String_or_Stream    

    if PatternDict is None: PatternDict = {}

    initial_position = stream.tell()

    # -- check for the begin of line condition (BOL)
    begin_of_line_f   = check(stream, '^')
    begin_of_stream_f = check(stream, '<<BOS>>')
    if begin_of_stream_f: skip_whitespace(stream)

    if begin_of_line_f: begin_of_stream_f = True
    
    # -- MAIN: transform the pattern into a state machine
    pre, core, post = snap_conditional_expression(stream, PatternDict)

    if core is None: 
        stream.seek(initial_position)
        return None

    # -- check for end of line condition (EOL) 
    # -- check for terminating whitespace
    end_of_line_f   = check(stream, "$")
    end_of_stream_f = check(stream, "<<EOS>>")

    if end_of_line_f: end_of_stream_f = True

    __error_check(begin_of_line_f, begin_of_stream_f, pre, stream, "pre-context")
    __error_check(end_of_line_f, end_of_stream_f, post, stream, "post-context")

    __ensure_whitespace_follows(initial_position, stream)
    
    pattern = Pattern_Prep(CoreSM         = core, 
                           BeginOfLineF   = begin_of_line_f,
                           BeginOfStreamF = begin_of_stream_f,
                           PreContextSM   = pre,
                           EndOfLineF     = end_of_line_f,
                           EndOfStreamF   = end_of_stream_f,
                           PostContextSM  = post,
                           Sr             = SourceRef.from_FileHandle(stream),
                           PatternString  = read_pattern_string(stream, initial_position),
                           AllowNothingIsNecessaryF = AllowNothingIsNecessaryF)
    
    return pattern

def read_pattern_string(fh, StartPos):
    """Reads the regular expression string which was interpreted to build the 
    pattern. 
    """
    end_position = fh.tell()
    fh.seek(StartPos)
    result = fh.read(end_position - StartPos)
    if not result:
        result = fh.read(1)
        fh.seek(-1, 1)
    return result

def snap_conditional_expression(stream, PatternDict):
    """conditional expression: expression
                               expression / expression                 = post conditioned expression
                               expression / expression /               = pre conditioned expression
                               expression / expression / expression    = pre and post conditioned expression
       TODO: <- ($8592) for pre-context
             -> ($8594) for post-context


        RETURNS: pre_context, core_pattern, post_context
    """                     
    __debug_entry("conditional expression", stream)    

    # -- expression
    pattern_0 = __core(stream, PatternDict) 
    if pattern_0 is None: 
        return None, None, None
    
    # -- '/'
    if not check(stream, '/'): 
        # (1) expression without pre and post condition
        #     pattern_0 is already beautified by '__core()'
        return None, pattern_0, None
        
    # -- expression
    pattern_1 = __core(stream, PatternDict) 
    if pattern_1 is None: 
        return None, pattern_0, None
    
    # -- '/'
    if not check(stream, '/'): 
        # (2) expression with only a post condition
        #     NOTE: setup_post_context() marks state origins!
        return None, pattern_0, pattern_1

    # -- expression
    pattern_2 = __core(stream, PatternDict) 
    if pattern_2 is None: 
        # (3) expression with only a pre condition
        #     NOTE: setup_pre_context() marks the state origins!
        return pattern_0, pattern_1, None
    else:
        # (4) expression with post and pre-context
        return pattern_0, pattern_1, pattern_2

def __core(stream, PatternDict):
    result = snap_expression(stream, PatternDict)
    if result is None: return None
    else:              return beautifier.do(result)

def snap_expression(stream, PatternDict):
    """expression:  term
                    term | expression
    """              
    __debug_entry("expression", stream)    
    # -- term
    result = snap_term(stream, PatternDict) 
    if result is None: 
        return __debug_exit(None, stream)

    # -- optional '|'
    if not check(stream, '|'): 
        return __debug_exit(result, stream)
    
    position_1 = stream.tell()
    __debug_print("'|' (in expression)")

    # -- expression
    result_2 = snap_expression(stream, PatternDict) 
    __debug_print("expression(in expression):",  result_2)
    if result_2 is None:
        stream.seek(position_1) 
        return __debug_exit(result, stream)

    result = parallelize.do([result, result_2])
    return __debug_exit(nfa_to_dfa.do(result), stream)

def snap_term(stream, PatternDict):
    """term:  primary
              primary term 
    """
    __debug_entry("term", stream)    

    # -- primary
    result = snap_primary(stream, PatternDict) 
    __debug_print("##primary(in term):", result)
    if result is None: return __debug_exit(None, stream)
    position_1 = stream.tell()

    # -- optional 'term' 
    result_2 = snap_term(stream, PatternDict) 
    __debug_print("##term(in term):",  result_2)
    if result_2 is None: 
        stream.seek(position_1)
        return __debug_exit(result, stream)
    
    result = sequentialize.do([result, result_2], 
                              MountToFirstStateMachineF=True, 
                              CloneRemainingStateMachinesF=False)    

    return __debug_exit(result, stream)
        
def snap_primary(stream, PatternDict):
    """primary:  " non_double_quote *  "              = character string
                 [ non_rect_bracket_close ]           = set of characters
                 { identifier }                       = pattern replacement
                 ( expression )
                 non_control_character+               = lonely characters
                 primary repetition_cmd
    """
    global SPECIAL_TERMINATOR 

    __debug_entry("primary", stream)    
    x = stream.read(1)
    if   x == "": return __debug_exit(None, stream)

    # -- 'primary' primary
    if   x == "\"": result = snap_character_string.do(stream)
    elif x == "[":  
        stream.seek(-1, 1); 
        result = snap_character_set_expression(stream, PatternDict)
    elif x == "{":  result = snap_replacement(stream, PatternDict)
    elif x == ".":  result = create_ALL_BUT_NEWLINE_state_machine(stream)
    elif x == "(":  result = snap_bracketed_expression(stream, PatternDict)

    elif x.isspace():
        # a lonestanding space ends the regular expression
        stream.seek(-1, 1)
        return __debug_exit(None, stream)

    elif x in ["*", "+", "?"]:
        raise RegularExpressionException("lonely operator '%s' without expression proceeding." % x) 

    elif x == "\\":
        result = snap_command(stream, PatternDict)
        if result is None:
            stream.seek(-1, 1)
            trigger_set = snap_property_set(stream)
            if trigger_set is None:
                # snap the '\'
                stream.read(1)
                char_code = snap_backslashed_character.do(stream)
                if char_code is None:
                    raise RegularExpressionException("Backslash followed by unrecognized character code.")
                trigger_set = char_code
            result = DFA()
            result.add_transition(result.init_state_index, trigger_set, AcceptanceF=True)

    elif x not in CONTROL_CHARACTERS and x != SPECIAL_TERMINATOR:
        # NOTE: The '\' is not inside the control characters---for a reason.
        #       It is used to define for example character codes using '\x' etc.
        stream.seek(-1, 1)
        result = snap_non_control_character(stream, PatternDict)

    else:
        # NOTE: This includes the '$' sign which means 'end of line'
        #       because the '$' sign is in CONTROL_CHARACTERS, but is not checked
        #       against. Thus, it it good to leave here on '$' because the
        #       '$' sign is handled on the very top level.
        # this is not a valid primary
        stream.seek(-1, 1)
        return __debug_exit(None, stream)

    # -- optional repetition command? 
    result_repeated = __snap_repetition_range(result, stream) 
    if result_repeated is not None: result = result_repeated

    return __debug_exit(result, stream)

def snap_case_folded_pattern(sh, PatternDict, NumberSetF=False):
    """Parse a case fold expression of the form \C(..){ R } or \C{ R }.
       Assume that '\C' has been snapped already from the stream.

       See function ucs_case_fold_parser.get_fold_set() for details
       about case folding.
    """
    def __add_intermediate_states(sm, character_list, start_state_idx, target_state_idx):
        next_idx = start_state_idx
        for letter in character_list[:-1]:
            next_idx = sm.add_transition(next_idx, letter)
        sm.add_transition(next_idx, character_list[-1], target_state_idx)

    def __add_case_fold(sm, Flags, trigger_set, start_state_idx, target_state_idx):
        for interval in trigger_set.get_intervals(PromiseToTreatWellF=True):
            for i in range(interval.begin, interval.end):
                fold = ucs_case_fold.get_fold_set(i, Flags)
                for x in fold:
                    if type(x) == list:
                        __add_intermediate_states(sm, x, start_state_idx, target_state_idx)
                    else:
                        trigger_set.add_interval(Interval(x, x+1))


    pos = sh.tell()
    skip_whitespace(sh)
    # -- parse the optional options in '(' ')' brackets
    if NumberSetF: default_flag_txt = "s"
    else:          default_flag_txt = "sm"

    flag_txt = optional_flags(sh, "case fold",
                              default_flag_txt,
                              { "s": "simple case fold",
                                "m": "multi character sequence case fold",
                                "t": "special turkish case fold rules", },
                              [])

    if NumberSetF and "m" in flag_txt:
        sh.seek(pos)
        error.log("Option 'm' not permitted as case fold option in set expression.\n" + \
                  "Set expressions cannot absorb multi character sequences.", sh)

    skip_whitespace(sh)

    result = snap_curly_bracketed_expression(sh, PatternDict, "case fold operator", "C")[0]

    if NumberSetF:
        trigger_set = result.get_number_set()
        if trigger_set is None or trigger_set.is_empty():
            error.log("Expression in case fold does not result in character set.\n" + 
                      "The content in '\\C{content}' may start with '[' or '[:'.", sh)

        # -- perform the case fold for Sets!
        for interval in trigger_set.get_intervals(PromiseToTreatWellF=True):
            for i in range(interval.begin, interval.end):
                fold = ucs_case_fold.get_fold_set(i, flag_txt)
                for x in fold:
                    assert type(x) != list
                    trigger_set.add_interval(Interval(x, x+1))

        result = trigger_set

    else:
        # -- perform the case fold for DFAs!
        for state_idx, state in result.states.items():
            for target_state_idx, trigger_set in state.target_map.get_map().items():
                __add_case_fold(result, flag_txt, trigger_set, state_idx, target_state_idx)

    return result

def snap_command(stream, PatternDict):
    global CommandDB

    for command_str, snap_function in CommandDB:
        if check(stream, command_str):
            return snap_function(stream, PatternDict)

    return None
    
def snap_non_control_character(stream, PatternDict):
    __debug_entry("non-control characters", stream)

    # (*) read first character
    char_code = utf8.__read_one_utf8_code_from_stream(stream)
    if char_code is None:
        error.log("Character could not be interpreted as UTF8 code or End of File reached prematurely.", 
                  stream)
    result = DFA()
    result.add_transition(result.init_state_index, char_code, AcceptanceF=True)
    return __debug_exit(result, stream)
    
def __snap_repetition_range(the_state_machine, stream):    
    """Snaps a string that represents a repetition range. The following 
       syntaxes are supported:
           '?'      one or none repetition
           '+'      one or arbitrary repetition
           '*'      arbitrary repetition (even zero)
           '{n}'    exactly 'n' repetitions
           '{m,n}'  from 'm' to 'n' repetitions
           '{n,}'   arbitrary, but at least 'n' repetitions
    """       
    assert the_state_machine.__class__.__name__ == "DFA", \
           "received object of type '%s'" % the_state_machine.__class__.__name__ + "\n" + \
           repr(the_state_machine)

    position_0 = stream.tell()
    x = stream.read(1)
    if   x == "+": result = repeat.do(the_state_machine, 1)
    elif x == "*": result = repeat.do(the_state_machine)
    elif x == "?": result = repeat.do(the_state_machine, 0, 1)
    elif x == "{":
        repetition_range_str = __snap_until(stream, "}")
        if len(repetition_range_str) and not repetition_range_str[0].isdigit():
            # no repetition range, so everything remains as it is
            stream.seek(position_0)
            return the_state_machine
            
        try:
            if repetition_range_str.find(",") == -1:
                # no ',' thus "match exactly a certain number": 
                # e.g. {4} = match exactly four repetitions
                number = int(repetition_range_str)
                result = repeat.do(the_state_machine, number, number)
                return result
            # a range of numbers is given       
            fields = repetition_range_str.split(",")
            fields = map(lambda x: x.strip(), fields)

            number_1 = int(fields[0].strip())
            if fields[1] == "": number_2 = -1                      # e.g. {2,}
            else:               number_2 = int(fields[1].strip())  # e.g. {2,5}  
            # produce repeated state machine 
            result = repeat.do(the_state_machine, number_1, number_2)
            return result
        except:
            raise RegularExpressionException("error while parsing repetition range expression '%s'" \
                                             % repetition_range_str)
    else:
        # no repetition range, so everything remains as it is
        stream.seek(position_0)
        return the_state_machine
    
    return result

def create_ALL_BUT_NEWLINE_state_machine(stream):
    global Setup
    result = DFA()
    # NOTE: Buffer control characters are supposed to be filtered out by the code
    #       generator.
    trigger_set = NumberSet(Interval(ord("\n"))).get_complement(Setup.buffer_encoding.source_set)
    if trigger_set.is_empty():
        error.log("The set of admissible characters contains only newline.\n"
                  "The '.' for 'all but newline' is an empty set.",
                  SourceRef.from_FileHandle(stream))

    result.add_transition(result.init_state_index, trigger_set, AcceptanceF=True) 
    return result
    
def snap_bracketed_expression(stream, PatternDict):
    position = stream.tell()
    result = snap_expression(stream, PatternDict)
    if not check(stream, ")"): 
        stream.seek(position)
        remainder_txt = stream.readline().replace("\n", "").replace("\r", "")
        raise RegularExpressionException("Missing closing ')' after expression; found '%s'.\n" % remainder_txt \
                                         + "Note, that patterns end with the first non-quoted whitespace.\n" \
                                         + "Also, closing brackets in quotes do not close a syntax block.")

    if result is None:
        length = stream.tell() - position
        stream.seek(position)
        raise RegularExpressionException("expression in brackets has invalid syntax '%s'" % \
                                         stream.read(length))
    return result

def snap_nothing(stream, PatternDict):
    return DFA.Nothing()

def snap_any(stream, PatternDict):
    return DFA.Any()

def snap_universal(stream, PatternDict):
    return DFA.Universal()

def snap_empty(stream, PatternDict):
    return DFA.Empty()

def snap_reverse(stream, PatternDict):
    result = snap_curly_bracketed_expression(stream, PatternDict, "reverse operator", "R")[0]
    return reverse.do(result, EnsureDFA_f=False)

def snap_sanitizer(stream, PatternDict):
    result = snap_curly_bracketed_expression(stream, PatternDict, "sanatizer operator", "A")[0]
    return sanitizer.do(result)

def snap_head(stream, PatternDict):
    result = snap_curly_bracketed_expression(stream, PatternDict, "\\Head", "A")[0]
    return stem_and_branches.head(result)

def snap_tails(stream, PatternDict):
    result = snap_curly_bracketed_expression(stream, PatternDict, "\\Head", "A")[0]
    return stem_and_branches.tails(result)

def snap_anti_pattern(stream, PatternDict):
    result = snap_curly_bracketed_expression(stream, PatternDict, "anti-pattern operator", "A")[0]
    return sanitizer.do(complement.do(result))

def snap_complement(stream, PatternDict):
    pattern_list = snap_curly_bracketed_expression(stream, PatternDict, "complement operator", "Co")
    if len(pattern_list) == 1: tmp = pattern_list[0]
    else:                      tmp = union.do(pattern_list)
    return complement.do(tmp)

def snap_union(stream, PatternDict):
    pattern_list = snap_curly_bracketed_expression(stream, PatternDict, "union operator", "Union", 
                                                   MinN=2, MaxN=INTEGER_MAX)
    return union.do(pattern_list)

def snap_intersection(stream, PatternDict):
    pattern_list = snap_curly_bracketed_expression(stream, PatternDict, "intersection operator", "Intersection", 
                                                   MinN=2, MaxN=INTEGER_MAX)
    return intersection.do(pattern_list)

def snap_two_or_union_of_more_state_machines(Func, stream, PatternDict, Name, Cmd):
    sm_list = snap_curly_bracketed_expression(stream, PatternDict, Name, Cmd, 
                                              MinN=2, MaxN=INTEGER_MAX)
    sm0 = sm_list[0]
    if len(sm_list) == 2: sm1 = sm_list[1]
    else:                 sm1 = union.do(sm_list[1:])

    return Func(sm0, sm1)

def snap_cut_begin(stream, PatternDict):
    return snap_two_or_union_of_more_state_machines(cut.cut_begin,
                                                    stream, PatternDict,
                                                    "cut-begin", "CutBegin")

def snap_cut_end(stream, PatternDict):
    return snap_two_or_union_of_more_state_machines(cut.cut_end,
                                                    stream, PatternDict,
                                                    "cut-end", "CutEnd")

def snap_leave_begin(stream, PatternDict):
    return snap_two_or_union_of_more_state_machines(cut.leave_begin,
                                                    stream, PatternDict,
                                                    "leave-begin", "LeaveBegin")

def snap_leave_end(stream, PatternDict):
    return snap_two_or_union_of_more_state_machines(cut.leave_end,
                                                    stream, PatternDict,
                                                    "leave-end", "LeaveEnd")

def snap_begin(stream, PatternDict):
    return snap_two_or_union_of_more_state_machines(derived.is_begin, 
                                                    stream, PatternDict, 
                                                    "begin operator", "Begin") 

def snap_end(stream, PatternDict):
    return snap_two_or_union_of_more_state_machines(derived.is_end, 
                                                    stream, PatternDict, 
                                                    "end operator", "End") 

def snap_in(stream, PatternDict):
    return snap_two_or_union_of_more_state_machines(derived.is_in, 
                                                    stream, PatternDict, 
                                                    "in operator", "In") 

def snap_not_begin(stream, PatternDict):
    return snap_two_or_union_of_more_state_machines(derived.not_begin, 
                                                    stream, PatternDict, 
                                                    "not-begin operator", "NotBegin") 

def snap_not_end(stream, PatternDict):
    return snap_two_or_union_of_more_state_machines(derived.not_end, 
                                                    stream, PatternDict, 
                                                    "not-end operator", "NotEnd") 

def snap_not_in(stream, PatternDict):
    return snap_two_or_union_of_more_state_machines(derived.not_in, 
                                                    stream, PatternDict, 
                                                    "not-in operator", "NotIn") 

def snap_difference(stream, PatternDict):
    sm_list = snap_curly_bracketed_expression(stream, PatternDict, "difference operator", "Intersection",
                                              MinN=2, MaxN=2)
    return difference.do(sm_list[0], sm_list[1])

def snap_symmetric_difference(stream, PatternDict):
    sm_list = snap_curly_bracketed_expression(stream, PatternDict, "intersection operator", "Intersection", 
                                              MinN=2, MaxN=2)
    return symmetric_difference.do(sm_list)

def snap_curly_bracketed_expression(stream, PatternDict, Name, TriggerChar, MinN=1, MaxN=1):
    """Snaps a list of RE's in '{' and '}'. The separator between the patterns 
    is whitespace. 'MinN' and 'MaxN' determine the number of expected patterns.
    Set 'MaxN=INTEGER_MAX' for an arbitrary number of patterns.

    RETURNS: result = list of patterns, if MinN <= len(result) <= MaxN 
             else, the function sys.exit()-s.
    """
    assert MinN <= MaxN
    assert MinN > 0

    skip_whitespace(stream)

    # Read over the trigger character 
    if not check(stream, "{"):
        error.log("Missing opening '{' after %s %s." % (Name, TriggerChar), stream)

    result = []
    while 1 + 1 == 2:
        pattern = snap_expression(stream, PatternDict) 
        if pattern is not None:
            result.append(pattern)

        if check(stream, "}"):
            break
        elif check_whitespace(stream):
            continue
        elif check(stream, "/") or check(stream, "$"):
            error.log("Pre- or post contexts are not allowed in %s \\%s{...} expressions." % (Name, TriggerChar), stream)
        else:
            error.log("Missing closing '}' %s in \\%s{...}." % (Name, TriggerChar), stream)

    if MinN != MaxN:
        if len(result) < MinN:
            error.log("At minimum %i pattern%s required between '{' and '}'" \
                      % (MinN, "" if MinN == 1 else "s"), stream)
        if len(result) > MaxN:
            error.log("At maximum %i pattern%s required between '{' and '}'" \
                      % (MaxN, "" if MaxN == 1 else "s"), stream)
    else:
        if len(result) != MinN:
            error.log("Exactly %i pattern%s required between '{' and '}'" \
                      % (MinN, "" if MinN == 1 else "s"), stream)

    def ensure_dfa(sm):
        if not sm.is_DFA_compliant(): return nfa_to_dfa.do(sm)
        else:                         return sm

    return [ensure_dfa(sm) for sm in result]

# MUST BE SORTED WITH LONGEST PATTERN FIRST!
CommandDB = sorted([
   # Note, that there are backlashed elements that may appear also in strings.
   # \a, \X, ... those are not treated here. They are treated in 
   # 'snap_backslashed_character()'.
   ("C",            snap_case_folded_pattern),   # OK
   ("R",            snap_reverse),               # OK
   #
   ("Intersection", snap_intersection),          # OK
   ("Union",        snap_union),                 # OK
   ("Not",          snap_complement),            # OK
   ("Diff",         snap_difference),            # OK
   ("SymDiff",      snap_symmetric_difference),  # OK
   ("Universal",    snap_universal),             #
   ("Empty",        snap_empty),                 # 
   #
   ("Nothing",      snap_nothing),               # OK
   ("Any",          snap_any),                   # OK
   ("Sanitize",     snap_sanitizer),             # 
   ("A",            snap_anti_pattern),          # OK
   #
   ("Head",         snap_head),                  # OK
   ("Tails",        snap_tails),                 # OK
   #
   ("Begin",        snap_begin),                 # OK
   ("End",          snap_end),                   # OK
   ("In",           snap_in),                    # OK
   ("NotBegin",     snap_not_begin),             # OK
   ("NotEnd",       snap_not_end),               # OK
   ("NotIn",        snap_not_in),                # OK
   #
   ("CutBegin",     snap_cut_begin),             # OK
   ("CutEnd",       snap_cut_end),               # OK
   ("LeaveBegin",   snap_leave_begin),           # OK
   ("LeaveEnd",     snap_leave_end),             # OK

   # Sort by length (longest first), then sort by name
], key=lambda x: (-len(x[0]), x[0]))

special_character_set_db = {
    # The closing ']' is to trigger the end of the traditional character set
    "alnum":  "a-zA-Z0-9]",
    "alpha":  "a-zA-Z]",
    "blank":  " \\t]",
    "cntrl":  "\\x00-\\x1F\\x7F]", 
    "digit":  "0-9]",
    "graph":  "\\x21-\\x7E]",
    "lower":  "a-z]",
    "print":  "\\x20-\\x7E]", 
    "punct":  "!\"#$%&'()*+,-./:;?@[\\]_`{|}~\\\\]",
    "space":  " \\t\\r\\n]",
    "upper":  "A-Z]",
    "xdigit": "a-fA-F0-9]",
}

def snap_character_set_expression(stream, PatternDict):
    # GRAMMAR:
    #
    # set_expression: 
    #                 [: set_term :]
    #                 traditional character set
    #                 \P '{' propperty string '}'
    #                 '{' identifier '}'
    #
    # set_term:
    #                 "alnum" 
    #                 "alpha" 
    #                 "blank" 
    #                 "cntrl" 
    #                 "digit" 
    #                 "graph" 
    #                 "lower" 
    #                 "print" 
    #                 "punct" 
    #                 "space" 
    #                 "upper" 
    #                 "xdigit"
    #                 "union"        '(' set_term [ ',' set_term ]+ ')'
    #                 "intersection" '(' set_term [ ',' set_term ]+ ')'
    #                 "difference"   '(' set_term [ ',' set_term ]+ ')'
    #                 "complement"   '(' set_term ')'
    #                 set_expression
    # 
    trigger_set = snap_set_expression(stream, PatternDict)

    if trigger_set is None: 
        error.log("Regular Expression: snap_character_set_expression called for something\n" + \
                  "that does not start with '[:', '[' or '\\P'", stream)
    elif trigger_set.is_empty():
        error.warning("Regular Expression: Character set expression results in empty set.", stream)

    # Create state machine that triggers with the trigger set to SUCCESS
    # NOTE: The default for the ELSE transition is FAIL.
    sm = DFA()
    sm.add_transition(sm.init_state_index, trigger_set, AcceptanceF=True)

    return __debug_exit(sm, stream)

def snap_set_expression(stream, PatternDict):
    assert     stream.__class__.__name__ == "StringIO" \
            or stream.__class__.__name__ == "file"

    __debug_entry("set_expression", stream)

    result = snap_property_set(stream)
    if result is not None: return result

    x = stream.read(2)
    if   x == "\\C":
        return snap_case_folded_pattern(stream, PatternDict, NumberSetF=True)

    elif x == "[:":
        result = snap_set_term(stream, PatternDict)
        skip_whitespace(stream)
        x = stream.read(2)
        if x != ":]":
            raise RegularExpressionException("Missing closing ':]' for character set expression.\n" + \
                                             "found: '%s'" % x)
    elif x[0] == "[":
        stream.seek(-1, 1)
        result = traditional_character_set.do(stream)   

    elif x[0] == "{":
        stream.seek(-1, 1)
        result = snap_replacement(stream, PatternDict, StateMachineF=False)   

    else:
        result = None

    return __debug_exit(result, stream)

def snap_property_set(stream):
    position = stream.tell()
    x = stream.read(2)
    if   x == "\\P": 
        stream.seek(position)
        return property.do(stream)
    elif x == "\\N": 
        stream.seek(position)
        return property.do_shortcut(stream, "N", "na") # UCS Property: Name
    elif x == "\\G": 
        stream.seek(position)
        return property.do_shortcut(stream, "G", "gc") # UCS Property: General_Category
    elif x == "\\E": 
        skip_whitespace(stream)
        if check(stream, "{") == False:
            error.log("Missing '{' after '\\E'.", stream)
        encoding_name = __snap_until(stream, "}").strip()
        result = codec_db.get_supported_unicode_character_set(encoding_name)
        if result is None:
            error.log("Error occured at this place.", stream)
        return result
    else:
        stream.seek(position)
        return None

def snap_set_term(stream, PatternDict):
    global special_character_set_db

    __debug_entry("set_term", stream)    

    operation_list     = [ 
        "union", "intersection", "difference", "complement",
        "inverse"  # => Detect deprecated "inverse" instead of "complement".
    ]
    character_set_list = special_character_set_db.keys()

    skip_whitespace(stream)
    position = stream.tell()

    # if there is no following '(', then enter the 'snap_expression' block below
    word = read_identifier(stream)

    if word in operation_list: 
        set_list = snap_set_list(stream, word, PatternDict)
        # if an error occurs during set_list parsing, an exception is thrown about syntax error

        L      = len(set_list)
        result = set_list[0]

        if word == "inverse":
            error.log("Usage of 'inverse' instead of 'complement'", stream)

        elif word == "complement":
            # The inverse of multiple sets, is to be the inverse of the union of these sets.
            if L > 1:
                for character_set in set_list[1:]:
                    result.unite_with(character_set)
            return __debug_exit(result.get_complement(Setup.buffer_encoding.source_set), stream)

        elif L < 2:
            error.log("Regular Expression: A %s operation needs at least\n" % word + \
                      "two sets to operate on them.",
                      stream)
            
        elif   word == "union":
            for sub_set in set_list[1:]:
                result.unite_with(sub_set)
        elif word == "intersection":
            for sub_set in set_list[1:]:
                result.intersect_with(sub_set)
        elif word == "difference":
            for sub_set in set_list[1:]:
                result.subtract(sub_set)

    elif word in character_set_list:
        reg_expr = special_character_set_db[word]
        result   = traditional_character_set.do_string(reg_expr)

    elif word:
        error.verify_word_in_list(word, character_set_list + operation_list, 
                                  "Unknown keyword '%s'." % word, stream)
    else:
        stream.seek(position)
        result = snap_set_expression(stream, PatternDict)

    return __debug_exit(result, stream)

def snap_set_list(stream, set_operation_name, PatternDict):
    __debug_entry("set_list", stream)

    skip_whitespace(stream)
    if stream.read(1) != "(": 
        error.log("Missing opening bracket '%s' operation." % set_operation_name,
                  stream)

    set_list = []
    while 1 + 1 == 2:
        skip_whitespace(stream)
        result = snap_set_term(stream, PatternDict)
        if result is None: 
            error.log("Missing set expression list after %s operation." % set_operation_name,
                      stream)
        set_list.append(result)
        skip_whitespace(stream)
        tmp = stream.read(1)
        if tmp != ",": 
            if tmp != ")":
                stream.seek(-1, 1)
                error.log("Missing closing ')' or argument seperator ',' in %s operation." % set_operation_name,
                          stream)
            return __debug_exit(set_list, stream)


   

def __error_check(ConditionLine, ConditionStream, Sm, stream, Name):
    condition_n = 0
    if   ConditionLine:   condition_n += 1
    elif ConditionStream: condition_n += 1
    elif Sm is not None:  condition_n += 1

    if condition_n > 1:
        error.log("More than one %s." % Name, stream)
