.SECONDARY:

OBJS =  lexer.o          \
		boeck_Lexer.o    \
		max_Lexer.o      \
		moritz_Lexer.o             

ifdef ASSERTS_ENABLED_F
	CCFLAG_ASSERTS=# By default asserts are enabled
else 
	CCFLAG_ASSERTS=-DQUEX_OPTION_ASSERTS_DISABLED
endif

CC := g++ -ggdb -Wall -Werror -DQUEX_OPTION_MULTI 

lexer: $(OBJS)
	g++ $(OBJS) -ggdb -o $@ 
	 
# -DQUEX_OPTION_ASSERTS_DISABLED
# -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED 

lexer.o: lexer.cpp max_Lexer moritz_Lexer boeck_Lexer
	$(CC) -c $< -o $@ -I$(QUEX_PATH) $(CCFLAG_ASSERTS) 

%.o: %.cpp 
	$(CC) -c $< -o $@ -I$(QUEX_PATH) $(CCFLAG_ASSERTS) 
	
# -DQUEX_OPTION_ASSERTS_DISABLED
# -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED 

%.E: %.cpp
	$(CC) $< -E -o $@ -I$(QUEX_PATH) $(CCFLAG_ASSERTS) 
		
# -DQUEX_OPTION_ASSERTS_DISABLED
# -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED 

max_Lexer \
max_Lexer.cpp:    max.qx
	quex -i token.qx $< -o max::Lexer -b 4                \
		 --token-id-prefix MAX_TKN_ \
		 --suppress 6

moritz_Lexer \
moritz_Lexer.cpp: moritz.qx
	quex -i token.qx $< -o moritz::Lexer -b 2                \
		 --token-id-prefix MORITZ_TKN_ \
		 --suppress 6

boeck_Lexer \
boeck_Lexer.cpp:  boeck.qx
	quex -i token.qx $< -o boeck::Lexer --encoding utf8 \
		 --token-id-prefix TKN_ \
		 --suppress 6

clean:
	rm -rf boeck_Lexer*
	rm -rf max_Lexer*
	rm -rf moritz_Lexer*
	rm -rf lexer
	rm -rf *.E
	rm -rf lexer.o
