from   quex.input.setup                               import NotificationDB
from   quex.input.regular_expression.pattern          import Pattern_Prep
import quex.input.regular_expression.core             as     regular_expression
from   quex.input.code.base                           import SourceRef, \
                                                             SourceRef_DEFAULT, \
                                                             SourceRefObject
from   quex.engine.state_machine.core                 import StateMachine  
import quex.engine.state_machine.construction.sequentialize as sequentialize
import quex.engine.state_machine.algorithm.beautifier as     beautifier    
import quex.engine.state_machine.check.identity       as     identity
import quex.engine.state_machine.check.tail           as     tail
from   quex.engine.misc.tools                         import typed
from   quex.engine.misc.interval_handling             import NumberSet
from   quex.engine.counter                            import IndentationCount_Pre, \
                                                             CountAction, \
                                                             CountActionMap, \
                                                             cc_type_name_db, \
                                                             cc_type_db
import quex.engine.misc.error                         as     error
import quex.engine.misc.error_check                   as     error_check
from   quex.engine.misc.file_in                       import check, \
                                                             check_or_die, \
                                                             skip_whitespace, \
                                                             read_identifier, \
                                                             read_integer
from   quex.constants  import E_CharacterCountType
from   quex.blackboard import setup as Setup

from   collections import defaultdict
from   operator    import itemgetter

class CountBase_Prep:
    @typed(sr=SourceRef)
    def __init__(self, sr, Name, IdentifierList):
        self.sr                = sr
        self.name              = Name
        self.identifier_list   = IdentifierList
        self._ca_map_specifier = CountActionMap_Prep()

    def _base_parse(self, fh, IndentationSetupF=False):
        """Parses pattern definitions of the form:
       
              [ \t]                                       => grid 4;
              [:intersection([:alpha:], [\X064-\X066]):]  => space 1;

        In other words the right hand side *must* be a character set.

        ADAPTS: result to contain parsing information.
        """

        # NOTE: Catching of EOF happens in caller: parse_section(...)
        #
        while 1 + 1 == 2:
            skip_whitespace(fh)
            if check(fh, ">"): 
                break
            
            # A regular expression state machine
            pattern, identifier, sr = _parse_definition_head(fh, self.identifier_list)
            if pattern is None and IndentationSetupF:
                error.log("Keyword '\\else' cannot be used in indentation setup.", fh)

            # '_parse_definition_head()' ensures that only identifiers mentioned in 
            # 'result' are accepted. 
            if self.requires_count():
                count = _read_value_specifier(fh, identifier, 1)
                self.specify(identifier, pattern, count, sr)
            else:
                self.specify(identifier, pattern, sr)

            if not check(fh, ";"):
                error.log("Missing ';' after '%s' specification." % identifier, fh)

        return # Must be followed by 'finalization'

class LineColumnCount_Prep(CountBase_Prep):
    """Line/column number count specification.
    ___________________________________________________________________________
    The main result of the parsing the the Base's .count_command_map which is 
    an instance of CountActionMap_Prep.
    ____________________________________________________________________________
    """
    @typed(sr=SourceRef)
    def __init__(self, fh):
        sr        = SourceRef.from_FileHandle(fh)
        self.__fh = fh
        CountBase_Prep.__init__(self, sr, 
                                "Line/column counter", 
                                ("space", "grid", "newline")) 

    def parse(self):
        self._base_parse(self.__fh, IndentationSetupF=False)

        # Finalize / Produce 'LineColumnCount' object.
        # 
        ca_map = self._ca_map_specifier.finalize(
                              Setup.buffer_codec.source_set.minimum(), 
                              Setup.buffer_codec.source_set.least_greater_bound(), 
                              self.sr)
        check_grid_values_integer_multiples(ca_map)
        check_defined(ca_map, self.sr, E_CharacterCountType.LINE)
        return ca_map 

    def requires_count(self):
        return True

    @typed(sr=SourceRef, Identifier=(str,unicode))
    def specify(self, Identifier, Pattern, Count, sr):
        if Pattern is None:
            self._ca_map_specifier.define_else(cc_type_db[Identifier], Count, sr)
        else:
            trigger_set = extract_trigger_set(sr, Identifier, Pattern) 
            self._ca_map_specifier.add(trigger_set, cc_type_db[Identifier], Count, sr)

