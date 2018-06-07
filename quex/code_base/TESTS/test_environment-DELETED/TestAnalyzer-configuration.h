/* -*- C++ -*-   vim: set syntax=cpp:
*
* (C) 2005-2017 Frank-Rene Schaefer
* ABSOLUTELY NO WARRANTY                                                     */
#ifndef __QUEX_INCLUDE_GUARD__ANALYZER__CONFIGURATION____TESTANALYZER
#define __QUEX_INCLUDE_GUARD__ANALYZER__CONFIGURATION____TESTANALYZER
/* Additionally to the 'local' include guard, there is an include indicator
*
*         __INCLUDE_INDICATOR_QUEX__CONFIGURATION
*
* If it is defined, this means, that another lexical analyzer configuration
* has been included before this. That in turn means, that multiple lexical
* analyzers are used. The configuration settings of the previous analyzer
* need to be undefined. And, this happens in "configuration/undefine".
*
* NOTE: We do undefine without making sure that there is an older definition
*       from a configuration file. This allows users to define some
*       configuration options on the command line without being immediately
*       deleted by "configuration/undefine".                                 */
#ifdef __QUEX_INCLUDE_INDICATOR__ANALYZER__CONFIGURATION
#include "test_environment/lib/analyzer/configuration/undefine"
#else
#   define __QUEX_INCLUDE_INDICATOR__ANALYZER__CONFIGURATION
#endif

#define QUEX_SETTING_VERSION           "0.68.2"
#define QUEX_SETTING_BUILD_DATE        "Wed May 30 15:42:45 2018"
#define QUEX_SETTING_ANALYZER_VERSION  "0.0.0-pre-release"

#ifndef    QUEX_OPTION_PLAIN_C
#define    QUEX_OPTION_PLAIN_C
#endif

/* Following checks are best done here:
*   -- Verification of the 'C++/C' version.
*   -- Assert control by this configuration file.
*
* Errors would be hard to find if the two checks were made in
*   -- 'quex/code_base/configuration/validation' or
*   -- 'quex/code_base/configuration/derived'.                               */
#if ! defined(QUEX_OPTION_PLAIN_C) && ! defined(__cplusplus)
#   error "QUEX_OPTION_PLAIN_C must be defined if no C++ compiler is used! Call quex with option '--language C'."
#endif

#if defined(__QUEX_INCLUDE_INDICATOR__ASSERTS)
#   error "Asserts included before configuration file. However, the configuration file MUST control asserts!"
#endif

#ifndef  QUEX_OPTION_COMPUTED_GOTOS
/* #define QUEX_OPTION_COMPUTED_GOTOS */
#endif
#ifndef    QUEX_OPTION_ENDIAN_LITTLE
#define    QUEX_OPTION_ENDIAN_LITTLE
#endif
#ifndef    QUEX_OPTION_ENDIAN_BIG
/* #define QUEX_OPTION_ENDIAN_BIG */
#endif
#ifndef    QUEX_OPTION_ENDIAN_SYSTEM
#define    QUEX_OPTION_ENDIAN_SYSTEM
#endif

/* OPTIONS: ___________________________________________________________________
*
* Activate/Deactivate Options via comment/uncomment. Options without a
* double underline '__' at the beginning can be turned off in the created
* engine. Options that do start with '__' configure the machine for the
* specified behavior. Such options are better not touched.
*
* -- Line Number / Column Number Counting:
*    Turning counting off may result in engine speed-up.                     */
#ifndef    QUEX_OPTION_COUNTER_LINE
#define    QUEX_OPTION_COUNTER_LINE
#endif
#ifndef    QUEX_OPTION_COUNTER_COLUMN
#define    QUEX_OPTION_COUNTER_COLUMN
#endif
/* #define QUEX_OPTION_INDENTATION_TRIGGER */
/* Quex can determine whether certain handlers are not used at all.  If so,
* computation time can be spared and quex comments the following options out.
*                                                                           */
/* #define QUEX_OPTION_ON_ENTRY_HANDLER_PRESENT */
/* #define QUEX_OPTION_ON_EXIT_HANDLER_PRESENT */

