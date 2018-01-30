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
	 -fsanitize=address -I./ -I$(QUEX_PATH)                   \
	 -DQUEX_OPTION_DEBUG_SHOW_MODES        \
	 -DQUEX_OPTION_COUNTER_LINE_DISABLED   \
	 -DQUEX_OPTION_RUNTIME_MODE_TRANSITION_CHECK   

LD := $(LD0) -DQUEX_OPTION_COUNTER_COLUMN_DISABLED 

LD4     := $(LD) -DQUEX_SETTING_BUFFER_SIZE=4
LD65536 := $(LD) -DQUEX_SETTING_BUFFER_SIZE=65536

QUEX := $(QUEX_PATH)/quex-exe.py --suppress 3 --language C --token-id-prefix TK_

# (*) RULES ____________________________________________________________________
# -- application
all: $(TEST_FILES)

on_match.exe: on_match.qx 
	$(QUEX) -i $< -o EHLexer 
	$(LD4) ./lexer.c EHLexer.c -o $@  

on_indentation-%.exe: on_indentation-%.qx 
	$(QUEX) -i $< -o EHLexer 
	$(LD0) -DQUEX_SETTING_BUFFER_SIZE=65536 ./lexer.c EHLexer.c -o $@ 

on_load_failure.exe: on_load_failure.qx 
	$(QUEX) -i $< -o EHLexer 
	$(LD0) -DQUEX_SETTING_BUFFER_SIZE=6 ./lexer-probed.c EHLexer.c -o $@ 

on_bad_lexatom.exe: on_bad_lexatom.qx 
	$(QUEX) -i $< -o EHLexer --encoding utf16
	$(LD65536) ./lexer.c EHLexer.c -o $@ 

on_buffer_overflow.exe: on_buffer_overflow.qx 
	$(QUEX) -i $< -o EHLexer 
	$(LD4) ./lexer.c EHLexer.c -o $@ \
	       -DUNIT_TEST_DEFINE_MEMORY_MANAGER_IMPLEMENTATION

on_buffer_before_change.exe: on_buffer_before_change.qx 
	$(QUEX) -i $< -o EHLexer 
	$(LD4) ./lexer.c EHLexer.c -o $@  

on_skip_range_open.exe: on_skip_range_open.qx 
	$(QUEX) -i $< -o EHLexer 
	$(LD4) ./lexer.c EHLexer.c -o $@ `icu-config --ldflags`   

on_skip_range_open-customized.exe: on_skip_range_open-customized.qx 
	$(QUEX) -i $< -o EHLexer
	$(LD4) ./lexer.c EHLexer.c -o $@ `icu-config --ldflags`  

%.exe: %.qx 
	$(QUEX) -i $< -o EHLexer
	$(LD4) ./lexer.c EHLexer.c -o $@ `icu-config --ldflags`  

transit%.exe: transit%.qx lexer.c 
	$(QUEX) -i $< -o EHLexer 
	$(LD) ./lexer.c EHLexer.c -o $@ `icu-config --ldflags`      


# (*) HELPERS __________________________________________________________________
clean:	
	rm -f EHLexer*
	rm -f EasyLexer*
	rm -f *.exe
	rm -f lexer.o
	rm -f lexer
	rm -f token_ids
	rm -f *.bak
	rm -f $(TEST_FILES)
