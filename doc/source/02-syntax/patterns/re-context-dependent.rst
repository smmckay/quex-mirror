.. _sec:pre-and-post-contexts:

Pre- and Post-Contexts
#######################

Patterns may require a restricted context. Modes and mode transitions model
larger contexts such as *languages*. A more concise type of context is the
*border*, i.e. to what comes before or after the pattern. Relying on regular
expressions pre- and post-contexts provide a means to specify such constraints.
Typical border conditions are 'begin-of-line' or 'end-of-line'. Those can 
be caught by matching regular expressions. 

The reliance on regular expressions implies that only the data stream context
can be considered for matching. The lexer's state or that of any external
component cannot be considered that way. There is an exception though: the
conditions 'begin-of-stream' and 'end-of-stream'. Precisely, they are
conditions on the lexer's current input pointer and the byte loader.  For the
sake of convenience syntax is provided to deal with the two conditions.

.. describe:: <<BOS>> P

    Defines the pre-context 'begin-of-stream'. The pattern ``P`` only matches
    at the beginning of the input stream. 

.. describe:: P <<EOS>>

    Defines the post-context 'end-of-stream'. The pattern ``P`` only matches at
    the end of the input stream. This post context must be considered with care
    in situations where there might be no explicit end-of-stream condition,
    such as byte loaders based on socket connections.

Notably, there must be *white space* between the ``<<BOS>>`` and the pattern as well
as after a pattern which is followed by ``<<EOS>>``.  Any other dependency on
object states must be expressed by mode transitions.  The rest of this section
deals with context dependencies on the input stream itself, i.e. those which
can be expressed by regular expressions.  

A pre-context matches backwards before the start position of the current
analyzer step. A post-context matches after what is matched by the core
pattern.  Lexatoms matching the pre- and post-contexts are not part of the
matching pattern's lexeme.  The example in figure :ref:`pre-and-post-context`
shows the example of a matching pattern::

    "hello "/"world"/"!"

That is, ``world`` is only matched if it appears after ``"hello "`` and before
``"!"``. The lexatoms before and after the sequence ``world`` are considered,
but are they do not contribute to the resulting lexeme which is solely what
matched the regular expression ``"world"``. The first lexatom to be considered
in the next analysis step is the exclamation mark. That is, the input pointer
is set to the position right after where the core pattern matches, even though
further content has been considered already as a post-context.

.. _fig:pre-and-post-context:

.. figure:: ../../figures/pre-and-post-context.png

   Pre- and post context around a core pattern.
 
The following syntax elements are available for the specification of
context rules.

.. describe:: ^R 

   a  regular expression ``R``, but only at the beginning of a line. This
   condition holds whenever the scan starts *right after a newline character*
   or at the *beginning of the character stream* (i.e. ``<<BOS>>`` is implied).
   It scans only for a single newline character 0x0A '\\n' backwards,
   independent on how the particular operating system codes the newline. 

.. describe:: R$ 

    a regular expression R, but only at the *end of a line* or at *the end of
    the input stream* (i.e. <<EOS>> is implied). Traditionally, a newline can
    be coded in two ways: the Unix-way with a plain 0x0A '\\n' or the DOS-way
    with the sequence 0x0D 0x0A '\\r\\n'. By default both are considered as
    post-context.  The command line option ``--no-DOS`` allows one to waive the
    consideration of DOS newlines.

For other cases than the aforementioned regular expressions can be defined.  In
the following, ``R``, ``S``, and ``Q`` represent regular expressions. ``R``
represents the core pattern of what is relevant for the matching lexeme. ``Q``
is the pre-context and ``S`` is the post-context.  The following means allow to
specify pre- and post-contexts based on regular expressions.

.. describe:: R/S

   matches an ``R``, but only if it is followed by an ``S``. Upon match the
   input is set right after where ``R`` matched.  ``S`` is the post-context of
   ``R``.  
   
   The case where the repeated or optional end of ``R`` matches the beginning
   of ``S`` is handled by a *philosophical cut* to avoid the 'dangerous
   trailing context' :cite:`Paxson1995flex` problem [#f1]_. The 'philosophical
   cut' modifies the post context, so that the core pattern matches as long as
   possible. This is in accordance with the longest match, which is Quex's
   philosophy of analysis.
		 
.. describe:: Q/R/ 

    matches ``R`` from the current position, but only if it is preceded by a
    ``Q``. Practically, this means the analyzer goes backwards in order to
    determine the condition.  ``Q`` is the pre-context of ``R``.
                  
.. describe:: Q/R/S 

    matches ``R`` from the current position, but only if the preceding matches
    a ``Q`` and the following matches an ``S``.  ``Q`` is the pre-context of
    ``R`` and ``S`` is its post-context.

Neither pre- nor post-context should contain an empty path. An empty path means
that even no lexatom satisfies the condition. Such a condition is always
fulfilled and, therefore, such a pre- or post-context is not really a
constraint.  Pre- and post contexts are the utmost syntactical unit. This means
that they cannot be logically or-ed.   The following specification
is *dysfunctional*.::

   (A/B)|(C/D) => QUEX_TKN_SOME();   // WRONG!

However, the functionality of it can be achieved by splitting the or-ed
condition and associating it with the same action as follows.::

   A/B  => QUEX_TKN_SOME();          // OK!
   C/D  => QUEX_TKN_SOME();          // OK!

.. rubric:: Footnotes

.. [#f1] The POSIX draft :cite:`ISO1993posix` mentions that text matched by
    those patterns is undefined. The origin of this problem lies in the way state
    machines are treated.  To avoid this a 'stepping backward from the end of the
    post-condition to the end of the core pattern' must be implemented. Quex does
    exactly that, but it needs to modify the state machines sometimes (in which
    case a warning message is issued).
          
