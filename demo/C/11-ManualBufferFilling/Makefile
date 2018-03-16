# PURPOSE: Manual Buffer Filling via Feeder and Gavager
#
# License: MIT; Project http://quex.sourceforge.net
# (C) Frank-Rene Schaefer; FREE OF CHARGE--ABSOLUTELY NO WARRANTY.
#_______________________________________________________________________________
.PHONY: clean
.SECONDARY:

COMPILER := gcc -ggdb -pedantic -Wconversion -Wall -Werror -W
LD       := $(COMPILER) -I./ $(ADD_FLAGS) 
LD_PLAIN     := $(LD) -DQUEX_SETTING_BUFFER_SIZE=13 
LD_CONVERTER := $(LD) -DQUEX_SETTING_TRANSLATION_BUFFER_SIZE=6 \
	                  -DQUEX_SETTING_BUFFER_SIZE=16            \
			          -DQUEX_TYPE_LEXATOM=wchar_t              \
			          -DQUEX_EXAMPLE_WITH_CONVERTER            \
			          -DQUEX_OPTION_CONVERTER_ICONV
# HINTS: -DQUEX_OPTION_ASSERTS_DISABLED
#        -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED 
#        -DQUEX_OPTION_DEBUG_SHOW

FILES := feeder-plain.exe  feeder-converter.exe  \
	     gavager-plain.exe gavager-converter.exe \
         point-plain.exe

all: $(FILES)

feeder-plain.exe:       lexer-feeder.c receiver.c  plain/lexPlain.c
	$(LD_PLAIN)     -o $@ $^ 
          
gavager-plain.exe:      lexer-gavager.c receiver.c plain/lexPlain.c
	$(LD_PLAIN)     -o $@ $^ 
          
point-plain.exe:        lexer-point.c              plain/lexPlain.c
	$(LD_PLAIN)     -o $@ -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=0 $^

feeder-converter.exe:   lexer-feeder.c receiver.c  converter/lexConverter.c
	$(LD_CONVERTER) -o $@ $^ 

gavager-converter.exe:  lexer-gavager.c receiver.c converter/lexConverter.c
	$(LD_CONVERTER) -o $@ $^ 

point-converter.exe:    lexer-point.c              converter/lexConverter.c
	$(LD_CONVERTER) -o $@ -DQUEX_SETTING_BUFFER_MIN_FALLBACK_N=0 $^ 
          
plain/lexPlain.c: lexPlain.qx 
	quex -i lexPlain.qx -o lexPlain --odir plain \
		 --language C            

converter/lexConverter.c: lexConverter.qx 
	quex -i lexConverter.qx -o lexConverter --odir converter \
		 --buffer-element-type wchar_t \
		 --language            C            

clean:	
	rm -rf plain/ converter/ *.o $(FILES) tmp.*
