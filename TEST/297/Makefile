INCLUDES := -I$(QUEX_PATH)/quex/code_base/TESTS/test_environment/ \
		    -I$(QUEX_PATH)/quex/code_base/TESTS/

DEFINES  := -DQUEX_OPTION_UNIT_TEST_NO_IMPLEMENTATION_IN_HEADER

SRC_CPP  := lexer.cpp \
	        $(QUEX_PATH)/quex/code_base/TESTS/test_environment/TestAnalyzer-dummy.cpp

SRC_C    := lexer.c \
	        $(QUEX_PATH)/quex/code_base/TESTS/test_environment/TestAnalyzer-dummy.c

all: lexerCpp lexerC

lexerCpp: $(SRC_CPP)
	@g++ $(INCLUDES) $(DEFINES) -DQUEX_INLINE=inline $^ -o $@
	
lexerC: $(SRC_C)
	@gcc $(INCLUDES) $(DEFINES) -DQUEX_INLINE= -D__QUEX_OPTION_PLAIN_C $^ -o $@

