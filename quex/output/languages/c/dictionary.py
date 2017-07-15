from   quex.output.languages.cpp.dictionary import Language as LanguageCpp

class Language(LanguageCpp):
    def __init__(self):      
        LanguageCpp.__init__(self)

    def NAMESPACE_REFERENCE(self, NameList, TrailingDelimiterF=True):
        result = "".join("%s_" % name for name in NameList)
        if TrailingDelimiterF: return result
        else:                  return result[:-1]
    def token_template_file(self):    return "/token/TXT-C"     
    def token_template_i_file(self):  return "/token/TXT-C.i"    
    def token_default_file(self):     return "/token/CDefault.qx" 
    def analyzer_template_file(self): return "/analyzer/TXT-C"   

    def NAMESPACE_OPEN(self, NameList):  return ""
    def NAMESPACE_CLOSE(self, NameList): return ""
