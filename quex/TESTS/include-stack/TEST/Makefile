
TESTS = queue.exe 

all: $(TESTS)

CC =  \
     g++ -ggdb -Wall -Werror -fsanitize=address     \
	 -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED \
	 -DQUEX_SETTING_TOKEN_QUEUE_SIZE=5              \
	 -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED \
	 -DQUEX_SETTING_TOKEN_QUEUE_SIZE=5              \
	 -DQUEX_SETTING_TOKEN_QUEUE_SAFETY_BORDER=1 #
	 #-DQUEX_OPTION_DEBUG_SHOW

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
