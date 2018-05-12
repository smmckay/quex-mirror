#include<iostream> 
#include<cstring> 

#include "EasyLexer/EasyLexer"

static void test(size_t Size0, size_t ContentSize0, size_t Size1, size_t ContentSize1);
static void print_this(EasyLexer* lex, int Index, size_t Size, size_t ContentSize);

int 
main(int argc, char** argv) 
{        
    test(77, 60, 66, 50);
    test(77, 0,  66, 50);
    test(0,  0,  66, 50);
    test(77, 60, 66, 0);
    test(77, 0,  66, 0);
    test(0,  0,  66, 0);
    test(77, 60,  0, 0);
    test(77, 0,   0, 0);
    test(0,  0,   0, 0);

    return 0;
}

void 
test(size_t Size0, size_t ContentSize0, size_t Size1, size_t ContentSize1)
{
    using namespace std;
    EasyLexer_lexatom_t*  end_of_content_p;
    EasyLexer_lexatom_t*  buffer_0 = (Size0 == 0) ? 0x0 : new EasyLexer_lexatom_t[Size0+2];
    EasyLexer_lexatom_t*  buffer_1 = (Size1 == 0) ? 0x0 : new EasyLexer_lexatom_t[Size1+2];

    if( Size0 ) {
        buffer_0[0]       = QUEX_SETTING_BUFFER_LIMIT_CODE;
        buffer_0[Size0-1] = QUEX_SETTING_BUFFER_LIMIT_CODE;
        end_of_content_p  = &buffer_0[ContentSize0+1];
        *end_of_content_p = QUEX_SETTING_BUFFER_LIMIT_CODE;
        memset(&buffer_0[1], 'a', ContentSize0); 
    }
    else {
        end_of_content_p = (EasyLexer_lexatom_t*)0;
    }
    EasyLexer qlex(&buffer_0[0], Size0, end_of_content_p); 

    cout << "--------------------------------------------------------------------------\n";
    cout << "Constructor:\n";
    print_this(&qlex, 0, Size0, ContentSize0);

    if( Size1 ) {
        buffer_1[0]       = QUEX_SETTING_BUFFER_LIMIT_CODE;
        buffer_1[Size1-1] = QUEX_SETTING_BUFFER_LIMIT_CODE;
        memset(&buffer_1[1], 'b', ContentSize1);
        end_of_content_p  = &buffer_1[ContentSize1+1];
        *end_of_content_p = QUEX_SETTING_BUFFER_LIMIT_CODE;
    }
    else {
        end_of_content_p = (EasyLexer_lexatom_t*)0;
    }

    EasyLexer_lexatom_t*  prev;
    qlex.collect_user_memory(&prev);
    assert(qlex.reset_memory(buffer_1, Size1, end_of_content_p));
    if( prev ) delete [] prev;

    cout << "\n\n";
    cout << "reset_buffer reported buffer: " << ((prev == buffer_0) ? "Correct" : "False");
    if( prev != buffer_0 ) cout << "\n## " << (long)prev << " " << (long)buffer_0 << endl;
    cout << "\n\n";

    cout << "'reset_buffer':\n";
    print_this(&qlex, 1, Size1, ContentSize1);

    if( buffer_1 ) {
        qlex.collect_user_memory(&prev);
        assert(qlex.reset_memory((EasyLexer_lexatom_t*)0x0, 0, (EasyLexer_lexatom_t*)0x0));
        if( prev ) delete [] prev;

        cout << "\n\n";
        cout << "reset_buffer reported buffer: " << ((prev == buffer_1) ? "Correct" : "False");
        if( prev != buffer_1 ) cout << "\n## " << (long)prev << " " << (long)buffer_1 << endl;
        cout << "\n\n";
        
        if( prev ) delete [] prev;
    }
}

static void
print_this(EasyLexer* lex, int Index, size_t Size, size_t ContentSize)
{
    using namespace std;

    cout << "   (Size"  << Index << " = " << Size;
    cout << ", ContentSize"  << Index << " = " << ContentSize << ")\n";
    if( lex->buffer._memory._front ) {
        cout << "   size       = " << (lex->buffer._memory._back + 1 - lex->buffer._memory._front) << endl;
        cout << "   eof offset = " << (lex->buffer.input.end_p       - lex->buffer._memory._front) << endl;
    } else {
        assert(! lex->buffer._memory._back);
        assert(! lex->buffer.input.end_p);
        assert(lex->buffer._read_p == (EasyLexer_lexatom_t*)0);
        assert(lex->buffer._lexeme_start_p == (EasyLexer_lexatom_t*)0);
        assert(lex->buffer.input.lexatom_index_begin == -1);
        assert(lex->buffer.input.lexatom_index_end_of_stream == -1);
        cout << "   <empty buffer>"  << endl; 
    }
}
