import quex.engine.utf8                   as utf8
from   quex.engine.interval_handling      import NumberSet
from   quex.engine.misc.file_in           import error_msg
from   quex.blackboard                    import E_IncidenceIDs, \
                                                 setup as Setup

__line_counter_in_loop = """
    __QUEX_IF_COUNT_LINES_IF( input == (QUEX_TYPE_CHARACTER)%s ) { 
        __QUEX_IF_COUNT_LINES_ADD((size_t)1);
    }
"""

def line_counter_in_loop():
    TrafoInfo = Setup.buffer_codec_transformation_info
    if TrafoInfo is None: return __line_counter_in_loop % "'\\n'"

    newline_code = get_newline_in_codec(TrafoInfo)
    if newline_code is None: return "" # Codec does not have newline
    else:                    return __line_counter_in_loop % newline_code


__line_column_counter_in_loop = """
    __QUEX_IF_COUNT_IF( input == (QUEX_TYPE_CHARACTER)%s ) { 
        __QUEX_IF_COUNT_LINES_ADD((size_t)1);
        __QUEX_IF_COUNT_COLUMNS_SET((size_t)0);
        __QUEX_IF_COUNT_COLUMNS(reference_p = QUEX_NAME(Buffer_tell_memory_adr)(&me->buffer));
    }
"""

def line_column_counter_in_loop():
    TrafoInfo = Setup.buffer_codec_transformation_info
    if TrafoInfo is None: return __line_column_counter_in_loop % "'\\n'"

    newline_code = get_newline_in_codec(TrafoInfo)
    if newline_code is None: return "" # Codec does not have newline
    else:                    return __line_column_counter_in_loop % newline_code

def get_newline_in_codec(TrafoInfo):
    """Translate the code for the newline character into the given codec by 'TrafoInfo'.

       RETURNS: None if the transformation is not possible.
    """
    tmp = NumberSet(ord('\n'))
    if isinstance(TrafoInfo, (str, unicode)):
        if   TrafoInfo == "utf8-state-split":  pass
        elif TrafoInfo == "utf16-state-split": pass
        else:                                  
            error_msg("Character encoding '%s' unknown to skipper.\n" % TrafoInfo + \
                      "For line number counting assume code of newline character code to be '0x%02X'." % ord('\n'),
                      DontExitF=True)
        return ord('\n')

    tmp.transform(TrafoInfo)
    return tmp.get_the_only_element() # Returns 'None' if there is none

def get_character_sequence(Sequence):
    txt         = ""
    comment_txt = ""
    for letter in Sequence:
        comment_txt += "%s, " % utf8.unicode_to_pretty_utf8(letter)
        txt += "0x%X, " % letter

    return txt, comment_txt

def get_on_skip_range_open(ModeName, OnSkipRangeOpen, CloserSequence):
    """For unit tests 'Mode' may actually be a string, so that we do not
       have to generate a whole mode just to get the 'on_skip_range_open' 
       code fragment.
    """
    if Mode is None: return ""

    txt = ""
    if not Mode.incidence_db.has_key(E_IncidenceIDs.SKIP_RANGE_OPEN):
        txt += 'QUEX_ERROR_EXIT("\\nLexical analyzer mode \'%s\':\\n"\n' % ModeName + \
               '                "End of file occurred before closing skip range delimiter!\\n"' + \
               '                "The \'on_skip_range_open\' handler has not been specified.");'
    else:
        closer_string = ""
        for letter in CloserSequence:
            closer_string += utf8.unicode_to_pretty_utf8(letter).replace("'", "")

        txt  = "#define Closer \"%s\"\n" % closer_string
        txt += Mode.incidence_db[E_IncidenceIDs.SKIP_RANGE_OPEN].get_text()
        txt += "#undef  Closer\n"
        txt += "RETURN;\n"

    return txt


