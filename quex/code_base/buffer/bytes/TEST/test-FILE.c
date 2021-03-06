/* PURPOSE: See comment in file 'basic_functionality.c'                      */
#include <basic_functionality.h>
#include "test_c/lib/buffer/bytes/ByteLoader_FILE"
#include "test_c/lib/buffer/bytes/ByteLoader_FILE.i"
#include "test_c/lib/buffer/bytes/ByteLoader.i"
#include "test_c/lib/quex/MemoryManager.i"
#include <hwut_unit.h>

int
main(int argc, char** argv)
{
    QUEX_NAME(ByteLoader)*  me;
    hwut_info("QUEX_NAME(ByteLoader): FILE;\n"
              "CHOICES: basic, init-pos;");

    hwut_verify(QUEX_NAME(ByteLoader_FILE_new_from_file_name)("not-existing-file.txt") == (QUEX_NAME(ByteLoader)*)0);
    hwut_verify(QUEX_NAME(ByteLoader_FILE_new)(NULL, false) == (QUEX_NAME(ByteLoader)*)0);
    me = QUEX_NAME(ByteLoader_FILE_new_from_file_name)("test.txt");

    hwut_if_choice("basic")    verify_basic_functionality(me);
    hwut_if_choice("init-pos") initial_position(me);

    me->delete_self(me);

    return 0;
}

