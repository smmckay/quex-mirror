#ifndef __TOKEN_H__
#define __TOKEN_H__

#ifndef    QUEX_TYPE_TOKEN_ID
#   define QUEX_TYPE_TOKEN_ID              uint32_t
#endif
namespace quex {

    struct Token {

    public:
        void set(const QUEX_TYPE_TOKEN_ID ID)  { id = ID; }

        QUEX_TYPE_TOKEN_ID    id;

        QUEX_TYPE_TOKEN_ID    type_id() const                       { return id; }
        static const char*    map_id_to_name(QUEX_TYPE_TOKEN_ID ID) { (void)ID; return ""; } 

        const std::string     type_id_name() const { return map_id_to_name(id); }

#   ifdef     QUEX_OPTION_TOKEN_STAMPING_WITH_LINE_AND_COLUMN
#       ifdef QUEX_OPTION_COUNTER_LINE
        QUEX_TYPE_TOKEN_LINE_N    _line_n;
        QUEX_TYPE_TOKEN_LINE_N    line_number() const                                 { return _line_n; }
        void                      set_line_number(const QUEX_TYPE_TOKEN_LINE_N Value) { _line_n = Value; }
#       endif
#       ifdef  QUEX_OPTION_COUNTER_COLUMN
        QUEX_TYPE_TOKEN_COLUMN_N  _column_n;
        QUEX_TYPE_TOKEN_COLUMN_N  column_number() const                                   { return _column_n; }
        void                      set_column_number(const QUEX_TYPE_TOKEN_COLUMN_N Value) { _column_n = Value; }
#       endif
#   endif

    };

extern void QUEX_NAME_TOKEN(copy)(Token* me, const Token* Other);
extern void QUEX_NAME_TOKEN(construct)(Token* __this);
extern void QUEX_NAME_TOKEN(destruct)(Token* __this);
extern bool QUEX_NAME_TOKEN(take_text)(Token*                   __this, 
                                       const QUEX_TYPE_LEXATOM* Begin, 
                                       const QUEX_TYPE_LEXATOM* End);
}

#include <quex/code_base/lexeme.i>
#endif

 	  	 
