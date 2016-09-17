from   quex.input.files.specifier.mode import Mode_Prep
from   quex.input.setup                import NotificationDB
import quex.engine.misc.error          as     error
from   quex.engine.misc.tools          import typed
import quex.blackboard                 as     blackboard
from   quex.blackboard                 import setup as Setup
from   quex.blackboard                 import E_IncidenceIDs

@typed(ModePrepList=[Mode_Prep])
def do(ModePrepList):
    """Consistency check of mode database

       -- Are there applicable modes?
       -- Start mode:
          -- specified (more than one applicable mode req. explicit specification)?
          -- is defined as mode?
          -- start mode is not inheritable only?
       -- Entry/Exit transitions are allows?
    """
    if Setup.token_class_only_f:
        if ModePrepList:
            error.log("Modes found in input files. However, only a token class is generated.", 
                      DontExitF=True)
        return

    if not ModePrepList:
        error.log("No single mode defined - bailing out", Prefix="consistency check")

    mode_name_list             = sorted([mode.name for mode in ModePrepList]) 
    # Applicable modes can only be determined after possible addition of "inheritable: only"
    implemented_mode_name_list = sorted([mode.name for mode in ModePrepList 
                                         if mode.implemented_f()]) 

    for mode in ModePrepList:
        __empty_mode_detection(mode, implemented_mode_name_list)

    if len(implemented_mode_name_list) == 0:
        error.log("There is no mode that can be implemented---all existing modes are 'inheritable only'.\n" + \
                  "modes are = " + repr(mode_name_list)[1:-1],
                  Prefix="consistency check")

    # (*) If a conversion or a codec engine is specified, then the 
    #     'on_bad_lexatom' handler must be specified in every mode.
    if False and (Setup.buffer_codec.name != "unicode" or Setup.converter_f):
        for mode in ModePrepList:
            # Later ... 
            if False and E_IncidenceIDs.BAD_LEXATOM not in mode.incidence_db:
                error.warning("Missing 'on_bad_lexatom' handler in mode '%s' (or its base modes).\n" % mode.name + \
                              "This is dangerous while using a codec engine or a converter (iconv, icu, ...).\n" + \
                              "The feature is not yet supported, but the infrastructure is currently setup for it.",
                              mode.sr, 
                              SuppressCode=NotificationDB.warning_codec_error_with_non_unicode)

    # (*) Start mode specified?
    __start_mode(implemented_mode_name_list, mode_name_list)

    # (*) Entry/Exit Transitions
    for mode in ModePrepList:
        if not mode.implemented_f(): continue
        __entry_transitions(mode, ModePrepList, mode_name_list)
        __exit_transitions(mode, ModePrepList, mode_name_list)

    for mode in ModePrepList:
        # (*) [Optional] Warnings on Outrun
        if Setup.warning_on_outrun_f:
             mode.check_low_priority_outruns_high_priority_pattern()

        # (*) Special Patterns shall not match on same lexemes
        if NotificationDB.error_on_special_pattern_same not in Setup.suppressed_notification_list:
            mode.check_match_same(NotificationDB.error_on_special_pattern_same)

        # (*) Special Patterns (skip, indentation, etc.) 
        #     shall not be outrun by another pattern.
        if NotificationDB.error_on_special_pattern_outrun not in Setup.suppressed_notification_list:
            mode.check_special_incidence_outrun(NotificationDB.error_on_special_pattern_outrun)

        # (*) Special Patterns shall not have common matches with patterns
        #     of higher precedence.
        if NotificationDB.error_on_special_pattern_subset not in Setup.suppressed_notification_list:
            mode.check_higher_priority_matches_subset(NotificationDB.error_on_special_pattern_subset)

        # (*) Check for dominated patterns
        if NotificationDB.error_on_dominated_pattern not in Setup.suppressed_notification_list:
            mode.check_dominated_pattern(NotificationDB.error_on_dominated_pattern)

def __start_mode(implemented_mode_name_list, mode_name_list):
    """If more then one mode is defined, then that requires an explicit 
       definition 'start = mode'.
    """
    assert len(implemented_mode_name_list) != 0

    assert blackboard.initial_mode is not None

    start_mode = blackboard.initial_mode.get_pure_text()

    # Start mode present and applicable?
    error.verify_word_in_list(start_mode, mode_name_list,
                        "Start mode '%s' is not defined." % start_mode,
                        blackboard.initial_mode.sr)
    error.verify_word_in_list(start_mode, implemented_mode_name_list,
                        "Start mode '%s' is inheritable only and cannot be instantiated." % start_mode,
                        blackboard.initial_mode.sr)

def __access_mode(Mode, ModePrepList, OtherModeName, ModeNameList, EntryF):
    type_str = { True: "entry from", False: "exit to" }[EntryF]

    error.verify_word_in_list(OtherModeName, ModeNameList,
              "Mode '%s' permits the %s mode '%s'\nbut no such mode exists." % \
              (Mode.name, type_str, OtherModeName), Mode.sr)

    for mode in ModePrepList:
        if mode.name == OtherModeName: return mode
    # OtherModeName MUST be in ModePrepList, at this point in time.
    assert False

def __error_transition(Mode, OtherMode, EntryF):
    type_str  = { True: "entry",      False: "exit" }[EntryF]
    type0_str = { True: "entry from", False: "exit to" }[EntryF]
    type1_str = { True: "exit to",    False: "entry from" }[EntryF]

    error.log("Mode '%s' permits the %s mode '%s' but mode '%s' does not" % (Mode.name, type0_str, OtherMode.name, OtherMode.name),
              Mode.sr, DontExitF=True)
    error.log("permit the %s mode '%s' or any of its base modes." % (type1_str, Mode.name),
              OtherMode.sr, DontExitF=True)
    error.log("May be, use explicitly mode tag '<%s: ...>' for restriction." % type_str, 
              Mode.sr)

def __exit_transitions(mode, ModePrepList, mode_name_list):
    for exit_mode_name in mode.exit_mode_name_list:
        exit_mode = __access_mode(mode, ModePrepList, exit_mode_name, mode_name_list, EntryF=False)

        # Check if this mode or one of the base modes can enter
        for base_mode in mode.base_mode_sequence:
            if base_mode.name in exit_mode.entry_mode_name_list: break
        else:
            __error_transition(mode, exit_mode, EntryF=False)

def __entry_transitions(mode, ModePrepList, mode_name_list):
    for entry_mode_name in mode.entry_mode_name_list:
        entry_mode = __access_mode(mode, ModePrepList, entry_mode_name, mode_name_list, EntryF=True)

        # Check if this mode or one of the base modes can be reached
        for base_mode in mode.base_mode_sequence:
            if base_mode.name in entry_mode.exit_mode_name_list: break
        else:
            __error_transition(mode, entry_mode, EntryF=True)
           

def __empty_mode_detection(mode, implemented_mode_name_list):
    if   mode.implemented_f():                     return
    elif mode.name in  implemented_mode_name_list: return

    error.warning("Mode without pattern and event handlers needs to be 'inheritable only'.\n" + \
                  "<inheritable: only> has been set automatically.", mode.sr)
