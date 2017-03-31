#include <cstdio>
#include <cstdlib>
#include <cstring>

#include <quex/code_base/extra/test_environment/TestAnalyzer>
#include <quex/code_base/single.i>

QUEX_NAMESPACE_LEXEME_NULL_OPEN
QUEX_TYPE_LEXATOM  QUEX_LEXEME_NULL_IN_ITS_NAMESPACE = (QUEX_TYPE_LEXATOM)0;
QUEX_NAMESPACE_LEXEME_NULL_CLOSE

QUEX_NAMESPACE_MAIN_OPEN

//#define QUEX_TOKEN_POLICY_SET_ID()       /* empty */
//#define QUEX_TOKEN_POLICY_PREPARE_NEXT() /* empty */

#if 0
bool 
QUEX_NAME_TOKEN(take_text)(QUEX_TYPE_TOKEN*         __this, 
                           QUEX_TYPE_ANALYZER*      analyzer, 
                           const QUEX_TYPE_LEXATOM* Begin, 
                           const QUEX_TYPE_LEXATOM* End)
{
    printf("Lexical Analyzer Receives:\n");
    printf("   '%s'\n", Begin);
    return true;
}
#endif

QUEX_NAMESPACE_MAIN_CLOSE

#include <quex/code_base/analyzer/C-adaptions.h>
#include <quex/code_base/analyzer/Counter.i>

int
main(int argc, char** argv)
{
    using namespace quex;

    uint8_t TestString0[] = "AsSalaamu Alaikum";
    size_t  TestString0L  = strlen((const char*)TestString0);

    /* Ensure some settings that cause the accumulator to extend its memory */
    __quex_assert(QUEX_SETTING_ACCUMULATOR_INITIAL_SIZE == 0);
    __quex_assert(QUEX_SETTING_ACCUMULATOR_GRANULARITY_FACTOR == 1);

    if( argc < 2 ) return -1;

    if( strcmp(argv[1], "--hwut-info") == 0 ) {
        printf("Accumulator;\n");
        printf("CHOICES: String, Character, N-Character, N-String, Mix;\n");
        return 0;
    }
    TestAnalyzer            analyzer;
    QUEX_NAME(Accumulator)& accumulator = analyzer.accumulator;

#   define self analyzer

    analyzer._token_queue.write_iterator = analyzer._token_queue.begin;
    analyzer._token_queue.read_iterator = analyzer._token_queue.begin;
    (void)QUEX_NAME(Accumulator_construct)(&accumulator, &analyzer);

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

    return 0;
}
