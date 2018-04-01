# PURPOSE: Files for Packaging vs. Files in Code Base
#
# This test compares the files which are considered by the source 
# packager with the files which are acutally present in the code base.
# Ideally, all files from the code base shall be present in the list
# of considered files for packaging.
#
# (C) 2018 Frank-Rene Schaefer
#______________________________________________________________________________
import sys
import os
sys.path.insert(0, os.environ["QUEX_PATH"])

import quex.output.languages.cpp.source_package as source_package

if "--hwut-info" in sys.argv:
    print "Files for Packaging vs. Files in Code Base;"
    sys.exit()

package_set = source_package.__collect_files(None)

code_base_dir   = os.path.join(os.environ["QUEX_PATH"], "quex/code_base")
code_base_dir_L = len(code_base_dir)
code_base_set   = set()
for root, dummy, file_list in os.walk(code_base_dir):
    if root.find("TEST") != -1: continue
    code_base_set.update(os.path.join(root, f)[code_base_dir_L+1:] 
                         for f in file_list 
                         if     not f.startswith("TXT") \
                            and not f.startswith("README.txt") \
                            and not f.startswith("tmp") \
                            and not f.endswith("DELETED") \
                            and root.find("test_environment") == -1)

def test(Title, A, B, MustBeEmptyF):
    result = A.difference(B)
    assert MustBeEmptyF == False or len(result) == 0
    if MustBeEmptyF: comment = "(no output is good output)"
    else:            comment = ""
    print "%s %s {" % (Title, comment)
    for f in sorted(result):
        print "    %s" % f
    print "}" 

test("Files in package but not in code base", package_set, code_base_set, 
     MustBeEmptyF=True)
    
test("Files in code base but not in package", code_base_set, package_set, 
     MustBeEmptyF=False)


