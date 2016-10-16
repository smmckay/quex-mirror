
from   quex.input.setup                   import NotificationDB
import quex.input.regular_expression.core as     regular_expression
import quex.input.files.mode_option       as     mode_option
import quex.input.files.consistency_check as     consistency_check
import quex.input.files.code_fragment     as     code_fragment
from   quex.input.files.specifier.mode    import Mode_PrepPrep     
from   quex.input.code.core               import CodeUser
from   quex.input.code.base               import SourceRef
                                          
import quex.engine.misc.error             as     error
from   quex.engine.misc.file_in           import EndOfStreamException, \
                                                 check, \
                                                 check_or_die, \
                                                 read_identifier, \
                                                 read_until_letter, \
                                                 read_until_whitespace, \
                                                 skip_whitespace
import quex.blackboard as blackboard
from   quex.blackboard import setup as Setup, \
                              standard_incidence_db

def parse(fh):
    """This function parses a mode description and enters it into the 
    'blackboard.mode_prep_prep_db'. Modes are represented by Mode_PrepPrep
    objects.
    """

    # NOTE: Catching of EOF happens in caller: parse_section(...)
    skip_whitespace(fh)
    mode_name = read_identifier(fh, OnMissingStr="Missing identifier at beginning of mode definition.")

    # NOTE: constructor does register this mode in the mode_db
    new_mode  = Mode_PrepPrep(mode_name, SourceRef.from_FileHandle(fh))

    # (*) inherited modes / option_db
    skip_whitespace(fh)
    dummy = fh.read(1)
    if dummy not in [":", "{"]:
        error.log("missing ':' or '{' after mode '%s'" % mode_name, fh)

    if dummy == ":":
        __parse_option_list(new_mode, fh)

    # (*) read in pattern-action pairs and events
    while __parse_element(new_mode, fh): 
        pass

def finalize_modes(ModePrepPrepDb):
    mode_prep_db = __finalize_modes_prep(ModePrepPrepDb)

    return dict((name, mode_prep.finalize(mode_prep_db)) 
                for name, mode_prep in mode_prep_db.iteritems() 
                if mode_prep.implemented_f())

def __finalize_modes_prep(ModePrepPrepDb):
    assert all(isinstance(x, Mode_PrepPrep) for x in ModePrepPrepDb.itervalues())

    # (BEFORE) Parsing --> Mode_PrepPrep

    # (*) Mode_PrepPrep --> Mode_Prep
    #     * collection of options_db from base modes
    #     * collection of incidence_db from base modes
    #     * finalize all mentioned patterns in a mode
    #       (patterns are not yet collected from base modes)
    mode_prep_db = dict(
        (mode_prep_prep.name, mode_prep_prep.finalize(ModePrepPrepDb))
        for mode_prep_prep in ModePrepPrepDb.itervalues()
    )

    # (*) Mode_Prep: pre finalize
    #     All patterns of all modes have been finalized
    #     => collect all patterns and loopers from base modes 
    #     => generate pattern list / terminal configuration
    for mode_prep in mode_prep_db.itervalues():
        mode_prep.pre_finalize(mode_prep_db)

    consistency_check.do_pre(mode_prep_db.values())

    if not Setup.token_class_only_f:
        __determine_initial_mode(mode_prep_db)

    # (*) Mode_Prep --> Mode
    #     Pattern lists are determined for each mode
    #     => Each mode is determined whether mode is implemented or not.
    #     => Determine the concerned mode names for mode handlers
    consistency_check.do(mode_prep_db.values())

    return mode_prep_db

def __determine_initial_mode(ModePrepDb):
    if not blackboard.initial_mode.sr.is_void():
        return

    # Choose an applicable mode as start mode
    first_candidate = None
    for name, mode in ModePrepDb.iteritems():
        if not mode.implemented_f(): 
            continue
        elif first_candidate is not None:
            error.log("No initial mode defined via 'start' while more than one applicable mode exists.\n" + \
                      "Use for example 'start = %s;' in the quex source file to define an initial mode." \
                      % first_candidate.name)
        else:
            first_candidate = mode

    if first_candidate is None:
        error.log("No mode that can be implemented--all modes <inheritable: only>.")
    else:
        blackboard.initial_mode = CodeUser(first_candidate.name, SourceReference=first_candidate.sr)

