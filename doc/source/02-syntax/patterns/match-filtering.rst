Match Filtering
###############

In this section, it is shown how operations from DFA algebra may be used to
produce DFAs that match a specific subset of lexemes. Given a DFA ``P`` which
matches a certain set of lexemes, a new resulting DFA is constructed that
matches only those lexeme which match a second DFA ``Q`` in some manner.
It is possible to 'extract' those lexemes which match or match not a second
DFA ``Q`` at the beginning, somwhere inside, or at the end. Namely, those
lexemes are

.. describe:: ``\NotBegin{P Q}``: 

      All lexemes that match `P`, except for those that *begin* with something
      that matches `Q`.  The corresponding regular expression is::

          \Diff{P (\Universal)Q}  

.. describe:: ``\NotEnd{P Q}`` 

      All lexemes that match `P`, except for those that *end* with something
      that matches `Q`.  The corresponding regular expression is::

          \Diff{P (\Universal)Q}  

.. describe:: ``\NotIn{P Q}`` 

      All lexemes that match `P`, except for those that *contain* a subsequence 
      that matches `Q`.  The corresponding regular expression is::

          \Diff{P (\Universal)Q(\Universal)}  


The positive cases are:

.. describe:: ``\Begin{P Q}``: 

      Only those lexemes that match `P` which *begin* with something
      that matches `Q`.  The corresponding regular expression is::

          \Intersection{P (\Universal)Q}  

.. describe:: ``\End{P Q}`` 

      Only those lexemes that match `P` which *end* with something
      that matches `Q`.  The corresponding regular expression is::

          \Intersection{P (\Universal)Q}  

.. describe:: ``\In{P Q}`` 

      Only lexemes that match `P` which *contain* a subsequence 
      that matches `Q`.  The corresponding regular expression is::

          \Intersection{P (\Universal)Q(\Universal)}  

In the last section the derived operations ``\Begin``, ``\In``, ``\End``, 
``\NotBegin``, ``\NotIn``, and ``\NotEnd`` were introduced that prune the
set of matching lexemes based another 'pruning pattern'. The next section
introduces operations that cut the lexemes of the set of matching lexemes
itself.
