from   quex.output.languages.cpp.dictionary import Language as LanguageCpp
from   quex.constants                       import E_Files
import quex.blackboard                      as     blackboard
from   quex.blackboard                      import setup as Setup

class Language(LanguageCpp):
    all_extension_db = {
        "": {
              E_Files.SOURCE:              ".c",
              E_Files.HEADER:              ".h",
              E_Files.HEADER_IMPLEMTATION: ".c",
        },
    }

    INLINE = "" # "static"

    def __init__(self):      
        LanguageCpp.__init__(self)

    def NAMESPACE_REFERENCE(self, NameList, TrailingDelimiterF=True):
        return "" # C knows no namespaces
    def token_template_file(self):    return "%s/token/TXT-C"       % self.CODE_BASE
    def token_template_i_file(self):  return "%s/token/TXT-C.i"     % self.CODE_BASE
    def token_default_file(self):     return "%s/token/CDefault.qx" % self.CODE_BASE
    def analyzer_template_file(self): return "%s/analyzer/TXT-C"    % self.CODE_BASE

    def NAMESPACE_OPEN(self, NameList):  return ""
    def NAMESPACE_CLOSE(self, NameList): return ""

    def TOKEN_SET_MEMBER(self, Member, Value):
        return "self.token_p(&self)->%s = %s;" % (Member, Value)

    def TOKEN_SEND(self, TokenName):
        return "self.send(&self, %s);" % TokenName

    def TOKEN_SEND_TEXT(self, TokenName, Begin, End):
        return "self.send_text(&self, %s, %s, %s);" % (TokenName, Begin, End)

    def TOKEN_SEND_N(self, N, TokenName):
        return "self.send_n(&self, %s, (size_t)%s);\n" % (TokenName, N)

    def MEMBER_FUNCTION_DECLARATION(self, signature):
        if not blackboard.condition_holds(signature.condition):
            return ""
        argument_list_str = ", ".join("%s %s" % (arg_type, arg_name) 
                                      for arg_type, arg_name, default in signature.argument_list)

        if signature.constant_f: constant_str = "const "
        else:                    constant_str = ""
        if signature.argument_list: me_str = "%sQUEX_TYPE_ANALYZER* me, " % constant_str
        else:                       me_str = "%sQUEX_TYPE_ANALYZER* me" % constant_str

        return "%s (*%s)(%s%s);" % (signature.return_type, signature.function_name, 
                                    me_str, argument_list_str) 

    def MEMBER_FUNCTION_ASSIGNMENT(self, MemberFunctionSignatureList):
        txt = [
            "    me->%s = QUEX_NAME(MF_%s);" % (signature.function_name, signature.function_name)
            for signature in MemberFunctionSignatureList
            if blackboard.condition_holds(signature.condition)
        ]
        return "\n".join(txt)
        
    def RAISE_ERROR_FLAG(self, Name):
        return "self.error_code_set_if_first(&self, %s);\n" % Name

    def MODE_GOTO(self, Mode):
        return "self.enter_mode(&self, %s);" % Mode

    def MODE_GOSUB(self, Mode):
        return "self.push_mode(&self, %s);" % Mode

    def MODE_GOUP(self):
        return "self.pop_mode(&self);"

    def type_replacements(self):
        acn = Setup.analyzer_class_name
        return [
             ("QUEX_TYPE_TOKEN",          "struct %s_tag" % self.NAME_IN_NAMESPACE(Setup.token_class_name, Setup.token_class_name_space)),
             ("QUEX_TYPE0_TOKEN",         "struct %s_tag" % Setup.token_class_name),
             ("QUEX_TYPE_ANALYZER",       "struct %s_tag" % self.NAME_IN_NAMESPACE(Setup.analyzer_class_name, Setup.analyzer_name_space)),
             ("QUEX_TYPE0_ANALYZER",      "struct %s_tag" % Setup.analyzer_class_name),
             ("QUEX_TYPE_MEMENTO",        "struct %s_tag" % self.NAME_IN_NAMESPACE("%s_Memento" % Setup.analyzer_class_name, Setup.analyzer_name_space)),
             ("QUEX_TYPE0_MEMENTO",       "struct %s_Memento_tag" % Setup.analyzer_class_name),
             ("QUEX_TYPE_LEXATOM",        "%s_lexatom_t" % acn),
             ("QUEX_TYPE_TOKEN_ID",       "%s_token_id_t" % acn),
             ("QUEX_TYPE_TOKEN_LINE_N",   "%s_token_line_n_t" % acn),
             ("QUEX_TYPE_TOKEN_COLUMN_N", "%s_token_column_n_t" % acn),
             ("QUEX_TYPE_ACCEPTANCE_ID",  "%s_acceptance_id_t" % acn),
             ("QUEX_TYPE_INDENTATION",    "%s_indentation_t" % acn)
        ]

    def FOOTER_IN_IMPLEMENTATION(self):
        return blackboard.Lng.SOURCE_REFERENCED(blackboard.footer)
