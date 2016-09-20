# (C) Frank-Rene Schaefer
#
#        .--( LineColumnCount )--------------------------------.
#        |                                                     |
#        | + count_command_map (map: count command --> value)  |
#        '-----------------------------------------------------'
#
#
#        .--( IndentationCount ---> LineColumnCount )----------.
#        |                                                     |
#        | + whitespace_character_set                          |
#        | + bad_space_character_set                           |
#        | + sm_newline                                        |
#        | + sm_newline_suppressor                             |
#        | + sm_comment                                        |
#        '-----------------------------------------------------'
#
# (C) Frank-Rene Schaefer
#______________________________________________________________________________                      

from   quex.input.code.base                        import SourceRef
import quex.engine.analyzer.door_id_address_label  as     dial
from   quex.engine.operations.operation_list       import Op
from   quex.engine.misc.tools                      import typed
from   quex.engine.misc.interval_handling          import NumberSet, NumberSet_All
import quex.engine.misc.error                      as     error

from   quex.blackboard import setup as Setup, \
                              E_CharacterCountType, \
                              E_R
from   collections     import namedtuple, defaultdict
from   operator        import itemgetter
from   itertools       import izip

cc_type_db = {
    "space":                     E_CharacterCountType.COLUMN,
    "grid":                      E_CharacterCountType.GRID,
    "newline":                   E_CharacterCountType.LINE,
    "bad":                       E_CharacterCountType.BAD,
    "whitespace":                E_CharacterCountType.WHITESPACE,
    # Following are only webbed into the 'CA_Map' to detect overlaps:
    "begin(newline suppressor)": E_CharacterCountType.X_BEGIN_NEWLINE_SUPPRESSOR,
    "begin(newline)":            E_CharacterCountType.X_BEGIN_NEWLINE,
    "begin(comment to newline)": E_CharacterCountType.X_BEGIN_COMMENT_TO_NEWLINE,
    "end(newline)":              E_CharacterCountType.X_END_NEWLINE,
}

cc_type_name_db = dict((value, key) for key, value in cc_type_db.iteritems())

count_operation_db_without_reference = {
    E_CharacterCountType.BAD:    lambda Parameter, Dummy=None: [ 
        Op.GotoDoorId(Parameter)
    ],
    E_CharacterCountType.COLUMN: lambda Parameter, Dummy=None: [
        Op.ColumnCountAdd(Parameter)
    ],
    E_CharacterCountType.GRID:   lambda Parameter, Dummy=None: [
        Op.ColumnCountGridAdd(Parameter)
    ],
    E_CharacterCountType.LINE:   lambda Parameter, Dummy=None: [
        Op.LineCountAdd(Parameter),
        Op.AssignConstant(E_R.Column, 1),
    ],
    E_CharacterCountType.LOOP_ENTRY: lambda Parameter, Dummy=None: [ 
    ],
    E_CharacterCountType.LOOP_EXIT: lambda Parameter, Dummy=None: [ 
    ],
    E_CharacterCountType.COLUMN_BEFORE_APPENDIX_SM: lambda Parameter, ColumnNPerCodeUnit: [
        Op.ColumnCountAdd(Parameter)
    ],
    E_CharacterCountType.BEFORE_RELOAD: lambda Parameter, Dummy=None: [ 
    ],
    E_CharacterCountType.AFTER_RELOAD: lambda Parameter, Dummy=None: [ 
    ],
}

