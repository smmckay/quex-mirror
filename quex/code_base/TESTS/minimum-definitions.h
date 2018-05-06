#include "test_environment/lib/compatibility/stdint.h"
#include <assert.h>
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

#define QUEX_SETTING_BUFFER_LIMIT_CODE                 0
#define QUEX_SETTING_CHARACTER_NEWLINE_IN_ENGINE_CODEC 0x0A
#ifndef QUEX_SETTING_BUFFER_SIZE_MIN
#  define QUEX_SETTING_BUFFER_SIZE_MIN                   64
#endif
#ifndef QUEX_SETTING_BUFFER_SIZE
#  define QUEX_SETTING_BUFFER_SIZE                       4096
#endif
#ifndef   QUEX_SETTING_BUFFER_FILLER_SEEK_TEMP_BUFFER_SIZE
#  define QUEX_SETTING_BUFFER_FILLER_SEEK_TEMP_BUFFER_SIZE 512
#endif
#ifndef   QUEX_SETTING_TRANSLATION_BUFFER_SIZE             
#  define QUEX_SETTING_TRANSLATION_BUFFER_SIZE             1024
#endif
#ifndef   QUEX_SETTING_CHARACTER_CODEC
#  define QUEX_SETTING_CHARACTER_CODEC  utf8
#endif
#define QUEX_OPTION_ENDIAN_SYSTEM                    
#define QUEX_SETTING_ICU_PIVOT_BUFFER_SIZE               1024
#define QUEX_NAMESPACE_MAIN        
#define QUEX_NAMESPACE_MAIN_OPEN   
#define QUEX_NAMESPACE_MAIN_CLOSE  
#define QUEX_NAME_TOKEN(NAME)      TestAnalyzerToken_ ## NAME
#define QUEX_NAMESPACE_TOKEN_OPEN  
#define QUEX_NAMESPACE_TOKEN_CLOSE 
#ifndef   QUEX_TYPE_LEXATOM
#  define QUEX_TYPE_LEXATOM uint8_t
#endif
#define   QUEX_TOKEN_ID(X)    QUEX_TKN_ ## X
#ifndef   QUEX_TYPE_TOKEN_ID
#  define QUEX_TYPE_TOKEN_ID int
#endif
typedef QUEX_TYPE_LEXATOM  TestAnalyzer_lexatom_t;
typedef QUEX_TYPE_TOKEN_ID TestAnalyzer_token_id_t;


