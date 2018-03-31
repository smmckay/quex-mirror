include ../Makefile.lexer

# Leave the generated code for debugging etc.
.SECONDARY:Simple/Simple.c 

test: Simple/Simple.c ../lexer.c
	$(LDC) $^ -o $@ -DPRINT_LINE_COLUMN_NUMBER -DPRINT_TOKEN                  

Simple/Simple.c: test.qx
	$(QUEX_PATH)/quex-exe.py \
		                     --encoding utf8          \
							 -b 1                  \
							 -i $<                 \
							 -o Simple             \
							 --language C --debug-exception

clean:
	rm -rf Simple* test *.o
