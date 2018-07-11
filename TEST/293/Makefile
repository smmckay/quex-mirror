include ../Makefile.lexer

OBJS =  lexer.o IConvLexer.o CodecLexer.o

CC := $(LDCPP_ICONV) \
	  -DQUEX_OPTION_MULTI_EXT \
	  -DQUEX_OPTION_CONVERTER_ICONV_EXT
	  # -DQUEX_OPTION_ASSERTS_DISABLED_EXT
      # -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED_EXT 

all: lexer

lexer: lexer.cpp IConv/Lexer.cpp Codec/Lexer.cpp
	@$(CC) $^ -o $@ -I. \
		 -DQUEX_OPTION_LEXEME_CONVERTERS_DISABLED_EXT

IConv/Lexer.cpp:    iconv.qx
	quex --cbm -i $< -o IConv::Lexer --odir IConv -b 4 \
		 --token-id-prefix ICONV_TKN_

Codec/Lexer.cpp:    codec.qx
	quex --cbm -i $< -o Codec::Lexer --odir Codec --encoding utf8 --bet wchar_t  \
		 --token-id-prefix CODEC_TKN_

Message0:      codec.qx  
	quex --cbm -i $< -o X --encoding utf16 --bet u8  # => Error u8 cannot hold utf16

Message1:      codec.qx
	quex --cbm -i $< -o X --encoding utf16 --bet u16 --token-id-prefix CODEC_TKN_ # => Ok, 'u16' can hold utf16

Message2:      codec.qx
	quex --cbm -i $< -o X --encoding utf16 --bet u32 --token-id-prefix CODEC_TKN_  # => Ok, 'u32' can hold utf32

Message3:      codec.qx
	quex --cbm -i $< -o X --encoding utf16 --bet int16_t --token-id-prefix CODEC_TKN_  # => Error, range 'i16' = 32768

clean:
	@rm -rf lexer X Lexer
	@rm -rf IConv* Codec*
	@rm -rf *.E
	@rm -rf lexer.o
	@rm -rf X*
