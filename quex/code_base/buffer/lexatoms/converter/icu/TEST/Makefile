# Testing the implementation of the 'Converter' interface for the IConv
# library.
#
# There are three tests: 
#
#     'one-beat': The complete source is converted completely into
#                 the drain (source and drain a fully available).
#
#     'stepwise-source': The source is fed into the converter byte-
#                        by byte. So the converter must eventually
#                        wait until a character representation is
#                        complete.
#
#     'stepwise-drain': It is left only place for one character to
#                       be converted, so the converter must stop
#                       at the right source positions.
#
# (C) Frank-Rene Schaefer
#______________________________________________________________________________

.SECONDARY:

FILES := $(foreach S, 1 2 4 WC, one-beat-$(S).exe)       \
	     $(foreach S, 1 2 4 WC, stepwise-drain-$(S).exe) \
	     $(foreach S, 1 2 4 WC, stepwise-source-$(S).exe) 

TEST_SUPPORT_DIR := ../../TEST-SUPPORT#

BASIC_SOURCES := $(TEST_SUPPORT_DIR)/basic_functionality.c \
	             basic_functionality-icu.c

DEFS := -DQUEX_OPTION_ASSERTS \
	    -DQUEX_SETTING_BUFFER_FILLER_SEEK_TEMP_BUFFER_SIZE_EXT=6 \
        -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N_EXT=0 

INCLUDES := -I. -I$(HWUT_PATH)/support/C -I$(TEST_SUPPORT_DIR) -I../../../../../TESTS -I../../../../../

ICU_LIBS := $(shell icu-config --ldflags) 

CC := g++ $(INCLUDES) $(DEFS) \
		-ggdb  \
		-Wall -Werror \
        -Werror-implicit-function-declaration -DQUEX_INLINE=inline 

all: $(FILES)

hwut-info:
	@echo $(FILES)

hwut-end: clean
	@echo Bye

%-1.exe: %.cpp ut
	$(CC) $< $(BASIC_SOURCES) $(ICU_LIBS) -o $@ -DQUEX_TYPE_LEXATOM_EXT=uint8_t 

%-2.exe: %.cpp ut
	$(CC) $< $(BASIC_SOURCES) $(ICU_LIBS) -o $@ -DQUEX_TYPE_LEXATOM_EXT=uint16_t 

%-4.exe: %.cpp ut
	$(CC) $< $(BASIC_SOURCES) $(ICU_LIBS) -o $@ -DQUEX_TYPE_LEXATOM_EXT=uint32_t 

%-WC.exe: %.cpp ut
	$(CC) $< $(BASIC_SOURCES) $(ICU_LIBS) -o $@ -DQUEX_TYPE_LEXATOM_EXT=wchar_t 

ut:
	python ../../../../../TESTS/code_base_instatiation.py ut buffer quex analyzer

%.E: %.cpp
	g++ $(DEFS) $(INCLUDES) -E $< -o $@

%.E: %.c
	g++ $(DEFS) $(INCLUDES) -E $< -o $@

clean:
	rm -rf $(FILES) ut *.o *.E *~
