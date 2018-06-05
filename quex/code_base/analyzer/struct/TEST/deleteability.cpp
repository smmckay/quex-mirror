#include <Dumlyzer>
#include "test_cpp/lib/quex/MemoryManager"
#include "test_cpp/lib/quex/MemoryManager.i"
#include <hwut_unit.h>



Dumlyzer* dl;

int
main(int argc, char** argv)
{


#   if 1
    uint8_t memory[] { QUEX_SETTING_BUFFER_LIMIT_CODE, 'x', QUEX_SETTING_BUFFER_LIMIT_CODE };

    // Dumlyzer*  dl = new Dumlyzer((QUEX_NAME(ByteLoader)*)0, NULL);
    dl = new Dumlyzer(&memory[0], 3, &memory[3-1]);
#   else
    Mini*  dl = new Mini();
#   endif

    delete dl;

    return 0;
}
