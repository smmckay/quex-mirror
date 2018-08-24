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
from   quex.engine.operations.operation_list       import Op
from   quex.engine.misc.tools                      import typed, do_and_delete_if
from   quex.engine.misc.interval_handling          import NumberSet
import quex.engine.misc.error                      as     error

from   quex.blackboard import setup as Setup
from   quex.constants  import E_CharacterCountType, \
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
    E_CharacterCountType.BAD:    lambda Parameter, Dummy=None, Dummy2=None: [ 
        Op.GotoDoorId(Parameter)
    ],
    E_CharacterCountType.COLUMN: lambda Parameter, Dummy=None, Dummy2=None: [
        Op.ColumnCountAdd(Parameter)
    ],
    E_CharacterCountType.GRID:   lambda Parameter, Dummy=None, Dummy2=None: [
        Op.ColumnCountGridAdd(Parameter)
    ],
    E_CharacterCountType.LINE:   lambda Parameter, Dummy=None, Dummy2=None: [
        Op.LineCountAdd(Parameter),
        Op.AssignConstant(E_R.Column, 1),
    ],
    E_CharacterCountType.LOOP_ENTRY: lambda Parameter, Dummy=None, Dummy2=None: [ 
    ],
    E_CharacterCountType.LOOP_EXIT: lambda Parameter, Dummy=None, Dummy2=None: [ 
    ],
    E_CharacterCountType.COLUMN_BEFORE_APPENDIX_SM: lambda Parameter, ColumnNPerCodeUnit, ColumnAdd: [
        Op.ColumnCountAdd(ColumnAdd)
    ],
    E_CharacterCountType.BEFORE_RELOAD: lambda Parameter, Dummy=None, Dummy2=None: [ 
    ],
    E_CharacterCountType.AFTER_RELOAD: lambda Parameter, Dummy=None, Dummy2=None: [ 
    ],
}

