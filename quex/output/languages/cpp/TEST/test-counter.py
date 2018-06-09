#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# PURPOSE: 
#
# Test character counting functionality for different encodings. The set of encodings
# include constant and dynamic character size encodings. For all encodings the
# 'collaboration' with grid and line number counting is tested.
#
# Codecs: ASCII, UTF8, UTF16, UTF32, CP737
# 
# Counter Databases: (1) Default, where a reference pointer counting can be 
#                        implemented.
#                    (2) A dedicated counter database where no reference 
#                        counter implementation is possible.
#
# For encodings with variable character sizes, the second number in the choice
# defines the number of chunks to be used for a letter. For example, 'utf_8-3'
# means that letters are used that consist of three bytes.
#
# Test cases are created from a 'test_list' (see variable below). For 'higher'
# encodings (UTF8, ...) the letters 'a', 'b', 'c' ... are sometimes replaced by
# letters from higher unicode code pages. For example, when three bytes are
# to be setup, letters from 0x800 to 0xFFFF are used for utf8. 
#
# The usage of a reference pointer in the generated code is verified at
# this point [RP]. 
#
# The setup of characters of the desired size is verified at this point [CS].
#
# (C) Frank-Rene Schaefer
#______________________________________________________________________________
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])

import quex.input.regular_expression.engine           as     core
import quex.input.files.specifier.counter             as     counter
import quex.engine.state_machine.transformation.core  as     bc_factory
import quex.output.languages.core                     as     languages
import quex.output.counter.run_time                   as     run_time_counter

from   quex.blackboard  import setup as Setup, Lng

from   itertools import chain
from   os        import system
import codecs
import subprocess
from   StringIO  import StringIO

Setup.language_db = languages.db["C"]()


if "--hwut-info" in sys.argv:
    # Information for HWUT
    #
    print "Character Counter: Default Implementation"
    print "CHOICES: " \
          "ascii-1, ascii-1-wo-ReferenceP, " \
          "utf_16_le-1, utf_16_le-1-wo-ReferenceP, " \
          "utf_16_le-2, utf_16_le-2-wo-ReferenceP, " \
          "utf_32_le-1, utf_32_le-1-wo-ReferenceP, " \
          "cp737-1, cp737-1-wo-ReferenceP, " \
          "utf_8-1, utf_8-1-wo-ReferenceP, "   \
          "utf_8-2, utf_8-2-wo-ReferenceP, "   \
          "utf_8-3, utf_8-3-wo-ReferenceP, "   \
          "utf_8-4, utf_8-4-wo-ReferenceP;"  
    print "SAME;"
    sys.exit(0)

test_template_list = [
    # 'a', 'b', 'c', and 'd' are PLACEHOLDERS for characters of a specific
    # encoding and code-unit number to be specified in 
    # 'prepare_test_input_file(...)'.
    "",
    "a",
    "ab",
    "abc", 
    "abcd",
    "\t",
    "a\t",
    "ab\t",
    "abc\t",
    "abcd\t",
    "\t",
    "a\ta",
    "ab\ta",
    "abc\ta",
    "abcd\ta",
    "\n",
    "a\n",
    "\na",
    "b\nb",
    "c\nc",
    "\t\n",
    "\n\t",
    "\t\n\t",
    "\t\n\t",
    "\t\na",
    "\n\tb",
    "\t\n\tc",
    "\t\n\td",
]

# default: trivial identity association
trivial_db = { 
    "a": u"a", "b": u"b", "c": u"c", "d": u"d", "\n": u"\n", "\t": u"\t" 
} 

def get_test_string_list(Codec, CodeUnitsPerCharacter):
    """RETURNS: [0] Characters being used.
                [1] List of test strings in unistr
    """
    db = get_letter_db(Codec, CodeUnitsPerCharacter)
    test_string_list = [
        u"".join(db[letter] for letter in test_string_template)
        for test_string_template in test_template_list
    ]
    return db.values(), test_string_list

def get_letter_db(Codec, CodeUnitsPerCharacter):
    global trivial_db
    if Codec == "utf_8":
        code_unit_size = 1 # [byte]
        if   CodeUnitsPerCharacter == 1: db = {}
        elif CodeUnitsPerCharacter == 2: db = { "a": u"ا", "b": u"ب", "c": u"ت", "d": u"ى" }  # 2 byte letters
        elif CodeUnitsPerCharacter == 3: db = { "a": u"", "b": u"", "c": u"", "d": u"" }  # 3 byte letters
        elif CodeUnitsPerCharacter == 4: db = { "a": u"𐅃", "b": u"𐅄", "c": u"𐅅", "d": u"𐅆" }  # 4 word letters
    elif Codec == "utf_16_le":
        code_unit_size = 2 # [byte]
        if   CodeUnitsPerCharacter == 1: db = {}
        elif CodeUnitsPerCharacter == 2: db = { "a": u"𐅃", "b": u"𐅄", "c": u"𐅅", "d": u"𐅆" } # 2 word letters
    elif Codec == "utf_32_le":
        code_unit_size = 4 # [byte]
        db             = {}
    else:
        code_unit_size = 1 # [byte]
        db             = {}

    for letter, replacement in trivial_db.iteritems():
        if letter not in db: db[letter] = replacement

    return db

def write_test_string(test_str, Codec):
    # Write data content into file to work with.
    fh = codecs.open("./data/input.txt", "wb", Codec.lower())
    fh.write(test_str)
    fh.close()

