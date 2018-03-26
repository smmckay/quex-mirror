/* PURPOSE: See comment in file 'basic_functionality.c'                      */
#include <basic_functionality.h>
#include "ut/lib/buffer/bytes/ByteLoader_POSIX"
#include "ut/lib/buffer/bytes/ByteLoader_POSIX.i"
#include "ut/lib/buffer/bytes/ByteLoader.i"
#include "ut/lib/MemoryManager.i"
#include <hwut_unit.h>

int
main(int argc, char** argv)
{
    QUEX_NAME(ByteLoader)*  me;
    hwut_info("QUEX_NAME(ByteLoader): POSIX;\n"
              "CHOICES: basic, init-pos;");

    hwut_verify(QUEX_NAME(ByteLoader_POSIX_new_from_file_name)("not-existing-file.txt") == (QUEX_NAME(ByteLoader)*)0);
    hwut_verify(QUEX_NAME(ByteLoader_POSIX_new)(-1) == (QUEX_NAME(ByteLoader)*)0);
    me = QUEX_NAME(ByteLoader_POSIX_new_from_file_name)("test.txt");

    hwut_if_choice("basic")    verify_basic_functionality(me);
    hwut_if_choice("init-pos") initial_position(me);

    me->delete_self(me);

    return 0;
}

