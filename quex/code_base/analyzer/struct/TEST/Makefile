FILES    := test-constructor.exe \
	        test-reset.exe \
	        test-include_push.exe \
	        test-include-deep.exe 

DEFINES  := \
	        -DQUEX_OPTION_UNIT_TEST_NO_IMPLEMENTATION_IN_HEADER_EXT \
			-DQUEX_SETTING_BUFFER_SIZE_EXT=31 \
			-DQUEX_SETTING_BUFFER_SIZE_MIN_EXT=3  \
			-DQUEX_SETTING_BUFFER_FALLBACK_N_EXT=2  \
			-DQUEX_SETTING_LEXATOM_LOADER_CONVERTER_BUFFER_SIZE_EXT=32 \
			-DQUEX_OPTION_INCLUDE_STACK_EXT 
			# -DQUEX_OPTION_CONVERTER_ICONV_EXT \

INCLUDES := -I. -Iut/lib -I$(HWUT_PATH)/support/C -I../../../TESTS

CC       := gcc -Wall $(INCLUDES) $(DEFINES) -ggdb -DQUEX_INLINE= #-lefence # -fsanitize=address
CPP      := g++ -Wall $(INCLUDES) $(DEFINES) -ggdb -DQUEX_INLINE=inline -fstack-protector-all # -lefence -fsanitize=address

TESTENV  := ../../../TESTS

LIB_ICU  := `icu-config --ldflags --cppflags`
	
all:     $(FILES)

hwut-info: 
	@echo $(FILES)

%.exe: %.c TestAnalyzer-dummy.o 
	$(CC) $< common.c TestAnalyzer-dummy.o -o $@ $(LIB_ICU)

%.exe: %.cpp TestAnalyzer-dummy-cpp.o 
	$(CPP) $< TestAnalyzer-dummy-cpp.o -lefence -o $@ $(LIB_ICU)

TestAnalyzer-dummy.o: $(TESTENV)/test_c_emm/TestAnalyzer-dummy.c 
	$(CC) -c -DQUEX_OPTION_PLAIN_C_EXT $< -o $@

TestAnalyzer-dummy-cpp.o: $(TESTENV)/test_cpp_emm/TestAnalyzer-dummy.cpp 
	$(CC) -c $< -o $@

clean:
	rm -rf *.exe *.o *~ tmp.* *.gc* *.E *.sw[mnop]  common.o
