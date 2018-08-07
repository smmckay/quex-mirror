include ../Makefile.lexer

# QX_FILE := ecmascript.qx
# FOREIGN_TIDF := --foreign-token-id-file ecmascript_yacc.hpp
FOREIGN_TIDF := #

all:  lexer with without

lexer: ../lexer-simply.cpp
	quex --cbm -i ecmascript.qx                      \
		 -o  Simple                                  \
		 --foreign-token-id-file ecmascript_yacc.hpp \
		 --encoding            utf8			         \
		 --buffer-element-size 1                     \
		 --buffer-element-type 'unsigned char'       
	$(LDCPP) -DQUEX_SETTING_BUFFER_SIZE_EXT=4 $^ Simple/Simple.cpp -o lexer -ggdb -DPRINT_LINE_COLUMN 

without: ../lexer-simply.cpp 
	quex --cbm -i without-derivation.qx \
		-o  Simple                                  \
		--encoding utf8			                    \
		--buffer-element-size 1                     \
		--buffer-element-type 'unsigned char'       \
		--no-count 
	$(LDCPP) -DQUEX_SETTING_BUFFER_SIZE_EXT=4 $^ Simple/Simple.cpp -o $@ -ggdb 

with: ../lexer-simply.cpp
	quex --cbm -i with-derivation.qx \
		-o  Simple                                  \
		--encoding utf8			                    \
		--buffer-element-size 1                     \
		--buffer-element-type 'unsigned char'       \
		--no-count 
	$(LDCPP) -DQUEX_SETTING_BUFFER_SIZE_EXT=4 $^ Simple/Simple.cpp -o $@ -ggdb

%.E: %.cpp
	$(CPP) -E $^ > $@ 

clean: 
	rm -rf Simple* f lexer without with
