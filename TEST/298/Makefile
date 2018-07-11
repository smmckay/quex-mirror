all:
	quex --cbm -i               ecmascript.qx    \
		 --analyzer-class       ecmascript_lexer \
		 --token-id-prefix      TOK_             \
		 --template-compression                  \
		 --encoding                utf8             \
		 -b                     1                \
		 --debug-exception                       \
		 2>&1

without-debug:
	quex --cbm -i               ecmascript.qx    \
		 --analyzer-class       ecmascript_lexer \
		 --token-id-prefix      TOK_             \
		 --template-compression                  \
		 --encoding                utf8             \
		 -b                     1                

clean:
	rm -rf ecmascript_lexer*
	rm -f tmp.*
