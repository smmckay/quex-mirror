Reset: mention 'byte_order_reversion' must be reset, manually.
       user_reset: user must free any resource, in case of failure.

Using 'reset memory' and later 'reset_ByteLoader' requires to check
for the 'buffer._memory.ownership' before reload! 

-- Function: 'collect_user_owned_memory()' to be called before
             reset/include_pop/destructor.

-- Including: Buffer splits, so that frequent inclusion does not require
              allocation of huge amounts of buffers.

-- Reset: user_reset must destruct newly created resources and 
                     mark them 'absent' in case of failure.

    qlex.collect_user_memory(&prev);
    assert(qlex.reset(buffer_1, Size1, end_of_content_p));
    if( prev ) delete [] prev;

-- ByteLoader->input_handle_ownership => prevent closure/freeing of handle

-- warn about the 'c_str()': the string does not 'live' long enough to 
   be assigned to a variable.

   For c_str() the only safe usage is when you pass it as a parameter to a function. 

   In doubt: use 
   "size_t copy (char* s, size_t len, size_t pos = 0) const;"
   Do not forget terminating zero using std::string::length();

-- QUEX_NAME(something) must be invoqued with Lexer::QUEX_NAME(something)
   if 'using namespace Lexer;' is not given.

-- MEmbers in token type remain in same sequence as they are mentioned.
   => packaging may be controlled.

-- Use of converters => include

    #include <quex/code_base/buffer/lexatoms/converter/iconv/Converter_IConv>
    #include <quex/code_base/buffer/lexatoms/converter/iconv/Converter_IConv.i>
    #include <quex/code_base/buffer/lexatoms/converter/icu/Converter_ICU>
    #include <quex/code_base/buffer/lexatoms/converter/icu/Converter_ICU.i>

-- On error in analyzer function --> TKN_TERMINATION + error message.
   + error_code

-- if( lexer->error_code ) lexer->print_this();

-- feeder/gavager: 'GoodBye' token may trigger on border of given chunk, even 
                   if there might be more data.
                   => Trick: check whether last element fits last of 'bye'
                             => deliver a little less.

                   
-- not 'CONTINUE' after mode change. Assert triggers, otherwise resume same mode.
    on_entry => QUEX_TKN_MODE_STRING_ENTER(LexemeNull);
    on_exit  => QUEX_TKN_MODE_STRING_EXIT(LexemeNull);
   May be extremely confusing! 'on_entry' is executed, but old mode is working.

-- upon 'include': Token queue must be empty! Otherwise, tokens are lost!
   => something like 'INCLUDE' 'FILE_NAME' is ok, if the inclusion happens
      after 'FILE_NAME'.

-- self_token_p --> self_write_token_p

-- token::take_text does no longer take analyzer as argument, otherwise
                    it could not be shared between analyzers

-- include 'lexeme' in token type definition requires INCLUDE_CONVERTER_DECLARATION

-- token stamping:

    #define QUEX_ACTION_TOKEN_STAMP(ME)                 \
            QUEX_ACTION_TOKEN_STAMP_LINE_NUMBER(ME);    \
            QUEX_ACTION_TOKEN_STAMP_COLUMN_NUMBER(ME);  \
            self_write_token_p()->number_ = self.my_counter++;   