count_operation_db_with_reference = {
    E_CharacterCountType.BAD:    lambda Parameter, ColumnNPerCodeUnit: [
        Op.ColumnCountReferencePDeltaAdd(E_R.InputP, ColumnNPerCodeUnit, False),
        Op.ColumnCountReferencePSet(E_R.InputP),
        Op.GotoDoorId(Parameter) 
    ],
    E_CharacterCountType.COLUMN: lambda Parameter, ColumnNPerCodeUnit: [
    ],
    E_CharacterCountType.GRID:   lambda Parameter, ColumnNPerCodeUnit: [
        Op.ColumnCountReferencePDeltaAdd(E_R.InputP, ColumnNPerCodeUnit, True),
        Op.ColumnCountGridAdd(Parameter),
        Op.ColumnCountReferencePSet(E_R.InputP)
    ],
    E_CharacterCountType.LINE:   lambda Parameter, ColumnNPerCodeUnit: [
        Op.LineCountAdd(Parameter),
        Op.AssignConstant(E_R.Column, 1),
        Op.ColumnCountReferencePSet(E_R.InputP)
    ],
    E_CharacterCountType.LOOP_ENTRY: lambda Parameter, ColumnNPerCodeUnit: [ 
        Op.ColumnCountReferencePSet(Parameter) 
    ],
    E_CharacterCountType.LOOP_EXIT: lambda Parameter, ColumnNPerCodeUnit: [ 
        Op.ColumnCountReferencePDeltaAdd(Parameter, ColumnNPerCodeUnit, False) 
    ],
    E_CharacterCountType.COLUMN_BEFORE_APPENDIX_SM: lambda Parameter, ColumnNPerCodeUnit: [
        Op.ColumnCountReferencePDeltaAdd(Parameter, ColumnNPerCodeUnit, False),
        Op.ColumnCountReferencePSet(E_R.InputP)
    ],
    # BEFORE RELOAD:                                            input_p
    #                                                           |
    #                [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
    #                                            |
    #                                            reference_p
    #    
    #     column_n += (input_p - reference_p) * ColumnNPerCodeUnit
    #
    #  AFTER RELOAD:  input_p
    #                 |
    #                [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
    #                 |
    #                 reference_p                                   
    #       
    E_CharacterCountType.BEFORE_RELOAD: lambda Parameter, ColumnNPerCodeUnit: [ 
        Op.ColumnCountReferencePDeltaAdd(Parameter, ColumnNPerCodeUnit, False) 
    ],
    E_CharacterCountType.AFTER_RELOAD: lambda Parameter, ColumnNPerCodeUnit: [ 
        Op.ColumnCountReferencePSet(Parameter) 
    ],
}

class CountAction(namedtuple("CountAction", ("cc_type", "value", "sr"))):
    def __new__(self, CCType, Value, sr=None):
        return super(CountAction, self).__new__(self, CCType, Value, sr)

    incidence_id_db = {}
    @classmethod
    def incidence_id_db_get(cls, CA):
        """RETURNS: Unique incidence id for a given count action.

        Same count actions will have the same incidence id. Initialize the 
        'incidence_id_db' with 'CountAction.incidence_id_db.clear()' before 
        generating a new set of count action incidence ids.
        """
        key = (CA.cc_type, CA.value)
        incidence_id = CA.incidence_id_db.get(key)
        if incidence_id is None:
            incidence_id = dial.new_incidence_id()
            CA.incidence_id_db[key] = incidence_id
        return incidence_id

    def get_OpList(self, ColumnCountPerChunk):
        if ColumnCountPerChunk is None:
            return count_operation_db_without_reference[self.cc_type](self.value)
        else:
            return count_operation_db_with_reference[self.cc_type](self.value, 
                                                                   ColumnCountPerChunk)

    def is_equal(self, Other):
        """Two Count Actions are equal, if the CC-Type and the Parameter are
        the same. The source reference (.sr) does not have to be the equal.
        """
        if   self.cc_type != Other.cc_type: return False
        elif self.value != Other.value:     return False
        else:                               return True

