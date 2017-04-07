# (C) 2005-2010 Frank-Rene Schaefer
# ABSOLUTELY NO WARANTY
from   quex.DEFINITIONS                   import QUEX_PATH
from   quex.engine.misc.file_in           import get_include_guard_extension, \
                                                 make_safe_identifier
from   quex.engine.misc.file_operations   import open_file_or_die
from   quex.engine.misc.string_handling   import blue_print
import quex.blackboard                    as     blackboard
from   quex.blackboard                    import setup as Setup, Lng

import re
from   collections import OrderedDict

def do(MapTokenIDToNameFunctionStr):
    """RETURNS: [0] header code
                [1] implementation
    """
    assert blackboard.token_type_definition is not None

    if blackboard.token_type_definition.manually_written():
        # User has specified a manually written token class
        return "", ""

    txt, txt_i = _do(blackboard.token_type_definition)

    # Return declaration and implementation as two strings
    if Setup.token_class_only_f:
        txt   = _clean_for_independence(txt)
        txt_i = _clean_for_independence(txt_i)
        map_token_id_to_name_function_str =   \
                _clean_for_independence(MapTokenIDToNameFunctionStr) 

    if Setup.language.upper() == "C++":
        # In C++ we do inline, so we can do everything in the header file
        header_txt         = "".join([txt, "\n", txt_i])
        implementation_txt = ""
    else:
        # In C, there's a separate file in any case
        header_txt         = txt
        implementation_txt = txt_i 

    if Setup.token_class_only_f: 
        implementation_txt +=  map_token_id_to_name_function_str \
                             + lexeme_null_implementation() 

    return header_txt, implementation_txt

