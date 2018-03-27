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

INCLUDES := -I. -Iut/lib -I$(HWUT_PATH)/support/C -I../../../TESTS

CC       := gcc -Wall $(INCLUDES) $(DEFINES) -ggdb #-lefence # -fsanitize=address
CPP      := g++ -Wall $(INCLUDES) $(DEFINES) -ggdb -fstack-protector-all # -lefence -fsanitize=address

TESTENV  := ../../../TESTS

LIB_ICU  := `icu-config --ldflags --cppflags`
	
all:     $(FILES)

hwut-info: 
	@echo $(FILES)

%.exe: %.c TestAnalyzer-dummy.o ut
	$(CC) $< common.c TestAnalyzer-dummy.o -o $@ $(LIB_ICU)

%.exe: %.cpp TestAnalyzer-dummy-cpp.o ut
	$(CPP) $< TestAnalyzer-dummy-cpp.o -lefence -o $@ $(LIB_ICU)

# Trick: Use 'QUEX_OPTION_MULTI' to avoid inclusion of 'multi.i' in 'single.i'
#        which is included in 'TestAnalyzer-dummy.c'.
TestAnalyzer-dummy.o: $(TESTENV)/test_environment/TestAnalyzer-dummy.c ut
	$(CC) -c -D__QUEX_OPTION_PLAIN_C -DQUEX_OPTION_MULTI $< -o $@

TestAnalyzer-dummy-cpp.o: $(TESTENV)/test_environment/TestAnalyzer-dummy.cpp ut
	$(CC) -c -DQUEX_OPTION_MULTI $< -o $@

ut:
	python $(TESTENV)/code_base_instatiation.py ut 

clean:
	rm -rf *.exe *.o *~ tmp.* *.gc* *.E *.sw[mnop] ut common.o
