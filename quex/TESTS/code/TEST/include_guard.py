#! /usr/bin/env python
import os
import sys
sys.path.append(os.environ["QUEX_PATH"])

from   operator import attrgetter
from   quex.input.code.base       import get_current_line_info_number
from   quex.engine.misc.file_in   import skip_whitespace

class info:
    def __init__(self, FileName, LineN, Name):
        self.file_name = FileName
        self.line_n    = LineN
        self.name      = Name

include_guard_list = []
max_length         = 0 
for root, dir_list, file_list in os.walk(os.environ["QUEX_PATH"] + "/quex"):
    if   root.find(".svn")       != -1: continue
    elif root.find("/TEST/OUT")  != -1: continue
    elif root.find("/TEST/GOOD") != -1: continue
    elif root.find("/TEST/ADM")  != -1: continue
    elif root.find("/DESIGN")    != -1: continue
    elif root.find("/TEST")      != -1: continue
    elif root.find("/code_base") == -1: continue

    ## print root
    for file in file_list:
        ext = os.path.splitext(file)[1]
        if ext not in ["", ".i", ".h", ".txt", ".bak"]: continue
        elif file.endswith("~"): continue
        elif file.startswith("TXT-"): continue
        elif file.lower() in ["makefile", "tags", "readme", "readme.txt"]: continue
        file_name = root + "/" + file

        fh = open(file_name, "rb")
        try:    skip_whitespace(fh)
        except: continue 
        for line in fh.readlines():
            if line.find("INCLUDE_GUARD") == -1:  
                continue
            line = line.strip()
            if line[0] != "#":                    continue
            fields = line[1:].split()
            # include guards work with '#ifndef' or '#if ! defined( .... )'
            if fields[0] == "ifndef":
                if len(fields) < 2:               continue
                include_guard = fields[1]
            elif len(fields) >= 3 and fields[0] == "if" and fields[1] == "!" and fields[2].find("defined") != -1:
                nice_line = line[1:].replace("if", "").replace("!", "").replace("defined", "").replace("(", " ").replace(")", " ") 
                fields = nice_line.split()
                if len(fields) < 1: continue
                include_guard = fields[0]
            else:
                continue

            include_guard_list.append(info(file_name, 
                                           get_current_line_info_number(fh), 
                                           include_guard))
            if len(fields[1]) > max_length: max_length = len(include_guard)
            break
        else:
            include_guard_list.append(info(file_name, -1, "<<No INCLUDE_GUARD directive found>>"))

def better_name(FileName):
    L = len(os.environ["QUEX_PATH"] + "/quex/code_base/")
    suffix  = FileName[L:]
    if suffix == "": return "<EmptyFileName>"
    suffix  = suffix.replace("/", "__")
    suffix  = suffix.replace(".", "_")
    suffix  = suffix.replace("-", "_")
    # Transition from lower to upper case --> space
    result      = suffix[0]
    prev_letter = suffix[0]
    for letter in suffix[1:]:
        if prev_letter.islower() and letter.isupper(): result += "_"
        result     += letter
        prev_letter = letter
    suffix  = result.upper()
    return "QUEX_INCLUDE_GUARD__" + suffix

def __AUX_helper_to_name_the_include_guards_according_to_quex_convention():
    global include_guard_list

    stranger_list = [ x.file_name for x in include_guard_list if x.name != better_name(x.file_name) ]
    for x in include_guard_list:
        if x.file_name not in stranger_list: continue
        print x.file_name + ":1:",
        # Cut the QUEX_PATH from the file name

        print " %s" % better_name(x.file_name)

def check_include_guard_convention():
    stranger_list = filter(lambda x: x.name != better_name(x.file_name), include_guard_list)
    L = max(map(lambda x: len(x.name), stranger_list))

    print "Following include guards do not follow convention:"
    for x in sorted(stranger_list, key=attrgetter("file_name")):
        print "%s%s --> %s" % \
              (x.name, " " * (L - len(x.name)), better_name(x.file_name))

def check_include_guard_undefinition():
    global include_guard_list

    undef_file_name = os.environ["QUEX_PATH"] + "/quex/code_base/include-guard-undef"
    fh = open(undef_file_name)
    undef_unique = {}
    for line in fh.readlines():
        index = line.find("undef")
        if index == -1: continue
        fields = line[index:].split()
        if len(fields) < 2: continue
        undef_unique[fields[1]] = True

    # Filter out empty include guards
    include_guard_list = filter(lambda x: x.line_n != -1, include_guard_list)

    undef_list = undef_unique.keys()
    stranger_list = filter(lambda x: x.name not in undef_list, include_guard_list)
    L = max(map(lambda x: len(x.name), stranger_list))

    print "Following include guards are not undefined in %s:" % undef_file_name.replace(os.environ["QUEX_PATH"], "<<QUEX_PATH>>")
    stranger_list.sort(lambda a,b: cmp(a.name, b.name))
    for x in stranger_list:
        ext = os.path.splitext(x.file_name)[1]
        base_file_name = os.path.basename(x.file_name)
        if ext == ".txt" or (len(base_file_name) >=3 and base_file_name[:3] == "TXT"): continue
        print "%s" % x.name

    include_guard_name_list = map(lambda x: x.name, include_guard_list)    
    stranger_list = filter(lambda name: name not in include_guard_name_list, undef_list)

    print "Following are undefined but nowhere defined:"
    stranger_list.sort()
    if len(stranger_list) != 0:
        L = max(map(lambda name: len(name), stranger_list))
        for name in stranger_list:
            print "%s%s" % \
                  (name, " " * (L - len(name)))
    else:
        print "<None>"

if "--hwut-info" in sys.argv:
    print "Include Guards for C/C++"
    print "CHOICES: convention;"
    sys.exit()

if "convention" in sys.argv:
    check_include_guard_convention()

elif "undefinition" in sys.argv:
    check_include_guard_undefinition()

elif "help" in sys.argv:
    # Help to develop include guard according quex-internal convention
    __AUX_helper_to_name_the_include_guards_according_to_quex_convention()
