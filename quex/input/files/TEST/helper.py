from   quex.input.files.specifier.mode import Mode_PrepPrep     
from   quex.input.files.mode           import __parse_element as parse_mode_element
from   quex.input.files.core           import parse_default_token_definition
from   quex.input.code.base            import SourceRef
import quex.output.languages.core      as     languages
from   quex.token_db                   import token_id_db, token_id_db, token_id_implicit_list
from   quex.blackboard                 import setup as Setup

from   StringIO import StringIO

Setup.token_id_prefix_plain = "TOKEN_"
Setup.token_class_name      = "Token"
Setup.language_db = languages.db["C++"]()
parse_default_token_definition({})

def test(Command, Txt):
    token_id_db.clear()
    del token_id_implicit_list[:]
    print "________________________________________________________"
    print 
    expr     = "%s%s" % (Command, Txt)
    sh       = StringIO(expr)
    new_mode = Mode_PrepPrep("UT_Mode", SourceRef.from_FileHandle(sh))
    parse_mode_element(new_mode, sh)
    print expr
    print
    for pap in new_mode.pattern_action_pair_list:
        pattern_str = pap.pattern().pattern_string()
        action_str  = pap.action().get_text()
        print "    '%s' -> %s" % (pattern_str, action_str)

    print "    Token Identifiers: %s" % repr(sorted(token_id_db.keys())).replace("[", "").replace("]", "")
    print "    Token Identifiers(implicit): %s" % repr([x[0] for x in token_id_implicit_list]).replace("[", "").replace("]", "")
    print
