Modes
=====

A lexer does everything it does in a mode.  A lexer mode is similar to human
moods in the sense that it relates to specific behavior [#f1]_, but differs in
a way that a lexer is is only in one distinct mode at a time. A lexer's
behavior is primarily determined by its reactions to pattern matches and its
reactions to events such as 'failure' or 'termination.  Lexer modes are a
syntactic means to describe a lexer's different behaviors with respect to their
*diversity* and *commonality*.

Behavioral diversity occurs when analysis depends on context.  That is, a
pattern in the input stream may have different meanings dependent on the
context in which they appear. An input language may have a 'math mode', for
example where the backslash '\' sign stands for set-subtraction, and a 'TeX
markup' :cite:`Knuth1986texbook` mode where the '\' prefixes a command.

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
popped from the stack and re-entered. No target mode needs to be specified for
``GOUP`` to return. This functionality enables the definition of a mode which
is entered by different modes and needs to return to from where it has been
entered.  Its mechanics are similar to function calls in many programming
languages.

The ``mode`` sections define what actions to execute upon what pattern match,
the define mode transitions, column-line numbering, indentation based scopes
(offside rule), if required, etc.  It is the ``mode`` sections that define the
procedure of lexical analysis. 

.. rubric:: Footnotes

.. [#f1] The funny analogy between people's moods and modes is 
         adapted from Donald Knuth's TexBook :cite:`Knuth1986texbook`,
         in his introduction to chapter 13.