class IndentationCount_Prep(CountBase_Prep):
    """Indentation counter specification.
    ____________________________________________________________________________
    The base's .count_command_map contains information about how to count the 
    space at the beginning of the line. The count until the first non-whitespace
    is the 'indentation'. 
    
    +bad:

    The spec contains information about what characters are not supposed to
    appear in indentation (bad characters). Depending on the philosophical
    basis, some might consider 'space' as evil, others consider 'tab' as evil.

    +newline:

    A detailed state machine can be defined for 'newline'. This might be 
    '\n|(\r\n)' or more complex things.

    +suppressor:

    A newline might be suppressed by '\' for example. For that, it might be
    specified as 'newline suppressor'.
    ____________________________________________________________________________
    """
    @typed(sr=SourceRef)
    def __init__(self, fh):
        sr        = SourceRef.from_FileHandle(fh)
        self.__fh = fh
        self.whitespace_character_set = SourceRefObject("whitespace", None)
        self.bad_space_character_set  = SourceRefObject("bad", None)
        self.sm_newline               = SourceRefObject("newline", None)
        self.sm_newline_suppressor    = SourceRefObject("suppressor", None)
        self.sm_comment_list          = []

        # The base class defines the '._ca_map_specifier'.
        # However, in this class it is only used for error checking.
        CountBase_Prep.__init__(self, sr, "Indentation counter", 
                                ("whitespace", "comment", "newline", "suppressor", "bad"))

    def parse(self):
        self._base_parse(self.__fh, IndentationSetupF=True)

        # Finalize / Produce 'IndentationCount' object.
        # 
        if self.whitespace_character_set.get() is None:
            whitespace = self.__whitespace_default()
            self.__specify_character_set(self.whitespace_character_set, 
                                         "whitespace", whitespace, 
                                         sr=SourceRef_DEFAULT)
        if self.sm_newline.get() is None:
            self.__specify_newline(self.__sm_newline_default(), SourceRef_DEFAULT)

        # -- consistency
        self._consistency_check()

        if self.sm_newline_suppressor.set_f():
            sm_suppressed_newline = sequentialize.do([self.sm_newline_suppressor.get(),
                                                      self.sm_newline.get()])
            sm_suppressed_newline = beautifier.do(sm_suppressed_newline)
        else:
            sm_suppressed_newline = None

        def get_pattern(SM, PS, SR):
            if SM is None: return None
            return Pattern_Prep(SM, PatternString=PS, Sr=SR)

        pattern_comment_list = []
        for sm_comment in self.sm_comment_list:
            only_common_f, \
            common_f       = tail.do(self.sm_newline.get(), sm_comment.get())

            error_check.tail(only_common_f, common_f, 
                             "indentation handler's newline", self.sm_newline.sr, 
                             "comment", sm_comment.sr)
            pattern = get_pattern(sm_comment.get(), 
                                  "<indentation comment>", 
                                  sm_comment.sr)
            pattern_comment_list.append(pattern)

        return IndentationCount_Pre(self.sr, 
                                    self.whitespace_character_set.get(), 
                                    self.bad_space_character_set.get(), 
                                    get_pattern(self.sm_newline.get(), 
                                                "<indentation newline>",
                                                self.sm_newline.sr),
                                    get_pattern(sm_suppressed_newline, 
                                                "<indentation suppressed newline>", 
                                                self.sm_newline_suppressor.sr),
                                    pattern_comment_list)

    def requires_count(self):
        return False

    def specify(self, identifier, pattern, sr):
        if   identifier == "whitespace": 
            self.__specify_character_set(self.whitespace_character_set, 
                                         "whitespace", pattern, sr)
        elif identifier == "bad":        
            self.__specify_character_set(self.bad_space_character_set, 
                                         "bad", pattern, sr)
        elif identifier == "newline":    
            self.__specify_newline(pattern.sm, sr)
        elif identifier == "suppressor": 
            self.__specify_suppressor(pattern.sm, sr)
        elif identifier == "comment":    
            self.__specify_comment(pattern.sm, sr)
        else:                            
            return False
        return True

    @typed(sr=SourceRef)
    def __specify_character_set(self, ref, Name, PatternOrNumberSet, sr):
        cset = extract_trigger_set(sr, Name, PatternOrNumberSet)
        self._ca_map_specifier.add(cset, cc_type_db[Name], None, sr)
        prev_cset = ref.get()
        if prev_cset is None: ref.set(cset, sr)
        else:                 prev_cset.unite_with(cset)

    @typed(sr=SourceRef)
    def __specify_newline(self, Sm, sr):
        assert Sm is not None 
        _error_if_defined_before(self.sm_newline, sr)

        if not Sm.is_DFA_compliant(): Sm = beautifier.do(Sm)

        beginning_char_set = Sm.get_beginning_character_set()
        ending_char_set    = Sm.get_ending_character_set()

        self._ca_map_specifier.add(beginning_char_set, 
                                   E_CharacterCountType.X_BEGIN_NEWLINE, 
                                   None, sr)

        # Do not consider a character from newline twice
        ending_char_set.subtract(beginning_char_set)
        if not ending_char_set.is_empty():
            self._ca_map_specifier.add(ending_char_set, 
                                       E_CharacterCountType.X_END_NEWLINE, 
                                       None, sr)

        self.sm_newline.set(Sm, sr)

    @typed(sr=SourceRef)
    def __specify_suppressor(self, Sm, sr):
        _error_if_defined_before(self.sm_newline_suppressor, sr)

        if not Sm.is_DFA_compliant(): Sm = beautifier.do(Sm)

        self._ca_map_specifier.add(Sm.get_beginning_character_set(), 
                                   E_CharacterCountType.X_BEGIN_NEWLINE_SUPPRESSOR,
                                   None, sr)
        self.sm_newline_suppressor.set(Sm, sr)

    @typed(sr=SourceRef)
    def __specify_comment(self, Sm, sr):
        for before in self.sm_comment_list:
            if not identity.do(before.get(), Sm): continue
            error.log("'comment' has been defined before;", sr, DontExitF=True)
            error.log("at this place.", before.sr)

        if not Sm.is_DFA_compliant(): Sm = beautifier.do(Sm)

        self._ca_map_specifier.add(Sm.get_beginning_character_set(), 
                                   E_CharacterCountType.X_BEGIN_COMMENT_TO_NEWLINE,
                                   None, sr)

        sm_comment = SourceRefObject("comment", None)
        sm_comment.set(Sm, sr)
        self.sm_comment_list.append(sm_comment)

    def __sm_newline_default(self):
        """Default newline: '(\n)|(\r\n)'
        """
        global cc_type_name_db

        newline_set = NumberSet(ord('\n'))
        retour_set  = NumberSet(ord('\r'))

        before = self._ca_map_specifier.find_occupier(newline_set, set())
        if before is not None:
            error.log("Trying to implement default newline: '\\n' or '\\r\\n'.\n" 
                      "The '\\n' option is not possible, since it has been occupied by '%s'.\n" \
                      "No newline can be defined by default. " \
                      "Indentation handlers without newline are unfeasible."
                      % cc_type_name_db[before.cc_type], before.sr) 

        sm = StateMachine.from_character_set(newline_set)

        if Setup.dos_carriage_return_newline_f:
            before = self._ca_map_specifier.find_occupier(retour_set, set())
            if before is not None:
                error.warning("Trying to implement default newline: '\\n' or '\\r\\n'.\n" 
                              "The '\\r\\n' option is not possible, since '\\r' has been occupied by '%s'." \
                              % cc_type_name_db[before.cc_type],
                              before.sr, 
                              SuppressCode=NotificationDB.warning_default_newline_0D_impossible)
            else:
                sm.add_transition_sequence(sm.init_state_index, [retour_set, newline_set])

        return sm

    def __whitespace_default(self):
        """Try to define default whitespace ' ' or '\t' if their positions
        are not yet occupied in the count_command_map.
        """
        cs0 = NumberSet(ord(" "))
        cs1 = NumberSet(ord("\t"))
        result = NumberSet()
        if not self._ca_map_specifier.find_occupier(cs0, set()):
            result.unite_with(cs0)
        if not self._ca_map_specifier.find_occupier(cs1, set()):
            result.unite_with(cs1)

        if result.is_empty():
            error.log("Trying to implement default whitespace ' ' or '\\t' failed.\n"
                      "Characters are occupied by other elements.", self.sr)
        return result

    def _consistency_check(self):
        if     self.sm_newline_suppressor.get() is not None \
           and self.sm_newline.get() is None:
            error.log("A newline 'suppressor' has been defined.\n"
                      "But there is no 'newline' in indentation defintion.", 
                      self.sm_newline_suppressor.sr)


