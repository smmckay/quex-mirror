#include<fstream>    
#include<fstream> 
#include <Simple/Simple>
#include <Simple/lib/buffer/bytes/ByteLoader_stream.i>

using namespace std;

int 
main(int argc, char** argv) 
{        

    // we want to have error outputs in stdout, so that the unit test could see it.
    ifstream  istr("example.txt");
    Simple    qlex(QUEX_NAME(ByteLoader_stream_new)(&istr), 
                   (QUEX_NAME(Converter)*)0);
    Simple_Token     Token;

    qlex._parent_memento = 0;
    qlex.include_pop();

    return 0;
}

