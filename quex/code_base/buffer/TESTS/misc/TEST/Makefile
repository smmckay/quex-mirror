all: construct_destruct_included.exe

construct_destruct_included.exe: 
	gcc construct_destruct_included.c -ggdb \
		-I$(QUEX_PATH) -I$(HWUT_PATH)/support/C -o $@ \
		-DQUEX_SETTING_BUFFER_INCLUDE_MIN_SIZE=4      \
		-DQUEX_SETTING_BUFFER_SIZE=11                 \
	    -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=1

clean: 
	rm -f *.exe *.o 
	rm -f tmp.*
