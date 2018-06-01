import quex.output.analyzer.indentation_handler as     indentation_handler
from   quex.engine.misc.string_handling         import blue_print
from   quex.blackboard                          import setup as Setup, \
                                                       Lng, \
                                                       E_IncidenceIDs
from   operator import attrgetter

def do(ModeDb):
    LexerClassName   = Setup.analyzer_class_name
    DerivedClassName = Setup.analyzer_derived_class_name

    mode_setup_txt = __setup(ModeDb)

    # -- mode class member function definitions (on_entry, on_exit, has_base, ...)
    mode_class_member_functions_txt = write_member_functions(ModeDb.values())

    txt  = Lng.FRAME_IN_NAMESPACE_MAIN("".join([
        mode_setup_txt,
        mode_class_member_functions_txt,
    ]))

    return blue_print(txt, [
        ["$$LEXER_CLASS_NAME$$",         LexerClassName],
        ["$$LEXER_DERIVED_CLASS_NAME$$", DerivedClassName]
    ])

def write_member_functions(Modes):
    # -- get the implementation of mode class functions
    #    (on_entry, on_exit, on_indent, on_dedent, has_base, has_entry, has_exit, ...)
    txt  = [
        Lng.DEFINE_SELF("me"), 
        "#define LexemeNull  (&QUEX_NAME(LexemeNull))\n"
        "#define RETURN      return\n"
    ]
    txt.extend(
        get_implementation_of_mode_functions(mode, Modes)
        for mode in Modes        
    )
    txt.extend([
        "#undef self\n",
        "#undef LexemeNull\n",
        "#undef RETURN\n",
    ])
    return "".join(txt)

mode_function_implementation_str = \
"""
void
$on_entry(QUEX_TYPE_ANALYZER* me, const QUEX_NAME(Mode)* FromMode) {
    (void)me;
    (void)FromMode;
$$ENTER-PROCEDURE$$
}

void
$on_exit(QUEX_TYPE_ANALYZER* me, const QUEX_NAME(Mode)* ToMode)  {
    (void)me;
    (void)ToMode;
$$EXIT-PROCEDURE$$
}

$$ON_INDENTATION-PROCEDURE$$

#ifdef QUEX_OPTION_RUNTIME_MODE_TRANSITION_CHECK
bool
$has_base(const QUEX_NAME(Mode)* Mode) {
    (void)Mode;
$$HAS_BASE_MODE$$
}

bool
$has_entry_from(const QUEX_NAME(Mode)* Mode) {
    (void)Mode;
$$HAS_ENTRANCE_FROM$$
}

bool
$has_exit_to(const QUEX_NAME(Mode)* Mode) {
    (void)Mode;
$$HAS_EXIT_TO$$
}
#endif    

void
$on_buffer_before_change(void* me /* 'aux' -> 'self' via 'me' */)
{
    const QUEX_TYPE_LEXATOM* BufferBegin = self.buffer.begin(&self.buffer);
    const QUEX_TYPE_LEXATOM* BufferEnd   = self.buffer.end(&self.buffer);
    (void)me; (void)BufferBegin; (void)BufferEnd;
$$ON_BUFFER_BEFORE_CHANGE$$
}

QUEX_INLINE void
QUEX_NAME(Buffer_print_overflow_message)(QUEX_NAME(Buffer)* buffer); 

void
$on_buffer_overflow(void*  me /* 'aux' -> 'self' via 'me' */)
{
    const QUEX_TYPE_LEXATOM* LexemeBegin = self.buffer._lexeme_start_p;
    const QUEX_TYPE_LEXATOM* LexemeEnd   = self.buffer._read_p;
    const size_t             BufferSize  = (size_t)(self.buffer.size(&self.buffer)); 

$$ON_BUFFER_OVERFLOW$$
    (void)me; (void)LexemeBegin; (void)LexemeEnd; (void)BufferSize;
}
"""                         

