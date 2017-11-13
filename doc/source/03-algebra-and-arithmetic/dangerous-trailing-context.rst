The Dangerous Trailing Context
==============================

There are situations where the setup of a post context is dysfunctional. The so
called 'dangerous trailing context' (DTC) where traditional lexers fail is presented
as deficiency as in the following quotes.

.. epigraph::

    There are patterns where the ending of the first pattern matches the 
    beginning of the second, such as ``zx*/x*y`` ...

    -- Flex manual :cite:`Paxson1995flex`:

.. epigraphs::

   ... if the trailing portion of r matches the beginning of x, the result is
   unspecified ...
  
   -- POSIX Standard :cite:`OpenGroup2016`. 

These statements are *unprecise* and *insufficient*.  They are *unprecise*,
because it is unclear what 'matching' shall mean in that context.  The
condition is *insufficient*, as the examples ``xx/x`` and ``x/x+`` meet the
condition but are of no issue for post-context implementation.  The same holds
for ``x/x+``.  On the other hand, an expression such as ``[a-c]+/(ab|c)``
inhabits a DTC, even if it is difficult to interprete the citations in a way to
that they relate to the setup.  Due to the lack of formal precise definitions,
the DTC remains mysterious.  As a deficiency which is imprecisely defined, the
DTC puts lexical analyzer generators in general at doubt!

With the newly introduced operators, though, an analysis is possible which
leads to precise constraints and pinpoints to a rational healing procedure.
First, let us understand what is going on with the DTC.  A functional
post-contexted pattern ``R/P`` behaves as follows:

    # It signalizes a *match* if and only if the concatenation of ``RP``
      matches the current input stream.

    # It *resets the input stream* such as that the end of the matched 
      lexeme matches ``P``.

There is no reason to doubt the first characteristic, since it is built upon
concatenation which is an well established procedure.  On the other hand, the
second required functionality can be doubted.  The general post-context
approach implies that the input position is stored upon acceptance of the core
pattern. Figure :ref:`fig:nice-post-context` shows the example of a lexeme
matching the expression ``ab/cd``. When state '3' is reached at time 't3' the
input position is stored. Finally, when state '5' is reached and the
concatenation of ``ab`` and ``cd`` matched, the input position is restored so
that the next analysis step may start at where 't3' ended. The next character
to be considered is `c`.

.. image:: fig:nice-post-context

The post-context procedure works fine as long as the concatenation procedure
combines acceptance states of the core pattern with the init state of the
post-context. But this is not always guaranteed. In section
:ref:`sec-concatenation-optionality-repetition` the effect of postponed
concatenated optionality has been discussed. If a core pattern ``xx?`` and a
post-context ``xxx`` are concatenated the optionality is pulled at the end,
i.e.::

          (xx?)(xx) ---> xxx(x?)

This is shown in figure :ref:`dtc-post-poned-repetition`. As can be seen, the
acceptance state of the core pattern is webbed into multiple states. The post
context requires that at least two `x` follow the core pattern. Therefore, the
correct input position would be right before the last two `x`. However, there
is state which would allow to store the input position.  The minimum length
lexeme is `xxx`. Thus storing at state 0 would fail, since then three of the
matching `x` would remain. Storing at state 1 would work for that case.
However, for the lexeme `xxxx`, again it fails. Then, again three `xxx` would
remain. Consequently, there is no state where the input position can be 
stored to work with one lexeme without conflicting with the needs of 
another lexeme.

.. image:: dtc-post-poned-repetition

          x         x         x           x
   ( 0 )---->( 1 )---->( 2 )---->(( 3 ))---->(( 4 ))
                 
The example of ``(xx?)/(xx)`` cannot be solved by input position store and
restore states. 

Concatenating two DFAs means to cancel the acceptance of the core acceptance
states, and to connect them via epsilon transition to the init state of the
post context.  An epsilon transition is a transition on no lexatom, such that
the result becomes an NFA. The required transformation from NFA to DFA, now,
has some problematic implications. If a state *A* reaches *B* via epsilon
transition, then their transition maps are considered together.  Any transition
on which the combined states trigger on a common lexatom issues the combined
consideration of the according target states. A sequence of such combined
consideration can be viewed as 'walking together' of core and post-context.
Through this walking together, an optionality (or particularly a loop) is
post-poned after a sequence of iterated lexatoms in the core pattern until
something different appears in the post context. As a result the exact cut
between core and post context cannot be found in the concatenated pattern. 