class CountActionMap(list):
    """Map: NumberSet --> CountAction
    """
    @staticmethod
    def from_list(NsCaList):
        result = CountActionMap()
        for entry in NsCaList:
            result.append(entry)
        return result

    def pruned_clone(self, SubSet):
        return CountActionMap.from_list(self.iterable_in_sub_set(SubSet))

    def get_count_commands(self, CharacterSet):
        """Finds the count command for column, grid, and newline. This does NOT
        consider 'chunk number per character'. The consideration is on pure 
        character (unicode) level.
        
        RETURNS: [0] column increment (None, if none, -1 if undetermined)
                 [1] grid step size   (None, if none, -1 if undetermined)
                 [2] line increment   (None, if none, -1 if undetermined)

            None --> no influence from CharacterSet on setting.
            '-1' --> no distinct influence from CharacterSet on setting.
                     (more than one possible).

        NOTE: If one value not in (None, -1), then all others must be None.
        """

        db = {
            E_CharacterCountType.COLUMN: None,
            E_CharacterCountType.GRID:   None,
            E_CharacterCountType.LINE:   None,
        }

        for character_set, entry in self:
            if entry.cc_type not in db: 
                continue
            elif character_set.is_superset(CharacterSet):
                db[entry.cc_type] = entry.value
                break
            elif character_set.has_intersection(CharacterSet): 
                db[entry.cc_type] = -1     

        return db[E_CharacterCountType.COLUMN], \
               db[E_CharacterCountType.GRID], \
               db[E_CharacterCountType.LINE]

    def column_grid_line_iterable_pruned(self, CharacterSet):
        """Iterate over count command map. It is assumed that anything in the map
        is 'valid'. 
        """
        considered_set = (E_CharacterCountType.COLUMN, 
                          E_CharacterCountType.GRID, 
                          E_CharacterCountType.LINE)
        for character_set, info in self:
            if character_set.has_intersection(CharacterSet):
                if info.cc_type not in considered_set: continue
                yield character_set.intersection(CharacterSet), info

    @typed(CharacterSet=(NumberSet, None))
    def get_column_number_per_code_unit(self, CharacterSet=None):
        """Considers the counter database which tells what character causes
        what increment in line and column numbers. However, only those characters
        are considered which appear in the CharacterSet. 

        RETURNS: None -- If there is NO distinct column increment.
                 >= 0 -- The increment of column number for every character
                         from CharacterSet.
        """
        # MOST LIKELEY: CharacterSet is None always
        if CharacterSet is None: CharacterSet = NumberSet_All()
        column_incr_per_character = None
        number_set                = None
        for character_set, info in self.column_grid_line_iterable_pruned(CharacterSet):
            if info.cc_type != E_CharacterCountType.COLUMN: 
                continue
            elif column_incr_per_character is None:       
                column_incr_per_character = info.value
                number_set                = character_set
            elif column_incr_per_character == info.value: 
                number_set.unite_with(character_set)
            else:
                return None

        if column_incr_per_character is None:
            return None                       # TODO: return 0

        # HERE: There is only ONE 'column_n_increment' command. It appears on
        # the character set 'number_set'. If the character set is represented
        # by the same number of chunks, than the column number per chunk is
        # found.
        if not Setup.buffer_codec.variable_character_sizes_f():
            return column_incr_per_character

        chunk_n_per_character = \
            Setup.buffer_codec.lexatom_n_per_character(number_set) 
        if chunk_n_per_character is None:
            return None
        else:
            return float(column_incr_per_character) / chunk_n_per_character

    def union_of_all(self):
        return NumberSet.from_union_of_iterable(
            number_set for number_set, ca in self
        )

    def iterable_in_sub_set(self, SubSet):
        """Searches for CountInfo objects where the character set intersects
        with the 'SubSet' given as arguments. 

        YIELDS: [0] NumberSet where the trigger set intersects with SubSet
                [1] Related 'CountAction' object.
        """
        for character_set, count_action in self:
            intersection = SubSet.intersection(character_set)
            if intersection.is_empty(): continue
            yield intersection, count_action

    def is_equal(self, Other):
        if len(self) != len(Other):
            return False
        for x, y in izip(self, Other):
            x_number_set, x_count_action = x
            y_number_set, y_count_action = y
            if not x_number_set.is_equal(y_number_set):
                return False
            elif not x_count_action.is_equal(y_count_action):
                return False
        return True

    def __str__(self):
        def _db_to_text(title, CountCmdInfoList):
            txt = "%s:\n" % title
            for character_set, info in sorted(CountCmdInfoList, key=lambda x: x[0].minimum()):
                if type(info.value) in [str, unicode]:
                    txt += "    %s by %s\n" % (info.value, character_set.get_utf8_string())
                else:
                    txt += "    %3i by %s\n" % (info.value, character_set.get_utf8_string())
            return txt

        db_by_name = defaultdict(list)
        for character_set, info in self:
            name = cc_type_name_db[info.cc_type]
            db_by_name[name].append((character_set, info))

        txt = [
            _db_to_text(cname, count_command_info_list)
            for cname, count_command_info_list in sorted(db_by_name.iteritems(), key=itemgetter(0))
        ]
        return "".join(txt)

class CountBase:
    pass
         
class LineColumnCount(CountBase):
    def __init__(self, SourceReference, CountActionMap=None):
        self.sr = SourceReference
        # During Parsing: The 'count_command_map' is specified later.
        self.count_command_map = CountActionMap

    def get_column_number_per_code_unit(self, CharacterSet=None):
        return self.count_command_map.get_column_number_per_code_unit(CharacterSet)

