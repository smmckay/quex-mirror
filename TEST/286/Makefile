include ../Makefile.lexer

lexer: lexer.cpp tokenizer_it.cpp
	$(LDCPP) $^ -o $@ -ggdb

tokenizer_it.cpp: simple.qx
	quex -i simple.qx -o tokenizer_it \
         --bet wchar_t \

clean:
	rm -f lexer
	rm -f tokenizer_it tokenizer_it*
	rm -f *.o
