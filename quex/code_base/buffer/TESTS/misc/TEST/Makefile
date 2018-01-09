TESTS := construct_destruct_included.exe \
	     extend_and_migrate.c

all: $(TESTS)

%.exe: %.c
	gcc $< -ggdb \
		-I$(QUEX_PATH) -I$(HWUT_PATH)/support/C -o $@ \
		-DQUEX_SETTING_BUFFER_INCLUDE_MIN_SIZE=4      \
		-DQUEX_SETTING_BUFFER_SIZE=11                 \
	    -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=1

hwut-info:
	@echo $(TESTS)

clean: 
	rm -f *.exe *.o 
	rm -f tmp.*
