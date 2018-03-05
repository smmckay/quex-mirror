#! /usr/bin/env python
from   quex.engine.misc.string_handling import blue_print
import quex.output.analyzer.modes       as     mode_classes

from   quex.DEFINITIONS import QUEX_PATH, \
                               QUEX_VERSION
import quex.token_db    as     token_db
import quex.blackboard  as     blackboard
from   quex.blackboard  import setup as Setup, \
                               Lng

def do(ModeDB, Epilog):
    assert token_db.token_type_definition is not None

    LexerClassName                 = Setup.analyzer_class_name
    quex_converter_coding_name_str = Setup.converter_ucs_coding_name
    mode_id_definition_str         = mode_classes.mode_id_definition(ModeDB)

    # -- instances of mode classes as members of the lexer
    mode_object_members_txt,     \
    mode_specific_functions_txt, \
    friend_txt                   = mode_classes.get_related_code_fragments(ModeDB)

    # -- define a pointer that directly has the type of the derived class
    if Setup.analyzer_derived_class_name:
        analyzer_derived_class_name    = Setup.analyzer_derived_class_name
        derived_class_type_declaration = Lng.FORWARD_DECLARATION(Setup.analyzer_derived_class_name)
    else:
        analyzer_derived_class_name    = Setup.analyzer_class_name
        derived_class_type_declaration = ""

    token_class_file_name = token_db.token_type_definition.get_file_name()
    token_class_name      = token_db.token_type_definition.class_name
    token_class_name_safe = token_db.token_type_definition.class_name_safe

    include_guard_ext = Lng.INCLUDE_GUARD(
            Lng.NAMESPACE_REFERENCE(Setup.analyzer_name_space) 
            + "__" + Setup.analyzer_class_name)

    lexer_name_space_safe = Lng.INCLUDE_GUARD(Lng.NAMESPACE_REFERENCE(Setup.analyzer_name_space))

    template_code_txt = Lng.open_template(Lng.analyzer_template_file())

    template_code_txt, \
    member_function_signature_list = declare_member_functions(template_code_txt)

    txt = blue_print(template_code_txt, [
        ["$$___SPACE___$$",                      " " * (len(LexerClassName) + 1)],
        ["$$CLASS_BODY_EXTENSION$$",             Lng.SOURCE_REFERENCED(blackboard.class_body_extension)],
        ["$$INCLUDE_GUARD_EXTENSION$$",          include_guard_ext],
        ["$$LEXER_CLASS_NAME$$",                 LexerClassName],
        ["$$LEXER_NAME_SPACE_EXT$$",             lexer_name_space_safe],
        ["$$LEXER_CLASS_NAME_SAFE$$",            Setup.analyzer_name_safe],
        ["$$LEXER_CONFIG_FILE$$",                Setup.get_file_reference(Setup.output_configuration_file)],
        ["$$LEXER_DERIVED_CLASS_DECL$$",         derived_class_type_declaration],
        ["$$LEXER_DERIVED_CLASS_NAME$$",         analyzer_derived_class_name],
        ["$$QUEX_MODE_ID_DEFINITIONS$$",         mode_id_definition_str],
        ["$$MEMENTO_EXTENSIONS$$",               Lng.SOURCE_REFERENCED(blackboard.memento_class_extension)],
        ["$$MODE_CLASS_FRIENDS$$",               friend_txt],
        ["$$MODE_OBJECTS$$",                     mode_object_members_txt],
        ["$$MODE_SPECIFIC_ANALYSER_FUNCTIONS$$", mode_specific_functions_txt],
        ["$$PRETTY_INDENTATION$$",               "     " + " " * (len(LexerClassName)*2 + 2)],
        ["$$QUEX_TEMPLATE_DIR$$",                QUEX_PATH + Lng.CODE_BASE],
        ["$$QUEX_VERSION$$",                     QUEX_VERSION],
        ["$$TOKEN_CLASS_DEFINITION_FILE$$",      Setup.get_file_reference(token_class_file_name)],
        ["$$TOKEN_CLASS$$",                      token_class_name],
        ["$$TOKEN_CLASS_NAME_SAFE$$",            token_class_name_safe],
        ["$$TOKEN_ID_DEFINITION_FILE$$",         Setup.output_token_id_file_ref],
        ["$$CORE_ENGINE_CHARACTER_CODING$$",     quex_converter_coding_name_str],
        ["$$USER_DEFINED_HEADER$$",              Lng.SOURCE_REFERENCED(blackboard.header) + "\n"],
        ["$$USER_DEFINED_FOOTER$$",              Lng.SOURCE_REFERENCED(blackboard.footer) + "\n"],
        ["$$EPILOG$$",                           Epilog],
     ])

    return txt, member_function_signature_list

