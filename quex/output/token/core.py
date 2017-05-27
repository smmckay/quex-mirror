# (C) 2005-2017 Frank-Rene Schaefer
# ABSOLUTELY NO WARANTY
from   quex.input.files.token_type              import TokenTypeDescriptor
from   quex.engine.misc.string_handling         import blue_print
import quex.output.token.id_generator as     token_id_maker
import quex.blackboard                          as     blackboard
from   quex.blackboard                          import setup as Setup, Lng

from   collections import OrderedDict

def do():
    """RETURNS: [0] Header content for token id definition, or None.
                [1] Global declaration of the 'lexeme null', or ""
                [2] Header text of the token class definition.
                [3] Implementation of the token class.
    """
    assert blackboard.token_type_definition is not None

    token_id_header = token_id_maker.do(Setup) 

    if blackboard.token_type_definition.manually_written():
        # User has specified a manually written token class
        # (LexemeNull must be declared in global header)
        global_lexeme_null_declaration = \
                Lng.COMMENT("A manually written token class has been provided.\n"
                            + "See file '%s'." % Setup.output_token_class_file
                            + "Declaration of 'lexeme null' is provided here.\n"
                            + "The token class implementation must provide its definition.\n") \
                + Lng.LEXEME_NULL_DECLARATION()
        header_txt         = ""
        implementation_txt = ""
    else:
        # (LexemeNull is declared in token class header)
        global_lexeme_null_declaration = ""
        header_txt,        \
        implementation_txt = _do(blackboard.token_type_definition)

    return token_id_header, \
           global_lexeme_null_declaration, \
           header_txt, \
           implementation_txt

def _do(Descr):
    txt, txt_i = _do_core(blackboard.token_type_definition)

    if Setup.language.upper() == "C++":
        # C++: declaration and (inline) implementation in header.
        header_txt         = "\n".join([txt, txt_i])
        implementation_txt = ""
    else:
        # C: declaration in header, implementation in source file.
        header_txt         = txt
        implementation_txt = txt_i 

    # The 'lexeme null' definition *must be* in the implementation file!
    # Except that the token class comes from outside
    if not Setup.extern_token_class_file:
        if not implementation_txt:
            implementation_txt = "%s\n" % _include_token_class_header()
        implementation_txt += Lng.LEXEME_NULL_IMPLEMENTATION()

    return header_txt, implementation_txt

