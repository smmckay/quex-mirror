Cause and Effect
================

Lexical analysis is understood as the process that transforms an input stream
of lexatoms into a stream of tokens (atomic chunks of meaning).  Pattern
matching lies at the core of this process. Tokens are sent as reaction to
patterns matching adjacent lexatoms in the input stream. For a given position
in the input stream a *distinct* pattern matches the best and determines the
action to be performed.  

.. toctree::

    pattern-action-pairs.rst
    match-precedence.rst
    match-actions.rst

.. rubrik:: Footnotes

.. [#f1] See section :ref:`sec:lexical-analysis`.