def do_implementation(ModeDB, MemberFunctionSignatureList):

    func_txt = Lng.open_template(Lng.analyzer_template_i_file())

    func_txt = blue_print(func_txt, [
        ["$$MEMBER_FUNCTION_ASSIGNMENT$$",              Lng.MEMBER_FUNCTION_ASSIGNMENT(MemberFunctionSignatureList)],
        ["$$CONSTRUCTOR_EXTENSTION$$",                  Lng.SOURCE_REFERENCED(blackboard.class_constructor_extension)],
        ["$$DESTRUCTOR_EXTENSTION$$",                   Lng.SOURCE_REFERENCED(blackboard.class_destructor_extension)],
        ["$$USER_DEFINED_PRINT$$",                      Lng.SOURCE_REFERENCED(blackboard.class_print_extension)],
        ["$$CONSTRUCTOR_MODE_DB_INITIALIZATION_CODE$$", __mode_db_constructor_code(ModeDB)],
        ["$$RESET_EXTENSIONS$$",                        Lng.SOURCE_REFERENCED(blackboard.reset_extension)],
        ["$$MEMENTO_EXTENSIONS_PACK$$",                 Lng.SOURCE_REFERENCED(blackboard.memento_pack_extension)],
        ["$$MEMENTO_EXTENSIONS_UNPACK$$",               Lng.SOURCE_REFERENCED(blackboard.memento_unpack_extension)],
    ])
    return "\n%s\n" % func_txt

def __mode_db_constructor_code(ModeDb):
    if not ModeDb: return ""

    L = max(len(m.name) for m in ModeDb.itervalues())

    def condition(mode):
        return Lng.EQUAL("%s %s" % (Lng.MODE_BY_ID(mode.name), " " * (L-len(mode.name))),
                         Lng.ADDRESS_OF(Lng.NAME_IN_NAMESPACE_MAIN(mode.name)))

    return "".join(
        "    %s\n" % Lng.ASSERT(condition(mode))
        for mode in ModeDb.itervalues() 
    )


class Signature:
    def __init__(self, ReturnType, FunctionName, ArgumentList):
        self.return_type   = ReturnType
        self.function_name = FunctionName
        self.argument_list = ArgumentList

    @classmethod
    def from_String(cls, String):
        """SYNTAX: return-type; function-name; argument-list;

        argument-list:   type ':' name ','
        """
        def type_and_name(SubString):
            fields   = [x.strip() for x in SubString.split()]
            type_str = " ".join(fields[:-1])
            name_str = fields[-1]
            return type_str, name_str

        open_i  = String.find("(")
        close_i = String.rfind(")")
        return_type, function_name = type_and_name(String[:open_i])
        argument_list = [ 
            type_and_name(x) 
            for x in String[open_i+1:close_i].split(",") if x.strip()
        ]

        return cls(return_type, function_name, argument_list)

def member_functions(Txt):
    """YIELDS:
       [0] begin index of letter in 'Txt'
       [1] end index of letter in 'Txt'
       [2] signature of function
    """
    start_i = 0
    while 1 + 1 == 2:
        begin_i = Txt.find("$$MF:", start_i+1)
        if begin_i == -1: break
        end_i   = Txt.find("$$", begin_i+1)
        if end_i == -1: break
        yield begin_i, end_i+2, Signature.from_String(Txt[begin_i+len("$$MF:"):end_i])
        start_i = end_i + 2

    return 

def declare_member_functions(Txt):
    """RETURNS: [0] 'Txt' with member function declarations replaced.
                [1] list of function signatures in the sequence of their appearance.
    """
    txt = []
    signature_list = []
    last_i = 0
    for begin_i, end_i, signature in member_functions(Txt):
        if signature is None: continue
        txt.append(Txt[last_i:begin_i])
        txt.append(Lng.MEMBER_FUNCTION_DECLARATION(signature))
        last_i = end_i
        signature_list.append(signature)
    txt.append(Txt[last_i:])
    return "".join(txt), signature_list