count_operation_db_with_reference = {
    E_CharacterCountType.BAD:    lambda Parameter, ColumnNPerCodeUnit, Dummy=None: [
        Op.ColumnCountReferencePDeltaAdd(E_R.InputP, ColumnNPerCodeUnit, False),
        Op.ColumnCountReferencePSet(E_R.InputP),
        Op.GotoDoorId(Parameter) 
    ],
    E_CharacterCountType.COLUMN: lambda Parameter, ColumnNPerCodeUnit, Dummy=None: [
    ],
    E_CharacterCountType.GRID:   lambda Parameter, ColumnNPerCodeUnit, Dummy=None: [
        Op.ColumnCountReferencePDeltaAdd(E_R.InputP, ColumnNPerCodeUnit, True),
        Op.ColumnCountGridAdd(Parameter),
        Op.ColumnCountReferencePSet(E_R.InputP)
    ],
    E_CharacterCountType.LINE:   lambda Parameter, ColumnNPerCodeUnit, Dummy=None: [
        Op.LineCountAdd(Parameter),
        Op.AssignConstant(E_R.Column, 1),
        Op.ColumnCountReferencePSet(E_R.InputP)
    ],
    E_CharacterCountType.LOOP_ENTRY: lambda Parameter, ColumnNPerCodeUnit, Dummy=None: [ 
        Op.ColumnCountReferencePSet(Parameter) 
    ],
    E_CharacterCountType.LOOP_EXIT: lambda Parameter, ColumnNPerCodeUnit, Dummy=None: [ 
        Op.ColumnCountReferencePDeltaAdd(Parameter, ColumnNPerCodeUnit, False) 
    ],
    E_CharacterCountType.COLUMN_BEFORE_APPENDIX_SM: lambda Parameter, ColumnNPerCodeUnit, Dummy=None: [
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
    E_CharacterCountType.BEFORE_RELOAD: lambda Parameter, ColumnNPerCodeUnit, Dummy=None: [ 
        Op.ColumnCountReferencePDeltaAdd(Parameter, ColumnNPerCodeUnit, False) 
    ],
    E_CharacterCountType.AFTER_RELOAD: lambda Parameter, ColumnNPerCodeUnit, Dummy=None: [ 
        Op.ColumnCountReferencePSet(Parameter) 
    ],
}

class CountAction(namedtuple("CountAction", ("cc_type", "value", "extra_value", "sr"))):
    def __new__(self, CCType, Value, sr=None, ExtraValue=None):
        return super(CountAction, self).__new__(self, CCType, Value, ExtraValue, sr)

    def get_OpList(self, ColumnCountPerChunk):
        if ColumnCountPerChunk is None:
            db = count_operation_db_without_reference
        else:
            db = count_operation_db_with_reference

        return db[self.cc_type](self.value, ColumnCountPerChunk, self.extra_value)

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

    def prune(self, SuperSet):
        """Prune all NumberSets in the CountActionMap, so that they fit in the 
        'SuperSet'. If a NumberSets is not a subset of 'SuperSet' at all, then the
        according action is removed.
        """
        def do(element, SuperSet):
            character_set, count_action = element
            character_set.intersect_with(SuperSet)
            return character_set.is_empty()

        do_and_delete_if(self, do, SuperSet)

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

    def get_column_number_per_code_unit(self):
        """Considers the counter database which tells what character causes
        what increment in line and column numbers. However, only those characters
        are considered which appear in the CharacterSet. 

        RETURNS: None -- If there is NO distinct column increment.
                 >= 0 -- The increment of column number for every character
                         from CharacterSet.
        """
        CharacterSet = Setup.buffer_encoding.source_set
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
        if not Setup.buffer_encoding.variable_character_sizes_f():
            return column_incr_per_character

        chunk_n_per_character = \
            Setup.buffer_encoding.lexatom_n_per_character(number_set) 
        if chunk_n_per_character is None:
            return None
        else:
            return float(column_incr_per_character) / chunk_n_per_character

    def union_of_all(self):
        return NumberSet.from_union_of_iterable(
            number_set for number_set, ca in self
        )

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

class IndentationCount_Pre:
    @typed(sr=SourceRef,PatternListComment=list)
    def __init__(self, SourceReference,  
                 WhiteSpaceCharacterSet, BadSpaceCharacterSet,
                 PatternNewline, PatternSuppressedNewline, 
                 PatternListComment):
        """BadSpaceCharacterSet = None, if there is no definition of bad space.
        """
        self.sr                         = SourceReference
        self.whitespace_character_set   = WhiteSpaceCharacterSet
        self.bad_space_character_set    = BadSpaceCharacterSet
        self.pattern_newline            = PatternNewline
        self.pattern_suppressed_newline = PatternSuppressedNewline
        self.pattern_comment_list       = PatternListComment

    def finalize(self, CaMap):
        def _finalize(P, CaMap):
            if P: return P.finalize(CaMap)
            else: return None

        pattern_newline            = _finalize(self.pattern_newline, 
                                               CaMap)
        pattern_suppressed_newline = _finalize(self.pattern_suppressed_newline, 
                                               CaMap) 
        pattern_comment_list = [
            _finalize(pattern_comment, CaMap) 
            for pattern_comment in self.pattern_comment_list
        ]
        return IndentationCount(self.sr, 
                                self.whitespace_character_set, 
                                self.bad_space_character_set,
                                pattern_newline,
                                pattern_suppressed_newline,
                                pattern_comment_list)

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

class IndentationCount:
    def __init__(self, SourceReference,  
                 WhiteSpaceCharacterSet, BadSpaceCharacterSet,
                 PatternNewline, PatternSuppressedNewline, 
                 PatternListComment):
        """BadSpaceCharacterSet = None, if there is no definition of bad space.
        """
        self.sr                         = SourceReference
        self.whitespace_character_set   = WhiteSpaceCharacterSet
        self.bad_space_character_set    = BadSpaceCharacterSet
        self.pattern_newline            = PatternNewline
        self.pattern_suppressed_newline = PatternSuppressedNewline
        self.pattern_comment_list       = PatternListComment

    def get_sm_newline(self):
        return self.__get_sm(self.pattern_newline)

    def get_sm_suppressed_newline(self):
        return self.__get_sm(self.pattern_suppressed_newline)

    def get_sm_comment_list(self):
        return [ x.sm for x in self.pattern_comment_list if x.sm is not None ]

    def __get_sm(self, P):
        if P: return P.sm
        else: return None

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

