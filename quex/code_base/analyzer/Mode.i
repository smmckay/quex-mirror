/* -*- C++ -*-  vim:set syntax=cpp: 
 *
 * (C) 2004-2010 Frank-Rene Schaefer
 * ABSOLUTELY NO WARRANTY              */
#ifndef QUEX_INCLUDE_GUARD__ANALYZER__MODE_I
#define QUEX_INCLUDE_GUARD__ANALYZER__MODE_I

$$INC: definitions$$

QUEX_NAMESPACE_MAIN_OPEN

    QUEX_INLINE void
    QUEX_NAME(Mode_uncallable_analyzer_function)(QUEX_TYPE_ANALYZER* me)
    { 
        __quex_assert(0); 
        (void)me;
        return; 
    }

#   if ! defined(QUEX_OPTION_INDENTATION_DEFAULT_HANDLER)
    QUEX_INLINE void
    QUEX_NAME(Mode_on_indentation_null_function)(QUEX_TYPE_ANALYZER*  me, 
                                                 QUEX_TYPE_LEXATOM* LexemeBegin, 
                                                 QUEX_TYPE_LEXATOM* LexemeEnd)
    { (void)me; (void)LexemeBegin; (void)LexemeEnd; }
#   endif

    QUEX_INLINE void
    QUEX_NAME(Mode_on_entry_exit_null_function)(QUEX_TYPE_ANALYZER* me, 
                                                const QUEX_NAME(Mode)* TheMode) 
    { (void)me; (void)TheMode; }

    QUEX_INLINE bool
    QUEX_NAME(ModeStack_construct)(QUEX_NAME(ModeStack)* me,
                                   const size_t          N)
    {
        me->begin = (const QUEX_NAME(Mode)**)QUEX_GNAME_LIB(MemoryManager_allocate)(
                                    N * sizeof(QUEX_NAME(Mode)*),
                                    E_MemoryObjectType_MODE_STACK);
        if( ! me->begin ) {
            QUEX_NAME(ModeStack_resources_absent_mark)(me);
            return false;
        }
        else {
            me->end        = &me->begin[0];
            me->memory_end = &me->begin[N];
            return true;
        }
    }

    QUEX_INLINE void
    QUEX_NAME(ModeStack_destruct)(QUEX_NAME(ModeStack)* me)
    {
        if( me->begin ) {
            QUEX_GNAME_LIB(MemoryManager_free)((void*)&me->begin[0],
                                       E_MemoryObjectType_MODE_STACK);
        }
        QUEX_NAME(ModeStack_resources_absent_mark)(me);
    }

    QUEX_INLINE void
    QUEX_NAME(ModeStack_resources_absent_mark)(QUEX_NAME(ModeStack)* me)
    {
        me->begin      = (const QUEX_NAME(Mode)**)0;
        me->end        = (const QUEX_NAME(Mode)**)0;
        me->memory_end = (const QUEX_NAME(Mode)**)0;
    }

    QUEX_INLINE bool
    QUEX_NAME(ModeStack_resources_absent)(QUEX_NAME(ModeStack)* me)
    {
        return    me->end        == (const QUEX_NAME(Mode)**)0
               && me->memory_end == (const QUEX_NAME(Mode)**)0;
    }

    QUEX_INLINE void
    QUEX_NAME(ModeStack_print)(QUEX_NAME(ModeStack)* me)
    {
        const QUEX_NAME(Mode)** iterator = 0x0;
        if( QUEX_NAME(ModeStack_resources_absent)(me) ) {
            __QUEX_STD_printf("<uninitialized>\n");
        }
        else {
            __QUEX_STD_printf("{\n");
            __QUEX_STD_printf("    size:    %i;\n",
                              (int)(me->memory_end - me->begin));
            __QUEX_STD_printf("    content: [");
            if( me->end > me->memory_end || me->end < me->begin ) {
                __QUEX_STD_printf("<pointer corrupted>");
            }
            else {
                for(iterator=&me->end[-1]; iterator >= me->begin; --iterator) {
                    __QUEX_STD_printf("%s, ", (*iterator)->name);
                }
            }
            __QUEX_STD_printf("]\n");
            __QUEX_STD_printf("  }\n");
        }
    }

QUEX_NAMESPACE_MAIN_CLOSE

#endif /* QUEX_INCLUDE_GUARD__ANALYZER__MODE_I */