def _do_core(Descr):
    # The following things must be ensured before the function is called
    assert Descr is not None
    assert isinstance(Descr, TokenTypeDescriptor)

    include_guard_extension_str, \
    virtual_destructor_str,      \
    copy_str,                    \
    take_text_str                = _some_standard_stuff(Descr)

    # In case of plain 'C' the class name must incorporate the namespace (list)
    if Setup.language == "C":
        token_class_name = Setup.token_class_name_safe
    else:
        token_class_name = Descr.class_name

    converter_declaration_include    = Lng.CONVERTER_HELPER_DECLARATION()
    converter_implementation_include = Lng.CONVERTER_HELPER_IMLEMENTATION()

    # ------------
    # TODO: Following should be always placed in front of footer/header:
    # ------------
    helper_variable_replacements = [
        ["$INCLUDE_CONVERTER_DECLARATION",    converter_declaration_include],
        ["$INCLUDE_CONVERTER_IMPLEMENTATION", converter_implementation_include],
        ["$NAMESPACE_OPEN",                   "QUEX_NAMESPACE_TOKEN_OPEN"],
        ["$NAMESPACE_CLOSE",                  "QUEX_NAMESPACE_TOKEN_CLOSE"],
        ["$TOKEN_CLASS",                      token_class_name],
    ]

    if Setup.token_class_only_f: helper_definitions = _helper_definitions() 
    else:                        helper_definitions = ""

    template_str = Lng.open_template(Lng.token_template_file())
    txt = blue_print(template_str, [
        ["$$HELPER_DEFINITIONS$$",      helper_definitions],
        ["$$LEXEME_NULL_DECLARATION$$", Lng.LEXEME_NULL_DECLARATION()],
        ["$$BODY$$",                    Lng.SOURCE_REFERENCED(Descr.body)],
        ["$$CONSTRUCTOR$$",             Lng.SOURCE_REFERENCED(Descr.constructor)],
        ["$$COPY$$",                    copy_str],
        ["$$DESTRUCTOR$$",              Lng.SOURCE_REFERENCED(Descr.destructor)],
        ["$$DISTINCT_MEMBERS$$",        get_distinct_members(Descr)],
        ["$$FOOTER$$",                  Lng.SOURCE_REFERENCED(Descr.footer)],
        ["$$FUNC_TAKE_TEXT$$",          take_text_str],
        ["$$HEADER$$",                  Lng.SOURCE_REFERENCED(Descr.header)],
        ["$$INCLUDE_GUARD_EXTENSION$$", include_guard_extension_str],
        ["$$NAMESPACE_CLOSE$$",         Lng.NAMESPACE_CLOSE(Descr.name_space)],
        ["$$NAMESPACE_OPEN$$",          Lng.NAMESPACE_OPEN(Descr.name_space)],
        ["$$QUICK_SETTERS$$",           get_quick_setters(Descr)],
        ["$$SETTERS_GETTERS$$",         get_setter_getter(Descr)],
        ["$$TOKEN_REPETITION_N_GET$$",  Lng.SOURCE_REFERENCED(Descr.repetition_get)],
        ["$$TOKEN_REPETITION_N_SET$$",  Lng.SOURCE_REFERENCED(Descr.repetition_set)],
        ["$$UNION_MEMBERS$$",           get_union_members(Descr)],
        ["$$VIRTUAL_DESTRUCTOR$$",      virtual_destructor_str],
        ["$$TOKEN_CLASS_NAME_SAFE$$",   Descr.class_name_safe],
    ])
    txt = blue_print(txt, helper_variable_replacements)

    template_i_str = Lng.open_template(Lng.token_template_i_file())
    txt_i = blue_print(template_i_str, [
        ["$$INCLUDE_TOKEN_CLASS_HEADER$$", _include_token_class_header()],
        ["$$CONSTRUCTOR$$",                Lng.SOURCE_REFERENCED(Descr.constructor)],
        ["$$COPY$$",                       copy_str],
        ["$$DESTRUCTOR$$",                 Lng.SOURCE_REFERENCED(Descr.destructor)],
        ["$$FOOTER$$",                     Lng.SOURCE_REFERENCED(Descr.footer)],
        ["$$FUNC_TAKE_TEXT$$",             take_text_str],
        ["$$TOKEN_CLASS_HEADER$$",         Setup.get_file_reference(blackboard.token_type_definition.get_file_name())],
        ["$$INCLUDE_GUARD_EXTENSION$$",    include_guard_extension_str],
        ["$$NAMESPACE_OPEN$$",             Lng.NAMESPACE_OPEN(Descr.name_space)],
        ["$$NAMESPACE_CLOSE$$",            Lng.NAMESPACE_CLOSE(Descr.name_space)],
        ["$$TOKEN_REPETITION_N_GET$$",     Lng.SOURCE_REFERENCED(Descr.repetition_get)],
        ["$$TOKEN_REPETITION_N_SET$$",     Lng.SOURCE_REFERENCED(Descr.repetition_set)],
        ["$$TOKEN_CLASS_NAME_SAFE$$",      Descr.class_name_safe],
        ["$$MAP_ID_TO_NAME_CASES$$",       token_id_maker.do_map_id_to_name_cases()],
    ])
    txt_i = blue_print(txt_i, helper_variable_replacements)

    return txt, txt_i

#______________________________________________________________________________
# [MEMBER PACKAGING]
#
# The 'distinct_db' and 'union_db' dictionaries are not to be sorted for
# iteration! The members need to be written in the sequence which is provided 
# by '.items()'.
# => The ordered dictionary lists them in the sequence as when they were 
#    defined. 
# => User is able to define 'packaging'.
#______________________________________________________________________________

def get_distinct_members(Descr):
    TL = Descr.type_name_length_max()
    NL = Descr.variable_name_length_max()

    return "".join(
        __member(type_code, TL, name, NL)
        for name, type_code in Descr.distinct_db.items()      # No sort! [MEMBER PACKAGING]
    )

