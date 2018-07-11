# PURPOSE: Manual Buffer Filling via Feeder and Gavager
#
# License: MIT; Project http://quex.sourceforge.net
# (C) Frank-Rene Schaefer; FREE OF CHARGE--ABSOLUTELY NO WARRANTY.
#_______________________________________________________________________________
.PHONY: clean
.SECONDARY:

COMPILER := gcc -ggdb -pedantic -Wconversion -Wall -Werror -W
LD       := $(COMPILER) -I./ $(ADD_FLAGS) 
LD_PLAIN     := $(LD) -DQUEX_SETTING_BUFFER_SIZE_EXT=13 
LD_CONVERTER := $(LD) -DQUEX_SETTING_LEXATOM_LOADER_CONVERTER_BUFFER_SIZE_EXT=6 \
	                  -DQUEX_SETTING_BUFFER_SIZE_EXT=16            \
			          -DQUEX_TYPE_LEXATOM_EXT=wchar_t              \
			          -DQUEX_DEMO_WITH_CONVERTER            \
			          -DQUEX_DEMO_OPTION_CONVERTER_ICONV
# HINTS: -DQUEX_OPTION_ASSERTS_DISABLED_EXT
#        -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED_EXT 
#        -DQUEX_OPTION_DEBUG_SHOW_EXT

FILES := feeder-plain.exe  feeder-converter.exe  \
	     gavager-plain.exe gavager-converter.exe \
         point-plain.exe

all: $(FILES)

feeder-plain.exe:       lexer-feeder.c receiver.c  plain/Lexer.c
	$(LD_PLAIN)     -o $@ -DQUEX_SETTING_BUFFER_FALLBACK_N_EXT=3 $^ 
          
gavager-plain.exe:      lexer-gavager.c receiver.c plain/Lexer.c
	$(LD_PLAIN)     -o $@ -DQUEX_SETTING_BUFFER_FALLBACK_N_EXT=3 $^ 
          
point-plain.exe:        lexer-point.c              plain/Lexer.c
	$(LD_PLAIN)     -o $@ -DQUEX_SETTING_BUFFER_FALLBACK_N_EXT=0 $^

feeder-converter.exe:   lexer-feeder.c receiver.c  converter/Lexer.c
	$(LD_CONVERTER) -o $@ -DQUEX_SETTING_BUFFER_FALLBACK_N_EXT=3 $^ 

gavager-converter.exe:  lexer-gavager.c receiver.c converter/Lexer.c
	$(LD_CONVERTER) -o $@ -DQUEX_SETTING_BUFFER_FALLBACK_N_EXT=3 $^ 

point-converter.exe:    lexer-point.c              converter/Lexer.c
	$(LD_CONVERTER) -o $@ -DQUEX_SETTING_BUFFER_FALLBACK_N_EXT=0 $^ 
          
plain/Lexer.c: lexPlain.qx 
	quex --cbm -i lexPlain.qx -o Lexer --odir plain --language C            

converter/Lexer.c: lexConverter.qx 
	quex --cbm -i lexConverter.qx -o Lexer --odir converter \
		 --buffer-element-type wchar_t --language C            

clean:	
	rm -rf plain/ converter/ *.o $(FILES) tmp.*
