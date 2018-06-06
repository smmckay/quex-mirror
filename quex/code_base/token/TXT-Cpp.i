/* This content is pasted into header, so the include guard is superfluous. 
 * It is left in place, so that if some time later the code generator is 
 * adapted to generate independent files, it will still work safely.          */
#ifndef QUEX_INCLUDE_GUARD__TOKEN__GENERATED_I
#define QUEX_INCLUDE_GUARD__TOKEN__GENERATED_I

$$INCLUDE_TOKEN_CLASS_HEADER$$

QUEX_NAMESPACE_TOKEN_OPEN

QUEX_INLINE
$$TOKEN_CLASS$$::$$TOKEN_CLASS$$()
{
#   define self (*this)
#   define LexemeNull  (&QUEX_NAME(LexemeNull))
$$CONSTRUCTOR$$
#   undef  LexemeNull
#   undef  self
}

QUEX_INLINE
$$TOKEN_CLASS$$::$$TOKEN_CLASS$$(const $$TOKEN_CLASS$$& Other)
{
   $$TOKEN_CLASS$$_copy(this, &Other);
#   define self (*this)
#   define LexemeNull  (&QUEX_NAME(LexemeNull))
$$CONSTRUCTOR$$
#   undef  LexemeNull
#   undef  self
}

QUEX_INLINE
$$TOKEN_CLASS$$::~$$TOKEN_CLASS$$()
{
#   define self (*this)
#   define LexemeNull  (&QUEX_NAME(LexemeNull))
$$DESTRUCTOR$$
#   undef  LexemeNull
#   undef  self
}

QUEX_INLINE $$TOKEN_CLASS$$& 
$$TOKEN_CLASS$$::operator=(const $$TOKEN_CLASS$$& That) 
{ if( this != &That ) { $$TOKEN_CLASS$$_copy(this, &That); } return *this; }

QUEX_INLINE void
$$TOKEN_CLASS$$_construct($$TOKEN_CLASS$$* __this)
{
    /* Explicit constructor call by 'placement new' */
    new ((void*)__this) $$TOKEN_CLASS$$;
}

QUEX_INLINE void
$$TOKEN_CLASS$$_destruct($$TOKEN_CLASS$$* __this)
{
    if( ! __this ) return;
    __this->$$TOKEN_CLASS$$::~$$TOKEN_CLASS$$();  
}

QUEX_INLINE void
$$TOKEN_CLASS$$_copy($$TOKEN_CLASS$$* __this, const $$TOKEN_CLASS$$* __That)
{
#   define self  (*__this)
#   define Other (*__That)
#   define LexemeNull  (&QUEX_NAME(LexemeNull))
    (void)__this;
    (void)__That;
$$COPY$$
#   undef LexemeNull
#   undef Other
#   undef self
   /* If the user even misses to copy the token id, then there's
    * something seriously wrong.                                 */
   __quex_assert(__this->id == __That->id);
#ifdef     QUEX_OPTION_TOKEN_STAMPING_WITH_LINE_AND_COLUMN
#   ifdef QUEX_OPTION_TOKEN_STAMPING_WITH_LINE_AND_COLUMN
    __QUEX_IF_COUNT_LINES(__quex_assert(__this->_line_n == __That->_line_n));
    __QUEX_IF_COUNT_COLUMNS(__quex_assert(__this->_column_n == __That->_column_n));
#   endif
#endif
}

#ifdef QUEX_OPTION_TOKEN_TAKE_TEXT_SUPPORT
QUEX_INLINE bool 
$$TOKEN_CLASS$$_take_text($$TOKEN_CLASS$$*              __this, 
                          const QUEX_TYPE_LEXATOM* Begin, 
                          const QUEX_TYPE_LEXATOM* End)
/* RETURNS: true -- if the token claims ownership over the given memory.
 *          false -- if no ownership is claimed.                             */
{
#   define self      (*__this)
#   define LexemeNull  (&QUEX_NAME(LexemeNull))
    (void)__this;
$$FUNC_TAKE_TEXT$$
#   undef  LexemeNull
#   undef  self
    /* Default: no ownership.                                                */
    return false;
}
#endif

#ifdef QUEX_OPTION_TOKEN_REPETITION_SUPPORT
QUEX_INLINE size_t 
$$TOKEN_CLASS$$_repetition_n_get($$TOKEN_CLASS$$* __this)
{
#   define self (*__this)
    (void)__this;
$$TOKEN_REPETITION_N_GET$$
#   undef self
}

QUEX_INLINE void 
$$TOKEN_CLASS$$_repetition_n_set($$TOKEN_CLASS$$* __this, size_t N)
{
#   define self (*__this)
    (void)__this; (void)N;
$$TOKEN_REPETITION_N_SET$$
#   undef  self
}
#endif /* QUEX_OPTION_TOKEN_REPETITION_SUPPORT */

QUEX_NAMESPACE_TOKEN_CLOSE

#endif /* QUEX_INCLUDE_GUARD__TOKEN__GENERATED_I */
