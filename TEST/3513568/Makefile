include ../Makefile.lexer

ENGINE = Lexer/boeck_Lexer.c   

ifdef ASSERTS_ENABLED_F
	CCFLAG_ASSERTS=# By default asserts are enabled
else 
	CCFLAG_ASSERTS=-DQUEX_OPTION_ASSERTS_DISABLED
endif

CC := $(CC) -DQUEX_OPTION_MULTI -I.

lexer: Lexer/Lexer.c lexer.o Common-token.o
	$(LDC) $^ -o  $@ $(LIB_ICU) 
	 
%.o: %.c 
	$(CC) -ICommon $< -o $@ $(CCFLAG_ASSERTS) 

# -DQUEX_OPTION_ASSERTS_DISABLED
# -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED 

COMMON_TOKEN_OPTIONS = --token-class-file Common-token.h \
                       --suppress 5
	   	 	           # --no-message-on-extra-options \

Lexer/Lexer.c:  boeck.qx Common-token.c Common-token_ids
	quex -i $< -o boeck::Lexer -b 4 $(COMMON_TOKEN_OPTIONS) \
		 --language C --suppress 15 \
		 --debug-exception

Common-token_ids \
Common-token.c: 
	quex -i token_ids.qx token_type.qx \
		 -b 4                          \
		 --token-id-prefix TKN_        \
		 -o Common  --odir .           \
		 --token-class Common::Token   \
		 --token-class-only            \
	     --debug-exception \
		 --language C 

clean:
	rm -rf Lexer* lib* Common* lexer *.E *.o
