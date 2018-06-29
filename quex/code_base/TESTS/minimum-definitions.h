#include <assert.h>
#include "test_c/lib/quex/compatibility/stdint.h"
#ifndef   QUEX_OPTION_ASSERTS_EXT
#  define QUEX_OPTION_ASSERTS_EXT
#endif

#ifdef __cplusplus
#  include <string>
   class  TestAnalyzer;
#  define QUEX_NAME(NAME)                                TestAnalyzer_ ## NAME
#  define QUEX_TYPE_ANALYZER                             TestAnalyzer
   typedef void  (*QUEX_NAME(AnalyzerFunctionP))(TestAnalyzer*);
/*
#  ifndef QUEX_INLINE
#  define QUEX_INLINE inline
#  endif 
*/
#else
   struct TestAnalyzer;
#  define QUEX_NAME(NAME)                                TestAnalyzer_ ## NAME
#  define QUEX_TYPE_ANALYZER                             (struct TestAnalyzer)
   typedef void  (*QUEX_NAME(AnalyzerFunctionP))(struct TestAnalyzer*);
/*
#  ifndef QUEX_INLINE
#  define QUEX_INLINE static
#  endif 
*/
#endif

typedef long TestAnalyzer_stream_position_t;
#if ! defined(__cplusplus)
#define QUEX_SETTING_ENDIAN_IS_LITTLE()   quex_system_is_little_endian()
#else
#define QUEX_SETTING_ENDIAN_IS_LITTLE()   quex::system_is_little_endian()
#endif

#define QUEX_SETTING_BUFFER_LIMIT_CODE                 0
#define QUEX_SETTING_CHARACTER_NEWLINE_IN_ENGINE_CODEC 0x0A

#ifdef    QUEX_SETTING_BUFFER_SIZE_MIN_EXT
#  define QUEX_SETTING_BUFFER_SIZE_MIN     QUEX_SETTING_BUFFER_SIZE_MIN_EXT
#else
#  define QUEX_SETTING_BUFFER_SIZE_MIN     64
#endif

#ifdef   QUEX_SETTING_BUFFER_SIZE_EXT
#  define QUEX_SETTING_BUFFER_SIZE         QUEX_SETTING_BUFFER_SIZE_EXT
#else
#  define QUEX_SETTING_BUFFER_SIZE         4096
#endif

#ifdef    QUEX_SETTING_BUFFER_FILLER_SEEK_TEMP_BUFFER_SIZE_EXT
#  define QUEX_SETTING_BUFFER_FILLER_SEEK_TEMP_BUFFER_SIZE    QUEX_SETTING_BUFFER_FILLER_SEEK_TEMP_BUFFER_SIZE_EXT
#else
#  define QUEX_SETTING_BUFFER_FILLER_SEEK_TEMP_BUFFER_SIZE    512
#endif

#ifdef    QUEX_SETTING_TRANSLATION_BUFFER_SIZE_EXT
#  define QUEX_SETTING_TRANSLATION_BUFFER_SIZE  QUEX_SETTING_TRANSLATION_BUFFER_SIZE_EXT
#else
#  define QUEX_SETTING_TRANSLATION_BUFFER_SIZE  1024
#endif

#ifdef   QUEX_SETTING_CHARACTER_CODEC_EXT
#  define QUEX_SETTING_CHARACTER_CODEC   QUEX_SETTING_CHARACTER_CODEC_EXT
#else
#  define QUEX_SETTING_CHARACTER_CODEC  utf8
#endif

#ifdef    QUEX_SETTING_BUFFER_MIN_FALLBACK_N_EXT
#  define QUEX_SETTING_BUFFER_MIN_FALLBACK_N   QUEX_SETTING_BUFFER_MIN_FALLBACK_N_EXT
#else
#  define QUEX_SETTING_BUFFER_MIN_FALLBACK_N  4
#endif

#ifdef    QUEX_SETTING_ICU_PIVOT_BUFFER_SIZE_EXT
#  define QUEX_SETTING_ICU_PIVOT_BUFFER_SIZE   QUEX_SETTING_ICU_PIVOT_BUFFER_SIZE_EXT
#else
#  define QUEX_SETTING_ICU_PIVOT_BUFFER_SIZE   1024
#endif
#define QUEX_OPTION_ENDIAN_SYSTEM                    
#define QUEX_NAMESPACE_MAIN        
#define QUEX_NAMESPACE_MAIN_OPEN   
#define QUEX_NAMESPACE_MAIN_CLOSE  
#define QUEX_NAME_TOKEN(NAME)                           TestAnalyzer_Token_ ## NAME
#define QUEX_NAMESPACE_TOKEN_OPEN  
#define QUEX_NAMESPACE_TOKEN_CLOSE 
#define   QUEX_TOKEN_ID(X)    QUEX_TKN_ ## X
#ifndef   QUEX_TYPE_TOKEN_ID
#  define QUEX_TYPE_TOKEN_ID int
#endif

#ifndef   QUEX_TYPE_LEXATOM_EXT
#  define QUEX_TYPE_LEXATOM_EXT uint8_t
#endif
typedef QUEX_TYPE_LEXATOM_EXT  TestAnalyzer_lexatom_t;
typedef QUEX_TYPE_TOKEN_ID     TestAnalyzer_token_id_t;


