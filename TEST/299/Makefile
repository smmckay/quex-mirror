include ../Makefile.lexer


all:  lexer

lexer: Simple/Simple.cpp ../lexer-simply.cpp
	$(LDCPP) -DQUEX_SETTING_BUFFER_SIZE=4 -DPRINT_LINE_COLUMN $^ -o lexer -ggdb

%.E: %.cpp
	$(CPP) -E $^ > $@ 

Simple/Simple.cpp: ecmascript.qx
	quex -i ecmascript.qx                           \
		-o  Simple                                  \
		--foreign-token-id-file ecmascript_yacc.hpp \
		--template-compression                      \
		--encoding utf8			                    \
		--buffer-element-size 1                     \
		--buffer-element-type 'unsigned char'       \
		--language c++

clean: 
	rm -rf Simple* f lexer
