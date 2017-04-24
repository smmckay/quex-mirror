
TESTS = queue.exe \
		queue-real.exe 

ENGINE = TPLex.cpp

all: $(TESTS)

CCX = g++ -ggdb -Wall -Werror \
	 -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED \
	 -DQUEX_SETTING_TOKEN_QUEUE_SIZE=5 #

CC = $(CCX) \
	 -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED \
	 -DQUEX_SETTING_TOKEN_QUEUE_SIZE=5 \
	 -DQUEX_SETTING_TOKEN_QUEUE_SAFETY_BORDER=4 #

hwut-info:
	@echo $(TESTS)

queue.exe:            lexer.cpp 
	quex -i simple.qx -o TPLex 
	$(CC) -I$(QUEX_PATH) -DUNIT_TEST_PSEUDO_ANALYSIS lexer.cpp $(ENGINE) -lefence -o $@

queue-real.exe:       lexer.cpp  
	quex -i real.qx -o TPLex 
	$(CC) -I$(QUEX_PATH) lexer.cpp $(ENGINE) -lefence -o $@

%.E: %.cpp
	$(CC) -E -I$(QUEX_PATH) $< -o $@

%.o: %.cpp

clean:
	rm -rf TPLex*
	rm -rf $(TESTS)
	rm -rf *.o
