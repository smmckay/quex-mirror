#include "Simple/Simple.h"
#include "string.h"

int
main(int argc, char** argv)
{
    quex_Simple        qlex;
    FILE*              dummy_fh = fopen("main.c", "rb");
    QUEX_TYPE_LEXATOM* dummy_str = (QUEX_TYPE_LEXATOM*)"Otto";
    QUEX_TYPE_LEXATOM* dummy_str_end = dummy_str + strlen((const char*)dummy_str);

    /* Run this program with valgrind to see whether memory leak occurs. */
    QUEX_NAME(from_memory)(&qlex, 0x0, 0, 0x0);

    qlex.accumulator.add(&qlex.accumulator, dummy_str, dummy_str_end);

    qlex.post_categorizer.enter(&qlex.post_categorizer, (QUEX_TYPE_LEXATOM*)"Otto", 12); 

    qlex.include_push_file_name(&qlex, "main.c", NULL);

    QUEX_NAME(destruct)(&qlex);

    QUEX_NAME(from_memory)(&qlex, 0x0, 0, 0x0);
    qlex.include_push_file_name(&qlex, "main.c", NULL);
    qlex.reset_file_name(&qlex, "main.c", NULL);
    QUEX_NAME(destruct)(&qlex);
    fclose(dummy_fh);

    return 0;
}
