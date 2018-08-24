#include <cstdio>
#include <cstdlib>
#include <cstring>

#include <test_cpp/TestAnalyzer>
// #include "test_cpp/converter-from-lexeme.i"
#include "test_cpp/lib/lexeme_base.i"
#include "test_cpp/lib/extra/accumulator/Accumulator"
#include "test_cpp/lib/extra/accumulator/Accumulator.i"

int
main(int argc, char** argv)
{

    uint8_t TestString0[] = "AsSalaamu Alaikum";
    size_t  TestString0L  = strlen((const char*)TestString0);

    /* Ensure some settings that cause the accumulator to extend its memory */
    __quex_assert(QUEX_TestAnalyzer_SETTING_ACCUMULATOR_INITIAL_SIZE == 0);
    __quex_assert(QUEX_TestAnalyzer_SETTING_ACCUMULATOR_GRANULARITY_FACTOR == 1);

    if( argc < 2 ) return -1;

    if( strcmp(argv[1], "--hwut-info") == 0 ) {
        printf("Accumulator;\n");
        printf("CHOICES: String, Character, N-Character, N-String, Mix;\n");
        return 0;
    }
    TestAnalyzer              analyzer((TestAnalyzer_ByteLoader*)0, NULL);
    TestAnalyzer_Accumulator  accumulator;

#   define self analyzer

    analyzer._token_queue.write_iterator = analyzer._token_queue.begin;
    analyzer._token_queue.read_iterator = analyzer._token_queue.begin;
    (void)TestAnalyzer_Accumulator_construct(&accumulator, &analyzer);

    if     ( strcmp(argv[1], "String") == 0 ) {
        accumulator.add(TestString0, TestString0 + TestString0L);
        accumulator.print_this();
        accumulator.flush(0);
    }
    else if( strcmp(argv[1], "Character") == 0 ) {
        accumulator.add_character('a');
        accumulator.print_this();
        accumulator.flush(0);
    }
    else if( strcmp(argv[1], "N-Character") == 0 ) {
        for(int i = 0; i != 104; ++i) 
            accumulator.add_character(i % 26 + 'a');
        accumulator.print_this();
        accumulator.flush(0);
    }
    else if( strcmp(argv[1], "N-String") == 0 ) {
        for(int i = 0; i != 10; ++i) 
            accumulator.add(TestString0, TestString0 + TestString0L);
        accumulator.print_this();
        accumulator.flush(0);
    }
    else if( strcmp(argv[1], "Mix") == 0 ) {
        int p = 4711;
        for(int i = 0; i != 10; ++i) {
            p = (p + i) * (p + i) % 4711;  // pseudo random number
            if( p % 2 == 0 )
                accumulator.add(TestString0, TestString0 + TestString0L);
            else {
                accumulator.add_character(' ');
                accumulator.add_character(p % 26 + 'a');
                accumulator.add_character(' ');
            }
        }
        accumulator.print_this();
        accumulator.flush(0);
    }

    // QUEX_NAME(Accumulator_destruct)(&accumulator);

    printf("<terminated>\n");
    return 0;
}