def assert_reference_delta_count_implementation(counter_str, ExpectReferenceP_F):
    """Count the number of occurrences of the variable 'reference_p'. If
    it does not occur, this indicates that the counter has been implemented
    without reference-delta counting.

    The 'ExpectReferenceP_F' tells whether the implementation is expected to be
    done with reference-delta counting.

    EXITS: Upon unexpected implementation.
    """
    found_n = 0
    for i, line in enumerate(counter_str.splitlines()):
        if line.find("reference_p") == -1: continue
        found_n += 1
        if found_n == 3: break

    # [RP] If 'ReferenceP' is expected to be used, it must appear 3 times at least:
    #      1. at variable definition, 
    #      2. at reference pointer set
    #      3. at reference pointer addition.
    if ExpectReferenceP_F:
        assert found_n >= 3, "Counter should have been setup using a reference pointer."
    else:
        assert found_n == 0, "Counter should not have been setup using a reference pointer."

def get_test_application(encoding, ca_map):

    # (*) Setup the buffer encoding ___________________________________________
    #
    if   encoding == "utf_32_le": byte_n_per_code_unit = 4 
    elif encoding == "ascii":     byte_n_per_code_unit = 1
    elif encoding == "utf_8":     byte_n_per_code_unit = 1
    elif encoding == "utf_16_le": byte_n_per_code_unit = 2
    elif encoding == "cp737":     byte_n_per_code_unit = 1
    else:                         assert False

    Setup.buffer_setup("", byte_n_per_code_unit, 
                       encoding.replace("_le", "").replace("_",""))

    # (*) Generate Code _______________________________________________________
    #
    counter_function_name, \
    counter_str            = run_time_counter.get(ca_map, "TEST_MODE")
    counter_str            = counter_str.replace("static void", "void")

    # Double check if reference delta counting has been implemented as expected.
    expect_reference_p_f   = ca_map.get_column_number_per_code_unit() is not None
    assert_reference_delta_count_implementation(counter_str, 
                                                expect_reference_p_f)

    open("./data/test.c", "wb").write("#include <data/check.h>\n\n" 
                                      + counter_str)

    # (*) Compile _____________________________________________________________
    #
    os.system("rm -f test")
    compile_str =   "gcc -Wall -Werror -I. -ggdb ./data/check.c ./data/test.c "     \
                  + " -DQUEX_OPTION_COUNTER_EXT"                                \
                  + " -DDEF_COUNTER_FUNCTION='%s' " % counter_function_name \
                  + " -DDEF_FILE_NAME='\"data/input.txt\"' "                \
                  + " -DDEF_CHARACTER_TYPE=%s" % Setup.lexatom.type         \
                  + " -o test" 
                  # + " -DDEF_DEBUG_TRACE " 

    print "## %s" % compile_str            
    os.system(compile_str)

def run(Codec, TestStringList):
    for i, test_str in enumerate(TestStringList):
        # if i != 27: continue
        write_test_string(test_str, Codec)
        print "-------------------------------------------------"
        test_str_display = test_str.replace(u"\t", u"\\t").replace(u"\n", u"\\n").encode("utf8")
        print "(%2i) Test String (template): [%s]" % (i, test_template_list[i].replace("\t", "\\t").replace("\n", "\\n"))
        print "## %s" % test_str_display
        print
        sys.stdout.flush()
        subprocess.call("./test")

def determine_ca_map(without_reference_p_f, UsedCharacterSet):
    """RETURNS: [0] CaMap object.
    """
    verdict_f = False
    if without_reference_p_f:
        spec_txt = """
           [\\x0A] => newline 1;
           [\\t]   => grid    4;
           [abcd]  => space   1;   // 10 column unit
           [x]     => space 4711;  // => inhomogene counting
           \\else  => space   1;>  // 
        """
        verdict_f = False
    else:
        all_character_str = u"".join(UsedCharacterSet).replace("\n", "").replace("\t", "")
        spec_txt = u"""
           [\\n]   => newline 1;
           [\\t]   => grid 4;
           [%s]    => space 1;
           \\else   => space 1;>
        """ % all_character_str

    fh      = StringIO(spec_txt.encode("utf8"))
    fh.name = "<string>"
    ca_map  = counter.LineColumnCount_Prep(fh).parse()

    return ca_map

# Parse command line 'CHOICE' _________________________________________________
#
choice  = sys.argv[1]
fields  = choice.split("-")

# Test parameters _____________________________________________________________
#
# -- Encoding to be used for buffer.
encoding                 = fields[0]
# -- Number of code units per character in the test character sequence.
code_units_per_character = int(fields[1])
# -- Enforce implementation without reference pointer?
without_reference_p_f    = (choice.find("wo-ReferenceP") != -1)


# Generate test strings for given encoding and code units per char ____________
#
used_character_set, \
test_string_list         = get_test_string_list(encoding, 
                                                code_units_per_character)

# Construct the 'Count Action Map' (ca_map) ___________________________________
#
ca_map                   = determine_ca_map(without_reference_p_f, 
                                            used_character_set)


# Compile the test application ________________________________________________
#
get_test_application(encoding, ca_map)

# Run test application on generated input file ________________________________
#
run(encoding, test_string_list)
    
# Clean up ____________________________________________________________________
#
if False:
    print "#not remove files"
else:
    os.remove("data/input.txt")
    os.remove("test")
