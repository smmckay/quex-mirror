.. _sec:re-character-sets:

Character Set Expressions
==========================

Character set expressions are a tool to combine, filter and or select character
ranges conveniently. The character set expression ``[:alpha:]``, for example
matches all characters that are letters, i.e.  anything integer that corresponds
to the ASCII/Unicode values from from `a` (0x61) to `z` (0x7a) and `A` (0x41)
to `Z` (0x5A). It is part of the POSIX bracket expressions :ref:`Burns2001real` which
are listed below.  Further, this section explains how sets can be generated
from other sets via the operations *union*, *intersection*, *difference*, and
*complement*.

POSIX bracket expressions are basically shortcuts for some more regular
expressions that would look a bit more cumbersome if specified explicitly by
code points and ranges. The expressions and what they stand for are shown in
table :ref:`table:bracket-expressions`.

.. _table:bracket-expressions:

.. table::

    ==============  =================================  =====================================
    Expression      Meaning                            Related Regular Expression
    ==============  =================================  =====================================
    ``[:alnum:]``    Alphanumeric characters           ``[A-Za-z0-9]``                          
    ``[:alpha:]``    Alphabetic characters             ``[A-Za-z]``                             
    ``[:blank:]``    Space and tab                     ``[ \t]``                                
    ``[:cntrl:]``    Control characters                ``[\x00-\x1F\x7F]``                      
    ``[:digit:]``    Digits                            ``[0-9]``                                
    ``[:graph:]``    Visible characters                ``[\x21-\x7E]``                          
    ``[:lower:]``    Lowercase letters                 ``[a-z]``                                
    ``[:print:]``    Visible characters and spaces     ``[\x20-\x7E]``                          
    ``[:punct:]``    Punctuation characters            ``[!"#$%&'()*+,-./:;?@[\\\]_`{|}~]`` 
    ``[:space:]``    White space characters            ``[ \t\r\n\v\f]``                        
    ``[:upper:]``    Uppercase letters                 ``[A-Z]``                                
    ``[:xdigit:]``   Hexadecimal digits                ``[A-Fa-f0-9]``                          
    ==============  =================================  =====================================

Caution has to be taken if these expressions are used for non-English character
encodings. They are *solely* concerned with the ASCII character set. For more
sophisticated property processing the Unicode property expressions should be
considered as explained in section :ref:`sec:ucs-properties`. In particular, it
is advisable to use ``\P{ID_Start}``, ``\P{ID_Continue}``, ``\P{Hex_Digit}``,
``\P{White_Space}``, and ``\G{Nd}``.

Character sets can be defined and expanded in ``define`` sections the same way
as regular expressions. Character set operations may then be applied to complex
hierarchical set descriptions. The available operations correspond to those of
*algebra of sets* :cite:`Quine1969set` and are listed in table
:ref:`table:character-set-operations`. Notably, the algebraic operations on
*character sets* are not to be confused with the *DFA algebra* to be discussed
later.

.. _table:character-set-operations:

.. table::

    ===============================  =====================================================
    Syntax                           Example
    ===============================  =====================================================
    ``union(A0, A1, ...)``            ``union([a-z], [A-Z]) = [a-zA-Z]``
    ``intersection(A0, A1, ...)``     ``intersection([0-9], [4-5]) = [4-5]`` 
    ``complement(A0, A1, ...)``       ``complement([\x40-\5A]) = [\x00-\x3F\x5B-\U12FFFF]`` 
    ``difference(A, B0, B1, ...)``    ``difference([0-9], [4-5]) = [0-36-9]``
    ===============================  =====================================================

A ``union`` expression generates the union of all sets mentioned inside the
brackets.  An ``intersection`` expression results in the intersection of all
sets mentioned. The ``complement`` builds the complementary set of the union of
all mentioned sets. That is, the result is a set of characters which do not
occur in any the given set.  The difference between one set and another can be
computed via the ``difference`` function. Contrary to the ``union`` and
``intersection`` expressions, the arguments to ``difference`` may not be listed
arbitrarily-- ``difference(A, B)`` is not equal to ``difference(B, A)``.  The
``difference`` determines the difference between the first mentioned set and
all following arguments.  

At first glance, it seems unnatural to allow list of arbitrary size as
arguments to ``complement`` and ``difference``. This choice, though, has been
made for the sake of convenience, to spare the user a ``union`` expression,
in case that multiple sets are concerned.

.. note::

    The ``difference`` and ``intersection`` operation can be used conveniently
    for filtering. For example

    .. code-block:: cpp

      [: difference(\P{Script=Greek}, \G{Nd}, \G{Lowercase_Letter} :]

    results in the set of Greek characters except the digits and except the
    lowercase letters. To allow only the numbers from the Arabic code block
    ``intersection`` can be used as follows:

    .. code-block:: cpp

      [: intersection(\P{Block=Arabic}, \G{Nd}) :]

The result of character set expressions is not always easy to foresee. Using
Quex's command line functionality to display the results of regular expressions
may provide more insight into the result of an operation. For example, the
following command line displays what characters remain if the numbers and
lowercase letters are taken out of the set of Greek letters.

.. code-block:: bash

   > quex --set-by-expression 'difference(\P{Script=Greek}, \G{Nd}, \G{Lowercase_Letter})'

The command line query feature is discussed in chapter
:ref:`sec:command-line-queries`.  The subsequent section elaborates on the
concept of Unicode properties and how they may be used to produce character
sets.