class CountActionMap_Prep(object):
    """Association of character sets with triggered count commands.
    ___________________________________________________________________________

                   list: (character set, CountAction)

    where the 'character set' specifies a subset of characters for which there
    is a definition by the given 'parameter'. The character sets are disjoint.

    This map is used to determine whether actions on character sets are defined 
    more than once. The CountAction contains source references. This allows
    for detailed error messages.
    ___________________________________________________________________________
    """
    __slots__ = ("__map", "__else")
    def __init__(self):
        """Primarily, the '__map' member stores the list of associations between
        character sets and the count command entry. The '__else' contains the 
        count command which waits to be applied to the remaining set of characters.
        """
        self.__map  = CountActionMap()
        self.__else = None

    def finalize(self, GlobalMin, GlobalMax, SourceReference, ForLineColumnCountF=False):
        """After all count commands have been assigned to characters, the 
        remaining character set can be associated with the 'else-CountAction'.
        """
        if self.__else is None: 
            else_cmd = CountAction(E_CharacterCountType.COLUMN, 1, SourceRef_DEFAULT)
            error.warning("No '\else' defined in counter setup. Assume '\else => space 1;'", SourceReference, 
                          SuppressCode=NotificationDB.warning_counter_setup_without_else)
        else:                   
            else_cmd = self.__else
        
        remaining_set = self.get_remaining_set(GlobalMin, GlobalMax)
        if not remaining_set.is_empty():
            self.__map.append((remaining_set, else_cmd))

        return self.__map

    @typed(sr=SourceRef, Identifier=E_CharacterCountType)
    def define_else(self, CC_Type, Value, sr):
        """Define the '\else' character set which is resolved AFTER everything has been 
        defined.
        """
        if self.__else is not None:
            error.log("'\\else has been defined more than once.", sr, 
                      DontExitF=True)
            error.log("Previously, defined here.", self.__else.sr)
        self.__else = CountAction(CC_Type, Value, sr)

    def add(self, CharSet, CC_Type, Value, sr):
        if CharSet.is_empty(): 
            error.log("Empty character set found for '%s'." % cc_type_name_db[CC_Type], sr)
        elif CC_Type == E_CharacterCountType.GRID:
            self.check_grid_specification(Value, sr)
        self.check_intersection(CC_Type, CharSet, sr)
        self.__map.append((CharSet, CountAction(CC_Type, Value, sr)))

    def check_intersection(self, CcType, CharSet, sr):
        """Check whether the given character set 'CharSet' intersects with 
        a character set already mentioned in the map. Depending on the CcType
        of the new candidate certain count commands may be tolerated, i.e. 
        their intersection is not considered.
        """
        intersection_tolerated = {
            E_CharacterCountType.COLUMN:                     (),
            E_CharacterCountType.GRID:                       (),
            E_CharacterCountType.LINE:                       (),
            E_CharacterCountType.WHITESPACE:                 (),
            E_CharacterCountType.BAD:                        (), 
            # Only to detect interference
            E_CharacterCountType.X_BEGIN_NEWLINE_SUPPRESSOR: (),
            E_CharacterCountType.X_BEGIN_NEWLINE:            (E_CharacterCountType.X_END_NEWLINE,),
            E_CharacterCountType.X_END_NEWLINE:              (E_CharacterCountType.X_BEGIN_NEWLINE,),
            E_CharacterCountType.X_BEGIN_COMMENT_TO_NEWLINE: (), 
        }[CcType]

        interferer = self.find_occupier(CharSet, Tolerated=intersection_tolerated)
        if interferer is None:
            return
        _error_set_intersection(CcType, interferer, sr)

    def get_remaining_set(self, GlobalMin, GlobalMax):
        """Return the set of characters which are not associated with count commands.
        Restrict the operation to characters from GlobalMin to GlobalMax (inclusively).
        """
        result = self.__get_remaining_set()
        result.cut_lesser(GlobalMin)
        result.cut_greater_or_equal(GlobalMax)
        return result

    def find_occupier(self, CharSet, Tolerated):
        """Find a command that occupies the given CharSet, at least partly.
           RETURN: None, if no such occupier exists.
        """
        for character_set, before in self.__map:
            if   before.cc_type in Tolerated:                 continue
            elif not character_set.has_intersection(CharSet): continue
            return before
        return None

    def __get_remaining_set(self):
        ignored = (E_CharacterCountType.BAD, 
                   E_CharacterCountType.X_BEGIN_NEWLINE_SUPPRESSOR, 
                   E_CharacterCountType.X_BEGIN_NEWLINE, 
                   E_CharacterCountType.X_END_NEWLINE) 
        result  = NumberSet()
        for character_set, info in self.__map:
            if info.cc_type in ignored: continue
            result.unite_with(character_set)
        return result.get_complement(Setup.buffer_codec.source_set)

    def check_grid_specification(self, Value, sr):
        if   Value == 0: 
            error.log("A grid count of 0 is nonsense. May be define a space count of 0.", sr)
        elif Value == 1:
            error.warning("Indentation grid counts of '1' are equivalent of to a space\n" + \
                          "count of '1'. The latter is faster to compute.",
                          sr)

    def __str__(self):
        def _db_to_text(title, CountOpInfoList):
            txt = "%s:\n" % title
            for character_set, info in sorted(CountOpInfoList, key=lambda x: x[0].minimum()):
                if type(info.value) in [str, unicode]:
                    txt += "    %s by %s\n" % (info.value, character_set.get_utf8_string())
                else:
                    txt += "    %3i by %s\n" % (info.value, character_set.get_utf8_string())
            return txt

        db_by_name = defaultdict(list)
        for character_set, info in self.__map:
            name = cc_type_name_db[info.cc_type]
            db_by_name[name].append((character_set, info))

        txt = [
            _db_to_text(cname, count_command_info_list)
            for cname, count_command_info_list in sorted(db_by_name.iteritems(), key=itemgetter(0))
        ]
        return "".join(txt)

