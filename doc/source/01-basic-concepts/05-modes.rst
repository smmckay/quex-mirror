Modes
=====

A lexer does everything it does in a mode.  A lexer mode is similar to human
moods in the sense that it relates to specific behavior [#f1]_, but
distinguishes itself by being distinct for a given point in time. A lexer's
behavior is expressed by the conditions under which it identifies patterns in a
data stream and its reactions to it. Further, a modes behavior describes its
reactions to events such as 'character encoding error', 'failure', 'buffer
overflow', and the like. 

Mode transition is a means to model a change in behavior.  There are two
types of transitions: *history independent*, and *history dependent*. A history
independent mode transition transits to a target mode while forgetting about its
origin. A history dependent transition keeps track of the mode from where the mode
transition was initiated. A mode that has been entered that way can return to
the mode from where it has been entered without knowing it explicitly. The means
to perform that are ``GOTO`` and ``GOSUB`` keywords which underline its 
correspondance to traditional function calls.

The primary goal of modes is to model *diversity*.  Behavioral diversity occurs
when analysis depends on context.  That is, a data stream may contain several
'languages', i.e. several way how information is coded. A programming language
might provide a ``MATH`` mode, for example where the backslash ``\`` sign stands for
set-subtraction, and a ``TEX_MARKUP`` mode :cite:`Knuth1986texbook` mode where the
``\\`` prefixes a command.

Behavioral *commonality* can be expressed by inheritance. That is, if two modes
behave the same in some aspects, they may share a common base mode that
implements this common behavior. This helps, for example, to specify the common
behavior upon 'termination' in one single mode. All modes that inherit it
behave the same with that respect.

.. rubric:: Footnotes

.. [#f1] The funny analogy between people's moods and modes is 
         adapted from Donald Knuth's TexBook :cite:`Knuth1986texbook`,
         in his introduction to chapter 13.
