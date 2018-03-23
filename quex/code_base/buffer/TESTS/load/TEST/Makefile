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
		  -I. -I$(HWUT_PATH)/support/C -I../../../../ \
		  $(DEFS) 

CC := gcc \
		  -Wall -Werror -ggdb \
		  -I. -I$(HWUT_PATH)/support/C -I../../../../ \
		  $(DEFS) 

all: $(TESTS)

hwut-info:
	@echo $(TESTS)

hwut-end: clean
	@echo Bye

%-fb0.exe: %.c ut
	$(CC) $(FALLBACK_0) -DQUEX_TYPE_LEXATOM=uint8_t $< -o $@ 
%-fb1.exe: %.c ut
	$(CC) $(FALLBACK_1) -DQUEX_TYPE_LEXATOM=uint8_t $< -o $@
%-fb2.exe: %.c ut
	$(CC) $(FALLBACK_2) -DQUEX_TYPE_LEXATOM=uint8_t $< -o $@
%-fb2-32.exe: %.c ut
	$(CC) $(FALLBACK_2) -DQUEX_TYPE_LEXATOM=uint32_t $< -o $@
%-api.exe: %-api.c ut
	$(CC) $(FALLBACK_2) -DQUEX_TYPE_LEXATOM=uint32_t $< -o $@ $(ICU_LIBS) \
		-DHWUT_OPTION_NO_ASSUMPTION_ON_LEXATOM_INDEX_AT_END

ut:
	python ../../../../TESTS/code_base_instatiation.py ut analyzer compatibility buffer lexeme_converter

clean: 
	rm -rf $(PROGRAMS) ut
	rm -rf *-gen.[ch]
	rm -rf *-gen.[ch].[ch]   # some unattended build results ...
	rm -rf *.exe
