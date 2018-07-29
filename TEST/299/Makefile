include ../Makefile.lexer

# QX_FILE := ecmascript.qx
# FOREIGN_TIDF := --foreign-token-id-file ecmascript_yacc.hpp
FOREIGN_TIDF := #

all:  lexer

lexer: Simple/Simple.cpp ../lexer-simply.cpp
	$(LDCPP) -DQUEX_SETTING_BUFFER_SIZE_EXT=4 $^ -o lexer -ggdb # -DPRINT_LINE_COLUMN 

%.E: %.cpp
	$(CPP) -E $^ > $@ 

without: 
	quex --cbm -i without-derivation.qx \
		-o  Simple                                  \
		--encoding utf8			                    \
		--buffer-element-size 1                     \
		--buffer-element-type 'unsigned char'       \
		--language c++ \
		--no-count > tmp-wo.txt

with: 
	quex --cbm -i with-derivation.qx \
		-o  Simple                                  \
		--encoding utf8			                    \
		--buffer-element-size 1                     \
		--buffer-element-type 'unsigned char'       \
		--language c++ \
		--no-count > tmp-w.txt

clean: 
	rm -rf Simple* f lexer
