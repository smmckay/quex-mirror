# Database of all supported languages.
# 
# (C) Frank-Rene Schaefer
#______________________________________________________________________________
from   quex.output.languages.cpp.dictionary      import Language as LanguageCpp
from   quex.output.languages.c.dictionary        import Language as LanguageC
from   quex.output.languages.graphviz.dictionary import Language as LanguageGraphViz

db = {
    "C++": LanguageCpp,
    "C":   LanguageC,
    "DOT": LanguageGraphViz
}