def _parse_definition_head(fh, IdentifierList):

    if check(fh, "\\default"): 
        error.log("'\\default' has been replaced by keyword '\\else' since quex 0.64.9!", fh)
    elif check(fh, "\\else"): 
        pattern = None
    else:                      
        pattern = regular_expression.parse(fh)

    skip_whitespace(fh)
    check_or_die(fh, "=>", " after character set definition.")

    skip_whitespace(fh)
    identifier = read_identifier(fh, OnMissingStr="Missing identifier following '=>'.")
    error.verify_word_in_list(identifier, IdentifierList,
                              "Unrecognized specifier '%s'." % identifier, fh)
    skip_whitespace(fh)

    return pattern, identifier, SourceRef.from_FileHandle(fh)

def _read_value_specifier(fh, Keyword, Default=None):
    skip_whitespace(fh)
    value = read_integer(fh)
    if value is not None:     return value

    # not a number received, is it an identifier?
    variable = read_identifier(fh)
    if   variable != "":      return variable
    elif Default is not None: return Default

    error.log("Missing integer or variable name after keyword '%s'." % Keyword, fh) 

_ca_map_default = None
def LineColumnCount_Default():
    global _ca_map_default

    if _ca_map_default is None:
        specifier = CountActionMap_Prep()
        specifier.add(NumberSet(ord('\n')), E_CharacterCountType.LINE, 1, SourceRef_DEFAULT)
        specifier.add(NumberSet(ord('\t')), E_CharacterCountType.GRID, 4, SourceRef_DEFAULT)
        specifier.define_else(E_CharacterCountType.COLUMN,   1, SourceRef_DEFAULT)     # Define: "\else"
        _ca_map_default = specifier.finalize(Setup.buffer_codec.source_set.minimum(), 
                                             Setup.buffer_codec.source_set.least_greater_bound(), # Apply:  "\else"
                                             SourceRef_DEFAULT) 
    return _ca_map_default


