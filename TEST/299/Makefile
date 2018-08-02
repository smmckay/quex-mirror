include ../Makefile.lexer

# QX_FILE := ecmascript.qx
# FOREIGN_TIDF := --foreign-token-id-file ecmascript_yacc.hpp
FOREIGN_TIDF := #

all:  lexer

lexer: Simple/Simple.cpp ../lexer-simply.cpp
	$(LDCPP) -DQUEX_SETTING_BUFFER_SIZE_EXT=4 $^ -o lexer -ggdb # -DPRINT_LINE_COLUMN 

%.E: %.cpp
	$(CPP) -E $^ > $@ 

Simple/Simple.cpp: 
	quex --cbm -i ecmascript.qx \
		-o  Simple                                  \
		--foreign-token-id-file ecmascript_yacc.hpp \
		--encoding utf8			                    \
		--buffer-element-size 1                     \
		--buffer-element-type 'unsigned char'       \
		--language c++ \
		--no-count 

without: Simple/Simple.cpp ../lexer-simply.cpp 
	quex --cbm -i without-derivation.qx \
		-o  Simple                                  \
		--encoding utf8			                    \
		--buffer-element-size 1                     \
		--buffer-element-type 'unsigned char'       \
		--language c++ \
		--no-count 
	$(LDCPP) -DQUEX_SETTING_BUFFER_SIZE_EXT=4 $^ -o $@ -ggdb # -DPRINT_LINE_COLUMN 

with: Simple/Simple.cpp ../lexer-simply.cpp
	quex --cbm -i with-derivation.qx \
		-o  Simple                                  \
		--encoding utf8			                    \
		--buffer-element-size 1                     \
		--buffer-element-type 'unsigned char'       \
		--language c++ \
		--no-count 
	$(LDCPP) -DQUEX_SETTING_BUFFER_SIZE_EXT=4 $^ -o $@ -ggdb # -DPRINT_LINE_COLUMN 

clean: 
	rm -rf Simple* f lexer without with