def __parse_option_list(new_mode, fh):
    position = fh.tell()
    try:  
        # ':' => inherited modes/option_db follow
        skip_whitespace(fh)

        __parse_base_mode_list(fh, new_mode)
        
        while mode_option.parse(fh, new_mode):
            pass

    except EndOfStreamException:
        fh.seek(position)
        error.error_eof("mode '%s'." % new_mode.name, fh)

def __parse_base_mode_list(fh, new_mode):
    new_mode.direct_base_mode_name_list = []
    trailing_comma_f    = False
    while 1 + 1 == 2:
        if   check(fh, "{"): fh.seek(-1, 1); break
        elif check(fh, "<"): fh.seek(-1, 1); break

        skip_whitespace(fh)
        identifier = read_identifier(fh)
        if identifier == "": break

        new_mode.direct_base_mode_name_list.append(identifier)
        trailing_comma_f = False
        if not check(fh, ","): break
        trailing_comma_f = True


    if trailing_comma_f:
        error.warning("Trailing ',' after base mode '%s'." % new_mode.direct_base_mode_name_list[-1], fh) 
        
    elif len(new_mode.direct_base_mode_name_list) != 0:
        # This check is a 'service' -- for those who follow the old convention
        pos = fh.tell()
        skip_whitespace(fh)
        dummy_identifier = read_identifier(fh)
        if dummy_identifier != "":
            error.log("Missing separating ',' between base modes '%s' and '%s'.\n" \
                      % (new_mode.direct_base_mode_name_list[-1], dummy_identifier) + \
                      "(The comma separator is mandatory since quex 0.53.1)", fh)
        fh.seek(pos)

def __parse_element(new_mode, fh):
    """Returns: False, if a closing '}' has been found.
                True, else.
    """
    position = fh.tell()
    try:
        description = "pattern or event handler" 

        skip_whitespace(fh)
        # NOTE: Do not use 'read_word' since we need to continue directly after
        #       whitespace, if a regular expression is to be parsed.
        position = fh.tell()

        word = read_until_whitespace(fh)
        if word == "}": return False

        # -- check for 'on_entry', 'on_exit', ...
        if __parse_event(new_mode, fh, word): return True

        fh.seek(position)
        description = "start of mode element: regular expression"
        pattern     = regular_expression.parse(fh)
        pattern.set_source_reference(SourceRef.from_FileHandle(fh, new_mode.name))

        position    = fh.tell()
        description = "start of mode element: code fragment for '%s'" % pattern.pattern_string()

        __parse_action(new_mode, fh, pattern.pattern_string(), pattern)

    except EndOfStreamException:
        fh.seek(position)
        error.error_eof(description, fh)

    return True

def __parse_action(new_mode, fh, pattern_str, pattern):

    position = fh.tell()
    try:
        skip_whitespace(fh)
        position = fh.tell()
            
        code = code_fragment.parse(fh, "regular expression", ErrorOnFailureF=False) 
        if code is not None:
            assert isinstance(code, CodeUser), "Found: %s" % code.__class__
            new_mode.add_pattern_action_pair(pattern, code, fh)
            return

        fh.seek(position)
        word = read_until_letter(fh, [";"])
        if word == "PRIORITY-MARK":
            # This mark 'lowers' the priority of a pattern to the priority of the current
            # pattern index (important for inherited patterns, that have higher precedence).
            # The parser already constructed a state machine for the pattern that is to
            # be assigned a new priority. Since, this machine is not used, let us just
            # use its id.
            fh.seek(-1, 1)
            check_or_die(fh, ";", ". Since quex version 0.33.5 this is required.")
            new_mode.add_match_priority(pattern, fh)

        elif word == "DELETION":
            # This mark deletes any pattern that was inherited with the same 'name'
            fh.seek(-1, 1)
            check_or_die(fh, ";", ". Since quex version 0.33.5 this is required.")
            new_mode.add_match_deletion(pattern, fh)
            
        else:
            error.log("Missing token '{', 'PRIORITY-MARK', 'DELETION', or '=>' after '%s'.\n" % pattern_str + \
                      "found: '%s'. Note, that since quex version 0.33.5 it is required to add a ';'\n" % word + \
                      "to the commands PRIORITY-MARK and DELETION.", fh)


    except EndOfStreamException:
        fh.seek(position)
        error.error_eof("pattern action", fh)

