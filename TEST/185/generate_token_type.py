#
# USAGE: python generate_token_type.py > token-type.qx
#
# PURPOSE: Generate members of the token class that sort in a particular way,
#          but are given in a shuffled order. 
# => It checks that the code generator does only consider the position of 
#    mentioning when code is generated.
#______________________________________________________________________________
import random

def get_sequence(letter_list):
    result = []
    for x in letter_list:
        for y in letter_list:
            for z in letter_list:
                random = (ord(x) * 51 + ord(y) * 7 + ord(z) * 521) % 5 
                bit_n  = 8 * 2**random
                result.append("%s%s%s_position : uint%i_t;" % (x, y, z, bit_n))
    return result

def get_section(Name, Prefix, LetterList):
    seq = get_sequence(LetterList)
    random.shuffle(seq)

    print "%s{" % Name
    for position, line in enumerate(seq):
        line = line.replace("_position", "_position_%03i" % position)
        print "   %s%s" % (Prefix, line)
    print "}"

print "token_type {"
get_section("distinct ", "", "ABCDEFGHI")

print "union {"
get_section("", "    A_union0_", "ABCD")
get_section("", "    B_union1_", "ABCD")
get_section("", "    C_union2_", "ABCD")
get_section("", "    D_union3_", "ABCD")
print "}"

print "}"

