include ../Makefile.lexer

OBJS =  lexer.o IConvLexer.o CodecLexer.o

CC := $(LDCPP_ICONV) \
	  -DQUEX_OPTION_MULTI \
	  -DQUEX_OPTION_CONVERTER_ICONV
	  # -DQUEX_OPTION_ASSERTS_DISABLED
      # -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED 

all: lexer

lexer: lexer.cpp IConv_Lexer.cpp Codec_Lexer.cpp
	@$(CC) $^ -o $@ -I$(QUEX_PATH) \
		 -DQUEX_OPTION_AUX_STRING_DISABLED

%.E: %.cpp # IConvLexer.cpp CodecLexer.cpp
	$(CC) -c $< -o $@ -I$(QUEX_PATH) \
		 -DQUEX_OPTION_AUX_STRING_DISABLED \
		 -E
	
# quex -i 
	#

IConv_Lexer.cpp:    iconv.qx
	quex -i $< -o IConv::Lexer -b 4 \
		 --token-id-prefix ICONV_TKN_

Codec_Lexer.cpp:    codec.qx
	quex -i ~/prj/quex/trunk/quex/code_base/token/CppWChar.qx \
		 $< -o Codec::Lexer --codec utf8 --bet wchar_t  \
		 --token-id-prefix CODEC_TKN_

Message0:      codec.qx  
	quex -i $< -o X --codec utf16 --bet u8  # => Error u8 cannot hold utf16

Message1:      codec.qx
	quex -i $< -o X --codec utf16 --bet u16 --token-id-prefix CODEC_TKN_ # => Ok, 'u16' can hold utf16

Message2:      codec.qx
	quex -i $< -o X --codec utf16 --bet u32 --token-id-prefix CODEC_TKN_  # => Ok, 'u32' can hold utf32

Message3:      codec.qx
	quex -i $< -o X --codec utf16 --bet int16_t --token-id-prefix CODEC_TKN_  # => Error, range 'i16' = 32768

clean:
	@rm -rf lexer
	@rm -rf IConv* Codec*
	@rm -rf *.E
	@rm -rf lexer.o
	@rm -rf X*
