.. _sec-token-repetition:

Token Repetition
================

There are cases where a single step in the lexical analysis produces
multiple lexical tokens with the same token identifier. A classical
example is the 'block-close' token that appears in indentation based
languages, such as Python. Consider, for example the following python
code fragment:
 
.. code-block:: python

     for i in range(10):
         if i in my_list:
             print "found"
     print "<end>"

When the lexical analyzer passes ``"found"`` and transits to the 
last ``print`` statement, it needs to close *three* indentation levels.
Thus, three 'block-close' tokens need to be sent as result of one
single analysis step. 

The obvious solution is to have a field inside the token that tells how often
it is to be repeated. Indeed, this is what the token send macro
``self_send_n()`` does. For it to function, the policy of how to set and
get the repetition number must be defined inside the token class 
(see ``repetition_set`` and ``repetition_get`` in :ref:`sec-token-class`).

Tokens that should carry the potential to be sent repeatedly must be
mentioned in a ``repeated_token`` section inside the quex input sources, 
e.g.

.. code-block:: cpp

      repeated_token {
          ABC;
          XYZ;
          CLOSE;
      }


where ``QUEX_TKN_XYZ`` is the token identifier that can be repeated. Now, the
generated engine supports token repetition for the above three token ids.  This
means that ``self_send_n()`` can be used for them and the token receive
functions consider their possible repetition. That means that if, for example, 

.. code-block:: cpp

     self_send_n(5, QUEX_TKN_XYZ);

is called from inside the analyzer, then

.. code-block:: cpp
 
     token_id = my_lexer.receive();

will return five times the token identifier ``QUEX_TKN_XYZ`` before it does the
next analysis step. Note, implicit token repetition may have a minor impact on
performance since for each analysis step an extra comparison is necessary. In
practical, though, the reduction of function calls for repetition largely
outweighs this impact.

