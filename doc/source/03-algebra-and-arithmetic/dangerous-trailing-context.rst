Context Considerations
======================

There is a special situation where DFA lexers fail to implement a functional
representation of post-contexts. The so called 'dangerous trailing context'
where traditional lexers fail is presented as deficiency as in 

.. epigraph::

    There are patterns where the ending of the first pattern matches the 
    beginning of the second, such as ``zx*/x*y`` ...

    -- Flex manual :cite:`Paxson1995flex`:

.. epigraphs::

   ... if the trailing portion of r matches the beginning of x, the result is
   unspecified ...
  
   -- POSIX Standard :cite:`OpenGroup2016`. 

The condition is *unprecise*, *insufficient*, and therefore *not universally
valid*.  It is *unprecise*, because it is unclear what 'matching' shall means
in that context.  The condition is *insufficient*. For example, the expression
``xx/x`` is composed out of a first statement with an ending that matches the
beginning of the second, but pose no problem to DFA based lexical analysis. The
same holds for ``xx*/x`` or ``x/x*``.  On the other hand, the expression
``[a-c]+/(ab|c)`` poses a problem of dangerous trailing context, even if it
is difficult to link it to the aforementioned condition. Due to the lack of
precision and formal language, a detection of a dangerous trailing context must
hit a user with surprise, a touch of mystery, and cluelessness of a corrective
action.

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
does not risk to supprise the user.

Solution for Dangerous Trailing Context
   In case of the dangerous trailing context a function, the *longest match
   paradigm* permits a modification of the post-context such that the 
   resulting expression does not contain a trailing context.

        B is transformed in ``\CutBegin{B T}`` for all T in ``\Branches``.

   Let this operation be called the 'philosophical cut'.

Quex issues a note in that case, while the produced analyser is functional and
its behavior must be considered to be expectable.

.. rubric:: footnotes

    Notably, at time of this writing (2017) the current version of flex (V
    2.6.1) does not complain about the last two cases of dangerous trailing
    contexts. Since the length of the post context is known upfront, the 
    distance to set back the input position can be determined upfront.

