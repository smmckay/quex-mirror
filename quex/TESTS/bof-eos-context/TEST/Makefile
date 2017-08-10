# Two lines to generate and compile the lexer:

all: explicit.exe implicit.exe 

hwut-info: 
	@echo explicit.exe implicit.exe

%.c: %.qx
	quex -i $< -o $* --language C

# -DQUEX_OPTION_DEBUG_SHOW 
%.exe: %.c lexer.c 
	gcc lexer.c $< -I$(QUEX_PATH) -I$(HWUT_PATH) \
		-DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED \
		-DHEADER_FILE='"$*.h"' -DLEXER_TYPE=quex_$* -DTITLE='"$*"' \
		-Wall -Werror \
		-o $@ -ggdb 

clean:
	rm -f *.exe implicit.c explicit.c \
		  *.h *-configuration.h *-token.h *-token_ids.h \
