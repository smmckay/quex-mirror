/* -*- C++ -*- vim:set syntax=cpp:
 * (C) Frankt-Rene Schaefer
 * ABSOLUTELY NO WARRANTY               */
#ifndef __QUEX_INCLUDE_GUARD__ANALYZER__MEMBER__MODE_HANDLING_I
#define __QUEX_INCLUDE_GUARD__ANALYZER__MEMBER__MODE_HANDLING_I

#include <quex/code_base/definitions>
#include <quex/code_base/analyzer/Mode>

QUEX_NAMESPACE_MAIN_OPEN

    QUEX_INLINE QUEX_NAME(Mode)*
    QUEX_NAME(get_mode)(QUEX_TYPE_ANALYZER* me) 
    { return me->__current_mode_p; }

    QUEX_INLINE int
    QUEX_NAME(get_mode_id)(const QUEX_TYPE_ANALYZER* me)
    { return me->__current_mode_p->id; }

    QUEX_INLINE const char*
    QUEX_NAME(get_mode_name)(const QUEX_TYPE_ANALYZER* me)
    { return me->__current_mode_p->name; }

    QUEX_INLINE void 
    QUEX_NAME(set_mode_brutally)(QUEX_TYPE_ANALYZER* me, QUEX_NAME(Mode)* ModeP) 
    /* Core of all mode setting functions. 
     *
     * ADAPTS: -- current mode pointer.
     *         -- current analyzer function pointer
     *         -- setting the buffer's handlers for 'on_buffer_overflow' and 
     *            'on_buffer_before_change'                                   */
    { 
        __quex_debug_show_mode_transition(me, ModeP);

        me->__current_mode_p          = ModeP;
        me->current_analyzer_function = ModeP->analyzer_function; 

        QUEX_NAME(Buffer_callbacks_set)(&me->buffer, 
                                             me->__current_mode_p->buffer_callbacks.on_buffer_before_change,
                                             me->__current_mode_p->buffer_callbacks.on_buffer_overflow,
                                             (void*)me);
    }

    QUEX_INLINE void
    QUEX_NAME(set_mode_brutally_by_id)(QUEX_TYPE_ANALYZER* me, const int ModeID)
    { 
        __quex_assert(ModeID < __QUEX_SETTING_MAX_MODE_CLASS_N);
        QUEX_NAME(set_mode_brutally)(me, QUEX_NAME(mode_db)[ModeID]); 
    }

    QUEX_INLINE void    
    QUEX_NAME(enter_mode)(QUEX_TYPE_ANALYZER* me, /* NOT const*/ QUEX_NAME(Mode)* TargetMode) 
    {
#       ifdef __QUEX_OPTION_ON_ENTRY_HANDLER_PRESENT
        QUEX_NAME(Mode)* SourceMode = me->__current_mode_p;
#       endif

#       ifdef __QUEX_OPTION_ON_EXIT_HANDLER_PRESENT
        me->__current_mode_p->on_exit(me, TargetMode);
#       endif

        QUEX_NAME(set_mode_brutally)(me, TargetMode);

#       ifdef __QUEX_OPTION_ON_ENTRY_HANDLER_PRESENT
        TargetMode->on_entry(me, SourceMode);         
#       endif
    }

    QUEX_INLINE QUEX_NAME(Mode)*
    QUEX_NAME(map_mode_id_to_mode)(QUEX_TYPE_ANALYZER* me, const int ModeID)
    { 
        (void)me;
        __quex_assert(ModeID >= 0);
        __quex_assert(ModeID < __QUEX_SETTING_MAX_MODE_CLASS_N); 
        return QUEX_NAME(mode_db)[ModeID]; 
    }

    QUEX_INLINE int  
    QUEX_NAME(map_mode_to_mode_id)(const QUEX_TYPE_ANALYZER* me, const QUEX_NAME(Mode)* Mode)
    { (void)me; return Mode->id; }

    QUEX_INLINE void 
    QUEX_NAME(pop_mode)(QUEX_TYPE_ANALYZER* me) 
    { 
        if( me->_mode_stack.end == me->_mode_stack.begin ) {
            QUEX_NAME(error_code_set_if_first)(me, E_Error_ModeStack_PopOnTopLevel);
        }
        else {
            --(me->_mode_stack.end);
            QUEX_NAME(enter_mode)(me, *me->_mode_stack.end); 
        }
    }

    QUEX_INLINE void
    QUEX_NAME(pop_drop_mode)(QUEX_TYPE_ANALYZER* me) 
    { 
        if( me->_mode_stack.end == me->_mode_stack.begin ) {
            QUEX_NAME(error_code_set_if_first)(me, E_Error_ModeStack_PopOnTopLevel);
        }
        else {
            --(me->_mode_stack.end);
            /* do not care about what was popped */
        }
    }
        
    QUEX_INLINE void       
    QUEX_NAME(push_mode)(QUEX_TYPE_ANALYZER* me, QUEX_NAME(Mode)* new_mode) 
    { 
        if( me->_mode_stack.end == me->_mode_stack.memory_end ) {
            QUEX_NAME(error_code_set_if_first)(me, E_Error_ModeStack_Overflow);
        }
        else {
            *me->_mode_stack.end = me->__current_mode_p;
            ++(me->_mode_stack.end);
            QUEX_NAME(enter_mode)(me, new_mode); 
        }
    }

QUEX_NAMESPACE_MAIN_CLOSE

#endif /* __QUEX_INCLUDE_GUARD__ANALYZER__MEMBER__MODE_HANDLING_I */
