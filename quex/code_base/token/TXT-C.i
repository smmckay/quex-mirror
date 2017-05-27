/* -*- C++ -*-   vim: set syntax=cpp: 
 * (C) 2004-2009 Frank-Rene Schaefer
 * ABSOLUTELY NO WARRANTY
 */
#ifndef __QUEX_INCLUDE_GUARD__TOKEN__GENERATED__$$INCLUDE_GUARD_EXTENSION$$_I
#define __QUEX_INCLUDE_GUARD__TOKEN__GENERATED__$$INCLUDE_GUARD_EXTENSION$$_I

#ifndef    __QUEX_OPTION_PLAIN_C
#   define __QUEX_OPTION_PLAIN_C
#endif

#include "$$TOKEN_CLASS_HEADER$$"
#include <quex/code_base/definitions>

$$INCLUDE_TOKEN_CLASS_HEADER$$

QUEX_INLINE void 
$TOKEN_CLASS_set($TOKEN_CLASS*            __this, 
                 const QUEX_TYPE_TOKEN_ID ID) 
{ __this->id = ID; }

QUEX_INLINE void 
$TOKEN_CLASS_construct($TOKEN_CLASS* __this)
{
#   define self (*__this)
#   define LexemeNull  (&QUEX_NAME_TOKEN(LexemeNull))
    (void)__this;
$$CONSTRUCTOR$$
#   undef  LexemeNull
#   undef  self
}

QUEX_INLINE void 
$TOKEN_CLASS_copy_construct($TOKEN_CLASS*       __this, 
                            const $TOKEN_CLASS* __That)
{
    QUEX_NAME_TOKEN(construct)(__this);
    QUEX_NAME_TOKEN(copy)(__this, __That);
}

QUEX_INLINE void 
$TOKEN_CLASS_destruct($TOKEN_CLASS* __this)
{
#   define self (*__this)
#   define LexemeNull  (&QUEX_NAME_TOKEN(LexemeNull))
    if( ! __this ) return;

$$DESTRUCTOR$$
#   undef  LexemeNull
#   undef  self
}

QUEX_INLINE void
$TOKEN_CLASS_copy($TOKEN_CLASS*       __this, 
                  const $TOKEN_CLASS* __That)
{
#   define self  (*__this)
#   define Other (*__That)
#   define LexemeNull  (&QUEX_NAME_TOKEN(LexemeNull))
    (void)__this;
    (void)__That;
$$COPY$$
#   undef  LexemeNull
#   undef  Other
#   undef  self
    /* If the user even misses to copy the token id, then there's
     * something seriously wrong.                                 */
    __quex_assert(__this->id == __That->id);
#   ifdef QUEX_OPTION_TOKEN_STAMPING_WITH_LINE_AND_COLUMN
    __QUEX_IF_COUNT_LINES(__quex_assert(__this->_line_n == __That->_line_n));
    __QUEX_IF_COUNT_COLUMNS(__quex_assert(__this->_column_n == __That->_column_n));
#   endif
}


QUEX_INLINE bool 
$TOKEN_CLASS_take_text($TOKEN_CLASS*            __this, 
                       const QUEX_TYPE_LEXATOM* Begin, 
                       const QUEX_TYPE_LEXATOM* End)
/* RETURNS: true -- if the token claims ownership over the given memory.
 *          false -- if no ownership is claimed.                             */
{
#   define self       (*__this)
#   ifdef  LexemeNull
#   error  "Error LexemeNull shall not be defined here."
#   endif
#   define LexemeNull  (&QUEX_NAME_TOKEN(LexemeNull))
    (void)__this;
    (void)Begin;
    (void)End;
$$FUNC_TAKE_TEXT$$
#   undef  LexemeNull
#   undef  self
    /* Default: no ownership.                                                */
    return false;
}

#ifdef QUEX_OPTION_TOKEN_REPETITION_SUPPORT
QUEX_INLINE size_t 
$TOKEN_CLASS_repetition_n_get($TOKEN_CLASS* __this)
{
#   define self        (*__this)
#   define LexemeNull  (&QUEX_NAME_TOKEN(LexemeNull))
    (void)__this;
$$TOKEN_REPETITION_N_GET$$
#   undef  LexemeNull
#   undef  self
}

QUEX_INLINE void 
$TOKEN_CLASS_repetition_n_set($TOKEN_CLASS* __this, size_t N)
{
#   define self        (*__this)
#   define LexemeNull  (&QUEX_NAME_TOKEN(LexemeNull))
    (void)__this;
    (void)N;
$$TOKEN_REPETITION_N_SET$$
#   undef  LexemeNull
#   undef  self
}
#endif /* QUEX_OPTION_TOKEN_REPETITION_SUPPORT */

QUEX_INLINE const char*
$TOKEN_CLASS_map_id_to_name(const QUEX_TYPE_TOKEN_ID TokenID)
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

$$FOOTER$$

#endif /* __QUEX_INCLUDE_GUARD__TOKEN__GENERATED__$$INCLUDE_GUARD_EXTENSION$$_I */
