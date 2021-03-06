Compile Options
===============

Quex offers a set of compile options that can be set by specifying them
via the ``-D`` flag of the C-compiler. No explicit setting is necessary to create a
working analyzer. The options, though, allow to configure and fine tune the
lexical analyzer engine. The compile options split into the following groups

.. cmacro:: QUEX_OPTION_ ...

   These macros can either be defined or not. If they are defined they trigger 
   a certain behavior. All macros of this group have a sibling of the shape::

       QUEX_OPTION_ ... _DISABLED

   If this option is set than any setting is overruled, even those that have 
   been set by quex. To disable asserts for example the compiler is called
   like this::

      $CC ... -DQUEX_OPTION_ASSERTS_DISABLED_EXT

   The disablement of asserts is, by the way, essential to high performance
   lexical analysis.

.. cmacro:: QUEX_SETTING_ ...

   These macros contain a value that is expanded in the code of quex. This can
   for example be used to set the buffer size with::

      $CC ... -DQUEX_SETTING_BUFFER_SIZE_EXT=4096

.. cmacro:: QUEX_TYPE_ ...

   By means of those macros types are defined. The following overrides Quex's
   definition for the internal character type::

      $CC ... -DQUEX_TYPE_LEXATOM=UChar


None of the following compile options is necessary to get a working analyser.
Indeed, many of them are already controlled by quex. Nevertheless, they provide
tool set for fine tuning or adaptations to less regular system constraints.

..  toctree:: 
    
    options.txt 
    settings.txt 
    types.txt
