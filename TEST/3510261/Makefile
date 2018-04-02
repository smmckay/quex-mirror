include ../Makefile.lexer

# Leave the generated code for debugging etc.
.SECONDARY:Simple/Simple.c 

test: Simple/Simple.c ../lexer.c
	$(LDC) -o $@ $^ -ggdb \
		-DPRINT_LINE_COLUMN_NUMBER \
		-DPRINT_TOKEN                  

Simple/Simple.c: test.qx
	quex -i $< -o Simple --language C --encoding utf8

clean:
	rm -rf Simple* test *.o