on_buffer_overflow_DEFAULT = """
    /* Try to double the size of the buffer, by default.                      */
    if( ! QUEX_NAME(Buffer_nested_negotiate_extend)(&self.buffer, 2.0) ) {
        QUEX_NAME(MF_error_code_set_if_first)(&self, E_Error_Buffer_Overflow_LexemeTooLong);
        QUEX_NAME(Buffer_print_overflow_message)(&self.buffer);
    }
"""                         

def get_implementation_of_mode_functions(mode, Modes):
    """Writes constructors and mode transition functions.

                void quex::lexer::enter_EXAMPLE_MODE() { ... }

    where EXAMPLE_MODE is a lexer mode from the given lexer-modes, and
    'quex::lexer' is the lexical analysis class.
    """
    # (*) on enter 
    on_entry_str  = Lng.CALL_MODE_HAS_ENTRY_FROM(mode.name)

    code_fragment = mode.incidence_db.get(E_IncidenceIDs.MODE_ENTRY)
    if code_fragment is not None:
        on_entry_str += Lng.SOURCE_REFERENCED(code_fragment)
        if on_entry_str.endswith("\n"): on_entry_str = on_entry_str[:-1]

    # (*) on exit
    on_exit_str   = Lng.CALL_MODE_HAS_EXIT_TO(mode.name)

    code_fragment = mode.incidence_db.get(E_IncidenceIDs.MODE_EXIT)
    if code_fragment is not None:
        on_exit_str += Lng.SOURCE_REFERENCED(code_fragment)

    # (*) on indentation
    mode_name_list     = [m.name for m in Modes]
    on_indentation_str = indentation_handler.do(mode, mode_name_list)
    on_indentation_str = __replace_function_names(on_indentation_str, mode, 
                                                  NullFunctionsF=False)

    # (*) has base mode
    base_mode_sequence = mode.implemented_base_mode_name_sequence() 
    if len(base_mode_sequence) == 1:
        assert base_mode_sequence[-1] == mode.name
        has_base_mode_str = "    %s" % Lng.RETURN_THIS(Lng.FALSE)
    else:
        base_mode_list    = base_mode_sequence
        has_base_mode_str = "\n    ".join(
            get_IsOneOfThoseCode(base_mode_list, CheckBaseModeF=True)
        )
        
    # (*) has entry from
    #     check whether the source mode is a permissible 'entry' mode
    entry_list         = mode.entry_mode_name_list() # (only implemented ones are listed)
    has_entry_from_str = "\n    ".join(
        get_IsOneOfThoseCode(entry_list, ConsiderDerivedClassesF=True)
    )

    # (*) has exit to
    #     check whether the target mode is a permissible 'exit' mode
    exit_list       = mode.exit_mode_name_list() # (only implemented ones are listed)
    has_exit_to_str = "\n    ".join(
        get_IsOneOfThoseCode(exit_list, ConsiderDerivedClassesF=True)
    )
    
    # (*) on buffer before change
    code_fragment = mode.incidence_db.get(E_IncidenceIDs.BUFFER_BEFORE_CHANGE)
    if code_fragment is not None:
        on_buffer_before_change = Lng.SOURCE_REFERENCED(code_fragment)
    else:
        on_buffer_before_change = Lng.ON_BUFFER_BEFORE_CHANGE_default()

    # (*) on buffer overflow
    code_fragment = mode.incidence_db.get(E_IncidenceIDs.BUFFER_OVERFLOW)
    if code_fragment is not None:
        on_buffer_overflow = Lng.SOURCE_REFERENCED(code_fragment)
    else:
        on_buffer_overflow = on_buffer_overflow_DEFAULT


    txt = __replace_function_names(mode_function_implementation_str, mode, 
                                   NullFunctionsF=False)

    result = blue_print(txt, [
        ["$$ENTER-PROCEDURE$$",      on_entry_str],
        ["$$EXIT-PROCEDURE$$",       on_exit_str],
        #
        ["$$ON_INDENTATION-PROCEDURE$$", on_indentation_str],
        #
        ["$$HAS_BASE_MODE$$",        has_base_mode_str],
        ["$$HAS_ENTRANCE_FROM$$",    has_entry_from_str],
        ["$$HAS_EXIT_TO$$",          has_exit_to_str],
        #
        ["$$ON_BUFFER_BEFORE_CHANGE$$", on_buffer_before_change],
        ["$$ON_BUFFER_OVERFLOW$$",      on_buffer_overflow],
        #
        ["$$MODE_NAME$$",            mode.name],
    ])

    return result