def get_union_members(Descr):
    TL = Descr.type_name_length_max()
    NL = Descr.variable_name_length_max()
    if not Descr.union_db: return ""
    
    txt = ["    union {\n"]
    for name, type_descr in Descr.union_db.items():           # No sort! [MEMBER PACKAGING]
        if isinstance(type_descr, OrderedDict):
            txt.append("        struct {\n")
            txt.extend(
                __member(sub_type, TL, sub_name, NL, IndentationOffset=" " * 8)
                for sub_name, sub_type in type_descr.items()  # No sort! [MEMBER PACKAGING]
            )
            txt.append("\n        } %s;\n" % name)
        else:
            txt.append("%s\n" % __member(type_descr, TL, name, NL, IndentationOffset=" " * 4))
    txt.append("    } content;\n")
    #txt += Lng._SOURCE_REFERENCE_END()
    return "".join(txt)

def __member(TypeCode, MaxTypeNameL, VariableName, MaxVariableNameL, IndentationOffset=""):
    my_def  = Lng._SOURCE_REFERENCE_BEGIN(TypeCode.sr)
    my_def += IndentationOffset
    my_def += Lng.CLASS_MEMBER_DEFINITION(TypeCode.get_pure_text(), MaxTypeNameL, 
                                          VariableName)
    my_def += Lng._SOURCE_REFERENCE_END(TypeCode.sr)
    return my_def

def get_setter_getter(Descr):
    """NOTE: All names are unique even in combined unions."""
    TL = Descr.type_name_length_max()
    NL = Descr.variable_name_length_max()
    variable_db = Descr.get_member_db()
    txt = ""
    for variable_name, info in variable_db.items():
        type_code = info[0]
        access    = info[1]
        type_str  = type_code.get_pure_text()
        txt += Lng._SOURCE_REFERENCE_BEGIN(type_code.sr)
        my_def = "    %s%s get_%s() const %s{ return %s; }" \
                 % (type_str,      " " * (TL - len(type_str)), 
                    variable_name, " " * ((NL + TL)- len(variable_name)), 
                    access)
        txt += my_def

        type_str = type_str.strip()
        type_str = type_str.replace("\t", " ")
        while type_str.find("  ") != -1:
            type_str = type_str.replace("  ", " ")
        if type_str not in ["char", "unsigned char", "singed char",
                            "short", "unsigned short", "singed short",
                            "int", "unsigned int", "singed int",
                            "long", "unsigned long", "singed long",
                            "float", "unsigned float", "singed float",
                            "double", "unsigned double", "singed double",
                            "uint8_t", "uint16_t", "uint32_t",
                            "int8_t", "int16_t", "int32_t",
                            "size_t", "uintptr_t", "ptrdiff_t"]:
            type_str += "&"

        txt += Lng._SOURCE_REFERENCE_BEGIN(type_code.sr)
        my_def = "    void%s set_%s(%s Value) %s{ %s = Value; }" \
               % (" " * (TL - len("void")), 
                  variable_name, type_str, " " * (NL + TL - (len(type_str) + len(variable_name))), 
                  access)
        txt += my_def

    txt += Lng._SOURCE_REFERENCE_END()
    return txt

