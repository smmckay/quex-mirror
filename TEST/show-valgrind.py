import sys
if len(sys.argv) > 1: file_name = sys.argv[1]
else:                 file_name = "tmp.txt"

fh = open(file_name)

root_cause = []

# valgrind must be run with '--leak-check=full --show-leak-kinds=all' to
# detect the leak in the Standard lib.
leak_in_std_lib = False

pos0 = 2
pos1 = 5

text    = []
error_f = False
for line in fh.readlines():
    if line.find("--") == 0 and line.find("-----") == -1:
        continue
    if line.find("==") == 0:
        # 'valgrind' line
        tail = line.split("==")[2].strip()
        n    = tail.split()
        if   line.find("All heap blocks were freed") != -1: 
            text.append( "VALGRIND: %s" % tail.replace("=", "").replace(".", "")) 
        elif line.find(" definitely lost:") != -1:          
            text.append( "VALGRIND: %s" % tail.replace("=", ""))
            error_f |= (n[pos0] != "0" or n[pos1] != "0")
        elif line.find(" indirectly lost:") != -1:          
            text.append( "VALGRIND: %s" % tail.replace("=", ""))
            error_f |= (n[pos0] != "0" or n[pos1] != "0")
        elif line.find(" possibly lost:") != -1:            
            text.append( "VALGRIND: %s" % tail.replace("=", ""))
            error_f |= (n[pos0] != "0" or n[pos1] != "0")
        elif line.find(" suppressed:") != -1:               
            text.append( "VALGRIND: %s" % tail.replace("=", "")) 
            error_f |= (n[pos0-1] != "0" or n[pos1-1] != "0")
        elif line.find(" by 0x") != -1:
            # If last 'by ..' line contains 'ld' it is a leak in the std_lib
            if line.find("/ld-") != -1: leak_in_std_lib = True
        elif     line.find("still reachable:") != -1 \
             and not leak_in_std_lib:          
            text.append("VALGRIND: %s" % tail.replace("=", ""))
            error_f |= (n[pos0] != "0" or n[pos1] != "0")

        if error_f:
            print "#error:", line
                            
        continue
    else:
        print line,

if error_f:
    print "".join(text)
else:
    print "VALGRIND:   All heap blocks were freed -- no leaks are possible"
