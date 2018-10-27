import quex.engine.misc.error                   as     error
from   quex.engine.misc.file_in                 import read_until_character, \
                                                       check, \
                                                       read_identifier, \
                                                       skip_whitespace
import quex.input.regular_expression.core       as     regular_expression
from   quex.input.regular_expression.auxiliary  import PatternShorthand
from   quex.input.code.base                     import SourceRef
import quex.blackboard                          as     blackboard
from   quex.output.syntax_elements              import Signature

from   StringIO import StringIO

def parse(fh):
    """Parses pattern definitions of the form:
   
          WHITESPACE  [ \t\n]
          IDENTIFIER  [a-zA-Z0-9]+
          OP_PLUS     "+"

          \function SOMETHING(sm = X, set = Y, number = N):
          
       That means: 'name' whitespace 'regular expression' whitespace newline.
       Comments can only be '//' nothing else and they have to appear at the
       beginning of the line.
       
       One regular expression can have more than one name, but one name can 
       only have one regular expression.
    """
    skip_whitespace(fh)
    if not check(fh, "{"):
        error.log("define region must start with opening '{'.", fh)

    while 1 + 1 == 2:
        skip_whitespace(fh)

        if check(fh, "}"): 
            return
        
        # Get the name of the pattern
        skip_whitespace(fh)
        if check(fh, "\\function"): name, value = _parse_function(fh)
        else:                       name, value = _parse_pattern(fh)

        blackboard.shorthand_db[name] = value

class FunctionCall:
    def do(self, PatternDict):
        # backup variables that are overwritten by local parameters
        backup_dict = dict(
            (name, value)
            for name, value in PatternDict.iteritems()
            if name in self.variable_names
        )

        # Parse the regular expression
        result = regular_expression.parse(StringIO(self.function_body)).sm

        # reset variables that have been temporarily overwritten
        PatternDict.update(backup_dict)

        return result

def _parse_function(fh):
    signature_str = read_until_character(fh, ":")
    signature     = Signature.from_string(signature_str)
    skip_whitespace(fh)
    # The function body remains a string until it is parsed at expansion time.
    function_body = read_until_character("\n").strip()
    name          = signature.function_name
    value         = FunctionCall(signature, function_body,
                                 Sr=SourceRef.from_FileHandle(fh))
    return name, value

def _parse_pattern(fh):
    name = read_identifier(fh, 
                           OnMissingStr="Missing identifier for pattern definition.")

    if blackboard.shorthand_db.has_key(name):
        error.log("Second definition of pattern '%s'.\n" % name + \
                  "Pattern names must be unique.", fh)

    skip_whitespace(fh)

    if check(fh, "}"): 
        error.log("Missing regular expression for pattern definition '%s'." % \
                  name, fh)

    # No encoding transformation, here. Transformation happens after 
    # expansion in a mode.
    pattern = regular_expression.parse(fh, AllowNothingIsFineF = True) 

    if pattern.has_pre_or_post_context():
        error.log("Pattern definition with pre- and/or post-context.\n" + \
                  "Pre- and Post-Contexts can only be defined inside mode definitions.", fh)
    state_machine = pattern.extract_sm()

    value = PatternShorthand(name, state_machine, SourceRef.from_FileHandle(fh), 
                             pattern.pattern_string())

    return name, value


