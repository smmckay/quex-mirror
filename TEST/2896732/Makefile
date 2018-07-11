include ../Makefile.lexer

lexer:
	quex --cbm -i uXa.qx -o Lexer \
		 --token-id-prefix QUEX_UUID_ --token-id-offset 1114114 \
		 -b 2 --suppress 15
	$(LDCPP_ICU) -o uXa uXa.cpp Lexer/Lexer.cpp \
		         -DQUEX_OPTION_TOKEN_STAMPING_WITH_LINE_AND_COLUMN_EXT \
				 $(LIB_ICU) -ggdb
clean:
	rm -rf Lexer*
	rm -rf ./uXa