def _error_set_intersection(CcType, Before, sr):
    global cc_type_name_db

    note_f = False
    if    CcType         == E_CharacterCountType.X_END_NEWLINE \
       or Before.cc_type == E_CharacterCountType.X_END_NEWLINE:
        note_f = True

    prefix = {
        E_CharacterCountType.COLUMN:                     "",
        E_CharacterCountType.GRID:                       "",
        E_CharacterCountType.LINE:                       "",
        E_CharacterCountType.BAD:                        "",
        E_CharacterCountType.WHITESPACE:                 "",
        E_CharacterCountType.X_BEGIN_NEWLINE_SUPPRESSOR: "beginning ",
        E_CharacterCountType.X_BEGIN_COMMENT_TO_NEWLINE: "beginning ",
        E_CharacterCountType.X_BEGIN_NEWLINE:            "beginning ",
        E_CharacterCountType.X_END_NEWLINE:              "ending ",
    }[CcType]

    error.log("The %scharacter set defined in '%s' intersects" % (prefix, cc_type_name_db[CcType]),
              sr, DontExitF=True, WarningF=False)
    error.log("with '%s' at this place." % cc_type_name_db[Before.cc_type], 
              Before.sr, DontExitF=note_f, WarningF=False)

    if note_f:
        error.log("Note, for example, 'newline' cannot end with a character which is subject\n"
                  "to indentation counting (i.e. 'space' or 'grid').", sr)