class IndentationCount(LineColumnCount):
    @typed(sr=SourceRef,PatternListComment=list)
    def __init__(self, SourceReference,  
                 WhiteSpaceCharacterSet, BadSpaceCharacterSet,
                 PatternNewline, PatternSuppressedNewline, 
                 PatternListComment):
        """BadSpaceCharacterSet = None, if there is no definition of bad space.
        """
        LineColumnCount.__init__(self, SourceReference, None)
        self.whitespace_character_set   = WhiteSpaceCharacterSet
        self.bad_space_character_set    = BadSpaceCharacterSet
        self.pattern_newline            = PatternNewline
        self.pattern_suppressed_newline = PatternSuppressedNewline
        self.pattern_comment_list       = PatternListComment

    def finalize(self, CaMap):
        def _finalize(P, CaMap):
            if P: return P.finalize(CaMap)
            else: return None

        self.pattern_newline            = _finalize(self.pattern_newline, 
                                                    CaMap)
        self.pattern_suppressed_newline = _finalize(self.pattern_suppressed_newline, 
                                                    CaMap) 
        for pattern_comment in self.pattern_comment_list:
            self.pattern_comment = _finalize(pattern_comment, CaMap) 
        return self

    def get_sm_newline(self):
        return self.__get_sm(self.pattern_newline)

    def get_sm_suppressed_newline(self):
        return self.__get_sm(self.pattern_suppressed_newline)

    def get_sm_comment_list(self):
        return [ x.sm for x in self.pattern_comment_list if x.sm is not None ]


    def __get_sm(self, P):
        if P: return P.sm
        else: return None

    def __str__(self):
        def cs_str(Name, Cs):
            if Cs is None: return ""
            msg  = "%s:\n" % Name
            if Cs is None: msg += "    <none>\n" 
            else:          msg += "    %s\n" % Cs.get_utf8_string()
            return msg

        def sm_str(Name, Pattern):
            if Pattern is None or Pattern.sm is None: return ""
            Sm = Pattern.sm
            msg = "%s:\n" % Name
            if Sm is None: 
                msg += "    <none>\n"
            else:          
                msg += "    %s\n" % Sm.get_string(NormalizeF=True, Option="utf8").replace("\n", "\n    ").strip()
            return msg

        txt = [ 
            cs_str("Whitespace",    self.whitespace_character_set),
            cs_str("Bad",           self.bad_space_character_set),
            sm_str("Newline",       self.pattern_newline),
            sm_str("Suppressed Nl", self.pattern_suppressed_newline)
        ]

        if self.pattern_comment_list is not None:
            txt.extend(
                sm_str("Comment", p)
                for p in self.pattern_comment_list
            )

        return "".join(txt)

def _error_set_intersection(CcType, Before, sr):
    global cc_type_name_db

    note_f = False
    if    CcType         == E_CharacterCountType.X_END_NEWLINE \
       or Before.cc_type == E_CharacterCountType.X_END_NEWLINE:
        note_f = True

    prefix = {
        E_CharacterCountType.COLUMN:                   "",
        E_CharacterCountType.GRID:                     "",
        E_CharacterCountType.LINE:                     "",
        E_CharacterCountType.BAD:                      "",
        E_CharacterCountType.WHITESPACE:               "",
        # Interference detection only
        E_CharacterCountType.X_BEGIN_NEWLINE_SUPPRESSOR: "beginning ",
        E_CharacterCountType.X_BEGIN_NEWLINE:            "beginning ",
        E_CharacterCountType.X_END_NEWLINE:              "ending ",
        E_CharacterCountType.X_BEGIN_COMMENT_TO_NEWLINE: "beginning ",
    }[CcType]

    error.log("The %scharacter set defined in '%s' intersects" % (prefix, cc_type_name_db[CcType]),
              sr, DontExitF=True)
    error.log("with '%s' at this place." % cc_type_name_db[Before.cc_type], 
              Before.sr, DontExitF=note_f)

    if note_f:
        error.log("Note, for example, 'newline' cannot end with a character which is subject\n"
                  "to indentation counting (i.e. 'space' or 'grid').", sr)

