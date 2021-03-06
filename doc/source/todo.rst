-- What modes are about!
    .. describe:: List of base modes  

      #. Base modes from which behavior is inherited.

    .. describe:: Tags in <...> brackets

      #. Skippers, i.e. machines that run in parallel without causing any
         token to be produced.

      #. Counting behavior, i.e. what character counts how many columns or 
         lines, or causes jumps on a column number grid.

      #. Indentation based scope parameters, defining what is a newline 
         what is white space, what is bad at the beginning of a line (the
         tab character or space?) :cite:`todo`.

      #. Transition control, specifying from where a mode can be entered
         and to what mode it may transit.

      #. Inheritance control, specifying if the mode can be inherited or
         not.

    .. describe:: Pattern-Action Pairs

      #. Patterns which are lurking to cause actions and send tokens.

    .. describe:: Event Handlers

      #. On-Incidence definitions for 'on_failure', 'on_end_of_stream', 
         etc.

TODO:
.. Talk about the 'lexeme in buffer': In this case, though, a callback must be
   implemented which reacts on the buffer's content change. On this event the
   callback must saveguard all related strings.

-- TODO: Mention the 'ByteLoader_Memory'
    TODO: callbacks 'on_buffer_overflow', 'on_content_change'
          that can load sequentially from memory.

-- '-o namespace::lexer' when used with multiple lexers where only the namespace
   differs, better use '--odir' to write lexers in separate directories.

-- token-class only: All lexers generated with '--no-lib-quex', token generation without '--no-lib-quex'.
-- with '--no-lib-quex', the flag where the headers are '-Idirectory' must be provided !

-- Algebra: pre and post context:

         pattern match <=> pre && core && post

     =>  NOT pattern <=> NOT pre || NOT core || not post
     ==  A | B       <=> (A_pre && A_core && A_post) || (B_pre && B_core && B_post)
     ==  A & B       <=> (A_pre && A_core && A_post) && (B_pre && B_core && B_post)
                         (A_pre && B_pre) && (A_core && B_core) && (A_post && B_post)

-- '--fallback-mandatory' => *MUST* be finite (mandatory with feeder/gavager)
   '--fallback-optional'  => NO REQUIREMENT

   SUBJECT: Fallback

   Fallback can be determined as the longest path to the first acceptance
   state.

   * Reload backward impossible for some ByteLoaders (Socket), or with 
     manually filled buffers.

   * Reload backward after reload forward is inefficient.

   BUT: FallbackN tries to maintain distance before lexeme start
        => Reload forward right before lexeme end means:
           Covered buffer size = lexeme length + fallback n (might be huge)

   => Two options 
   
      '--falback-mandatory' for cases where load backward is impossible.
      '--fallback-optional' for cases where reload is not to be imposed
         (makes sense for very long pre-contexts)

-- BUFFER_SIZE_MIN must fit the lexeme. => important for include optimization

/* Assert Strategy:
 *
 * Asserts are enabled by default. The lexer emits a warning message and tells
 * how to deactivate them. Asserts can be deactivated as follows.
 *
 *  'NDEBUG' (from Standard 'assert.h') => avoid surprises.
 *  'QUEX_OPTION_ASSERTS_DISABLED_EXT'  => solely prevent quex's asserts.     
 *                                                                            */
-- token class generation: Name of *lexer* must be specified, i.e. the
   token class must know the lexer for which lexer it is generated.

   => use of $$LEXER_CLASS$ macro

   OR: disable _take_text (==> good subject for unit tests, also)

-- Removal of implicit default namespace 'quex'

-- Converter Only generation:

   mention importance of '--bet' and '--encoding', the naming and maybe, the include guard.

    quex --co -o TestAnalyzer --odir ut --debug-exception --bet uint32_t    
    quex --co -o TestAnalyzer --odir ut --debug-exception --bet uint8_t --encoding utf8

    also mention '--csn' converter source name which influences function name prefix 
    and file names.
    
-- Mention:

   When types other than ISO stdint are used (uint8_t etc), then the headers
   must be manually extended (this is a nuissance).
   The 'header' section may not be used, since it may rely on types that are
   already defined in the configuration. Example: 'include Accumulator' which
   requires the token type id definition.

   Solution: 'first_header' section which may be inserted right in front of
   of all headers.

-- Mention:

    qlex.run(&qlex, self_print_token, true);

-- Manual written token class must include 'lexeme.i'

-- Minimal buffer size:   lexeme size 
                      + 1 lexatom to detect end 
                      + 2 border lexatoms of buffer

-- Easy include pattern:

    @[a-z/\-\.012]+ {
        printf(">> include %s;\n", &Lexeme[1]);
        QUEX_NAME(include_push_file_name)(&self, &Lexeme[1], 0x0);
    }
    on_end_of_stream {
        if( QUEX_NAME(include_pop)(&self) == false ) {
           QUEX_NAME(error_code_clear)(&self);
           self_send(QUEX_TKN_TERMINATION);
        }
        else { 
           printf("<< include\n");
        }
    }

@article{donnelly2004bison,
    title={Bison. the yacc-compatible parser generator},
    author={Donnelly, Charles and Stallman, Richard},
    year={2004},
    publisher={Free Software Foundation}
}

-- Anti-pattern: Investigate the behavior of the anti-pattern '\A{...}'
   documentation in 're-algebraic-expressions'.

-- Other RE-operations: review how far they are already implemented
                        through algebraic elements.

IMPORTANT: Do never directly assign to 'token_p->text' a string constant!
           Otherwise, quex will try to delete it!

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

-- String Accu:

   print {
        QUEX_NAME(Accumulator_print_this)(&me->accumulator);
   }
   header {
       include <quex/code_base/extra/accumulator/Accumulator>
    }
    footer {
       include <quex/code_base/extra/accumulator/Accumulator.i>
   }
   body {
        QUEX_NAME(Accumulator)          accumulator;
   }
   constructor {
        if( ! QUEX_NAME(Accumulator_construct)(&me->accumulator, me) ) {
            return false;
        }
   }
   destructor {
    __QUEX_IF_STRING_ACCUMULATOR(QUEX_NAME(Accumulator_destruct)(&me->accumulator));
    }

-- Post Categorizer

    print {
    QUEX_NAME(PostCategorizer_print_this)(&me->post_categorizer);

    }
    header {
#   include <quex/code_base/extra/post_categorizer/PostCategorizer>
    }
    footer {
#   include <quex/code_base/extra/post_categorizer/PostCategorizer.i>
    }
    body {
    }
    constructor {
    if( ! QUEX_NAME(PostCategorizer_construct)(&me->post_categorizer) ) {
        return false;
    }
    }
    destructor {
    }

-- 'print' and 'footer' sections
    "print":          "class_print_extension",
    "footer":         "class_footer_extension",          # -> in 'header' after all definitions.

-- mentions QUEX_TOKEN_ID(BRIEF)

