INCLUDES := -I$(QUEX_PATH)/quex/code_base/extra/test_environment/ \
		    -I$(QUEX_PATH)

DEFINES  := -DQUEX_OPTION_TOKEN_POLICY_SINGLE \
	        -DQUEX_OPTION_UNIT_TEST_NO_IMPLEMENTATION_IN_HEADER

SRC_CPP  := lexer.cpp \
	        $(QUEX_PATH)/quex/code_base/extra/test_environment/TestAnalyzer-dummy.cpp

SRC_C    := lexer.c \
	        $(QUEX_PATH)/quex/code_base/extra/test_environment/TestAnalyzer-dummy.c

all: lexerCpp lexerC

lexerCpp: $(SRC_CPP)
	@g++ $(INCLUDES) $(DEFINES) $^ -o $@
	
lexerC: $(SRC_C)
	@gcc $(INCLUDES) $(DEFINES) -D__QUEX_OPTION_PLAIN_C $^ -o $@

