#! /usr/bin/env python
#
# PURPOSE: Instantiate all or some of the code base directories/files.
#
# $1 = target directory.
# $* = directories to be instantiated from code base.
#
# '--adapt' adapts a given list of files to a specific include base.
# '--specify' adapts a given list of files to a specific include base.
#  
# $1 = target directory
# $* = file name list
#
# (C) Frank-Rene Schaefer
#______________________________________________________________________________
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), "../../../")))

import quex.output.languages.cpp.source_package as     source_package
from   quex.input.files.token_type              import TokenTypeDescriptorManual
import quex.output.analyzer.adapt               as     adapt
from   quex.output.languages.core import db
import quex.token_db              as     token_db
from   quex.blackboard            import setup as Setup, \
                                         Lng
if "--lang-C" in sys.argv: Setup.language_db = db["C"](); sys.argv.remove("--lang-C")
else:                      Setup.language_db = db["C++"]()
Setup.analyzer_class_name     = "TestAnalyzer"
Setup.token_class_name        = "TestAnalyzer_Token"
Setup.token_class_name_safe   = "TestAnalyzer_Token"
Setup.token_id_type           = "int"
Setup.extern_token_class_file = "no-name"

token_db.token_type_definition = \
        TokenTypeDescriptorManual(Setup.extern_token_class_file,
                                  Setup.token_class_name,
                                  Setup.token_class_name_space,
                                  Setup.token_class_name_safe,
                                  Setup.token_id_type)

if len(sys.argv) < 2:
    print "Error: require at least target directory."
    sys.exit()

if "--adapt" in sys.argv or "-a" in sys.argv:
    target_dir      = sys.argv[2]
    input_file_list = sys.argv[3:]

    for input_file in input_file_list:
        with open(input_file) as fh:
            txt = fh.read()
        txt = adapt.produce_include_statements(target_dir, txt)
        with open(input_file, "w") as fh:
            fh.write(txt)

elif "--specify" in sys.argv:
    Setup.analyzer_class_name = sys.argv[2]
    target_dir      = sys.argv[3]
    token_name      = "Token"
    input_file_list = sys.argv[3:]
    for input_file in input_file_list:
        with open(input_file) as fh:
            txt = fh.read()

        txt = adapt.do(target_dir, txt)
        with open(input_file, "w") as fh:
            fh.write(txt)

else:
    target_dir    = sys.argv[1]
    code_dir_list = sys.argv[2:]
    if not code_dir_list: code_dir_list = None
    try:    os.mkdir(target_dir)
    except: print "Directory '%s' already exists." % target_dir
    source_package.do(target_dir, code_dir_list)
