include ../Makefile.lexer

ifdef ASSERTS_ENABLED_F
	CCFLAG_ASSERTS=# By default asserts are enabled
else 
	CCFLAG_ASSERTS=-DQUEX_OPTION_ASSERTS_DISABLED_EXT
endif

LDC := $(LDC) -DQUEX_OPTION_MULTI_EXT -I. -ILexer -Wall -Werror

lexer: Lexer/Lexer.c lexer.c Common-token.c
	$(LDC) $^ -o  $@ $(LIB_ICU) 

lexerle.E: Lexer/Lexer.c 
	$(LDC) $^ -o  $@ $(LIB_ICU) -E > $@
	 
COMMON_TOKEN_OPTIONS = --token-class-file Common-token.h \
                       --suppress 5
	   	 	           # --no-message-on-extra-options \

Lexer/Lexer.c:  boeck.qx Common-token.c 
	quex --cbm -i $< -o Lexer -b 4 $(COMMON_TOKEN_OPTIONS) \
		 --language C --suppress 15 \
		 --token-id-prefix TKN_ \
		 --no-lib-quex \
		 --suppress 1 # --debug-exception

Common-token.c: 
	quex --cbm -i token_ids.qx token_type.qx \
		 -b 4                          \
		 -o Common  --odir .           \
		 --token-class Token           \
		 --token-class-only            \
	     --debug-exception             \
		 --language C 

#Lexer/Lexer.cpp:  boeck.qx Common-token.cpp Common-token_ids
#	quex -i $< -o boeck::Lexer -b 4 $(COMMON_TOKEN_OPTIONS) \
#		 --suppress 15 \
#		 # --debug-exception
#
#Common-token_ids \
#Common-token.cpp: 
#	quex -i token_ids.qx token_type.qx \
#		 -b 4                          \
#		 --token-id-prefix TKN_        \
#		 -o Common  --odir .           \
#		 --token-class Common::Token   \
#		 --token-class-only            \
#	     --debug-exception 

clean:
	rm -rf Lexer* lib* Common* lexer *.E *.o