Figure :ref:`fig:dtc-walk-together` shows the three cases of walking together.
In figure :ref:`fig:dtc-walk-together` a) core and post-context walk together, but
the core pattern hits an acceptance state at a point when the core pattern
hits its init state. Such is not a problem, because the post-context simply
starts freshly with an acceptance state of the core pattern-as it should.

In figure :ref:`fig:dtc-walk-together` b) the post-context and the core 
pattern deviate before the core pattern hits an acceptance state. This is 
also not a problem. If the state machine moves along the post-context's path
it can relate to the correct init state. If the state machine moves
towards the core's acceptance state, it meets there again the init state
of the post-context-as it should.

A real problem arises in :ref:`fig:dtc-walk-together` c). There the core's
acceptance state is reached during the walk-together. At this point, the init
state has to be mounted again and another potential store-input position is
required. This however, is an ambiguous situation with respect to the first
input storage situation. With the given findings, the dangerous trailing 
context can now be defined.

Dangerous Trailing Context (DTC)
   Let ``P`` denote a core pattern and ``Q`` denote a desired 
   post-context.  Then, a dangerous trailing context exists, if and only if::

     \exists B\,\in\,\Succ{P},\,with\, \Begin{Q B} != \Empty

   where 
     
     \Intersection{\LeaveBegin{Q B} \Loops{Q}} != \Empty

Post-contexts can basically be implemented by two means:

  .# Storing the input position at specific states and restoring it
     upon the acceptance of the concatenated pattern.

  .# Back-tracking, i.e. going backwards the revered post-context after
     the concatenated pattern matched until the beginning of the post
     context.

The first means is definitely impossible for cases of DTC.

However, there is the possibility of back tracking where one
searches for the beginning of the post-context by walking backwards. This
solution is discussed later. Before, the nature of the DTC needs to be
explored. As a consequence pattern will be identified where even back-tracking
does not solve the problem and the pattern combination requires adaption.

In other words, if there is some pattern `B` that spans a branch from
acceptance state to another acceptance state of `P`, which matches along the
beginning of `Q`, and if the path that matches in `Q` is not a loop at the
beginning of `Q`, then there is a DTC.

As discussed earlier, the *matching* behavior of a post-contexted pattern is
always guaranteed. However, the input stream cannot be reset properly in case
of the DTC. This can potentially be healed by tracing
the matched lexeme backwards along the reverse of the post-context. This works
properly in case of ``x+/x``, since obviously the match of the concatenation
appeared one position after the core context. However, tracing backwards
is equally sensible to the DTC. If the reverse 
post-context 'eats' into the reverse core pattern, it becomes unclear where
to stop.

Reverse Dangerous Trailing Context
   Let ``P`` denote a core pattern and ``Q`` denote a desired 
   post-context.  Then a reverse dangerous trailing context exists, if 
   and only if::

     \exists B\,\in\,\Succ{\R{P}},\,with\, \Begin{\R{Q} B} != \Empty

The reverse dangerous context makes it impossible to find the input position
via back-tracing.  This dilemma, however,  can be solved by philosophy, namely
the paradigm of *longest match*.  Consuming the maximum amount of the input
stream means that the position of the input stream needs to be set as far as
possible. Translated in the context of post-contexts, the core pattern shall
match as much as possible while the post-context may be pruned. However, care
has to be taken in order to maintain consistency.


%% ---- OLD -----

