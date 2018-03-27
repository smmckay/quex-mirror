include ../Makefile.lexer
INPUT=funny_comments # This is overidden by a command line argument of the for INPUT=something


DEFINES = \
		-DPRINT_LINE_COLUMN \
		-DQUEX_OPTION_COUNTER_LINE \
		-DQUEX_OPTION_COUNTER_COLUMN \

CC := $(LDCPP) -o lexer

all: $(INPUT)

funny_comments: 
	quex -i token.qx $(PREFIX)funny_comments.qx -o Simple --debug-exception
	$(CC) Simple/Simple*.cpp ../lexer-simply.cpp \
		$(DEFINES) -DQUEX_SETTING_BUFFER_SIZE=11

shell_comments: 
	quex -i token.qx $(PREFIX)shell_comments.qx -o Simple --debug-exception
	$(CC) Simple/Simple*.cpp ../lexer-simply.cpp \
		$(DEFINES) -DQUEX_SETTING_BUFFER_SIZE=4

c_comments: 
	quex -i token.qx $(PREFIX)c_comments.qx     -o Simple --debug-exception
	$(CC) Simple/Simple*.cpp ../lexer-simply.cpp \
		$(DEFINES) -DQUEX_SETTING_BUFFER_SIZE=4

## $(DEFINES) -DQUEX_SETTING_BUFFER_SIZE=1024

clean:
	@rm -rf lexer Simple* *.o