/* Begin of line pre-condition requires an extra flag in the buffer
* structure. Only out-comment this in case of tough memory restrictions,
* if no begin of line pre-condition is required.                            */
/* #define QUEX_OPTION_SUPPORT_BEGIN_OF_LINE_PRE_CONDITION */

/* The following flag indicates that the engine is running on a specific
* codec. Thus no converter is necessary. Use the flag to detect misuse.      */
/* #define QUEX_OPTION_ENGINE_RUNNING_ON_CODEC */
#
#ifndef QUEX_OPTION_TOKEN_REPETITION_SUPPORT
/* #define QUEX_OPTION_TOKEN_REPETITION_SUPPORT */
#endif
#ifndef QUEX_OPTION_TOKEN_TAKE_TEXT_SUPPORT
#define    QUEX_OPTION_TOKEN_TAKE_TEXT_SUPPORT
#endif
/* Mode Transitions:
*    If the engine was created without the flag '--no-mode-transition-check'
*    then code for mode transition control is inserted. It can be deactivated
*    by commenting the following option out.                                 */
#ifndef QUEX_OPTION_RUNTIME_MODE_TRANSITION_CHECK
#define    QUEX_OPTION_RUNTIME_MODE_TRANSITION_CHECK
#endif

/* QUEX_TYPE_X  --> Type of X in global namespace
* QUEX_TYPE0_X --> Type of X in local namespace (namespace omitted)          */
#if defined(QUEX_OPTION_PLAIN_C)
/* In 'C' there are no namespaces, so namespaces are coded directly
* into the type name. Both, global and local names are equal.            */
#   define QUEX_TYPE_DERIVED_ANALYZER  struct TestAnalyzer_tag

#   define QUEX_NAMESPACE_MAIN         TestAnalyzer

#else
/* Add namespaces for the global names of the classes of analyzer
* and token.                                                             */
#   define QUEX_TYPE_DERIVED_ANALYZER  TestAnalyzer

#   define QUEX_NAMESPACE_MAIN
#endif

#if defined(QUEX_OPTION_PLAIN_C)
#   define QUEX_NAMESPACE_TOKEN

#   define QUEX_LEXEME_NULL            TestAnalyzer_LexemeNull

#   define TestAnalyzer_Token_NAME       TestAnalyzer_Token_ ## NAME

#else
#   define QUEX_NAMESPACE_TOKEN

#   define QUEX_LEXEME_NULL             :: TestAnalyzer_LexemeNull

#   define TestAnalyzer_Token_NAME       TestAnalyzer_Token_ ## NAME

#endif


typedef uint8_t TestAnalyzer_lexatom_t;
typedef uint32_t TestAnalyzer_token_id_t;
typedef size_t TestAnalyzer_token_line_n_t;
typedef size_t TestAnalyzer_token_column_n_t;
typedef int TestAnalyzer_acceptance_id_t;



#ifndef    __QUEX_SETTING_MAX_MODE_CLASS_N
#   define __QUEX_SETTING_MAX_MODE_CLASS_N                 (2)
#endif
#ifndef    QUEX_SETTING_MODE_INITIAL_P
#   define QUEX_SETTING_MODE_INITIAL_P                     (&TestAnalyzer_M)
#endif

#ifndef    QUEX_SETTING_MODE_STACK_SIZE
#   define QUEX_SETTING_MODE_STACK_SIZE                                (size_t)8
#endif

/* BLC -- Buffer Limit Code:
*
* This code is used as a delimiter for buffer borders. When the analyzer
* hits a character with such a code, it knows that a border or the
* end of file has been reached.
*
* IT IS NOT SUPPOSED TO APPEAR IN THE NORMAL CHARACTER STREAM.               */
#ifndef    QUEX_SETTING_BUFFER_LIMIT_CODE
#   define QUEX_SETTING_BUFFER_LIMIT_CODE  ((TestAnalyzer_lexatom_t)0)
#endif

#define    QUEX_SETTING_CHARACTER_NEWLINE_IN_ENGINE_CODEC  ('\n')

