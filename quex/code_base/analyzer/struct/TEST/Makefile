FILES    := test-constructor.exe \
	        test-reset.exe \
	        test-include_push.exe \
	        test-include-deep.exe 

DEFINES  := \
	        -DQUEX_OPTION_UNIT_TEST_NO_IMPLEMENTATION_IN_HEADER \
			-DQUEX_OPTION_CONVERTER_ICONV \
			-DQUEX_SETTING_BUFFER_SIZE=31 \
			-DQUEX_SETTING_BUFFER_INCLUDE_MIN_SIZE=3  \
			-DQUEX_SETTING_TRANSLATION_BUFFER_SIZE=32 \
			-DQUEX_OPTION_INCLUDE_STACK \
			-DQUEX_OPTION_STRING_ACCUMULATOR \
            -DQUEX_OPTION_POST_CATEGORIZER 

INCLUDES := -I$(QUEX_PATH) \
 		    -I$(QUEX_PATH)/quex/code_base/test_environment \
			-I$(HWUT_PATH)/support/C

CC       := gcc -Wall $(INCLUDES) $(DEFINES) -ggdb # -fsanitize=address
CPP      := g++ -Wall $(INCLUDES) $(DEFINES) -ggdb -fstack-protector-all # -fsanitize=address

LIB_ICU  := `icu-config --ldflags --cppflags`
	
all:     $(FILES)

hwut-info: 
	@echo $(FILES)

%.exe: %.c TestAnalyzer-dummy.o
	$(CC) $^ -o $@ $(LIB_ICU)

%.exe: %.cpp TestAnalyzer-dummy-Cpp.o
	$(CPP) $^ -lefence -o $@ $(LIB_ICU)

%.E: %.c
	$(CC) -E $^ -o $@ 

# Trick: Use 'QUEX_OPTION_MULTI' to avoid inclusion of 'multi.i' in 'single.i'
#        which is included in 'TestAnalyzer-dummy.c'.
TestAnalyzer-dummy.o: $(QUEX_PATH)/quex/code_base/test_environment/TestAnalyzer-dummy.c
	$(CC) -c -D__QUEX_OPTION_PLAIN_C -DQUEX_OPTION_MULTI $< -o $@

TestAnalyzer-dummy-Cpp.o: $(QUEX_PATH)/quex/code_base/test_environment/TestAnalyzer-dummy.cpp
	$(CC) -c -DQUEX_OPTION_MULTI $< -o $@

TestAnalyzer-dummy.E: $(QUEX_PATH)/quex/code_base/test_environment/TestAnalyzer-dummy.c
	$(CC) -E $< -o $@

clean:
	rm -f *.exe *.o *~ tmp.* *.gc* *.E *.sw[mnop]
