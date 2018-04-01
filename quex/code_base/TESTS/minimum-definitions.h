#ifdef __cplusplus
   class  Tester;
#  define QUEX_NAME(NAME)                                Tester_ ## NAME
#  define QUEX_TYPE_ANALYZER                             Tester
   typedef void  (*QUEX_NAME(AnalyzerFunctionP))(Tester*);
#else
   struct Tester;
#  define QUEX_NAME(NAME)                                Tester_ ## NAME
#  define QUEX_TYPE_ANALYZER                             (struct Tester)
   typedef void  (*QUEX_NAME(AnalyzerFunctionP))(struct Tester*);
#endif

#define QUEX_SETTING_BUFFER_LIMIT_CODE                 0
#define QUEX_SETTING_CHARACTER_NEWLINE_IN_ENGINE_CODEC 0x0A
#define QUEX_SETTING_BUFFER_SIZE_MIN                   64
#define QUEX_SETTING_BUFFER_SIZE                       4096
#ifndef   QUEX_SETTING_BUFFER_FILLER_SEEK_TEMP_BUFFER_SIZE
#  define QUEX_SETTING_BUFFER_FILLER_SEEK_TEMP_BUFFER_SIZE 512
#endif
#ifndef   QUEX_SETTING_TRANSLATION_BUFFER_SIZE             
#  define QUEX_SETTING_TRANSLATION_BUFFER_SIZE             1024
#endif
#define QUEX_OPTION_ENDIAN_SYSTEM                    
#define QUEX_SETTING_ICU_PIVOT_BUFFER_SIZE               1024
#define QUEX_NAMESPACE_MAIN        
#define QUEX_NAMESPACE_MAIN_OPEN   
#define QUEX_NAMESPACE_MAIN_CLOSE  
#define QUEX_NAME_TOKEN(NAME)      TesterToken_ ## NAME
#define QUEX_NAMESPACE_TOKEN_OPEN  
#define QUEX_NAMESPACE_TOKEN_CLOSE 
#ifndef   QUEX_TYPE_LEXATOM
#  define QUEX_TYPE_LEXATOM uint8_t
#endif