def __parse_event(new_mode, fh, word):
    pos = fh.tell()

    # Allow '<<EOF>>' and '<<FAIL>>' out of respect for classical tools like 'lex'
    if   word == "<<EOF>>":                  word = "on_end_of_stream"
    elif word == "<<FAIL>>":                 word = "on_failure"
    elif word in blackboard.all_section_title_list:
        error.log("Pattern '%s' is a quex section title. Has the closing '}' of mode %s \n" % (word, new_mode.name) \
                  + "been forgotten? Else use quotes, i.e. \"%s\"." % word, fh)
    elif len(word) < 3 or word[:3] != "on_": return False

    comment = "Unknown event handler '%s'. \n" % word + \
              "Note, that any pattern starting with 'on_' is considered an event handler.\n" + \
              "use double quotes to bracket patterns that start with 'on_'."

    __general_validate(fh, new_mode, word, pos)
    error.verify_word_in_list(word, standard_incidence_db.keys(), comment, 
                              fh)
    __validate_required_token_policy_queue(word, fh, pos)

    continue_f = True
    if word == "on_end_of_stream" or word == "on_failure":
        # -- When a termination token is sent, no other token shall follow. 
        #    => Enforce return from the analyzer! Do not allow CONTINUE!
        # -- When an 'on_failure' is received allow immediate action of the
        #    receiver => Do not allow CONTINUE!
        continue_f = False

    new_mode.incidence_db[word] = \
            code_fragment.parse(fh, "%s::%s event handler" % (new_mode.name, word),
                                ContinueF=continue_f)

    return True

def __general_validate(fh, Mode, Name, pos):
    if Name == "on_indentation":
        fh.seek(pos)
        error.log("Definition of 'on_indentation' is no longer supported since version 0.51.1.\n"
                  "Please, use 'on_indent' for the event of an opening indentation, 'on_dedent'\n"
                  "for closing indentation, and 'on_nodent' for no change in indentation.\n"
                  "If you want to match 'on_indentation' as a string, use quotes.", fh) 


    def error_dedent_and_ndedent(code, A, B):
        error.log("Indentation event handler '%s' cannot be defined, because\n" % A,
                  fh, DontExitF=True)
        error.log("the alternative '%s' has already been defined." % B,
                  code.sr)

    if Name == "on_dedent" and Mode.incidence_db.has_key("on_n_dedent"):
        fh.seek(pos)
        code = Mode.incidence_db["on_n_dedent"]
        if not code.is_whitespace():
            error_dedent_and_ndedent(code, "on_dedent", "on_n_dedent")
                      
    if Name == "on_n_dedent" and Mode.incidence_db.has_key("on_dedent"):
        fh.seek(pos)
        code = Mode.incidence_db["on_dedent"]
        if not code.is_whitespace():
            error_dedent_and_ndedent(code, "on_n_dedent", "on_dedent")
                      
def __validate_required_token_policy_queue(Name, fh, pos):
    """Some handlers are better only used with token policy 'queue'."""

    if Name not in ["on_entry", "on_exit", 
                    "on_indent", "on_n_dedent", "on_dedent", "on_nodent", 
                    "on_indentation_bad", "on_indentation_error", 
                    "on_indentation"]: 
        return
    if Setup.token_policy == "queue":
        return

    pos_before = fh.tell()
    fh.seek(pos)
    error.warning("Using '%s' event handler, while the token queue is disabled.\n" % Name + \
                  "Use '--token-policy queue', so then tokens can be sent safer\n" + \
                  "from inside this event handler.", fh,
                  SuppressCode=NotificationDB.warning_on_no_token_queue) 
    fh.seek(pos_before)

