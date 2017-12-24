from   quex.engine.misc.string_handling  import blue_print
from   quex.blackboard                   import Lng, \
                                                E_IncidenceIDs
from   quex.token_db                     import token_repetition_token_id_list

def do(Mode):
    # 'on_dedent' and 'on_n_dedent cannot be defined at the same time.
    assert not (    E_IncidenceIDs.INDENTATION_DEDENT   in Mode.incidence_db \
                and E_IncidenceIDs.INDENTATION_N_DEDENT in Mode.incidence_db)

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

    code_fragment = Mode.incidence_db.get(E_IncidenceIDs.INDENTATION_DEDENT)
    if code_fragment is not None:
        on_dedent_str = Lng.SOURCE_REFERENCED(code_fragment)
    else:
        on_dedent_str = Lng.TOKEN_SEND("QUEX_TOKEN_ID(DEDENT)")

    code_fragment   = Mode.incidence_db.get(E_IncidenceIDs.INDENTATION_N_DEDENT)
    if code_fragment is not None:
        on_n_dedent_str = Lng.SOURCE_REFERENCED(code_fragment)
    else:
        on_n_dedent_str = Lng.TOKEN_SEND_N("ClosedN", "QUEX_TOKEN_ID(DEDENT)")

    code_fragment = Mode.incidence_db.get(E_IncidenceIDs.INDENTATION_ERROR)
    on_indentation_error = ""
    if code_fragment is not None:
        on_indentation_error = Lng.SOURCE_REFERENCED(code_fragment) 

    # Note: 'on_indentation_bad' is applied in code generation for 
    #       indentation counter in 'indentation_counter.py'.
    return blue_print(on_indentation_str, [
        ["$$INDENT-PROCEDURE$$",            on_indent_str],
        ["$$NODENT-PROCEDURE$$",            on_nodent_str],
        ["$$DEDENT-PROCEDURE$$",            on_dedent_str],
        ["$$N-DEDENT-PROCEDURE$$",          on_n_dedent_str],
        ["$$INDENTATION-ERROR-PROCEDURE$$", on_indentation_error]
    ])

on_indentation_str = """
#if defined(QUEX_OPTION_INDENTATION_TRIGGER) 
void
$on_indentation(QUEX_TYPE_ANALYZER*    me, 
                QUEX_TYPE_INDENTATION  Indentation, 
                QUEX_TYPE_LEXATOM*     Begin) 
{
    (void)me;
    (void)Indentation;
    (void)Begin;
#   ifndef self
#   define self          (*me)
#   endif
#   define Lexeme        Begin
#   define LexemeEnd     (me->buffer._read_p)

    QUEX_NAME(IndentationStack)*  stack = &me->counter._indentation_stack;
    QUEX_TYPE_INDENTATION*        start = 0x0;
    (void)start;

    __quex_assert((long)Indentation >= 0);

    if( Indentation > *(stack->back) ) {
        ++(stack->back);
        if( stack->back == stack->memory_end ) {
            QUEX_NAME(error_code_set_if_first)(me, E_Error_Indentation_StackOverflow);
            return;
        }
        *(stack->back) = Indentation;
$$INDENT-PROCEDURE$$
        return;
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
#           if defined(QUEX_OPTION_TOKEN_REPETITION_SUPPORT)
#           define ClosedN (start - stack->back)
$$N-DEDENT-PROCEDURE$$
#           undef  ClosedN
#           endif
        } else { 
#            define IndentationStackSize ((size_t)(1 + start - stack->front))
#            define IndentationStack(I)  (*(stack->front + I))
#            define IndentationUpper     (*(stack->back))
#            define IndentationLower     ((stack->back == stack->front) ? *(stack->front) : *(stack->back - 1))
#            define ClosedN              (start - stack->back)
             QUEX_NAME(error_code_set_if_first)(me,  
                                                E_Error_Indentation_DedentNotOnIndentationBorder);
$$INDENTATION-ERROR-PROCEDURE$$
#            undef IndentationStackSize 
#            undef IndentationStack  
#            undef IndentationUpper     
#            undef IndentationLower     
#            undef ClosedN
             return;
        }
    }

#   undef Lexeme    
#   undef LexemeEnd 
}
#endif
"""

