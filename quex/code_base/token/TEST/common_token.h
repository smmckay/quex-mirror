#ifndef INCLUDE_GUARD_COMMON_TOKEN_H
#define INCLUDE_GUARD_COMMON_TOKEN_H

$$INC: definitions$$

#define QUEX_NAME_TOKEN(X) TokenName_ ## X
#define QUEX_NAME(X)       LexerName_ ## X
#define QUEX_SETTING_USER_CLASS_DECLARATION_EPILOG 
#define QUEX_OPTION_TOKEN_TAKE_TEXT_SUPPORT
#define QUEX_OPTION_TOKEN_REPETITION_SUPPORT
#define __QUEX_SETTING_TOKEN_ID_REPETITION_TEST(X) true
#define QUEX_NAMESPACE_MAIN_OPEN 
#define QUEX_NAMESPACE_MAIN_CLOSE 

typedef struct {
    int     id;
    char*   text;
    size_t  repetition_n;
} Token;

typedef struct {
    E_Error  error_code;
} Lexer;

#define QUEX_TYPE_LEXATOM    uint8_t
#define QUEX_TYPE_TOKEN_ID   uint32_t
#define QUEX_TYPE_TOKEN      Token
#define QUEX_TYPE_ANALYZER   Lexer 
#define TokenId_TERMINATION  0
#define QUEX_TOKEN_ID(SHORT) TokenId_ ## SHORT

QUEX_INLINE void QUEX_NAME_TOKEN(construct)(QUEX_TYPE_TOKEN* me);
QUEX_INLINE void QUEX_NAME_TOKEN(destruct)(QUEX_TYPE_TOKEN* me); 
QUEX_INLINE bool QUEX_NAME_TOKEN(take_text)(QUEX_TYPE_TOKEN* me, 
                                            const char*      BeginP,
                                            const char*      EndP);
QUEX_INLINE void QUEX_NAME_TOKEN(repetition_n_set)(QUEX_TYPE_TOKEN* me, 
                                                   size_t           RepetitionN);
QUEX_INLINE size_t QUEX_NAME_TOKEN(repetition_n_get)(QUEX_TYPE_TOKEN* me); 

$$INC: token/TokenQueue$$

#include <support/C/hwut_unit.h>

extern void common_print_push(QUEX_NAME(TokenQueue)* me, int count, QUEX_TYPE_TOKEN* token_p);
extern void common_print_pop(QUEX_NAME(TokenQueue)* me, int count, QUEX_TYPE_TOKEN* token_p);
extern bool common_empty_queue(QUEX_NAME(TokenQueue)* me, int pop_n, int Size);

typedef enum {
    E_UNIT_TEST_PLAIN,
    E_UNIT_TEST_TEXT,
    E_UNIT_TEST_VOID,
} E_UnitTest;

#endif /* INCLUDE_GUARD_COMMON_TOKEN_H */
