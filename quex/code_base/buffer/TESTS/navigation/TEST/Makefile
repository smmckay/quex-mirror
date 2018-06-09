# PURPOSE: Building applications for massive seek&tell tests on the Buffer-seek.
#          
# Buffer seeking sets the 'read_p' to a specific character index. It includes
# loading the required content into the buffer's engine. The test depends on
# the size of a character and the fallback number (number of characters left
# in front, to prevent permanent backward loading).
#
# The files in this directory check on different filler types. They do not
# check on different byte-loader types. Byte-loading is extensively tested
# elsewhere.
# 
# QUEX_TYPE_LEXATOM and QUEX_SETTING_BUFFER_MIN_FALLBACK_N are controlled
# at compile time. Thus, to variate those two, different test object files 
# must be build from ONE source file. Therefore, for each combination a rule
# exists that produces the object file. Rules follow the scheme:
#
#              %-SIZE-FALLBACK_.exe: %.cpp
#
# with SIZE as sizeof(QUEX_TYPE_LEXATOM) and FALLBACK_ as the value of 
# QUEX_SETTING_BUFFER_MIN_FALLBACK_N.
#
# (C) Frank-Rene Schaefer
#______________________________________________________________________________
.SECONDARY:

TESTS := \
	     $(foreach S, 1 2 4, $(foreach FB, 0 1 2, test-Plain-$(S)-$(FB).exe)) \
	     $(foreach S, 1 2 4, $(foreach FB, 0 1 2, test-Converter-$(S)-$(FB).exe)) \
	     $(foreach FB, 0 1 2, test-Plain-wiostream-wchar_t-$(FB).exe) \
	     $(foreach S, 1 2 4, $(foreach FB, 0 2, test-Converter-StrangeStream-$(S)-$(FB).exe)) 

DEFS := -DQUEX_OPTION_ASSERTS_EXT \
	    -DQUEX_SETTING_TRANSLATION_BUFFER_SIZE_EXT=7 \
        -DQUEX_SETTING_BUFFER_FILLER_SEEK_TEMP_BUFFER_SIZE_EXT=5 

# -DUNIT_TEST_POSITIONING_TEST_N=128 

INCLUDES   := -I. -I$(HWUT_PATH)/support/C -I../../../../ 

SIZE_1     := -DQUEX_TYPE_LEXATOM=uint8_t
SIZE_2     := -DQUEX_TYPE_LEXATOM=uint16_t
SIZE_4     := -DQUEX_TYPE_LEXATOM=uint32_t
SIZE_WC    := -DQUEX_TYPE_LEXATOM=wchar_t
FALLBACK_0 := -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N_EXT=0 
FALLBACK_1 := -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N_EXT=1 
FALLBACK_2 := -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N_EXT=2

CFLAGS := -ggdb -Wall -Werror $(INCLUDES) $(DEFS) \
	      -fsanitize=address basic_functionality.c
CC     := gcc $(CFLAGS) -DQUEX_INLINE= -DQUEX_OPTION_PLAIN_C_EXT # -pg -fprofile-arcs
CCP    := g++ $(CFLAGS) -DQUEX_INLINE=inline 

XLIBS := $(shell icu-config --ldflags) 

all: $(TESTS)

hwut-info:
	@echo $(TESTS)

hwut-end: clean

# RULES _______________________________________________________________________
#
%-4-0.exe: %.c basic_functionality.c ut
	$(CC) $(SIZE_4) $(FALLBACK_0) $< $(XLIBS) -o $@ 
%-4-1.exe: %.c basic_functionality.c  ut
	$(CC) $(SIZE_4) $(FALLBACK_1) $< $(XLIBS) -o $@
%-4-2.exe: %.c basic_functionality.c  ut
	$(CC) $(SIZE_4) $(FALLBACK_2) $< $(XLIBS) -o $@

%-4-0.exe: %.cpp basic_functionality.c  ut
	$(CCP) $(SIZE_4) $(FALLBACK_0) $< $(XLIBS) -o $@
%-4-1.exe: %.cpp basic_functionality.c  ut
	$(CCP) $(SIZE_4) $(FALLBACK_1) $< $(XLIBS) -o $@
%-4-2.exe: %.cpp basic_functionality.c  ut
	$(CCP) $(SIZE_4) $(FALLBACK_2) $< $(XLIBS) -o $@

%-2-0.exe: %.c basic_functionality.c  ut
	$(CC) $(SIZE_2) $(FALLBACK_0) $< $(XLIBS) -o $@
%-2-1.exe: %.c basic_functionality.c  ut
	$(CC) $(SIZE_2) $(FALLBACK_1) $< $(XLIBS) -o $@
%-2-2.exe: %.c basic_functionality.c  ut
	$(CC) $(SIZE_2) $(FALLBACK_2) $< $(XLIBS) -o $@

%-wchar_t-0.exe: %.cpp basic_functionality.c  ut-cpp
	$(CCP) $(SIZE_WC) $(FALLBACK_0) $< $(XLIBS) -o $@
%-wchar_t-1.exe: %.cpp basic_functionality.c  ut-cpp
	$(CCP) $(SIZE_WC) $(FALLBACK_1) $< $(XLIBS) -o $@
%-wchar_t-2.exe: %.cpp basic_functionality.c  ut-cpp
	$(CCP) $(SIZE_WC) $(FALLBACK_2) $< $(XLIBS) -o $@

%-2-0.exe: %.cpp basic_functionality.c  ut-cpp
	$(CCP) $(SIZE_WC) $(FALLBACK_0) $< $(XLIBS) -o $@
%-2-1.exe: %.cpp basic_functionality.c  ut-cpp
	$(CCP) $(SIZE_WC) $(FALLBACK_1) $< $(XLIBS) -o $@
%-2-2.exe: %.cpp basic_functionality.c  ut-cpp
	$(CCP) $(SIZE_WC) $(FALLBACK_2) $< $(XLIBS) -o $@

%-1-0.exe: %.c basic_functionality.c  ut
	$(CC) $(SIZE_1) $(FALLBACK_0) $< $(XLIBS) -o $@
%-1-1.exe: %.c basic_functionality.c  ut
	$(CC) $(SIZE_1) $(FALLBACK_1) $< $(XLIBS) -o $@
%-1-2.exe: %.c basic_functionality.c  ut
	$(CC) $(SIZE_1) $(FALLBACK_2) $< $(XLIBS) -o $@

%-1-0.exe: %.cpp basic_functionality.c  ut-cpp
	$(CCP) $(SIZE_1) $(FALLBACK_0) $< $(XLIBS) -o $@
%-1-1.exe: %.cpp basic_functionality.c  ut-cpp
	$(CCP) $(SIZE_1) $(FALLBACK_1) $< $(XLIBS) -o $@
%-1-2.exe: %.cpp basic_functionality.c  ut-cpp
	$(CCP) $(SIZE_1) $(FALLBACK_2) $< $(XLIBS) -o $@


ut-cpp:
	python ../../../../TESTS/code_base_instatiation.py ut-cpp analyzer quex buffer lexeme_converter extra 
ut:
	python ../../../../TESTS/code_base_instatiation.py ut analyzer quex buffer lexeme_converter extra --language C

clean: 
	rm -rf $(TESTS) ut ut-cpp
	rm -rf *-gen.[ch]
	rm -rf *-gen.[ch].[ch]   # some unattended build results ...
	rm -rf *.exe