def get_IsOneOfThoseCode(ModeNameList, CheckBaseModeF=False,
                         ConsiderDerivedClassesF=False):
    mode_pointer_list = [
        "&QUEX_NAME(%s)" % mode_name for mode_name in ModeNameList
    ]

    condition_list = [
        ["Mode", "==", mp] for mp in mode_pointer_list
    ]
    if ConsiderDerivedClassesF:
        condition_list.extend(
            ["Mode->has_base(%s)" % mp] for mp in mode_pointer_list
        )
    if CheckBaseModeF:
        condition_list.extend(
            ["(%s)->has_base(Mode)" % mp] for mp in mode_pointer_list
        )

    txt = Lng.CONDITION_SEQUENCE(condition_list,
                                 [Lng.RETURN_THIS(Lng.TRUE)] * len(condition_list),
                                 Lng.RETURN_THIS(Lng.FALSE))
    return txt

def get_related_code_fragments(ModeDb):
    """
       RETURNS:  -- members of the lexical analyzer class for the mode classes
                 -- static member functions declaring the analyzer functions for he mode classes 
                 -- constructor init expressions (before '{'),       
                 -- constructor text to be executed at construction time 
                 -- friend declarations for the mode classes/functions

    """
    Modes = ModeDb.values()
    members_txt = "".join(
        "extern QUEX_NAME(Mode)  QUEX_NAME(%s);\n" % mode.name
        for mode in Modes
    )

    mode_functions_txt = __get_function_declaration(Modes, FriendF=False)
    friends_txt        = __get_function_declaration(Modes, FriendF=True)

    return members_txt,        \
           mode_functions_txt, \
           friends_txt

def __get_function_declaration(Modes, FriendF=False):

    if FriendF: prolog = "    friend "
    else:       prolog = "extern "

    db = {
        "analyzer_function":       [ "void", 
                                     [("QUEX_TYPE_ANALYZER*", "me")]],

        "on_indentation":          [ "void",
                                     [("QUEX_TYPE_ANALYZER*",   "me"), 
                                      ("QUEX_TYPE_INDENTATION", "Indentation"),
                                      ("QUEX_TYPE_LEXATOM*",    "Lexeme")]],

        "on_entry":                [ "void",
                                     [("QUEX_TYPE_ANALYZER*",    "me"),
                                      ("const QUEX_NAME(Mode)*", "mode")]],
        "on_exit":                 [ "void",
                                     [("QUEX_TYPE_ANALYZER*",    "me"),
                                      ("const QUEX_NAME(Mode)*", "mode")]],
        "has_base":                [ "bool",
                                     [("const QUEX_NAME(Mode)*", "mode")]],
        "has_entry_from":          [ "bool",
                                     [("const QUEX_NAME(Mode)*", "mode")]],
        "has_exit_to":             [ "bool",
                                     [("const QUEX_NAME(Mode)*", "mode")]],
        "on_buffer_before_change": [ "void", 
                                    [("void*",                   "aux")]],
        "on_buffer_overflow":      [ "void",
                                    [("void*",                   "aux")]],
    }
    def function_name(Name, ModeName):
        return Lng.NAME_IN_NAMESPACE_MAIN("%s_%s" % (ModeName, Name))

    def prepare(name, txt):
        if name in ("has_base", "has_entry_from", "has_exit_to"):
            new_txt  = "#ifdef QUEX_OPTION_RUNTIME_MODE_TRANSITION_CHECK\n"
            new_txt += txt
            new_txt += "#endif\n"
            return new_txt
        elif name == "on_indentation":
            new_txt  = "#ifdef QUEX_OPTION_INDENTATION_TRIGGER\n"
            new_txt += txt
            new_txt += "#endif\n"
            return new_txt
        else:
            return txt

    txt = []
    for mode in Modes:

        txt.extend(
            prepare(name, 
                    "%s;\n" % Lng.SIGNATURE(prolog, 
                                            function_name(name, mode.name), 
                                            ReturnType=db[name][0], ArgList=db[name][1]))
            for name in sorted(db.iterkeys())
        ) 

    return "".join(txt)

