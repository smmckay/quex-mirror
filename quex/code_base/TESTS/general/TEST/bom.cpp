#include <cstdio>
#include <iostream>
#include <fstream>
#define QUEX_NAME(X) (X)
#include "test_cpp/lib/quex/bom"
#include "test_cpp/lib/quex/bom.i"
#include <support/C/hwut_unit.h>


int
main(int argc, char** argv)
{
    const char* file_names[] = { "data/bocu1.txt", 
                                 "data/gb18030.txt",
                                 "data/scsu.txt",
                                 "data/utf16be.txt",
                                 "data/utf16le.txt",
                                 "data/utf32be.txt",
                                 "data/utf32le.txt",
                                 "data/utf7.txt",
                                 "data/utf8.txt",
                                 0x0,
    };
    const char**    iterator;
    E_ByteOrderMark bom = QUEX_BOM_NONE;

    hwut_info("BOM Snap: ifstream\n");

    for(iterator = file_names; *iterator != 0x0; ++iterator ) {
        std::ifstream  istr(*iterator);
        bom = quex::bom_snap(&istr);

        printf("%s\n", *iterator);
        printf("   CODEC: %s\n", quex::bom_name(bom));
        printf("   BYTES: ");
        while( ! istr.eof() )
        {
            printf("%02X.", (int)istr.get());
        }
        printf("\n");
        istr.close();
    }
}
