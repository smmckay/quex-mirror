FILES    := test-constructor.exe \
	        test-reset.exe \
	        test-include_push.exe \
	        test-include-deep.exe 

DEFINES  := \
	        -DQUEX_OPTION_UNIT_TEST_NO_IMPLEMENTATION_IN_HEADER \
			-DQUEX_OPTION_CONVERTER_ICONV \
			-DQUEX_SETTING_BUFFER_SIZE=31 \
			-DQUEX_SETTING_BUFFER_SIZE_MIN=3  \
			-DQUEX_SETTING_TRANSLATION_BUFFER_SIZE=32 \
			-DQUEX_OPTION_INCLUDE_STACK 

INCLUDES := -I. -I$(HWUT_PATH)/support/C -I../../../TESTS

CC       := gcc -Wall $(INCLUDES) $(DEFINES) -ggdb #-lefence # -fsanitize=address
CPP      := g++ -Wall $(INCLUDES) $(DEFINES) -ggdb -fstack-protector-all # -lefence -fsanitize=address

TESTENV  := $(QUEX_PATH)/quex/code_base/TESTS

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
TestAnalyzer-dummy.o: $(TESTENV)/test_environment/TestAnalyzer-dummy.c
	$(CC) -c -D__QUEX_OPTION_PLAIN_C -DQUEX_OPTION_MULTI $< -o $@

TestAnalyzer-dummy-Cpp.o: $(TESTENV)/test_environment/TestAnalyzer-dummy.cpp
	$(CC) -c -DQUEX_OPTION_MULTI $< -o $@

TestAnalyzer-dummy.E: $(TESTENV)/test_environment/TestAnalyzer-dummy.c
	$(CC) -E $< -o $@

ut:
	python ../../../TESTS/code_base_instatiation.py ut 

clean:
	rm -f *.exe *.o *~ tmp.* *.gc* *.E *.sw[mnop] ut
