TESTS := construct_destruct_included.exe \
	     extend_and_migrate-nested.exe \
	     extend_and_migrate.exe

CC    := gcc -ggdb -Wall -Werror \
		     -I. -I$(QUEX_PATH) -I$(HWUT_PATH)/support/C  \
		     -DQUEX_SETTING_BUFFER_INCLUDE_MIN_SIZE=4 \
		     -DQUEX_SETTING_BUFFER_SIZE=11            \

all: $(TESTS)

construct_destruct_included.exe: construct_destruct_included.c
	$(CC) -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=1 $^ -o $@

extend_and_migrate.exe: extend_and_migrate.c common.c
	$(CC) -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=0 $^ -o $@

extend_and_migrate-nested.exe: extend_and_migrate-nested.c common.c
	$(CC) -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=0 $^ -o $@
	    
%.E: %.c
	$(CC) -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=1 $^ -E > $@

hwut-info:
	@echo $(TESTS)

clean: 
	rm -f *.exe *.o *.E
	rm -f tmp.*