def _do(Descr):
    # The following things must be ensured before the function is called
    assert Descr is not None
    assert Descr.__class__.__name__ == "TokenTypeDescriptor"

    ## ALLOW: Descr.get_member_db().keys() == empty

    TemplateFile   = QUEX_PATH + Lng.token_template_file()
    TemplateIFile  = QUEX_PATH + Lng.token_template_i_file()

    template_str   = open_file_or_die(TemplateFile, Mode="rb").read()
    template_i_str = open_file_or_die(TemplateIFile, Mode="rb").read()
    
    virtual_destructor_str = ""
    if Descr.open_for_derivation_f: virtual_destructor_str = "virtual "

    if Descr.copy is None:
        # Default copy operation: Plain Copy of token memory
        copy_str = "__QUEX_STD_memcpy((void*)__this, (void*)__That, sizeof(QUEX_TYPE_TOKEN));\n"
    else:
        copy_str = Lng.SOURCE_REFERENCED(Descr.copy)

    if Descr.take_text is None:
        take_text_str = "return true;\n" 
    else:
        take_text_str = Lng.SOURCE_REFERENCED(Descr.take_text)

    include_guard_extension_str = get_include_guard_extension(
                                        Lng.NAMESPACE_REFERENCE(Descr.name_space) 
                                        + "__" + Descr.class_name)

    # In case of plain 'C' the class name must incorporate the namespace (list)
    token_class_name = Descr.class_name
    if Setup.language == "C":
        token_class_name = Setup.token_class_name_safe

    converter_declaration_include,   \
    converter_implementation_include = __get_converter_configuration(include_guard_extension_str)

    extra_at_begin_str = lexeme_null_declaration()
    extra_at_end_str   = ""

    namespace_open, namespace_close = __namespace_brackets()
    helper_variable_replacements = [
              ["$INCLUDE_CONVERTER_DECLARATION",    converter_declaration_include],
              ["$INCLUDE_CONVERTER_IMPLEMENTATION", converter_implementation_include],
              ["$NAMESPACE_CLOSE",                  namespace_close],
              ["$NAMESPACE_OPEN",                   namespace_open],
              ["$TOKEN_CLASS",                      token_class_name],
    ]

    if Setup.token_class_only_f:
        extra_at_begin_str += get_helper_definitions() 

    txt = blue_print(template_str, 
            [
              ["$$EXTRA_AT_BEGIN$$",  extra_at_begin_str],
              ["$$EXTRA_AT_END$$",    extra_at_end_str],
            ])
    txt = blue_print(txt,
             [
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

    txt   = blue_print(txt, helper_variable_replacements)

    txt_i = blue_print(template_i_str, 
            [
              ["$$EXTRA_AT_BEGIN$$",  extra_at_begin_str],
              ["$$EXTRA_AT_END$$",    extra_at_end_str],
            ])
    txt_i = blue_print(txt_i, 
                       [
                        ["$$CONSTRUCTOR$$",             Lng.SOURCE_REFERENCED(Descr.constructor)],
                        ["$$COPY$$",                    copy_str],
                        ["$$DESTRUCTOR$$",              Lng.SOURCE_REFERENCED(Descr.destructor)],
                        ["$$FOOTER$$",                  Lng.SOURCE_REFERENCED(Descr.footer)],
                        ["$$FUNC_TAKE_TEXT$$",          take_text_str],
                        ["$$TOKEN_CLASS_HEADER$$",      Setup.get_file_reference(blackboard.token_type_definition.get_file_name())],
                        ["$$INCLUDE_GUARD_EXTENSION$$", include_guard_extension_str],
                        ["$$NAMESPACE_OPEN$$",          Lng.NAMESPACE_OPEN(Descr.name_space)],
                        ["$$NAMESPACE_CLOSE$$",         Lng.NAMESPACE_CLOSE(Descr.name_space)],
                        ["$$TOKEN_REPETITION_N_GET$$",  Lng.SOURCE_REFERENCED(Descr.repetition_get)],
                        ["$$TOKEN_REPETITION_N_SET$$",  Lng.SOURCE_REFERENCED(Descr.repetition_set)],
                        ["$$TOKEN_CLASS_NAME_SAFE$$",   Descr.class_name_safe],
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
            "_id = ID; "
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

def __get_converter_configuration(IncludeGuardExtension):
    token_descr = blackboard.token_type_definition

    declaration_include    = Lng.CONVERTER_HELPER_DECLARATION()
    implementation_include = Lng.CONVERTER_HELPER_IMLEMENTATION()

    if not Setup.token_class_only_f:
        return declaration_include, implementation_include

    # From Here One: 'Sharable Token Class Generation'
    if Setup.language.upper() == "C++":
        function_prefix       = Lng.NAMESPACE_REFERENCE(token_descr.name_space) 
        function_def_prefix   = ""
        namespace_token_open  = Lng.NAMESPACE_OPEN(token_descr.name_space).replace("\n", " ")
        namespace_token_close = Lng.NAMESPACE_CLOSE(token_descr.name_space).replace("\n", " ")
        quex_name_prefix      = Setup.analyzer_class_name
    else:
        function_prefix       = token_descr.class_name_safe + " ##"
        function_def_prefix   = token_descr.class_name_safe + " ##"
        namespace_token_open  = ""
        namespace_token_close = ""
        quex_name_prefix      = Setup.analyzer_name_safe

    before = "" 
    after  = "" 

    declaration_include    = "%s%s\n%s" \
                             % (before, declaration_include, after)
    implementation_include = "%s%s\n%s" \
                             % (before, implementation_include, after)

    # In C:   Function call and def prefix is the same
    # In C++: We are in the same namespace, no prefix, function_def_prefix is empty anyway.
    return declaration_include, implementation_include

QUEX_lexeme_length_re         = re.compile("\\bQUEX_NAME\\(lexeme_length\\)", re.UNICODE)
QUEX_TYPE_LEXATOM_re          = re.compile("\\bQUEX_TYPE_LEXATOM\\b", re.UNICODE)
QUEX_LEXEME_NULL_re           = re.compile("\\bQUEX_LEXEME_NULL\\b", re.UNICODE)
QUEX_TYPE_ANALYZER_re         = re.compile("\\bQUEX_TYPE_ANALYZER\\b", re.UNICODE)
QUEX_LexemeNullDeclaration_re = re.compile("\\bQUEX_NAME\\(LexemeNullObject\\)", re.UNICODE)
QUEX_TYPE_LEXATOM_safe_re     = re.compile("\\$\\$quex_type_character\\$\\$", re.UNICODE)
PRAGMA_LINE                   = re.compile("^# *line\\b", re.UNICODE)

def _clean_for_independence(txt):
    token_descr = blackboard.token_type_definition

    global QUEX_MEMORY_FREE_re
    global QUEX_MEMORY_ALLOC_re
    global QUEX_lexeme_length_re
    global QUEX_TYPE_LEXATOM_re
    global QUEX_TYPE_ANALYZER_re
    global QUEX_LexemeNullDeclaration_re
    global QUEX_TYPE_LEXATOM_safe_re
    global QUEX_LEXEME_NULL_re

    #txt = QUEX_TYPE_LEXATOM_re.sub(Setup.buffer_lexatom_type, txt)
    txt = QUEX_TYPE_ANALYZER_re.sub("void", txt)
    txt = QUEX_LexemeNullDeclaration_re.sub(common_lexeme_null_str(), txt)
    txt = QUEX_TYPE_LEXATOM_safe_re.sub("QUEX_TYPE_LEXATOM", txt)
    txt = QUEX_lexeme_length_re.sub("%s_lexeme_length" % token_descr.class_name_safe, txt)
    txt = QUEX_LEXEME_NULL_re.sub(common_lexeme_null_str(), txt)

    # Delete any line references
    result = [
        "%s\n" % line
        for line in txt.splitlines()
        if PRAGMA_LINE.match(line) is None
    ]
    return "".join(result)

def __namespace_brackets(DefineF=False):
    token_descr = blackboard.token_type_definition

    if Setup.language.upper() == "C++":
        open_str  = Lng.NAMESPACE_OPEN(token_descr.name_space).strip()
        close_str = Lng.NAMESPACE_CLOSE(token_descr.name_space).strip()
        if DefineF:
            open_str  = open_str.replace("\n", "\\\n")
            close_str = close_str.replace("\n", "\\\n")
        return open_str, close_str
    else:
        return "", ""

def common_lexeme_null_str():
    token_descr = blackboard.token_type_definition
    if Setup.language.upper() == "C++": 
        # LexemeNull's namespace == token namespace, no explicit naming.
        return "LexemeNullObject"
    else:                               
        namespace_prefix = Lng.NAMESPACE_REFERENCE(token_descr.name_space) 
        return "%sLexemeNullObject" % namespace_prefix

def lexeme_null_declaration():
    if Setup.token_class_only_f:
        namespace_open, namespace_close = __namespace_brackets()
        return "".join([
                    "%s\n" % namespace_open,
                    "extern %s  %s;\n" % (Setup.buffer_lexatom_type, common_lexeme_null_str()),
                    "%s\n\n" % namespace_close,
                  ])
    else:
        # The following should hold in any both cases:
        return "".join([
                    "QUEX_NAMESPACE_LEXEME_NULL_OPEN\n",
                    "extern QUEX_TYPE_LEXATOM   QUEX_LEXEME_NULL_IN_ITS_NAMESPACE;\n" 
                    "QUEX_NAMESPACE_LEXEME_NULL_CLOSE\n",
                  ])

def lexeme_null_implementation():
    namespace_open, namespace_close = __namespace_brackets()

    return "".join([
                "%s\n" % namespace_open,
                "%s  %s = (%s)0;\n" % (Setup.buffer_lexatom_type, common_lexeme_null_str(), Setup.buffer_lexatom_type),
                "%s\n\n" % namespace_close,
              ])

helper_definitions_Cpp = """
#define QUEX_NAME_TOKEN(NAME)              %s_ ## NAME
#define QUEX_NAMESPACE_TOKEN_OPEN          %s
#define QUEX_NAMESPACE_TOKEN_CLOSE         %s
#define QUEX_NAMESPACE_LEXEME_NULL_OPEN    %s
#define QUEX_NAMESPACE_LEXEME_NULL_CLOSE   %s
"""

helper_definitions_C = """
#define QUEX_NAME_TOKEN(NAME)              %s_ ## NAME
#define QUEX_NAMESPACE_TOKEN_OPEN  
#define QUEX_NAMESPACE_TOKEN_CLOSE 
#define QUEX_NAMESPACE_LEXEME_NULL_OPEN     
#define QUEX_NAMESPACE_LEXEME_NULL_CLOSE    
"""

helper_definitions_common = """
#define QUEX_TYPE_LEXATOM                  %s
#define QUEX_TYPE_TOKEN_ID                 %s
#define QUEX_SETTING_CHARACTER_CODEC       %s

#include "%s" 
"""

def get_helper_definitions():
    namespace_open, namespace_close = __namespace_brackets(DefineF=True)
    token_descr                     = blackboard.token_type_definition
    if len(Setup.token_id_foreign_definition_file) != 0:
        token_id_definition_file = Setup.token_id_foreign_definition_file
    else:
        token_id_definition_file = Setup.output_token_id_file

    ln_namespace_open  = Lng.NAMESPACE_OPEN(Setup.lexeme_null_namespace).replace("\n", "\\\n")
    ln_namespace_close = Lng.NAMESPACE_CLOSE(Setup.lexeme_null_namespace).replace("\n", "\\\n")

    if Setup.language.upper() == "C++":
        txt = helper_definitions_Cpp \
               % (token_descr.class_name, 
                  namespace_open,    namespace_close,        
                  ln_namespace_open, ln_namespace_close)
    else:
        txt = helper_definitions_C % token_descr.class_name_safe

    txt += helper_definitions_common \
           % (Setup.buffer_lexatom_type,
              Setup.token_id_type,
              make_safe_identifier(Setup.buffer_codec.name).lower(),
              token_id_definition_file)

    return txt