def get_quick_setters(Descr):
    """NOTE: All names are unique even in combined unions."""
    variable_db         = Descr.get_member_db()
    used_signature_list = []

    def __quick_setter(ArgList, used_signature_list):
        """ArgList = [ [Name, Type], [Name, Type], ...]
         
           NOTE: There cannot be two signatures of the same type specification.
                 This is so, since functions are overloaded, have the same name
                 and only identify with their types.
        """
        signature = map(lambda x: x[1].get_pure_text(), ArgList)
        if signature in used_signature_list:
            return []
        else:
            used_signature_list.append(signature)

        def _get_arg(info, i):
            name, type_info = info
            type_str = type_info.get_pure_text()
            if type_str.find("const") != -1: type_str = type_str[5:]
            return "const %s& Value%i" % (type_str, i)

        def _get_assignment(info, i):
            name, type_info = info
            return "%s = Value%i; " % (variable_db[name][1], i)

        txt  = [
            "    void set(const QUEX_TYPE_TOKEN_ID ID, ",
            ", ".join(
                _get_arg(info, i) for i, info in enumerate(ArgList)
            ),
            ")\n    { ",
            "id = ID; "
        ]
        txt.extend(
            _get_assignment(info, i)
            for i, info in enumerate(ArgList)
        )
        txt.append("}\n")

        return txt

    def __combined_quick_setters(member_db, used_signature_list):
        member_list = member_db.items()
        if len(member_list) == 0: return []

        # sort the members with respect to their occurence in the token_type section
        member_list.sort(lambda x, y: cmp(x[1].sr.line_n, y[1].sr.line_n))
        L        = len(member_list)
        # build the argument list consisting of a permutation of distinct members
        arg_list = [ member_list[i] for i in range(L) ]

        return __quick_setter(arg_list, used_signature_list)

    # (*) Quick setters for distinct members
    txt = __combined_quick_setters(Descr.distinct_db, used_signature_list)

    # (*) Quick setters for union members
    complete_f = True
    for name, type_info in Descr.union_db.items():
        if isinstance(type_info, OrderedDict): 
            setter_txt = __combined_quick_setters(type_info, used_signature_list)
        else:                                  
            setter_txt = __quick_setter([[name, type_info]], used_signature_list)

        if not setter_txt: complete_f = False
        txt.extend(setter_txt)

    if not complete_f:
        txt.insert(0, "   /* Not all members are accessed via quick-setters (avoid overload errors). */")

    return "".join(txt)

helper_definitions_Cpp = """
#define QUEX_NAME_TOKEN(NAME)              %s_ ## NAME
#define QUEX_NAMESPACE_TOKEN_OPEN          %s
#define QUEX_NAMESPACE_TOKEN_CLOSE         %s
"""

helper_definitions_C = """
#define QUEX_NAME_TOKEN(NAME)              %s_ ## NAME
#define QUEX_NAMESPACE_TOKEN_OPEN  
#define QUEX_NAMESPACE_TOKEN_CLOSE 
"""

helper_definitions_common = """
#define QUEX_TYPE_LEXATOM                  %s
#define QUEX_TYPE_TOKEN_ID                 %s
#define QUEX_SETTING_CHARACTER_CODEC       %s

#include "%s" 
"""

def _include_token_class_header():
    return "#include \"%s\"" % \
           Setup.get_file_reference(Setup.output_token_class_file)

def _helper_definitions():
    token_descr = blackboard.token_type_definition

    if Setup.language.upper() == "C++":
        namespace_open  = Lng.NAMESPACE_OPEN(token_descr.name_space)
        namespace_close = Lng.NAMESPACE_CLOSE(token_descr.name_space)
        txt = helper_definitions_Cpp % (token_descr.class_name, 
                                        namespace_open, 
                                        namespace_close)        
    else:
        txt = helper_definitions_C % token_descr.class_name_safe

    txt += helper_definitions_common \
           % (Setup.buffer_lexatom_type,
              Setup.token_id_type,
              Lng.SAFE_IDENTIFIER(Setup.buffer_encoding.name),
              Setup.output_token_id_file_ref)

    return txt

def _some_standard_stuff(Descr):
    """RETURNS: [0] include guard string
                [1] virtual_destructor_str
                [2] body of the 'copy' function
                [3] body of the 'take_text' function
    """
    include_guard_extension_str = Lng.INCLUDE_GUARD(Lng.NAMESPACE_REFERENCE(Descr.name_space) 
                                                    + "__" + Descr.class_name)

    virtual_destructor_str = ""
    if Descr.open_for_derivation_f: 
        virtual_destructor_str = Lng.VIRTUAL_DESTRUCTOR_PREFIX

    if Descr.copy is None:
        # Default copy operation: Plain Copy of token memory
        copy_str = Lng.DEFAULT_TOKEN_COPY("__this", "__That")
    else:
        copy_str = Lng.SOURCE_REFERENCED(Descr.copy)

    if Descr.take_text is None:
        take_text_str = "%s\n" % Lng.RETURN_THIS(Lng.TRUE)
    else:
        take_text_str = Lng.SOURCE_REFERENCED(Descr.take_text)

    return include_guard_extension_str, \
           virtual_destructor_str, \
           copy_str, \
           take_text_str


