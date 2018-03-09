/* PURPOSE: See comment in file 'basic_functionality.c'                      */
#include <basic_functionality.h>
$$INC: buffer/bytes/ByteLoader_stream$$
$$INC: buffer/bytes/ByteLoader_stream.i$$
$$INC: buffer/bytes/ByteLoader.i$$
$$INC: MemoryManager.i$$
#include <hwut_unit.h>
#include <sstream> 
#include <string> 

int
main(int argc, char** argv)
{
    char               tmp_buffer[1024];
    std::ifstream      fstr("test.txt", std::ios::in);

    hwut_info("QUEX_NAME(ByteLoader): std::stringstream;\n"
              "CHOICES: basic, init-pos;");

    fstr.read(&tmp_buffer[0], TEST_FILE_SIZE);
    tmp_buffer[TEST_FILE_SIZE] = '\0';

    std::string         sbuffer(tmp_buffer);
    std::istringstream  sstr(sbuffer);
    QUEX_NAME(ByteLoader)*         me = QUEX_NAME(ByteLoader_stream_new)(&sstr);

    hwut_verify(QUEX_NAME(ByteLoader_stream_new)((std::stringstream*)0) == (QUEX_NAME(ByteLoader)*)0);

    hwut_if_choice("basic")    verify_basic_functionality(me);
    hwut_if_choice("init-pos") initial_position(me);

    me->delete_self(me);

    return 0;
}

