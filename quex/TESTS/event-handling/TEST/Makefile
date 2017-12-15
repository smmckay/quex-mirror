.PHONY: clean 
.SECONDARY: transition.exe \
	        transition-x.exe \
			on_skip_range_open.exe \
			on_skip_range_open-customized.exe
	 
TEST_FILES = transition.sh \
			 transition-x.sh \
			 on_skip_range_open.sh \
			 on_skip_range_open-customized.sh 

ifndef QUEX_PATH
    $(error The environment variable QUEX_PATH is not defined!)
endif


# (*) SETUP ____________________________________________________________________
# (*) COMPILER SETTINGS ________________________________________________________
#     (change COMPILER to whatever you use as compiler on the command line,
#     e.g. "make COMPILER=icpc" will use intel's c++ compiler)
COMPILER = gcc
LD = $(COMPILER) -Wno-deprecated -Wall -Werror \
	 -I./ -I$(QUEX_PATH) \
	 -DQUEX_OPTION_DEBUG_SHOW_MODES                \
	 -DQUEX_OPTION_COUNTER_COLUMN_DISABLED \
	 -DQUEX_OPTION_COUNTER_LINE_DISABLED   \
	 -DQUEX_OPTION_RUNTIME_MODE_TRANSITION_CHECK   
     # -ggdb \
	 # -DQUEX_OPTION_DEBUG_SHOW

QUEX := $(QUEX_PATH)/quex-exe.py --suppress 3 

# (*) RULES ____________________________________________________________________
# -- application
all: $(TEST_FILES)

hwut-info:
	@echo $(TEST_FILES)

transit%.sh: transit%.exe
	@cat template.sh | sed -e 's/EXE/$</g' > $@
	chmod ua+rx $@

on_skip_range_open.sh: on_skip_range_open.exe
	@cat template.sh | sed -e 's/EXE/$</g' > $@
	chmod ua+rx $@

on_skip_range_open-customized.sh: on_skip_range_open-customized.exe
	@cat template.sh | sed -e 's/EXE/$</g' > $@
	chmod ua+rx $@


transit%.exe: transit%.qx lexer.c 
	$(QUEX) -i $< -o EHLexer --token-id-prefix TK_ --debug-exception --language C
	$(LD) ./lexer.c EHLexer.c -o $@ \
		-D__TEST_DESCRIPTION='"Mode Transitions: $<"' \
		`icu-config --ldflags`      \
		-D__TEST_CHOICES='"1, 2, 3, error"'

on_buffer_overflow.exe: on_buffer_overflow.qx 
	echo $<
	$(QUEX) -i $< -o Simple --token-id-prefix TK_ --language C
	$(LD) ./lexer.c Simple.c -o $@ -ggdb \
		  -D__TEST_DESCRIPTION='"Customized 'on_buffer_overflow' event."' \
          -DQUEX_SETTING_BUFFER_SIZE=4 

on_skip_range_open.exe: on_skip_range_open.qx 
	echo $<
	$(QUEX) -i $< -o EHLexer --token-id-prefix TK_ --debug-exception --language C
	$(LD) ./lexer.c EHLexer.c -o $@ -ggdb \
		-D__TEST_DESCRIPTION='"Default 'on_skip_range_open' event."' \
		`icu-config --ldflags`      \
		-D__TEST_CHOICES='"default"' \
          -DQUEX_SETTING_BUFFER_SIZE=4 \

on_skip_range_open-customized.exe: on_skip_range_open-customized.qx 
	$(QUEX) -i $< -o EHLexer --token-id-prefix TK_ --debug-exception --language C
	$(LD) ./lexer.c EHLexer.c -o $@ \
		-D__TEST_DESCRIPTION='"Customized 'on_skip_range_open' event."' \
		`icu-config --ldflags`      \
		-D__TEST_CHOICES='"customized"' \
          -DQUEX_SETTING_BUFFER_SIZE=4 \

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