def __setup(ModeDb):
    txt = [
        initialization(mode)
        for mode in sorted(ModeDb.itervalues(), key=attrgetter("mode_id"))
    ]
    txt.append("\n")
    return "".join(txt)

def initialization(mode):
    return __replace_function_names(mode_setup_str, mode)

def __replace_function_names(txt, mode, NullFunctionsF=True):
    def name(Name, ModeName):
        return Lng.NAME_IN_NAMESPACE_MAIN("%s_%s" % (ModeName, Name))

    if NullFunctionsF and not mode.incidence_db.has_key(E_IncidenceIDs.MODE_ENTRY):
        on_entry = Lng.NAME_IN_NAMESPACE_MAIN("Mode_on_entry_exit_null_function")
    else:
        on_entry = name("on_entry", mode.name)

    if NullFunctionsF and not mode.incidence_db.has_key(E_IncidenceIDs.MODE_EXIT):
        on_exit = Lng.NAME_IN_NAMESPACE_MAIN("Mode_on_entry_exit_null_function")
    else:
        on_exit = name("on_exit", mode.name)

    if NullFunctionsF and not mode.incidence_db.has_key(E_IncidenceIDs.INDENTATION_HANDLER):
        on_indentation = Lng.NAME_IN_NAMESPACE_MAIN("Mode_on_indentation_null_function")
    else:
        on_indentation = name("on_indentation", mode.name)

    return blue_print(txt, [
        ["$$MN$$",                   mode.name],
        ["$analyzer_function",       name("analyzer_function", mode.name)],
        ["$on_indentation",          on_indentation],
        ["$on_entry",                on_entry],
        ["$on_exit",                 on_exit],
        ["$has_base",                name("has_base", mode.name)],
        ["$has_entry_from",          name("has_entry_from", mode.name)],
        ["$has_exit_to",             name("has_exit_to", mode.name)],
        ["$on_buffer_before_change", name("on_buffer_before_change", mode.name)],
        ["$on_buffer_overflow",      name("on_buffer_overflow", mode.name)],
    ])

mode_setup_str = \
"""QUEX_NAME(Mode) QUEX_NAME($$MN$$) = {
    /* name              */ "$$MN$$",
#   if      defined(QUEX_OPTION_INDENTATION_TRIGGER) \\
       && ! defined(QUEX_OPTION_INDENTATION_DEFAULT_HANDLER)
    /* on_indentation    */ $on_indentation,
#   endif
    /* on_entry          */ $on_entry,
    /* on_exit           */ $on_exit,
#   if      defined(QUEX_OPTION_RUNTIME_MODE_TRANSITION_CHECK)
    /* has_base          */ $has_base,
    /* has_entry_from    */ $has_entry_from,
    /* has_exit_to       */ $has_exit_to,
#   endif
    {
    /* on_buffer_before_change */ $on_buffer_before_change,
    /* on_buffer_overflow      */ $on_buffer_overflow,
    /* aux                     */ (void*)0,
    },

    /* analyzer_function */ $analyzer_function
};
"""

