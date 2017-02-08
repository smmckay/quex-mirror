FILES    := test-constructor.exe \
	        test-reset.exe \
	        test-include_push.exe

DEFINES  := -D__QUEX_OPTION_PLAIN_C \
	        -DQUEX_OPTION_UNIT_TEST_NO_IMPLEMENTATION_IN_HEADER \
			-DQUEX_OPTION_CONVERTER_ICONV \
			-DQUEX_SETTING_BUFFER_SIZE=256 \
			-DQUEX_SETTING_TRANSLATION_BUFFER_SIZE=256 \
			-DQUEX_OPTION_INCLUDE_STACK \
			-DQUEX_OPTION_STRING_ACCUMULATOR \
            -DQUEX_OPTION_POST_CATEGORIZER 

INCLUDES := -I$(QUEX_PATH) \
 		    -I$(QUEX_PATH)/quex/code_base/test_environment \
			-I$(HWUT_PATH)/support/C

CC       := gcc $(INCLUDES) $(DEFINES) -ggdb # -fsanitize=address
	
all:     $(FILES)

hwut-info: 
	@echo $(FILES)

%.exe: %.c TestAnalyzer-dummy.o
	$(CC) $^ -o $@ 

%.E: %.c
	$(CC) -E $^ -o $@ 

# Trick: Use 'QUEX_OPTION_MULTI' to avoid inclusion of 'multi.i' in 'single.i'
#        which is included in 'TestAnalyzer-dummy.c'.
TestAnalyzer-dummy.o: $(QUEX_PATH)/quex/code_base/test_environment/TestAnalyzer-dummy.c
	$(CC) -c -DQUEX_OPTION_MULTI $< -o $@

TestAnalyzer-dummy.E: $(QUEX_PATH)/quex/code_base/test_environment/TestAnalyzer-dummy.c
	$(CC) -E $< -o $@

clean:
	rm -f *.exe *.o *~ tmp.* *.gc*