/* PTC -- Path Termination code:
*
* Only required for path compression (see option '--path-compression' and
* '--path-compression-uniform' for quex on the command line). PTC must be
* different from the BLC so that the pathwalker does not get confuses if
* the input pointer stands on a buffer border and at the same time the
* path iterator stands at the end of the path.
*
* IT IS NOT SUPPOSED TO APPEAR IN THE NORMAL CHARACTER STREAM.               */
#ifndef    QUEX_SETTING_PATH_TERMINATION_CODE
#   define QUEX_SETTING_PATH_TERMINATION_CODE  ((TestAnalyzer_lexatom_t)1)
#endif

/* NOTE: A cast to 'size_t' would it make impossible to use the macro in
*       pre-processor comparisons.                                           */
#ifndef     QUEX_SETTING_BUFFER_SIZE
/* This setting must be defined as plain number, since there might
* be some pre-processor comparison operations depending on it.          */
#    define QUEX_SETTING_BUFFER_SIZE                                      131072
#endif

/* Lowest buffer size to consider, such that when a buffer is smaller, then
* the resulting frequency of buffer reloads causes a 'unbearable' performance
* decrease.
*
* A fine-tuned setting of this values considers: the memory read-access speed,
* the I/O speed, the max. expected lexeme sizem, and the expected average size
* of input streams. In most cases 32K will do well.
*
* Tuning this value only makes sense in environment where lots of files are
* included or where lexemes can become very large.                          */
#ifndef     QUEX_SETTING_BUFFER_SIZE_MIN
#    define QUEX_SETTING_BUFFER_SIZE_MIN                                  32768
#endif

#ifndef    QUEX_SETTING_BUFFER_FILLER_SEEK_TEMP_BUFFER_SIZE
#   define QUEX_SETTING_BUFFER_FILLER_SEEK_TEMP_BUFFER_SIZE                (512)
#endif
#ifndef    QUEX_SETTING_ICU_PIVOT_BUFFER_SIZE
#   define QUEX_SETTING_ICU_PIVOT_BUFFER_SIZE                               (64)
#endif

/* Initial size of the character accumulator.                                */
#ifndef     QUEX_SETTING_ACCUMULATOR_INITIAL_SIZE
#   define  QUEX_SETTING_ACCUMULATOR_INITIAL_SIZE                         (256)
#endif

/* Granularity, if new memory has to be allocated. The new memory will be by
* this factor greater than the previous.  Example: At start, memory contains
* 256 characters; then new allocation becomes necessary; if factor = 0.5, then
* the new memory will contain (256 + 128) = 384 characters. The next time, the
* new memory of size (384 + 192) = 576 characters.                          */

#ifndef     QUEX_SETTING_ACCUMULATOR_GRANULARITY_FACTOR
#   define  QUEX_SETTING_ACCUMULATOR_GRANULARITY_FACTOR                   (0.8)
#endif

/* If one mode requires indentation support, then the lexical analyser class
* must be setup for indentation counting. The following flag is defined or
* undefined by the lexical analyser generator quex.                         */
#if    defined(QUEX_OPTION_INDENTATION_TRIGGER)
#   ifndef    QUEX_SETTING_INDENTATION_STACK_SIZE
#      define QUEX_SETTING_INDENTATION_STACK_SIZE                         (64)
#   endif
#endif

#ifndef     QUEX_SETTING_TRANSLATION_BUFFER_SIZE
#    define QUEX_SETTING_TRANSLATION_BUFFER_SIZE ((size_t)65536)
#endif

#ifndef    QUEX_SETTING_CHARACTER_CODEC
#   define QUEX_SETTING_CHARACTER_CODEC unicode
#endif

#define    QUEX_TOKEN_ID(BRIEF)                             ((TestAnalyzer_token_id_t)QUEX_TKN_ ## BRIEF)
#define    __QUEX_SETTING_TOKEN_ID_REPETITION_TEST(TokenID) (false)
#ifndef    QUEX_SETTING_TOKEN_QUEUE_SIZE
#   define QUEX_SETTING_TOKEN_QUEUE_SIZE          ((size_t)64)
#endif

#include "test_environment/lib/analyzer/configuration/derived"

#endif /* __QUEX_INCLUDE_GUARD__ANALYZER__CONFIGURATION____TESTANALYZER */
