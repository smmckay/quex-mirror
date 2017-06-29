.. _sec:re-context-free:

Context Free Regular Expressions
==================================

Context free regular expressions match  against an input independent on what
comes before or after it.  Pre- and post-contexts for pattern matching are
explained in the subsequent section. All input files must be UTF8 encoded. The
syntax of context-free regular expressions in many aspects identical to that of
the popular tool 'lex' :cite:`Lesk1975lex`.

.. describe:: x 

     matches the character 'x'.  Characters match simply the character that
     they represent.  This is true, as long as those characters are not part of
     the set of syntactic operators--such as ``.``, ``[``, and  ``]``.

.. describe:: . 

     The dot is a syntactic operator. It matches any character in the current
     encoding except for the buffer limit code and '0x0A' for newline.  On
     systems where newline is coded as '0x0D, 0x0A' this does match the '0x0D'
     character whenever a newline occurs.

.. describe:: \\Any

     Matches absolutely any character.

.. describe:: [xyz]

     a 'character class' or 'character set'; in this case, the pattern matches
     either an ``x``, a ``y``, or a ``z``.  Character sets specify an
     *alternative* expression for a single character.  If the brackets ``[``
     and ``]`` are to be matched quotes or backslashes have to be used.

.. describe:: [:expression:]

     matches a set of characters that result from a character set expression
     `expression`. Section :ref:`sec:re-character-sets` discusses this feature
     in detail.  In particular ``[:alnum:]``, ``[:alpha:]`` and the like are
     the character sets as defined as POSIX bracket expressions.

.. describe:: [abj-oZ]

     a "character class" with a range in it; matches an ``a``, a ``b``, any
     letter from ``j`` through ``o``, and a ``Z``. The minus ``-`` is used to
     specify a range. The character to its left is the first character in the
     range.  The character to its right part is the last character of the range
     (``j-o`` is equivalent to ``jklmno``). Precisely, for all characters in
     the range it holds that their code point in Unicode is greater or equal
     to that of the left character and lesser or equal to that of the right
     character.

.. describe:: [^A-Z\\n]

     a "negated character class", i.e., any character but those in the class.
     The ``^`` character indicates *negation* at this point.  This expression
     matches any character *except* an uppercase letter or newline.

