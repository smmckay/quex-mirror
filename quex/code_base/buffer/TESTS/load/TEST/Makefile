TESTS := $(foreach DIRECTION, backward forward,             \
			 $(foreach FB, 0 1 2, $(DIRECTION)-fb$(FB).exe) \
			 $(DIRECTION)-fb2-32.exe                        \
	     ) \
		 forward-api.exe
.SECONDARY: $(TESTS)

FALLBACK_0 := -DQUEX_UT_SETTING_BUFFER_FALLBACK_N_EXT=0 
FALLBACK_1 := -DQUEX_UT_SETTING_BUFFER_FALLBACK_N_EXT=1 
FALLBACK_2 := -DQUEX_UT_SETTING_BUFFER_FALLBACK_N_EXT=2

ICU_LIBS   := $(shell icu-config --ldflags) 

DEFS = \
	   -DQUEX_OPTION_PLAIN_C_EXT \
	   -DQUEX_OPTION_ASSERTS 
#      -DQUEX_OPTION_INFORMATIVE_BUFFER_OVERFLOW_MESSAGE_EXT

CC_PURE := gcc \
		  -Wall -Werror -ggdb -DQUEX_INLINE= \
		  -I. -I$(HWUT_PATH)/support/C -I../../../../ -I../../../../TESTS \
		  $(DEFS) 

CC := gcc \
		  -Wall -Werror -ggdb -DQUEX_INLINE= \
		  -I. -I$(HWUT_PATH)/support/C -I../../../../ -I../../../../TESTS \
		  $(DEFS) 

all: $(TESTS)

hwut-info:
	@echo $(TESTS)

hwut-end: clean
	@echo Bye

%-fb0.exe: %.c 
	$(CC) $(FALLBACK_0) -DQUEX_TYPE_LEXATOM_EXT=uint8_t $< -o $@ 
%-fb1.exe: %.c 
	$(CC) $(FALLBACK_1) -DQUEX_TYPE_LEXATOM_EXT=uint8_t $< -o $@
%-fb2.exe: %.c 
	$(CC) $(FALLBACK_2) -DQUEX_TYPE_LEXATOM_EXT=uint8_t $< -o $@
%-fb2-32.exe: %.c 
	$(CC) $(FALLBACK_2) -DQUEX_TYPE_LEXATOM_EXT=uint32_t $< -o $@
%-api.exe: %-api.c 
	$(CC) $(FALLBACK_2) -DQUEX_TYPE_LEXATOM_EXT=uint32_t $< -o $@ $(ICU_LIBS) \
		-DHWUT_OPTION_NO_ASSUMPTION_ON_LEXATOM_INDEX_AT_END

clean: 
	rm -rf $(PROGRAMS) 
	rm -rf *-gen.[ch]
	rm -rf *-gen.[ch].[ch]   # some unattended build results ...
	rm -rf *.exe
