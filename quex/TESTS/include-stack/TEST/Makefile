
TESTS = queue.exe 

all: $(TESTS)

CC =  \
     g++ -ggdb -Wall -Werror -fsanitize=address     \
	 -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED_EXT \
	 -DQUEX_SETTING_TOKEN_QUEUE_SIZE_EXT=5              \
	 -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED_EXT \
	 -DQUEX_SETTING_TOKEN_QUEUE_SIZE_EXT=5              \
	 -DQUEX_SETTING_TOKEN_QUEUE_SAFETY_BORDER_EXT=1 #
	 #-DQUEX_OPTION_DEBUG_SHOW_EXT

all: queue.exe

hwut-info:
	@echo $(TESTS)

queue.exe:       lexer.cpp simple.qx 
	quex -i simple.qx -o Simple 
	$(CC) -I. lexer.cpp Simple/Simple.cpp -lefence -o $@

%.o: %.cpp

clean:
	rm -rf *.exe
	rm -rf Simple*
	rm -rf $(TESTS)
	rm -rf *.o
