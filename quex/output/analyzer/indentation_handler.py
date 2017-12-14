from   quex.engine.misc.string_handling  import blue_print
from   quex.blackboard                   import Lng, \
                                                E_IncidenceIDs

def do(Mode):
    # 'on_dedent' and 'on_n_dedent cannot be defined at the same time.
    assert not (    E_IncidenceIDs.INDENTATION_DEDENT   in Mode.incidence_db \
                and E_IncidenceIDs.INDENTATION_N_DEDENT in Mode.incidence_db)

    # A mode that deals only with the default indentation handler relies
    # on what is defined in '$QUEX_PATH/analyzer/member/on_indentation.i'
    if Mode.incidence_db.default_indentation_handler_f():
        return "    return;"

    code_fragment = Mode.incidence_db.get(E_IncidenceIDs.INDENTATION_INDENT)
    if code_fragment is not None:
        on_indent_str   = Lng.SOURCE_REFERENCED(code_fragment)
    else:
        on_indent_str   = Lng.TOKEN_SEND("QUEX_TOKEN_ID(INDENT)")

    code_fragment = Mode.incidence_db.get(E_IncidenceIDs.INDENTATION_NODENT)
    if code_fragment is not None:
        on_nodent_str   = Lng.SOURCE_REFERENCED(code_fragment)
    else:
        on_nodent_str   = Lng.TOKEN_SEND("QUEX_TOKEN_ID(NODENT)")

    on_dedent_str   = ""
    on_n_dedent_str = ""
    code_fragment = Mode.incidence_db.get(E_IncidenceIDs.INDENTATION_DEDENT)
    if code_fragment is not None:
        on_dedent_str = Lng.SOURCE_REFERENCED(code_fragment)

    code_fragment = Mode.incidence_db.get(E_IncidenceIDs.INDENTATION_N_DEDENT)
    if code_fragment is not None:
        on_n_dedent_str = Lng.SOURCE_REFERENCED(code_fragment)

    if (not on_dedent_str) and (not on_n_dedent_str):
        # If no 'on_dedent' and no 'on_n_dedent' is defined ... 
        on_dedent_str    = ""
        on_n_dedent_str  = "#if defined(QUEX_OPTION_TOKEN_REPETITION_SUPPORT)\n"
        on_n_dedent_str += "    %s\n" % Lng.TOKEN_SEND_N("ClosedN", "QUEX_TOKEN_ID(DEDENT)")
        on_n_dedent_str += "#else\n"
        on_n_dedent_str += "    while( start-- != stack->back ) %s\n" % Lng.TOKEN_SEND("QUEX_TOKEN_ID(DEDENT)")
        on_n_dedent_str += "#endif\n"

    code_fragment = Mode.incidence_db.get(E_IncidenceIDs.INDENTATION_ERROR)
    if code_fragment is not None:
        on_indentation_error = Lng.SOURCE_REFERENCED(code_fragment) 
    else:
        # Default: Blow the program if there is an indentation error.
        on_indentation_error = 'QUEX_ERROR_EXIT("Lexical analyzer mode \'%s\': indentation error detected!\\n"' \
                               % Mode.name + \
                               '                "No \'on_indentation_error\' handler has been specified.\\n");'

    # Note: 'on_indentation_bad' is applied in code generation for 
    #       indentation counter in 'indentation_counter.py'.
    txt = blue_print(on_indentation_str, [
        ["$$INDENT-PROCEDURE$$",            on_indent_str],
        ["$$NODENT-PROCEDURE$$",            on_nodent_str],
        ["$$DEDENT-PROCEDURE$$",            on_dedent_str],
        ["$$N-DEDENT-PROCEDURE$$",          on_n_dedent_str],
        ["$$INDENTATION-ERROR-PROCEDURE$$", on_indentation_error]
    ])
    return txt

on_indentation_str = """
#   define __QUEX_RETURN return
#   define RETURN        return
#   define CONTINUE      return
#   define Lexeme        LexemeBegin
#   define LexemeEnd     (me->buffer._read_p)

    QUEX_NAME(IndentationStack)*  stack = &me->counter._indentation_stack;
    QUEX_TYPE_INDENTATION*        start = 0x0;

    __quex_assert((long)Indentation >= 0);

    if( Indentation > *(stack->back) ) {
        ++(stack->back);
        if( stack->back == stack->memory_end ) QUEX_ERROR_EXIT("Indentation stack overflow.");
        *(stack->back) = Indentation;
$$INDENT-PROCEDURE$$
        __QUEX_RETURN;
    }
    else if( Indentation == *(stack->back) ) {
$$NODENT-PROCEDURE$$
    }
    else  {
        start = stack->back;
        --(stack->back);
#       if ! defined(QUEX_OPTION_TOKEN_REPETITION_SUPPORT)
#       define First true
$$DEDENT-PROCEDURE$$
#       undef  First
#       endif
        while( Indentation < *(stack->back) ) {
            --(stack->back);
#           if ! defined(QUEX_OPTION_TOKEN_REPETITION_SUPPORT)
#           define First false
$$DEDENT-PROCEDURE$$
#           undef  First
#           endif
        }

        if( Indentation == *(stack->back) ) { 
            /* 'Landing' must happen on indentation border. */
#           define ClosedN (start - stack->back)
$$N-DEDENT-PROCEDURE$$
#           undef  ClosedN
        } else { 
#            define IndentationStackSize ((size_t)(1 + start - stack->front))
#            define IndentationStack(I)  (*(stack->front + I))
#            define IndentationUpper     (*(stack->back))
#            define IndentationLower     ((stack->back == stack->front) ? *(stack->front) : *(stack->back - 1))
#            define ClosedN              (start - stack->back)
$$INDENTATION-ERROR-PROCEDURE$$
#            undef IndentationStackSize 
#            undef IndentationStack  
#            undef IndentationUpper     
#            undef IndentationLower     
#            undef ClosedN
        }
    }
    __QUEX_RETURN;

#   undef Lexeme    
#   undef LexemeEnd 
"""

