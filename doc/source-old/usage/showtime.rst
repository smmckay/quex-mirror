Show Time
=========

The processing of a Quex-generated engine can be made visible if the 
compile macro::

        QUEX_OPTION_DEBUG_SHOW
       
is defined (for example, by using ``-DQUEX_OPTION_DEBUG_SHOW_EXT`` as a compile
option). Quex generates code that is instrumented with macros that
are empty if this option is not set, and it if the compile option is defined
the macros expand to debug output code. The output is printed to 'standard
error' which is supposed to be immediately printed without buffering.  Based on
this output the inner function can be understood and analyzers can be debugged
in detail. Such output looks like the following::

    ./tmp.cpp:152:  * init state __________
    ./tmp.cpp:152:  input:           41 'A'
    ./tmp.cpp:152:  input position:  1
    ./tmp.cpp:195:  state 95 ______________
    ./tmp.cpp:195:  input:           42 'B'
    ./tmp.cpp:195:  input position:  2
    ./tmp.cpp:195:  state 95 ______________
    ./tmp.cpp:195:  input:           45 'E'
    ./tmp.cpp:195:  input position:  3
    ./tmp.cpp:195:  state 95 ______________
    ./tmp.cpp:195:  input:           52 'R'
    ...
    ./tmp.cpp:195:  state 95 ______________
    ./tmp.cpp:195:  input:           3A ':'
    ./tmp.cpp:195:  input position:  10
    ./tmp.cpp:536:  pre-terminal 7: [A-Z]+double-quote:double-quote
    ./tmp.cpp:539:  * terminal 7:   [A-Z]+double-quote:double-quote

This tells how the input triggers from one state to the next
and finally ends up in the terminal for ``[A-Z]:``. Especially, 
when reload is involved, it makes sense to set also the compile
option::

        QUEX_OPTION_DEBUG_SHOW_LOADS

If this option is set, additionally information about the buffer reload
process is printed. For example::

    FORWARD(entry)
    _________________________________________________________________
       buffer front--------------------------->[0000] 0x0000
                                               [0001] 0x0041
                                               [0002] 0x0042
                                               [0003] 0x0045
                                               [0004] 0x0052
                                               ...
                                               [000A] 0x003A
                                               [000B] 0x0020
       lexeme start--------------------------->[000C] 0x0047
                                               [000D] 0x0055
       input, buffer back--------------------->[000E] 0x0000
    _________________________________________________________________

is an output that tells that the start of the lexeme was at position '0xC' when
the reload was triggered and the current input was at the end of the buffer
content. The right-most numbers show the unicode value of the character that is
the content of the buffer at the given position. This feature comes especially
handy, if one tries to program a customizes character set converted. With the
compile option::

        QUEX_OPTION_DEBUG_SHOW_MODES

mode transitions can be made visible. With this option set, the analyzer
documents each mode change by outputs such as:: 

    | Mode change from GENERAL
    |             to   MATH
    ...
    | Mode change from MATH
    |             to   FORMAT_STRING
    ...
    | Mode change from FORMAT_STRING
    |             to   MATH
    ...

