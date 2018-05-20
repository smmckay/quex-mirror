#include "Simple/Simple.h"
#include "string.h"

int
main(int argc, char** argv)
{
    Simple            qlex;
    FILE*             dummy_fh = fopen("main.c", "rb");
    Simple_lexatom_t* dummy_str = (Simple_lexatom_t*)"Otto";
    Simple_lexatom_t* dummy_str_end = dummy_str + strlen((const char*)dummy_str);

    /* Run this program with valgrind to see whether memory leak occurs. */
    Simple_from_memory(&qlex, 0x0, 0, 0x0);

    qlex.accumulator.add(&qlex.accumulator, dummy_str, dummy_str_end);

    qlex.post_categorizer.enter(&qlex.post_categorizer, (Simple_lexatom_t*)"Otto", 12); 

    qlex.include_push_file_name(&qlex, "main.c", NULL);

    Simple_destruct(&qlex);

    Simple_from_memory(&qlex, 0x0, 0, 0x0);
    qlex.include_push_file_name(&qlex, "main.c", NULL);
    qlex.reset_file_name(&qlex, "main.c", NULL);
    Simple_destruct(&qlex);
    fclose(dummy_fh);

    return 0;
}
