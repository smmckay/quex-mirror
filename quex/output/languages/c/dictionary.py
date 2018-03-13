from   quex.output.languages.cpp.dictionary import Language as LanguageCpp
from   quex.constants                       import E_Files

class Language(LanguageCpp):
    all_extension_db = {
        "": {
              E_Files.SOURCE:              ".c",
              E_Files.HEADER:              ".h",
              E_Files.HEADER_IMPLEMTATION: ".c",
        },
    }

    def __init__(self):      
        LanguageCpp.__init__(self)

    def NAMESPACE_REFERENCE(self, NameList, TrailingDelimiterF=True):
        result = "".join("%s_" % name for name in NameList)
        if TrailingDelimiterF: return result
        else:                  return result[:-1]
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
        argument_list_str = ", ".join("%s %s" % (arg_type, arg_name) 
                                      for arg_type, arg_name in signature.argument_list)
        if signature.return_type != "void": return_str = "return "
        else:                               return_str = ""

        if signature.argument_list: me_str = "QUEX_TYPE_ANALYZER* me, "
        else:                       me_str = "QUEX_TYPE_ANALYZER* me"

        return "%s (*%s)(%s%s);\n" % (signature.return_type, 
                                                          signature.function_name, 
                                                          me_str,
                                                          argument_list_str) 

    def MEMBER_FUNCTION_ASSIGNMENT(self, MemberFunctionSignatureList):
        txt = [
            "    me->%s = QUEX_NAME(MF_%s);" % (signature.function_name, signature.function_name)
            for signature in MemberFunctionSignatureList
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

