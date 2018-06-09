
TESTS = queue.exe \
		queue-real.exe 

ENGINE = TPLex/TPLex.cpp

all: $(TESTS)

CCX = g++ -ggdb -Wall -Werror \
	 -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED_EXT \
	 -DQUEX_SETTING_TOKEN_QUEUE_SIZE_EXT=5 #

CC = $(CCX) \
	 -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED_EXT \
	 -DQUEX_SETTING_TOKEN_QUEUE_SIZE_EXT=5 \
	 -DQUEX_SETTING_TOKEN_QUEUE_SAFETY_BORDER_EXT=4 #

hwut-info:
	@echo $(TESTS)

queue.exe:            lexer.cpp 
	quex -i simple.qx -o TPLex 
	$(CC) -I. -DUNIT_TEST_PSEUDO_ANALYSIS lexer.cpp $(ENGINE) -lefence -o $@

queue-real.exe:       lexer.cpp  
	quex -i real.qx -o TPLex 
	$(CC) -I. lexer.cpp $(ENGINE) -lefence -o $@

%.E: %.cpp
	$(CC) -E -I$(QUEX_PATH) $< -o $@

%.o: %.cpp

clean:
	rm -rf TPLex*
	rm -rf $(TESTS)
	rm -rf *.o