With the introduced cut/concatenate arithmetic precise conditions can be
defined.  Further, a distinct solution can be derived which complies with the
paradigm of longest match. The dangerous trailing context exists in the
patterns _[#f0]::

        x+/x+
        yx+/x+y
        (abc)+/(abc)+
        [abc]+/(ab|c)
        x[ab]?/(ab|b)
        yx?/x?y
        (abc)+/(abc)?d
        u(y|x*)/x*z
        u(yx|x+)/x+z

While the mentioned holds, a dangerous trailing context does not appear in 
the following expressions::

        x+y/x+y
        yx+/yx+
        yx?/x
        (abc)+/(abc)
        (abc)/(abc)?d

In order to understand the nature of the dangerous trailing context, it is
necessary to reflect on the functioning of post-contexts. A post-context is
mounted to a core pattern by concatenation, i.e. its graph is mounted on the
core-patterns acceptance states. This is shown in figure
:ref:`fig:post-context-principle`.  An acceptance states of the core pattern
stores the input position when it is reached (indicated by the 'S' mark). When
an acceptance state of the post-context is reached, a match is triggered and
the input position must be reset to what has been stored in the core-pattern's
acceptance state (indicated by the 'R' mark).

This concept fails, though, in some situations. In section
:ref:`sec-concatenation-specials` the effect of post-poned concatenated
optionality has been discussed. Applied to the concatenation of core pattern
with an optionality and a similar post-context, this means, that the
optionality is post-poned and the transition from core pattern to post context
can no longer be associated with a particular state. This situation is
shown in figure :ref:`fig-ppco-dtc`.

Iteration:

            x                                 x
     ( 1 )---->(( 2 ))---.             ( 3 )----->(( 4 ))
                  '---<--' x

     => Condition for *dangerous tc*

         Exists a B in branches(P) where \Begin{Q B} is not empty

                         x
                  ( 1 )---->(( 2, 3, 4 ))------. x
                                  '--------<---'

     => No way to store where first pattern ends.
     => HEALING: backward detection.
                              x
                      ( 4i )----->(( 3i ))

        when an acceptance state is reached, new input position is there.

This situation can be healed, though, under certain circumstances. If the post
context can be walked along without ambiguity, then a walk-back delivers the
end of the core-pattern. If this is not possible, the reversed post-context
must be pruned. Fortunately, this is possible with the philosophy of longest
match. 

    A gg\R{P}

Backward detection must be in consistency with longest match.j


Figure :ref:`post-context-principle-in-action` shows an example how it works on
an input stream with the given automaton. After the "ab" in the input stream
has been passed, the input position is stored. However, a match is not yet
triggered, because the post context requires that it is followed by "c". When
the "c" has been consumed, now a match is triggered, but the input position is
reset to the place after "ab". However, there are cases where the approach with
*store* and *restore* states fails.


The problem of the dangerous trailing context stems from the fact that the
position of the input stream cannot be reset to a distinct position, because it
is unclear what element of the lexeme belongs to the core pattern and what
relates to the post context. This however, is exactly the same problem that
makes it impossible to reverse the concatenation.

Dangerous Trailing Context
   The *dangerous trailing context* occurs at the concatenation of a core
   pattern ``A`` with a post context ``B`` as ``A/B`` where::

     it exists a T in \Branches{A} where \Begin{Q T} != \Empty

   If a dangerous trailing context exists, then the plain concatenation of core
   and post-context result in a dysfunctional lexical analyzer.

On the first glance, such a situation seems like a dilemma for the lexer
generator. On one hand, leaving the user specified pattern untouched makes
it impossible to generate a functional lexer. On the other hand, modifying
the user's pattern might cause unexpected behavior. However, the dilemma
can be solved once the considered in the light of paradigm under which Quex
produces lexers: the *longest match*.

Longest match lexical analysis means that the lexer tries to consume as much of
the input stream as possible. In a post-context the input stream pointer must
be reset to the end of the core pattern, as soon as the post context has been
detected. In case of the dangerous trailing context, it is primarily undecided
where the core pattern's match ends and where the post-context's match begins.
The longest match paradigm, though, gives the preference to the core pattern.
The core pattern shall match as long as possible, i.e. pushing the post-context
as far as possible behind. Only then, the maximum amount of progress in the
input stream is achieved. 

Now, if one removes the beginning part of the post-context which matches a in
the core pattern, then where would be no dangerous trailing context and the
input stream would give preference to the match by the core pattern. Without
introducing new implicit rules, a modification of the DFA can be made which
does not risk to surprise the user.

Solution for Dangerous Trailing Context
   In case of the dangerous trailing context a function, the *longest match
   paradigm* permits a modification of the post-context such that the 
   resulting expression does not contain a trailing context.

        B is transformed in ``\CutBegin{B T}`` for all T in ``\Branches``.

   Let this operation be called the 'philosophical cut'.

Quex issues a note in that case, while the produced analyser is functional and
its behavior must be considered to be expectable.

.. rubric:: footnotes

    [#f1]_ Notably, at time of this writing (2017) the current version of flex (V
    2.6.1) does not complain about the last two cases of dangerous trailing
    contexts. Since the length of the post context is known upfront, the 
    distance to set back the input position can be determined upfront.

    [#f0]_ In this given case, there is a trivial solution: Knowing that three
    repetitions of ``x`` must appear in the post context, the input stream can
    be set three lexatoms backward upon match. For the general case of
    postponed optionality, there is no such remedy.

