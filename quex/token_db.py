from   quex.input.code.base import SourceRef, \
                                   SourceRef_VOID

class TokenInfo:
    def __init__(self, Name, ID, TypeName=None, SourceReference=SourceRef_VOID):
        self.name         = Name
        self.number       = ID
        self.related_type = TypeName
        self.id           = None
        self.sr           = SourceReference

#-----------------------------------------------------------------------------------------
# token_id_db: list of all defined token-ids together with the file position
#              where they are defined. See token_ide_maker, class TokenInfo.
#-----------------------------------------------------------------------------------------
token_id_db = {}

def get_used_token_id_set():
    return [ token.number for token in token_id_db.itervalues() if token.number is not None ]

def token_id_db_enter(fh, TokenIdName, NumericValue=None):
    global token_id_db
    if isinstance(fh, SourceRef): sr = fh
    elif fh is not None:          sr = SourceRef.from_FileHandle(fh)
    else:                         sr = None
    ti = TokenInfo(TokenIdName, NumericValue, SourceReference=sr)
    token_id_db[TokenIdName] = ti

#-----------------------------------------------------------------------------------------
# token_id_foreign_set: Set of token ids which came from an external token id file.
#                       All tokens which are not defined in an external token id file
#                       are defined by quex.
#-----------------------------------------------------------------------------------------
token_id_foreign_set = set()

#-----------------------------------------------------------------------------------------
# token_id_implicit_list: Keep track of all token identifiers that ware defined 
#                         implicitly, i.e. not in a token section or in a token id file. 
#                         Each list element has three cells:
#                         [ Prefix-less Token ID, Line number in File, File Name]
#-----------------------------------------------------------------------------------------
token_id_implicit_list = []

#-----------------------------------------------------------------------------------------
# token_repetition_support: Quex can be told to return multiple times the same
#                           token before further analyzsis happens. For this,
#                           the engine needs to know how to read and write the
#                           repetition number in the token itself.
# If the 'token_repetition_token_id_list' is None, then the token repetition feature
# is disabled. Otherwise, token repetition in 'token-receiving.i' is enabled
# and the token id that can be repeated is 'token_repetition_token_id'.
#-----------------------------------------------------------------------------------------
token_repetition_token_id_list = ""

#-----------------------------------------------------------------------------------------
# token_type_definition: Object that defines a (user defined) token class.
#
# The first token_type section defines the variable as a real 'TokenTypeDescriptor'.
#
# The setup_parser.py checks for the specification of a manually written token class file. 
# If so then an object of type 'ManualTokenClassSetup' is assigned.
#
# Default = None is detected by the 'input/file/core.py' and triggers the parsing of the 
# default token type description. 
#          
#-----------------------------------------------------------------------------------------
token_type_definition = None