def _error_if_defined_before(Before, sr):
    if not Before.set_f(): return

    error.log("'%s' has been defined before;" % Before.name, sr, 
              DontExitF=True)
    error.log("at this place.", Before.sr)

def extract_trigger_set(sr, Keyword, Pattern):
    if Pattern is None:
        return None
    elif isinstance(Pattern, NumberSet):
        return Pattern

    def check_can_be_matched_by_single_character(SM):
        bad_f      = False
        init_state = SM.get_init_state()
        if SM.get_init_state().is_acceptance(): 
            bad_f = True
        elif len(SM.states) != 2:
            bad_f = True
        # Init state MUST transit to second state. Second state MUST not have any transitions
        elif len(init_state.target_map.get_target_state_index_list()) != 1:
            bad_f = True
        else:
            tmp = set(SM.states.keys())
            tmp.remove(SM.init_state_index)
            other_state_index = tmp.__iter__().next()
            if len(SM.states[other_state_index].target_map.get_target_state_index_list()) != 0:
                bad_f = True

        if bad_f:
            error.log("For '%s' only patterns are addmissible which\n" % Keyword + \
                      "can be matched by a single character, e.g. \" \" or [a-z].", sr)

    check_can_be_matched_by_single_character(Pattern.sm)

    transition_map = Pattern.sm.get_init_state().target_map.get_map()
    assert len(transition_map) == 1
    return transition_map.values()[0]

def check_grid_values_integer_multiples(CaMap):
    """If there are no spaces and the grid is on a homogeneous scale,
       => then the grid can be transformed into 'easy-to-compute' spaces.
    """
    grid_value_list = []
    min_info        = None
    for character_set, info in CaMap:
        if info.cc_type == E_CharacterCountType.COLUMN: 
            return
        elif info.cc_type != E_CharacterCountType.GRID: 
            continue
        elif type(info.value) in (str, unicode): 
            # If there is one single 'variable' grid value, 
            # then no assumptions can be made.
            return
        grid_value_list.append(info.value)
        if min_info is None or info.value < min_info.value:
            min_info = info

    if min_info is None:
        return

    # Are all grid values a multiple of the minimum?
    if all(x % min_info.value == 0 for x in grid_value_list):
        error.warning("Setup does not contain spaces, only grids (tabulators). All grid\n" \
                      "widths are multiples of %i. The grid setup %s is equivalent to\n" \
                      % (min_info.value, repr(sorted(grid_value_list))[1:-1]) + \
                      "a setup with space counts %s. Space counts are faster to compute.\n" \
                      % repr(map(lambda x: x / min_info.value, sorted(grid_value_list)))[1:-1],
                      min_info.sr)
    return

def check_defined(CaMap, SourceReference, CCT):
    """Checks whether the character counter type has been defined in the 
    map.
    
    THROWS: Error in case that is has not been defined.
    """
    for character_set, info in CaMap:
        if info.cc_type == CCT: 
            return

    error.warning("Setup does not define '%s'." % cc_type_name_db[CCT], SourceReference, 
                  SuppressCode=NotificationDB.warning_counter_setup_without_newline)



