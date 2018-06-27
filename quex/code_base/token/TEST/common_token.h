#ifndef INCLUDE_GUARD_COMMON_TOKEN_H
#define INCLUDE_GUARD_COMMON_TOKEN_H

#include "test_c/lib/definitions"
typedef  int TestAnalyzer_indentation_t;
#define  QUEX_SETTING_INDENTATION_STACK_SIZE 64
#include "test_c/lib/analyzer/Counter"

#ifdef __cplusplus
#   define QUEX_INLINE inline
#else
#   define QUEX_INLINE 
#endif

typedef unsigned char TestAnalyzer_lexatom_t;
#define QUEX_NAME_TOKEN(X) TokenName_ ## X
#define QUEX_NAME(X)       LexerName_ ## X
#define QUEX_SETTING_USER_CLASS_DECLARATION_EPILOG_EXT 
#define QUEX_OPTION_TOKEN_TAKE_TEXT_SUPPORT
#define QUEX_OPTION_TOKEN_REPETITION_SUPPORT
#define QUEX_SETTING_TOKEN_ID_REPETITION_TEST(X) true
#define QUEX_NAMESPACE_MAIN_OPEN 
#define QUEX_NAMESPACE_MAIN_CLOSE 

typedef struct TestAnalyzer_Token_tag {
    int     id;
    char*   text;
    size_t  repetition_n;
    size_t  _line_n;
    size_t  _column_n;
} TestAnalyzer_Token;

typedef struct TestAnalyzer_tag {
    E_Error  error_code;
    TestAnalyzer_Counter  counter;
} TestAnalyzer;

#define QUEX_TYPE_LEXATOM    uint8_t
#define TestAnalyzer_token_id_t uint32_t
#define QUEX_TYPE_TOKEN      TestAnalyzer_Token
#define QUEX_TYPE_ANALYZER   TestAnalyzer 
#define TokenId_TERMINATION  0
#define QUEX_TOKEN_ID(SHORT) TokenId_ ## SHORT

QUEX_INLINE void TestAnalyzer_Token_construct(QUEX_TYPE_TOKEN* me);
QUEX_INLINE void TestAnalyzer_Token_destruct(QUEX_TYPE_TOKEN* me); 
QUEX_INLINE bool TestAnalyzer_Token_take_text(QUEX_TYPE_TOKEN*              me, 
                                              const TestAnalyzer_lexatom_t* BeginP,
                                              const TestAnalyzer_lexatom_t* EndP);
QUEX_INLINE void TestAnalyzer_Token_repetition_n_set(QUEX_TYPE_TOKEN* me, 
                                                     size_t           RepetitionN);
QUEX_INLINE size_t TestAnalyzer_Token_repetition_n_get(QUEX_TYPE_TOKEN* me); 

#include "ut/lib/token/TokenQueue"

#include <support/C/hwut_unit.h>

extern void common_print_push(TestAnalyzer_TokenQueue* me, 
                              int count, QUEX_TYPE_TOKEN* token_p);
extern void common_print_pop(TestAnalyzer_TokenQueue* me, 
                             int count, QUEX_TYPE_TOKEN* token_p);
extern int  common_empty_queue(TestAnalyzer_TokenQueue* me, int pop_n, int Size);

typedef enum {
    E_UNIT_TEST_PLAIN,
    E_UNIT_TEST_TEXT,
    E_UNIT_TEST_VOID,
} E_UnitTest;

#endif /* INCLUDE_GUARD_COMMON_TOKEN_H */
