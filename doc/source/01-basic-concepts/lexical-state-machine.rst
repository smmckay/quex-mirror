Lexical Analyzers
=================

Information is that what informs :cite:`wiki:Information`. It contains
knowledge, to be observed by a conscious observer, or data to be processed.
The information content, i.e. the entropy :cite:`Shannon1951`, is only
different from zero, if it is present in its source and lacks at its
destination.  Thus, information only exists in the context of information
transfer over space and time. 

Non-ephemeral information transfer either relies on 'writing', i.e. a
sequential interpretation of symbols, or 'pictures', i.e. a quasi-parallel
interpretation of symbols.  Pictures convey information very efficiently
relying on the recipicients intuition [#f3]_.  This implies that source and
drain must share a cultural context [#f4]_.  Pictures are a useful to describe
configurations of objects :cite:`Szeliski2010computer` (TODO better citation).
However, the space of describebable subjects suffers under the restrictions 
of a cultural context.

Sequential symbol flow, such as in writing,  requires knowledge of the language
being used.  However, the range of describable things extends beyond the set of
known objects. New concepts may be associated with new words relying on known
objects and their relations in a formal and distinct manner.  The range of
possible statements  even exceeds what is imaginable. The distinct and precise
nature of a formal sequential language makes it the prime candidate for
information transfer over space and time. Quex supports this type of
communication by the generation of interpreters of sequential data streams.

Sequential data streams are traditionally associated with a stream of letters.
In phonemic writing systems :cite:`CoulmanFlorian1989`, such as Latin, Arabic,
Hebrew, etc. letters correspond to graphemes representing sounds. The
letters of DNA are the four nucleotide bases A (adenine), C (cytosine), G
(guanine), and T (thymine) :cite:`pevsner2015bioinformatics`
:cite:`searls1992linguistics`.  Letters in digital transmission frames are
bytes or bits. In general terms, lexical analysis detects configurations of
letters and reports accordingly atomic meanings.  The subsequent section
shows an approach to interpret sequential data streams. 

State Machines
--------------

This section discusses state machines. An example may be considered in figure
:numref:`fig:state-machine-students-life`.  It displays the slightly idealized
daily life of a student. His states are 'study', 'eat', and 'sleep' as they are
shown as names framed by ellipses. The transitions between those states are
triggered by finite set of events, namely him becoming 'hungry', 'replete',
'tired', and an alarm clock that 'buzzes'.  The events are shown as annotations
to the arrows indicating state transitions.

.. _fig:state-machine-students-life:

.. figure:: ../figures/state-machine-students-life.png
   :scale: 60%
   :align: center
   
   Description of a student's life in terms of a state machine.


A state machine consists of a set of *states*, *state transition rules*, and
*actions* that are applied upon transitions :cite:`Arbib1972`.  A state in the
state machine can be either *active* or *inactive* indicating its ability to
react to incoming events. A state's transition behavior is specified in terms
of a transition map.

Transition Map:
   A state's transition map describes a state machines reaction when the state
   is active. It determines what event, of a closed set of events, causes what 
   subsequent state to become active.
   
A special state machine is the FSM, i.e. the finite state machine
:cite:`Roche1997`.  In a FSM there is only one state active at a time, called
the *current state*. This implies that there is no transition on the 'no event'
and the transition maps associate an event with a distinct successor state.
Quex generates FSMs [#f1]_. 

Finite state machines receive events at discrete times, i.e. sequentially.
Thus, *the activation of a state is the deterministic result of the sequence of
events that preceded*. As such, the activation of a state coincides with
the detection of a specific pattern in a sequential data stream. The letters of
a sequential data stream, further, constitute a closed set, namely the
'alphabet'.  Thus, letters may play the role of events in the FSM.  

Pattern-detecting state machines are called DFAs, so called *deterministic
finite automatons* :cite:`Hopcroft2006automata`. They distinguish states that
signal a match in the input stream  by labelling them as *acceptance states*.

.. _fig:state-machine-for-pattern-matching:

.. figure:: ../figures/state-machine-for-pattern-matching.png
   
   Pattern matching via DFA.

Figure :ref:`fig:state-machine-for-pattern-matching` shows a state machine
where a circle represents a state and the arrows possible state transitions. A
double circle indicates an acceptance state.  The depicted state machine can
detect the word 'fun'. Any aggregation of two or more lowercase letters is
identified as a 'WORD'.  A sequence of characters 'f', 'u', and 'n' guides from
the initial state to state 3. Any non-letter in that state would cause an else
transition, notifying that 'FUN' has been found.  A longer sequence such as
'fund' would be considered a 'WORD' because the transitions continue to state
4.  A sequence of less than two characters drops out either at state 0 or state
    1.  The 'else' path says that in that case a 'FAILURE' would be notified. 

There are two approaches of pattern matching:  *greedy/longest match* and
*shortest match*.  For greedy match, a lexer tries to 'eat' a maximum of
letters until it fails.  It walks along the state machine graph according to
the incoming letters, marks the acceptance of the last acceptance state that
it passed by, and eventually drops-out. Upon drop-out, it recalls the last
acceptance *indicating the longest possible match*. 

Contrary to that, with the approach of shortest match an analysis step
terminates upon hitting the first acceptance state. In this way, though, only a
subset of all possible pattern configurations can be matched.  Whenever a
pattern matches a superset of another, the approach fails in favor of the
shorter pattern. For example, if 'for' and 'forest' were keywords to be detected,
the analyzer would always stop at 'for' and never recognize a 'forest'. It
follows that the shortest match approach is not suited for a general solution.
The previously mentioned greedy match approach does. Greedy match is what Quex
implements.


.. rubric:: Footnotes

.. [#f1] Indeed, Quex first produces a so called NFA that combines all
         concurrent pattern matches in one single state machine. Then, 
         it applies powerset construction :cite:`Rabin:1959:FAD` to generate 
         a state machine where only one state is active at a time.

.. [#f2] The computer science expression 'lexeme' corresponds to a 'form of
         a lexeme' in linguistics.

.. [#f3] The popularity of the phrase 'A picture is worth a thousand words' 
         :cite:`TessFlanders1911` documents the human's comfort conveying 
         information in pictures.

.. [#f4] The buttons in graphical user interfaces are a good example. At the
         time of this writing, the 'save' button is often symbolized by a 
         storage diskette. The generation of our kids might not be able to
         associate this symbol with any meaning, simply because diskettes
         are no longer in use at all.

.. [#f5] Since the Unicode standard does not assign characters beyond 
         0x10ffff, in real life, the maximum amount of bytes in UTF8 is four.
