TESTS := $(foreach DIRECTION, backward forward,             \
			 $(foreach FB, 0 1 2, $(DIRECTION)-fb$(FB).exe) \
			 $(DIRECTION)-fb2-32.exe                        \
	     ) \
		 forward-api.exe
.SECONDARY: $(TESTS)

FALLBACK_0 := -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=0 
FALLBACK_1 := -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=1 
FALLBACK_2 := -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=2

ICU_LIBS   := $(shell icu-config --ldflags) 

DEFS = \
	   -D__QUEX_OPTION_PLAIN_C \
	   -DQUEX_OPTION_ASSERTS 
#      -DQUEX_OPTION_INFORMATIVE_BUFFER_OVERFLOW_MESSAGE

CC_PURE := gcc \
		  -Wall -Werror -ggdb \
		  -I. -I$(QUEX_PATH) -I$(HWUT_PATH)/support/C \
		  $(DEFS) 

CC := gcc \
		  -Wall -Werror -ggdb \
		  -I. -I$(QUEX_PATH) -I$(HWUT_PATH)/support/C \
		  $(DEFS) 

all: $(TESTS)

hwut-info:
	@echo $(TESTS)

hwut-end: clean
	@echo Bye

%-fb0.exe: %.c 
	$(CC) $(FALLBACK_0) -DQUEX_TYPE_LEXATOM=uint8_t $^ -o $@ 
%-fb1.exe: %.c 
	$(CC) $(FALLBACK_1) -DQUEX_TYPE_LEXATOM=uint8_t $^ -o $@
%-fb2.exe: %.c 
	$(CC) $(FALLBACK_2) -DQUEX_TYPE_LEXATOM=uint8_t $^ -o $@
%-fb2-32.exe: %.c 
	$(CC) $(FALLBACK_2) -DQUEX_TYPE_LEXATOM=uint32_t $^ -o $@
%-api.exe: %-api.c 
	$(CC) $(FALLBACK_2) -DQUEX_TYPE_LEXATOM=uint32_t $^ -o $@ $(ICU_LIBS) \
		-DHWUT_OPTION_NO_ASSUMPTION_ON_LEXATOM_INDEX_AT_END

clean: 
	rm -rf $(TEST_FILES)
	rm -rf *.o
	rm -rf *-gen.[ch]
	rm -rf *-gen.[ch].[ch]   # some unattended build results ...
	rm -rf *.exe
