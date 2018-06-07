INCLUDES := -I$(QUEX_PATH)/quex/code_base/TESTS/test_cpp \
		    -I$(QUEX_PATH)/quex/code_base/TESTS/test_c \
		    -I$(QUEX_PATH)/quex/code_base/TESTS/

DEFINES  := -DQUEX_OPTION_UNIT_TEST_NO_IMPLEMENTATION_IN_HEADER

SRC_CPP  := lexer.cpp \
	        $(QUEX_PATH)/quex/code_base/TESTS/test_cpp/TestAnalyzer-dummy.cpp

SRC_C    := lexer.c \
	        $(QUEX_PATH)/quex/code_base/TESTS/test_c/TestAnalyzer-dummy.c

all: lexerCpp lexerC

lexerCpp: $(SRC_CPP)
	@g++ $(INCLUDES) $(DEFINES) -DQUEX_INLINE=inline $^ -o $@
	
lexerC: $(SRC_C)
	@gcc $(INCLUDES) $(DEFINES) -DQUEX_INLINE= -DQUEX_OPTION_PLAIN_C $^ -o $@

clean:
	rm -rf lexerCpp lexerC
