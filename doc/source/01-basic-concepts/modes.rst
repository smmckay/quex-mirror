Modes
=====

A lexer does everything it does in a mode.  A lexer mode is similar to human
moods in the sense that it relates to specific behavior [#f1]_, but differs in
a way that a lexer is is only in one distinct mode at a time. A lexer's
behavior is primarily determined by its reactions to pattern matches and its
reactions to events such as 'failure' or 'termination.  Lexer modes are a
syntactic means to describe a lexer's different behaviors with respect to their
*diversity* and *commonality*.

Behavioral diversity occurs when analysis depends on 'context'.  That is
pattern in the input stream may have different meanings dependent on the
context in which they appear. An input language may have a 'math mode', for
example where the backslash '\' sign stands for set-subtraction, and a 'TeX
markup' :cite:`Knuth1986texbook` mode where the '\' prefixes a command.
Patterns which are redundant in some contexts might be removed from the
detection state machine--thus improving efficiency.  

Behavioral commonality can be expressed by inheritance. That is, if two modes
behave the same in some aspects, the may share a common base mode that
implements this common behavior. This helps, for example, to specify the common
behavior upon 'termination' in one single mode. All modes that inherit it
behave the same with that respect.

A lexer's mode can be changed in two ways: *history independent*, using ``GOTO
target`` and *history dependent* using ``GOSUB sub_mode`` and ``GOUP``.  Using
``GOTO target`` a current mode is forgotten as soon as the ``target`` mode is
entered.  Using ``GOSUB sub_mode`` the current mode is pushed on top of a stack
before the ``sub_mode`` mode is entered. Upon ``GOUP`` the top-most mode is
popped from the stack and re-entered. No ``current`` mode needs to be specified
for ``GOUP`` to return. This functionality enables the definition of a mode in
independently of the caller mode. Its mechanics are similar to function calls
in many programming languages.

The behavior of a lexer is determined by more than just the set of lurking
patterns and their related actions. The following enumeration lists all types
of behavior and the syntactic means that is used to specify them:

.. describe:: List of base modes  

  #. Base modes from which behavior is inherited.

.. describe:: Tags in <...> brackets

  #. Skippers, i.e. machines that run in parallel without causing any
     token to be produced.

  #. Counting behavior, i.e. what character counts how many columns or 
     lines, or causes jumps on a column number grid.

  #. Indentation based scope parameters, defining what is a newline 
     what is white space, what is bad at the beginning of a line (the
     tab character or space?) :cite:`todo`.

  #. Transition control, specifying from where a mode can be entered
     and to what mode it may transit.

  #. Inheritance control, specifying if the mode can be inherited or
     not.

.. describe:: Pattern-Action Pairs

  #. Patterns which are lurking to cause actions and send tokens.

.. describe:: Event Handlers

  #. On-Incidence definitions for 'on_failure', 'on_end_of_stream', 
     etc.

It is the ``mode`` sections in a Quex input file that define the procedure of
lexical analysis. Upon start-up, the lexical analyzer is setup in an initial
mode which is given by ``start = mode name;`` somewhere in the input files.
With this background the next section demonstrates a minimalist working example
which may be used to get into hands-on coding.

.. rubric:: Footnotes

.. [#f1] The funny analogy between people's moods and modes is 
         adapted from Donald Knuth's TexBook :cite:`Knuth1986texbook`,
         in his introduction to chapter 13.
