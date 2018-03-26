TESTS := construct_destruct_included.exe \
	     extend_and_migrate-nested.exe \
	     extend_and_migrate.exe \
		 negotiate_extend.exe

CC    := gcc -ggdb -Wall -Werror \
		     -I. -I../../../../TESTS -Iut/lib -I$(HWUT_PATH)/support/C  \
		     -DQUEX_SETTING_BUFFER_SIZE_MIN=4 \
		     -DQUEX_SETTING_BUFFER_SIZE=11            \

all: $(TESTS)

construct_destruct_included.exe: construct_destruct_included.c ut
	$(CC) -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=1 $< -o $@

extend_and_migrate.exe: extend_and_migrate.c common.c ut
	$(CC) -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=0 $< common.c -o $@

extend_and_migrate-nested.exe: extend_and_migrate-nested.c common.c ut
	$(CC) -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=0 $< common.c -o $@

negotiate_extend.exe: negotiate_extend.c common.c ut
	$(CC) -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=0 $< common.c -o $@
	    
%.E: %.c
	$(CC) -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=1 $^ -E > $@

hwut-info:
	@echo $(TESTS)

ut:
	python ../../../../TESTS/code_base_instatiation.py ut buffer compatibility

clean: 
	rm -rf *.exe *.o *.E ut tmp.*
