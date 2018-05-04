/* This content is pasted into header, so the include guard is superfluous. 
 * It is left in place, so that if some time later the code generator is 
 * adapted to generate independent files, it will still work safely.          */
#ifndef __QUEX_INCLUDE_GUARD__TOKEN__GENERATED__$$INCLUDE_GUARD_EXTENSION$$_I
#define __QUEX_INCLUDE_GUARD__TOKEN__GENERATED__$$INCLUDE_GUARD_EXTENSION$$_I

$$INCLUDE_TOKEN_CLASS_HEADER$$
$$INCLUDE_TOKEN_ID_HEADER$$
$$INC: lexeme_base.i$$

QUEX_NAMESPACE_TOKEN_OPEN

QUEX_INLINE
$TOKEN_CLASS::$TOKEN_CLASS()
{
#   define self (*this)
#   define LexemeNull  (&QUEX_NAME(LexemeNull))
$$CONSTRUCTOR$$
#   undef  LexemeNull
#   undef  self
}

QUEX_INLINE
$TOKEN_CLASS::$TOKEN_CLASS(const $TOKEN_CLASS& Other)
{
   QUEX_NAME_TOKEN(copy)(this, &Other);
#   define self (*this)
#   define LexemeNull  (&QUEX_NAME(LexemeNull))
$$CONSTRUCTOR$$
#   undef  LexemeNull
#   undef  self
}

QUEX_INLINE
$TOKEN_CLASS::~$TOKEN_CLASS()
{
#   define self (*this)
#   define LexemeNull  (&QUEX_NAME(LexemeNull))
$$DESTRUCTOR$$
#   undef  LexemeNull
#   undef  self
}

QUEX_INLINE void
QUEX_NAME_TOKEN(construct)($TOKEN_CLASS* __this)
{
    /* Explicit constructor call by 'placement new' */
    new ((void*)__this) $TOKEN_CLASS;
}

QUEX_INLINE void
QUEX_NAME_TOKEN(destruct)($TOKEN_CLASS* __this)
{
    if( ! __this ) return;
    __this->$TOKEN_CLASS::~$TOKEN_CLASS();  
}

QUEX_INLINE void
QUEX_NAME_TOKEN(copy)($TOKEN_CLASS* __this, const $TOKEN_CLASS* __That)
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
QUEX_NAME_TOKEN(take_text)($TOKEN_CLASS*              __this, 
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
QUEX_NAME_TOKEN(repetition_n_get)($TOKEN_CLASS* __this)
{
#   define self (*__this)
    (void)__this;
$$TOKEN_REPETITION_N_GET$$
#   undef self
}

QUEX_INLINE void 
QUEX_NAME_TOKEN(repetition_n_set)($TOKEN_CLASS* __this, size_t N)
{
#   define self (*__this)
    (void)__this; (void)N;
$$TOKEN_REPETITION_N_SET$$
#   undef  self
}
#endif /* QUEX_OPTION_TOKEN_REPETITION_SUPPORT */

QUEX_INLINE const char*
QUEX_NAME_TOKEN(map_id_to_name)(const QUEX_TYPE_TOKEN_ID TokenID)
{
   static char  error_string[64];

   /* NOTE: This implementation works only for token id types that are 
    *       some type of integer or enum. In case an alien type is to
    *       used, this function needs to be redefined.                  */
   switch( TokenID ) {
   default: {
       __QUEX_STD_sprintf(error_string, "<UNKNOWN TOKEN-ID: %i>", (int)TokenID);
       return error_string;
   }
$$MAP_ID_TO_NAME_CASES$$
   }
}

QUEX_NAMESPACE_TOKEN_CLOSE

#endif /* __QUEX_INCLUDE_GUARD__TOKEN__GENERATED__$$INCLUDE_GUARD_EXTENSION$$_I */
