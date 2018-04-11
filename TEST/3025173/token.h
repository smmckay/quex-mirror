#ifndef __TOKEN_H__
#define __TOKEN_H__

#include "gramma.h"

#ifndef    br_scan_token_id_t
#   define br_scan_token_id_t              uint32_t
#endif

namespace blackray {


struct Token {

    int                                    number_;
    std::basic_string<br_scan_lexatom_t> text_;


public:
    int                                    get_number() const
    { return number_; }
    void                                   set_name(int number)
    { number_ = number; }
    std::basic_string<br_scan_lexatom_t> get_text() const
    { return text_; }
    void                                   set_text(std::basic_string<br_scan_lexatom_t>& text)
    { text_ = text; }


    void set(const br_scan_token_id_t ID)
    { id = ID; }
    void set(const br_scan_token_id_t ID, int Value0)
    { id = ID; number_ = Value0; }
    void set(const br_scan_token_id_t ID, const std::basic_string<br_scan_lexatom_t>& Value0)
    { id = ID; text_ = Value0; }
    void set(const br_scan_token_id_t ID, int Value0, const std::basic_string<br_scan_lexatom_t>& Value1)
    { id = ID; number_ = Value0; text_ = Value1; }


        br_scan_token_id_t    id;

        br_scan_token_id_t    type_id() const      { return id; }
        static const char*    map_id_to_name(br_scan_token_id_t ID) {
          switch (ID) {
            case BR_TKN_DOT           : return "BR_TKN_DOT";
            case BR_TKN_TERMINATION   : return "BR_TKN_TERMINATION";
            case BR_TKN_UNINITIALIZED : return "BR_TKN_UNINITIALIZED";
            case BR_TKN_SEMI          : return "BR_TKN_SEMI";
            case BR_TKN_FROM          : return "BR_TKN_FROM";
            case BR_TKN_PARSE_ERROR   : return "BR_TKN_PARSE_ERROR";
            case BR_TKN_SCHEMA        : return "BR_TKN_SCHEMA";
            case BR_TKN_NUMBER        : return "BR_TKN_NUMBER";
            case BR_TKN_LITERAL       : return "BR_TKN_LITERAL";
            case BR_TKN_WHERE         : return "BR_TKN_WHERE";
            case BR_TKN_SELECT        : return "BR_TKN_SELECT";
            case BR_TKN_IDENTIFIER    : return "BR_TKN_IDENTIFIER";
            case BR_TKN_SHOW          : return "BR_TKN_SHOW";
            case BR_TKN_SCHEMAS       : return "BR_TKN_SCHEMAS";
            default                   : return "UNKNOWN";
          }
        } 
        
        const std::string     type_id_name() const { return map_id_to_name(id); }

#   ifdef     QUEX_OPTION_TOKEN_STAMPING_WITH_LINE_AND_COLUMN
#       ifdef QUEX_OPTION_COUNTER_LINE
        br_scan_token_line_n_t    _line_n;
        br_scan_token_line_n_t    line_number() const                           { return _line_n; }
        void                      set_line_number(const br_scan_token_line_n_t Value) { _line_n = Value; }
#       endif
#       ifdef  QUEX_OPTION_COUNTER_COLUMN
        br_scan_token_column_n_t  _column_n;
        br_scan_token_column_n_t  column_number() const                             { return _column_n; }
        void                      set_column_number(const br_scan_token_column_n_t Value) { _column_n = Value; }
#       endif
#   endif

};

inline void QUEX_NAME_TOKEN(copy)(Token* me, const Token* Other) {
  *me = *Other;
}

inline void QUEX_NAME_TOKEN(construct)(Token* __this) { }
inline void QUEX_NAME_TOKEN(destruct)(Token* __this) { }


} //namespace 

#include <br_scan/lib/lexeme.i>

#endif

 	  	 
