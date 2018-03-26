FILES = characters \
		from-utf8  \
		from-utf16 \
		from-utf32  


CC = g++ -Wall -Werror -W -I. -I$(HWUT_PATH) -ggdb 

all: $(FILES)

characters: characters.cpp ut
		$(CC) $< -o $@ 

from-utf8: basics.cpp ut
		$(CC) $< -o $@ -DSOURCE_NAME=utf8 -DSOURCE_TYPE=uint8_t 

from-utf16: basics.cpp ut
		$(CC) $< -o $@ -DSOURCE_NAME=utf16 -DSOURCE_TYPE=uint16_t 

from-utf32: basics.cpp ut
		$(CC) $< -o $@ -DSOURCE_NAME=utf32 -DSOURCE_TYPE=uint32_t 


%.E: %.cpp
		g++ -E -I$(QUEX_PATH) -I. -I$(HWUT_PATH) \
		$<                      \
		-DTEST_UTF8             \
		-DSOURCE_NAME=utf8      \
		-DSOURCE_TYPE=uint8_t   \
		-o $@ 

hwut-info:
	@echo $(FILES)

ut:
	python ../../TESTS/code_base_instatiation.py ut lexeme_converter compatibility

clean:
	rm -rf *.o $(FILES) ut

