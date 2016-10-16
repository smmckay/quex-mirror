Cause and Effect
================

The process of lexical analysis has been defined as the transformation of a
stream of lexatoms into a stream of tokens [#f1]_. The transformation is
achieved by sending tokens as reaction to matching patterns on a lexatom
sequence in the input stream. The first focusses on the *causes* of a pattern
match incidence. It shows how the one and only pattern is determined that wins
on a specific position in the stream.  The second subsection discusses the
*effect* of pattern matches. It describes how to associate pattern matches, and
other incidences, with actions to be executed when they occur.

.. toctree::

    match-precedence.rst
    match-actions.rst

.. rubrik:: Footnotes

.. [#f1] See section :ref:`sec:lexical-analysis`.

