#include <stddef.h>
#include <stdio.h>
#define QUEX_TYPE_STATISTICS_COUNTER unsigned int
#define __QUEX_STD_fopen             fopen
#define __QUEX_STD_fclose            fclose
#define __QUEX_STD_fprintf           fprintf
typedef unsigned char TestAnalyzer_lexatom_t;

#include "ut/lib/analyzer/Statistics"
#include "ut/lib/analyzer/Statistics.i"
#include <support/C/hwut_unit.h>


const TestAnalyzer_lexatom_t    TestAnalyzer_statistics_MODE_0_4711_boundary_list[] =
{ 0, 1, 2, 3, 197, 198, 199, 200 };
QUEX_TYPE_STATISTICS_COUNTER TestAnalyzer_statistics_MODE_0_4711_counter_list[9];

const TestAnalyzer_lexatom_t    TestAnalyzer_statistics_MODE_1_4712_boundary_list[] =
{ 1, 2, 3, 6, 12, 24, 48, 96, 192, };
QUEX_TYPE_STATISTICS_COUNTER TestAnalyzer_statistics_MODE_1_4712_counter_list[10];

const size_t XXX=5;

const TestAnalyzer_statistics_state  TestAnalyzer_statistics_state_list[] = {
    {
        /* mode_name   */ "MODE_0",
        /* state_index */ 4711,
        { 
            8,
            (const TestAnalyzer_lexatom_t*)TestAnalyzer_statistics_MODE_0_4711_boundary_list,
            (QUEX_TYPE_STATISTICS_COUNTER* const)TestAnalyzer_statistics_MODE_0_4711_counter_list,
        }
    },
    {
        /* mode_name   */ "MODE_1",
        /* state_index */ 4712,
        { 
            9,
            (const TestAnalyzer_lexatom_t*)TestAnalyzer_statistics_MODE_1_4712_boundary_list,
            (QUEX_TYPE_STATISTICS_COUNTER* const)TestAnalyzer_statistics_MODE_1_4712_counter_list,
        }
    }
};

const TestAnalyzer_statistics_state* TestAnalyzer_statistics_state_list_end = \
                            (const TestAnalyzer_statistics_state*)TestAnalyzer_statistics_state_list + 2;

int
main(int argc, char** argv)
{
    int   i = 0;
    FILE* fh = NULL;
    char  buffer[1024];

    hwut_info("Statistics Module");

    for(i = 0; i != 202; ++i) {
        TestAnalyzer_statistics_state_count(&TestAnalyzer_statistics_state_list[0], i);
        TestAnalyzer_statistics_state_count(&TestAnalyzer_statistics_state_list[1], i);
    } 
    TestAnalyzer_statistics_save("tmp.log");

    fh = fopen("tmp.log", "rb");
    i = (int)fread((void*)buffer, 1, 1024, fh);
    buffer[i] = '\0';
    printf("%s", buffer);
    fclose(fh);
    return 0;
}
