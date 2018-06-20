
TESTS = \
		simple-queue.exe \

ENGINE = Simple/Simple.cpp

all: $(TESTS)

CC = g++ -ggdb -Wall -Werror \
	 -DQUEX_SETTING_TOKEN_QUEUE_SIZE_EXT=3 \
	 -DQUEX_SETTING_TOKEN_QUEUE_SAFETY_BORDER_EXT=0 \
	 -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED_EXT \

hwut-info:
	@echo $(TESTS) 

simple-queue.exe: lexer.cpp  token.qx send-via-name.qx
	quex -i token.qx send-via-name.qx -o Simple \
		 --suppress 15
	$(CC) -I. lexer.cpp $(ENGINE) -o $@

%.E: %.cpp
	$(CC) -E -I$(QUEX_PATH) $< -o $@

%.o: %.cpp

clean:
	rm -rf Simple*
	rm -rf $(TESTS)
	rm -rf *.o
