# Two lines to generate and compile the lexer:

all: explicit.exe implicit.exe 

hwut-info: 
	@echo explicit.exe implicit.exe

%.c: %.qx
	quex -i $< -o $* --language C

# -DQUEX_OPTION_DEBUG_SHOW_EXT 
%.exe: %.c lexer.c 
	gcc lexer.c $*/$< -I. -I$(HWUT_PATH) \
		-DQUEX_OPTION_ASSERTS_EXT_WARNING_MESSAGE_DISABLED_EXT \
		-DQUEX_SETTING_BUFFER_SIZE_EXT=4 \
		-DHEADER_FILE='"$*/$*.h"' -DLEXER_TYPE=$* -DTITLE='"$*"' \
		-DTOKEN_TYPE=$*_Token -DCONSTRUCT=$*_from_file_name \
		-DGET_STRING=$*_Token_get_string \
		-Wall -Werror \
		-o $@ -ggdb 

clean:
	rm -rf *.exe implicit.c explicit.c explicit implicit \
		  *.h *-configuration.h *-token.h *-token_ids.h \
