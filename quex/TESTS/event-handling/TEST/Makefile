.PHONY: clean 
TEST_FILES := transition.exe \
	          transition-x.exe \
			  on_match.exe \
			  on_bad_lexatom.exe \
	          on_buffer_overflow.exe \
	          on_buffer_before_change.exe \
			  on_skip_range_open.exe \
			  on_skip_range_open-customized.exe
	 
ifndef QUEX_PATH
    $(error The environment variable QUEX_PATH is not defined!)
endif


# (*) SETUP ____________________________________________________________________
# (*) COMPILER SETTINGS ________________________________________________________
#     (change COMPILER to whatever you use as compiler on the command line,
#     e.g. "make COMPILER=icpc" will use intel's c++ compiler)
COMPILER = gcc

LD0 := $(COMPILER) -Wno-deprecated -Wall -Werror -ggdb \
	 -I. -IEHLexer/lib                                 \
	 -DQUEX_OPTION_DEBUG_SHOW_MODES_EXT                \
	 -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED_EXT
	 # -fsanitize=address 

LD := $(LD0) \
	  -DQUEX_OPTION_ASSERTS   

LD4     := $(LD) -DQUEX_SETTING_BUFFER_SIZE_EXT=4 \
	             -DQUEX_SETTING_BUFFER_FALLBACK_N_EXT=0 \
	             -DQUEX_OPTION_ASSERTS   
LD65536 := $(LD0) -DQUEX_SETTING_BUFFER_SIZE_EXT=65536 \
	              -DQUEX_SETTING_BUFFER_FALLBACK_N_EXT=256 \

QUEX  := $(QUEX_PATH)/quex-exe.py --cbm --suppress 3 --language C --token-id-prefix TK_ --no-count-lines --no-count-columns
QUEX2 := $(QUEX_PATH)/quex-exe.py --cbm --suppress 3 --language C --token-id-prefix TK_ --no-count-lines

# (*) RULES ____________________________________________________________________
# -- application
all: $(TEST_FILES)

on_match.exe: on_match.qx 
	$(QUEX) -i $< -o EHLexer 
	$(LD4) ./lexer.c EHLexer/EHLexer.c -o $@  

on_indentation-%.exe: on_indentation-%.qx 
	$(QUEX2) -i $< -o EHLexer 
	$(LD0) -DQUEX_SETTING_BUFFER_SIZE_EXT=65536 ./lexer.c EHLexer/EHLexer.c -o $@ 

on_load_failure.exe: on_load_failure.qx 
	$(QUEX) -i $< -o EHLexer 
	$(LD0) -DQUEX_SETTING_BUFFER_SIZE_EXT=6 ./lexer-probed.c EHLexer/EHLexer.c -o $@ 

on_bad_lexatom.exe: on_bad_lexatom.qx 
	$(QUEX) -i $< -o EHLexer --encoding utf16 --no-count
	$(LD65536) ./lexer.c EHLexer/EHLexer.c -o $@ 

on_bad_lexatom-utf8.exe: on_bad_lexatom-utf8.qx 
	$(QUEX) -i $< -o EHLexer --encoding utf8 --no-count
	$(LD65536) ./lexer.c EHLexer/EHLexer.c -o $@ 

on_bad_lexatom-utf8-loop.exe: on_bad_lexatom-utf8-loop.qx 
	$(QUEX) -i $< -o EHLexer --encoding utf8 --no-count
	$(LD65536) ./lexer.c EHLexer/EHLexer.c -o $@ # -DQUEX_OPTION_DEBUG_SHOW_EXT

on_bad_lexatom-table-cp1006.exe: on_bad_lexatom-table-cp1006.qx 
	$(QUEX) -i $< -o EHLexer --encoding cp1006 --no-count --bet uint8_t
	$(LD65536) ./lexer.c EHLexer/EHLexer.c -o $@ # -DQUEX_OPTION_DEBUG_SHOW_EXT

on_bad_lexatom-converter.exe: on_bad_lexatom-converter.qx 
	$(QUEX) -i $< -o EHLexer --no-count --bet uint32_t
	$(LD65536) ./lexer-with-converter.c EHLexer/EHLexer.c -o $@ `icu-config --ldflags` # -DQUEX_OPTION_DEBUG_SHOW_EXT

on_buffer_overflow.exe: on_buffer_overflow.qx lexer-with-converter.c
	$(QUEX) -i $< -o EHLexer --emm
	$(LD4) ./lexer.c EHLexer/EHLexer.c -o $@ \
	       -DUNIT_TEST_MEMORY_MANAGER -DUNIT_TEST_IN_UT

on_buffer_before_change.exe: on_buffer_before_change.qx 
	$(QUEX) -i $< -o EHLexer 
	$(LD4) ./lexer.c EHLexer/EHLexer.c -o $@  

on_skip_range_open.exe: on_skip_range_open.qx 
	$(QUEX) -i $< -o EHLexer 
	$(LD4) ./lexer.c EHLexer/EHLexer.c -o $@ `icu-config --ldflags`   

on_skip_range_open-customized.exe: on_skip_range_open-customized.qx 
	$(QUEX) -i $< -o EHLexer
	$(LD4) ./lexer.c EHLexer/EHLexer.c -o $@ `icu-config --ldflags`  

%.exe: %.qx 
	$(QUEX) -i $< -o EHLexer
	$(LD4) ./lexer.c EHLexer/EHLexer.c -o $@ `icu-config --ldflags`  

transit%.exe: transit%.qx lexer.c 
	$(QUEX) -i $< -o EHLexer 
	$(LD) ./lexer.c EHLexer/EHLexer.c -o $@ `icu-config --ldflags`      


# (*) HELPERS __________________________________________________________________
clean:	
	rm -rf EHLexer* EasyLexer* *.exe lexer.o lexer token_ids *.bak $(TEST_FILES) ut
