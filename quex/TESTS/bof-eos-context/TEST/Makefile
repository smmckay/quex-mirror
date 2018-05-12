# Two lines to generate and compile the lexer:

all: explicit.exe implicit.exe 

hwut-info: 
	@echo explicit.exe implicit.exe

%.c: %.qx
	quex -i $< -o $* --language C

# -DQUEX_OPTION_DEBUG_SHOW 
%.exe: %.c lexer.c 
	gcc lexer.c $*/$< -I. -I$(HWUT_PATH) \
		-DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED \
		-DQUEX_SETTING_BUFFER_SIZE=4 \
		-DHEADER_FILE='"$*/$*.h"' -DLEXER_TYPE=$* -DTITLE='"$*"' -DTOKEN_TYPE=$*_Token \
		-Wall -Werror \
		-o $@ -ggdb 

clean:
	rm -rf *.exe implicit.c explicit.c explicit implicit \
		  *.h *-configuration.h *-token.h *-token_ids.h \
