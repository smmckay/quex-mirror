# Two lines to generate and compile the lexer:

all: plain.exe implicit.exe plain_more.exe

hwut-info: 
	@echo plain.exe implicit.exe

%.c: %.qx
	quex -i $< -o $* --language C

%.exe: %.c lexer.c 
	gcc lexer.c $< -I$(QUEX_PATH) -I$(HWUT_PATH) \
		-DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED \
		-DHEADER_FILE='"$*.h"' -DLEXER_TYPE=quex_$* -DTITLE='"$*"' \
		-Wall -Werror \
		-o $@ -ggdb 

clean:
	rm -f plain.exe plain.c \
	      plain_more.exe plain_more.c \
	      implicit.exe implicit.c \
		  *.h *-configuration.h *-token.h *-token_ids.h \
