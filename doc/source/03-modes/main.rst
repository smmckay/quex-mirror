Modes
*****

A lexer does everything it does in a mode. Precisely, a mode is the aggregation
of behavior-related configurations which is associated with a distinct name:
the mode name. Behavior is concerned with *what* tokens are produced and *how*
they are produced as a reaction to some type of *input stream*.  A mode
specifies the *interpretation* of an input stream but also influences the
*efficiency of interpretation*. 

This chapter elaborates on modes. A lexer's essential characteristic is pattern
matching. This is discussed in detail. Mode transitions are discussed. Mode
inheritance is presented as it may be used to transparently construct complex
modes from smaller base modes [#f1]_ . Incidences are introduced which are
handled by dedicated handlers.  Then, mode tags (``<skip ...>``, ...) ...>``,
...) for skipping and line and column counting are explained. The *off-side
rule*, i.e. indentation based lexical analysis is handled with the
``indentation`` tag which is also explained in detail.  Eventually, some light
is shone on areas where vigilance is appropriate in order to avoid unexpected
behavior.

 #. pattern-matching

 #. transitions

 #. inheritance -> hierarchie
    <inheritable: ...>

 #. match precedence:
     #. length, pattern position, pattern position by base mode
     #. PRIORITY-MARK, DELETION-MARK
 
 #. incidence handlers

 #. tags
     #. <inheritable: >
     #. <exit >
     #. <entry >
     #. <skip, skip_range, skip_nested_range>
     #. <counter>
     #. <indentation>

 #. pitfalls
     #. regular expression pitfalls
     #. incidence handlers

.. toctree::

   matching/main.rst 
   transitions.rst
   inheritance.rst
   incidence-handlers.rst
   tags.rst
   pitfalls/main.rst


.. rubric:: Footnotes

.. [#f1] The *start conditions* in lex/flex :cite:`Paxson1995flex` are similar 
         to modes in a sense that they conditionally activate pattern matching 
         rules. However, lex does not provide a means to model inheritance 
         relationships between modes. The 'inclusiveness' of a mode in lex is 
         only related to rules without any start condition. 


