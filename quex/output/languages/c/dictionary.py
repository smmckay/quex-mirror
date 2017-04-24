from   quex.output.languages.cpp.dictionary import Language as LanguageCpp

class Language(LanguageCpp):
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