.. describe:: "[xyz]\\"foo"

     matches the literal string: ``[xyz]"foo``.  Any character, that is not
     backslash or backslash proceeded is applied in its original sense. A ``[``
     stands for code point 91 (hex.  5B), matches against a ``[`` and does not
     mean 'open character set'. Inside strings ANSI-C backslash-ed characters
     ``\n``, ``\t``, etc. can be used. The quote can be specified by ``\"``.
     The Unicode property ``\N{...}`` is also available since it results in a
     *single character*. However, other operators such as ``\P{....}`` result
     in *character sets*. They cannot be used inside strings.
      
.. describe:: \\C{ R } or \\C(flags){ R }

     Applies case folding for the given regular expression or character set 'R'.
     This basically provides a shorthand for writing regular expressions that
     need to map upper and lower case patterns, i.e.::

           \C{select} 

     matches for example:: 

           "SELECT", "select", "sElEcT", ...

     The expression ``R`` passed to the case folding operation needs to fit 
     the environment in which it was called. If the case folding is applied
     in a character set expression, then its content must be a character
     set expression, i.e.::

               [:\C{[:union([a-z], [ﬀİ]):]}:]   // correct
               [:\C{[a-z]}:]                    // correct

     but *not*::

               [:\C{union([a-z], [ﬀİ])}:]       // wrong
               [:\C{a-z}:]                      // wrong

     The algorithm for case folding follows Unicode Standard Annex #21 "CASE
     MAPPINGS", Section 1.3 :cite:`Unicode2015`. That is for example, the
     character 'k' is not only folded to 'k' (0x6B) and 'K' (0x4B) but also to
     'K' (0x212A).  Additionally, Unicode defines case foldings to multi
     character sequences, such as::

            ΐ   (0390) --> ι(03B9)̈(0308)́(0301)
            ŉ   (0149) --> ʼ(02BC)n(006E)
            I   (0049) --> i(0069), İ(0130), ı(0131), i(0069)̇(0307)
            ﬀ   (FB00) --> f(0066)f(0066)
            ﬃ   (FB03) --> f(0066)f(0066)i(0069)
            ﬗ   (FB17) --> մ(0574)խ(056D)

     .. note::

        Some case mappings may be supprising and trigger unexpected
        notifications. For example the case mapping for '\C{s}' consists not
        only of the letters 's' (0x53) and 'S' (0x73) but also of 'ſ' (0x17F).
        So if '\C{s}' is used in a single-byte buffer setup, Quex will 
        warn about the pattern containing elements that are incompatible with
        the buffer specification.

     As a speciality of the Turkish language, the 'i' with and without the dot
     are not the same. That is, a dot-less lowercase 'i' is folded to a dot-less 
     uppercase 'I' and a dotted 'i' is mapped to a dotted uppercase 'İ'. This 
     mapping, though, is mutually exclusive with the 'normal' case folding and 
     is not active by default. The following flags can be set in order to
     control the detailed case folding behavior:

     .. describe:: s

        The *s* flag enables simple case folding disabling the generation 
        of multi-character sequences.

     .. describe:: m

        The *m* flag enables the case folding to multi-character sequences.
        This flag is not available in character set expressions. In this
        case the result must be a set of characters and not a set of character
        sequences.

     .. describe:: t

        By setting the *t* flag, the turkish case mapping is enabled. Whenever
        the turkish case folding is an alternative, it is preferred.
    
     The default behavior corresponds to the flags *s* and *m* (i.e. ``\C{R}``
     ≡ ``\C(sm){R}``) for patterns and *s* (i.e. ``\C{R}`` ≡ ``\C(s){R}``) for
     character sets. Characters that are beyond the scope of the current
     encoding or input character byte width are cut out. 

.. describe:: \\R{ ... }

     Reverses the pattern specified in brackets. If for example, it is
     specified::

            \R{dlroW} => QUEX_TKN_WORD(Lexeme)

     then the token ``WORLD`` would be sent upon the appearance of 'World' in
     the input stream. This feature is mainly useful for definitions of
     patterns of right-to-left writing systems such as Arabic, Binti and
     Hebrew. Chinese, Japanese, as well as ancient Greek, ancient Latin,
     Egyptian, and Etruscan can be written in both directions.


.. describe:: \\0 

     a NULL character (ASCII/Unicode code point 0). This is to be used with
     *extreme caution*!  The NULL character is also used a buffer delimiter!
     See section :ref:`sec:formal-command-line-options` for specifying a different
     value for the buffer limit code.

.. describe:: \\U11A0FF 

     the character with hexadecimal value 11A0FF. A maximum of *six*
     hexadecimal digits can be specified.  Hexadecimal numbers with less than
     six digits must either be followed by a non-hex-digit, a delimiter such as
     ``"``, ``[``, or ``(``, or specified with leading zeroes (i.e. use
     \\U00071F, for hexadecimal 71F). The latter choice is probably the best
     candidate for an 'established habit'. Hexadecimal may can contain be
     uppercase or lowercase letters from A to F.

.. describe:: \\X7A27 

     the character with hexadecimal value 7A27. A maximum of *four* hexadecimal
     digits can be specified. The delimiting rules are are analogous to the
     rules for `\U`. 

.. describe:: \\x27 

    the character with hexadecimal value 27. A maximum of *two* hexadecimal
    digits can be specified. The delimiting rules are are analogous to the
    rules for `\U`. 

.. describe:: \\123 

    the character with octal value 123, a maximum of three digits less than 8
    can follow the backslash. The delimiting rules are analogous to the rules
    for `\U`. 


.. describe:: \\a, \\b, \\f, \\n, \\r, \\t, \\r, or \\v

    the ANSI-C interpretation of the backslash-ed character.

.. describe:: \\P{ Unicode Property Expression }

     the set of characters for which the `Unicode Property Expression` holds.
     Note, that these expressions cannot be used inside quoted strings.

.. describe:: \\N{ UNICODE CHARACTER NAME }

     the code of the character with the given Unicode character name. This is 
     a shortcut for ``\P{Name=UNICODE CHARACTER NAME}``. For possible
     settings of this character see :cite:`Unicode2015`.

.. describe:: \\G{ X }

     the code of the character with the given *General Category*. This is 
     a shortcut for ``\P{General_Category=X}``. Note, that these expressions 
     cannot be used inside quoted strings. For possible settings of the 
     ``General_Category`` property, see section :ref:`sec-formal-unicode-properties`.

.. describe:: \\E{ Codec Name }

     the subset of Unicode characters which is covered by the given encoding.
     Using this is particularly helpful to cut out uncovered characters when a
     encoding engine is used (see :ref:`sec:engine-encoding`).

 .. note:: 

    The brackets for pattern substituion and the brackets required for framing
    a command are not the same--both need to be specified. E.g.  to reverse
    what has been defined as ``PATTERN`` it needs to to be written::

                      \R{{PATTERN}} 

    which reads from inside to outside: expand the pattern definition,
    then reverse expanded pattern. 

Any character specified as character code, i.e. using `\`, `\x`, `\X`, or `\U`
are considered to be Unicode code points. For applications in English spoken
cultures this is identical to the ASCII encoding. For details about Unicode
code tables consider the standard :ref:`Unicode50`. Section
:ref:`sec:ucs-properties` gives an overview over the Unicode property system.

Two special expressions are due to the tradition of lex/flex. In Quex's
terminology they are actually event handlers. They are still present in the
form of patterns in recognition of history and can only be used in the ``mode``
section:

.. describe:: <<EOF>> 

    the incidence of an end-of-file (end of data-stream) it is a synonym for
    the incidence handler ``on_end_of_stream``. 

.. describe:: <<FAIL>> 

    the incidence of failure, i.e. no single pattern matched. It is a synonym
    for ``on_failure``.

The incidence handlers ``on_end_of_stream`` and ``on_failure`` are explained in
section :ref:`sec:incidence-handlers`.

.. note::

   The space character (UCS 32) is not allowed except in quotes or in range
   boundaries. In fact, it is supposed to separate the pattern from subsequent
   tokens such as ``=>``. Also, it cannot be backslash-ed.
   
   The backslash also does not suppress newline. A pattern must be completely
   specified in a single line. The ``define`` section may be used to break
   down patterns into smaller ones and combine them by expansion.

*Operations*    

Let ``R`` and ``S`` be regular expressions, i.e. a chain of characters
specified in the way mentioned above, or a regular expression as a result from
the operations below.  Much of the syntax is directly based on POSIX extended
regular expressions.
     
.. describe:: R* 

    *zero* or more occurrences of the regular expression ``R``.

.. describe:: R+ 

    *one* or more repetition of the regular expression ``R``.

.. describe:: R? 

    *zero* or *one* ``R``. That means, there maybe an ``R`` or not.

.. describe:: R{2,5} 

    anywhere from two to five repetitions of the regular expressions ``R``.

.. describe:: R{2,} 

    two or more repetitions of the regular expression ``R``.

.. describe:: R{4} 

    exactly four repetitions of the regular expression ``R``.

.. describe:: (R) 

    match an ``R``; parentheses are used to *group* operations, i.e. to
    override precedence, in the same way as the brackets in ``(a + b) * c``
    override the precedence of multiplication over addition in algebraic
    expressions.

.. describe:: RS 

    the regular expression ``R`` followed by the regular expression ``S``. This
    is usually called a *concatenation* or a *sequence*.

.. describe:: R|S 

    either an ``R`` or an ``S``, i.e. ``R`` and ``S`` both match. This is usually 
    called an *alternative*.

.. describe:: {NAME} 

    the expansion of the defined pattern "NAME". Pattern names can
    be defined in *define* sections (see section :ref:`sec:top-level-configuration`).


*Sanity*

This section presented a short summary on regular expression syntax. While
the following sections go into more detail, they also provide more powerful
means to model the matching behavior. However, with these operations it
becomes more challenging to define the exact desired regular expression.
In particular, patterns may be *admissible* and *inadmissible*.

An *inadmissible* pattern has one ore more of the following properties.

    * It matches an empty sequence. This would make the lexer accept on no
      input. The lexer would not proceed and stall on accepting nothing.

    * It does not match anything. A pattern that never matches cannot 
      be related to a reaction.

Any pattern which is not *inadmissible* in the above sense is *admissible*.
Whenever an inadmissible pattern is detected, an error is reported. Any pattern
that is not inadmissible is admissible. However, even for admissible patterns
there remains an issue with *sanity*. If a pattern contains a state that
iterates on any lexatom to itself, then this state would eat anything until the
end of input. As a shorthand to transform any pattern into a *sane* pattern the
following command may be used.

.. describe:: \\Sanitize{P}

     Sanitizes a pattern with regards to two issues. First, it removes
     acceptance of the zero-length lexeme. Second, it removes acceptance of
     tails of infinite length and arbirtrary lexatoms. Such patterns may indeed
     be produced by DFA algrebraic expressions--so this command helps to
     sanitize.

 The command line option ``--language dot`` allows to print state machine
 graphs. It is advisable to print graphs for the sanitized state machine
 in order to see whether it conforms the expectations.

 Notably, this command cannot sanitize patterns that do not accept anything
 or accept everything as discussed in the frame of DFA algebra.


