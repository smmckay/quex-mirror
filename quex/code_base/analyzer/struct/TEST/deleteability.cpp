#include <Dumlyzer>
#include <quex/code_base/MemoryManager>
#include <quex/code_base/MemoryManager.i>
#include <hwut_unit.h>

class MiniClass {
    MiniClass() {
    }
    uint8_t            __memory_token[sizeof(QUEX_TYPE_TOKEN)];
};

int
main(int argc, char** argv)
{
    using namespace quex;

    uint8_t memory[64];

#   if 1
    memset(&memory[0], 0x5A, sizeof(memory));
    memory[0]    = QUEX_SETTING_BUFFER_LIMIT_CODE;
    memory[64-1] = QUEX_SETTING_BUFFER_LIMIT_CODE;

    // Dumlyzer*  dl = new Dumlyzer((QUEX_NAME(ByteLoader)*)0, NULL);
    Dumlyzer*  dl = new Dumlyzer(&memory[0], 64, &memory[64-1]);
#   else
    MiniClass* dl = new MiniClass();
#   endif

    delete dl;

    return 0;
}
