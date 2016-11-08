TESTS := skip_range.exe \
	     skip_nested_range.exe

all: $(TESTS)

hwut-info:
	@echo $(TESTS)

%.exe: %.qx $(QUEX_PATH)/TEST/lexer.c 
	quex -i $< -o Simple --language C --debug-exception
	$(CC) $(QUEX_PATH)/TEST/lexer.c Simple.c -o $@ \
		  -DHWUT_INFO_MESSAGE=\"$*\" -DPRINT_TOKEN \
		  -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED \
		  -I. -I$(HWUT_PATH) -I$(QUEX_PATH)
	rm -f Simple*

clean:
	rm -f Simple*	
	rm -f *.exe


