/* -*- C++ -*-   vim: set syntax=cpp: 
 * (C) 2004-2009 Frank-Rene Schaefer
 * ABSOLUTELY NO WARRANTY
 */
#ifndef QUEX_TOKEN_INCLUDE_GUARD__TOKEN__GENERATED__I
#define QUEX_TOKEN_INCLUDE_GUARD__TOKEN__GENERATED__I

$$INCLUDE_TOKEN_CLASS_HEADER$$

QUEX_INLINE void 
QUEX_NAME_TOKEN(set)($$TOKEN_CLASS$$*         __this, 
                     const QUEX_TYPE_TOKEN_ID ID) 
{ __this->id = ID; }

QUEX_INLINE void 
QUEX_NAME_TOKEN(construct)($$TOKEN_CLASS$$* __this)
{
#   define self (*__this)
#   define LexemeNull  (&QUEX_GNAME(LexemeNull))
    (void)__this;
$$CONSTRUCTOR$$
#   undef  LexemeNull
#   undef  self
}

QUEX_INLINE void 
QUEX_NAME_TOKEN(copy_construct)($$TOKEN_CLASS$$*       __this, 
                                const $$TOKEN_CLASS$$* __That)
{
    QUEX_NAME_TOKEN(construct)(__this);
    QUEX_NAME_TOKEN(copy)(__this, __That);
}

QUEX_INLINE void 
QUEX_NAME_TOKEN(destruct)($$TOKEN_CLASS$$* __this)
{
#   define self (*__this)
#   define LexemeNull  (&QUEX_GNAME(LexemeNull))
    if( ! __this ) return;

$$DESTRUCTOR$$
#   undef  LexemeNull
#   undef  self
}

QUEX_INLINE void
QUEX_NAME_TOKEN(copy)($$TOKEN_CLASS$$*       __this, 
                      const $$TOKEN_CLASS$$* __That)
{
#   define self  (*__this)
#   define Other (*__That)
#   define LexemeNull  (&QUEX_GNAME(LexemeNull))
    if( __this == __That ) { return; }
$$COPY$$
#   undef  LexemeNull
#   undef  Other
#   undef  self
    /* If the user even misses to copy the token id, then there's
     * something seriously wrong.                                 */
    __quex_assert(__this->id == __That->id);
    $$<token-stamp-line>   __quex_assert(__this->_line_n == __That->_line_n);$$
    $$<token-stamp-column> __quex_assert(__this->_column_n == __That->_column_n);$$
}


$$<token-take-text>------------------------------------------------------------
QUEX_INLINE bool 
QUEX_NAME_TOKEN(take_text)($$TOKEN_CLASS$$*            __this, 
                           const QUEX_TYPE_LEXATOM* Begin, 
                           const QUEX_TYPE_LEXATOM* End)
/* RETURNS: true -- if the token claims ownership over the given memory.
 *          false -- if no ownership is claimed.                             */
{
#   define self       (*__this)
#   ifdef  LexemeNull
#   error  "Error LexemeNull shall not be defined here."
#   endif
#   define LexemeNull  (&QUEX_GNAME(LexemeNull))
    (void)__this;
    (void)Begin;
    (void)End;
$$FUNC_TAKE_TEXT$$
#   undef  LexemeNull
#   undef  self
    /* Default: no ownership.                                                */
    return false;
}
$$-----------------------------------------------------------------------------

$$<token-repetition>-----------------------------------------------------------
QUEX_INLINE size_t 
QUEX_NAME_TOKEN(repetition_n_get)($$TOKEN_CLASS$$* __this)
{
#   define self        (*__this)
#   define LexemeNull  (&QUEX_GNAME(LexemeNull))
    (void)__this;
$$TOKEN_REPETITION_N_GET$$
#   undef  LexemeNull
#   undef  self
}

QUEX_INLINE void 
QUEX_NAME_TOKEN(repetition_n_set)($$TOKEN_CLASS$$* __this, size_t N)
{
#   define self        (*__this)
#   define LexemeNull  (&QUEX_GNAME(LexemeNull))
    (void)__this;
    (void)N;
$$TOKEN_REPETITION_N_SET$$
#   undef  LexemeNull
#   undef  self
}
$$-----------------------------------------------------------------------------

$$FOOTER$$

#endif /* QUEX_TOKEN_INCLUDE_GUARD__TOKEN__GENERATED__I */
