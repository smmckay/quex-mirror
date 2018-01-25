Incidence Handlers
==================

Several incidences [#f1]_ may occur during lexical analysis. The user may
react to those incidences with hand written code in so called 'incidence
handlers'. They are specified inside a mode definition and follow the
example of ``on_some_incidence`` shown below in the mode 'EXAMPLE'.::

    mode EXAMPLE {
        on_some_incidence {
            /* user code */
        }
    }

Some incidence handlers receive additional information delivered as 'implicit
arguments'. Those are accessible variables are prepared without being
explicitly defined in the source code fragment itself.  In the documentation
below implicit variables are explained once at their first occurrence. An
implicit argument of a distinct name has the same meaning in all incidence
handlers where it appears. 

Mode Entry and Exit
^^^^^^^^^^^^^^^^^^^

Upon mode entry and exit the following two incidence handlers are executed.

.. data:: on_entry

    Implicit Argument: ``FromMode``

    Incidence handler to be executed on entrance of the mode. This happens as a
    reaction to mode transitions. ``FromMode`` is the mode from which the
    current mode is entered.

.. data:: on_exit

    Implicit Argument: ``ToMode``

    Incidence handler to be executed on exit of the mode. This happens as a
    reaction to mode transitions. The variable ``ToMode`` contains the mode to
    which the mode is left.

The incidence handlers are called from inside the member function
``self_enter_mode()``. ``on_exit`` is called before the mode transition is
accomplished. ``on_entry`` is called when the new mode has been set. Sending
tokens from inside the entry/exit handlers is is possible. However, the lexical
analyzer does not return immediately. If the 'single token' policy is used, a
token being sent might be overwritten if another sending occurs before return
from the token-receive function.  If the 'token queue' policy is used, it must
be chosen large enough to store tokens of all possible transition scenarios.


Pattern Matching
^^^^^^^^^^^^^^^^

The following two incidence handlers make it possible to specify actions to be
executed before and after the match specific actions. 

.. data:: on_match

    Implicit Arguments: ``Lexeme``, ``LexemeL``, ``LexemeBegin``, ``LexemeEnd``.

    This incidence handler is executed on every match.  It is executed *before*
    the pattern-action is executed that is related to the matching pattern. The
    implicit arguments allow access to the matched lexeme and correspond to
    what is passed to pattern-actions.

    ``Lexeme`` gives a pointer to a zero-terminated string that carries the
    matching lexeme. ``LexemeL`` is the lexeme's length. ``LexemeBegin`` gives
    a pointer to the begin of the lexeme which is not necessarily
    zero-terminated.  ``LexemeEnd`` points to the first lexatom after the last
    lexatom in the lexeme.

.. data:: on_after_match

    Implicit Arguments: ``Lexeme``, ``LexemeL``, ``LexemeBegin``, ``LexemeEnd``.

    The ``on_after_match`` handler is executed at every pattern match.
    Contrary to ``on_match`` it is executed *after* the action of the winning
    pattern.  To make sure that the handler is executed, it is essential that
    ``return`` is never a used in any pattern action directly. If a forced
    return is required, ``RETURN`` must be used. 

    .. warning::

        When using the token policy 'queue' and sending tokens from inside the 
        ``on_after_match`` function, then it is highly advisable to set the safety
        margin of the queue to the maximum number of tokens which are expected to
        be sent from inside this handler. Define::

               -DQUEX_SETTING_TOKEN_QUEUE_SAFETY_BORDER=...some number...
     
        on the command line to your compiler. Alternatively, quex can be passed the 
        command line option ``--token-policy-queue-safety-border`` followed by the
        specific number.

If a pattern matches, the following sequence of execution takes place. First,
``on_match`` of the mode is executed independently on what pattern matched.
Second, the pattern-specific action is executed. Third, the ``on_after_match``
is executed. Any handler that uses the ``return`` command breaks that sequence.
Using ``RETURN`` or ``CONTINUE`` triggers a direct jump to the
``on_after_match`` handler.

.. note::

   The ``on_failure`` handler, or the ``<<FAIL>>`` pattern handle actually
   'mismatches'.  Consequently, the ``on_match`` and ``on_after_match`` are not
   executed in that case.


Matching and Buffer Loading
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The incident of a input stream termination or a match failure can be handled by
the three handlers shown below.

.. data:: on_end_of_stream

   Incidence handler for the case that the end of file, or end of stream is reached.
   By means of this handler the termination of lexical analysis, or the return
   to an including file can be handled. This is equivalent to the ``<<EOF>>`` 
   pattern.

.. data:: on_load_failure

   Buffer loading failed for some unspecific reason. Under 'normal' conditions,
   this error must never occurr. However, it may occurr for example if a file
   is changed in the background, or someone inadvertedly tempered with the
   analyzers data structures, or if a defective low-level file system driver is
   used.

.. data:: on_buffer_overflow

   Implicit Arguments: ``self``, ``LexemeBegin``, ``LexemeEnd``, and ``BufferSize``.

   The reload process always tries to maintain the current lexeme inside the
   buffer. If the lexeme becomes as large as the buffer itself no new content
   can be loaded into the buffer. So, either new content must be provided,
   or an error handling must be triggered.

   By default, the buffer's memory is tried to be extended in a specific
   manner. Starting with a new size `s` as twice the size of the current buffer,
   an extension is tried. If that fails `s` is set to the average of `s`
   and the current size. This procedure is repeated until the allocation
   succeeds or `s` becomes equal to the current size. In the latter case
   an error code is set ('overflow') and a debug message is printed.

   One scenerio that necessitates a customized ``on_buffer_overflow`` handler
   is in an embedded environment, where dynamic allocation needs to be 
   prevented. In that case, setting an error code might be sufficient, 
   as in the example below.

   .. block:: cpp

      on_buffer_overflow {
          self.error_code = E_Error_Buffer_Overflow_LexemeTooLong;
      }

   The current buffer is available via ``self.buffer``. In particular the
   following two functions might be used to assing new memory or to extend it.

   .. function:: bool QUEX_NAME(Buffer_extend_root)(QUEX_NAME(Buffer)*  me, ptrdiff_t  SizeAdd)

      Attempts to allocate new memory for the buffer and migrates the
      content to the new memory. Returns ``false`` if and only if that
      attempt fails.

   .. function:: bool QUEX_NAME(Buffer_migrate_root)(QUEX_NAME(Buffer)*  me,
                                QUEX_TYPE_LEXATOM*  memory,
                                const size_t        MemoryLexatomN,
                                E_Ownership         Ownership) 

      Migrates the current buffer's content to the specified memory chunk.
      Returns ``false`` if and only if that attempt fails.

   The two functions operate on the ``root`` of nested buffers. This accounts
   for the fact that a buffer may be nested into an *including* buffer due to
   an include operation. When buffers are extended, the root of all nesting 
   is extended.

   .. warning::

       In case of error, an error code *must* be set in the ``on_buffer_overflow``
       handler. Otherwise, the lexer has no way to know that it has to stop. 

   TODO: elaborate: "In particular, when filling the buffer manually, a re-allocation may
   not be wanted"

.. data:: on_buffer_before_change

   Implicit Arguments: ``self``, ``BufferBegin``, ``BufferEnd``.

   The reload process always tries to maintain the current lexeme inside the
   buffer. If the lexeme becomes as large as the buffer itself, no reload can
   happen. In the case that the reload failed due to a lexeme being too long
   this handler is executed. Consider enlarging the buffer or using skippers
   which do not maintain the lexeme.

.. data:: on_failure

   Incidence handler for the case that a character stream does not match any
   pattern in the mode. This is equivalent to the ``<<FAIL>>`` pattern in the
   'lex' family of lexical analyzer generators. ``on_failure``, though, eats
   one character. The lexical analyzer may retry matching from what follows.

   .. note:: ``on_failure`` catches unexpected lexemes--lexemes where there is
             no match. This may be due to a syntax error in the data stream, 
             or due to an incomplete mode definition. In the first case, failure
             handling helps the user to reflect on what it feeds into the 
             interpreter. In the second case, it helps the developer of the 
             interpreter to debug its specification. It is always a good idea 
             to implement this handler.

   .. note:: The ``on_match`` and ``on_after_match`` handlers are not executed
             before and after the ``on_failure``. The reason is obvious, because 
             ``on_failure`` is executed because nothing matched. If nothing matched 
             then there is no incidence triggering ``on_match`` and ``on_after_match``.

   .. note:: Quex does not allow the definition of patterns which accept nothing.
             Actions, such as mode changes on the incidence of 'nothing has matched'
             can be implemented by ``on_failure`` and ``undo()`` as

             .. code-block:: cpp
              
                on_failure { self.undo(); self.enter_mode(NEW_MODE); }

             Or, in plain C

             .. code-block:: cpp
              
                on_failure { self_undo(); self_enter_mode(NEW_MODE); }

             If ``undo()`` is not used, the letter consumed by ``on_failure``
             is not available to the patterns of mode ``NEW_MODE``. 

      TODO: Raising of the 'E_Error_OnFailure' flag in case of manual 
            provision of the handler.

   .. note::

      A lesser intuitive behavior may occur when the token policy 'queue' is
      used, as it is by default. If the ``on_failure`` handler reports a
      ``FAILURE`` token it is appended to the token queue. The analysis does
      not necessarily stop immediately, but it continues until the queue is
      filled or the stream ends.  To implement an immediate exception like
      behavior, an additional member variable may be used, e.g.

      .. code-block:: cpp

         body {
             bool   on_failure_exception_f;
         } 
         constructor {
             on_failure_exception_f = false;
         }
         ...
         mode MINE {
            ...
            on_failure { self.on_failure_exception_f = true; }
         }

      Then, in the code fragment that receives the tokens the flag could be
      checked, i.e.

      .. code-block:: cpp

         ...
         my_lexer.receive(&token);
         if( my_lexer.on_failure_exception_f ) abort();
         ...

.. data:: on_bad_lexatom

   Implicit Arguments: ``BadLexatom``

   ``BadLexatom`` contains the lexatom beyond what is admissible according to the
   specified character encoding. If an input converter is specified, then the
   error is triggered during conversion and depends on the specified input 
   encoding. If no input converter is specified, the specified encoding of the
   engine itself determines whether a lexatom is admissible or not.

   The bad lexatom detection can be disabled by the command line options
   ``--no-bad-lexatom-detection`` or ``--nbld``.
   
The ``on_bad_lexatom`` has always precedence over ``on_failure``. That is, if
'--encoding ASCII' is specified as engine encoding and a value greater than 0x7F
appears, and encoding error is issued even if at the same time no pattern
matches. ``on_bad_lexatom`` also detects non-complient buffer loads--a little
late, hower. If a load procuder loads the buffer with data that contains the
buffer limit code, this this is detected upon the next attempt to reload[#f2]_.
When ``QUEX_OPTION_ON_LOAD_DETECT_BUFFER_LIMIT_CODE_IN_CONTENT`` is defined,
such situations are detected directly after reload.


Skippers
^^^^^^^^

In the case of range skipping, it is conceivable that the closing delimiters
never appear in the stream. In that case the following handler is executed.

.. data:: on_skip_range_open

   For a nested range skipper the ``Counter`` argument notifies additionally
   about the nesting level, i.e. the number of missing closing delimiters.

   A range skipper skips until it find the closing delimiter. The event handler
   ``on_skip_range_open`` handles the event that end of stream is reached
   before the closing delimiter. This is the case, for example if a range
   skipper scans for a terminating string "*/" but the end of file is reached
   before it is found. 


Indentation Based Scopes
^^^^^^^^^^^^^^^^^^^^^^^^
      
The default indentation handler already sends ``INDENT``, ``DEDENT`` and
``NODENT`` tokens as soon as it is activated by the mode tag
``<indentation:>``.  If the behavior needs to be controlled in more detail, the
following incidence handlers may be used. 

.. data:: on_indent

   Implicit Arguments: ``Indentation``

   If an opening indentation incidence occurs. The ``Indentation`` tells about
   the level of indentation. Usually, it is enough to send an ``INDENT`` token.

.. data:: on_dedent

   Implicit Arguments: ``First``, ``Indentation``

   If an closing indentation incidence occurs. If a line closes
   multiple indentation blocks, the handler is called *multiple*
   times. The argument ``First`` tells whether the first level of 
   indentation is reached. Sending a ``DEDENT`` token, should be enough.

.. data:: on_n_dedent

   Implicit Arguments: ``ClosedN``, ``Indentation``

   If an closing indentation incidence occurs. If a line closes multiple
   indentation blocks, the handler is called only *once* with the number of
   closed domains. ``ClosedN`` tells about the number of levels that have been
   closed.

   The handler should send ``ClosedN`` of ``DEDENT`` tokens, or if repeated
   tokens are enabled, ``send_self_n(ClosedN, DEDENT)`` might be used to 
   communicate several closings in a single token.

.. data:: on_nodent

   Implicit Arguments: ``Indentation``

   This handler is executed in case that the previous line had the same
   indentation as the current line.

.. data:: on_indentation_error

   Implicit Arguments: ``IndentationStackSize``, ``IndentationStack(I)``, 
                       ``IndentationUpper``, ``IndentationLower``, ``ClosedN``.

   Handler for the incidence that an indentation block was closed, but did not
   fit any open indentation domains. ``IndentationStackSize`` tells about
   the total size of the indentation stack. ``IndentationStack(I)`` delivers
   the indentation on level ``I``, ``IndentationUpper`` delivers the highest
   indentation and ``IndentationLower`` the lowest.

   Before this handler is called, the error flag 'Indentation_DedentNotOnIndentationBorder'
   is set. This might stop the lexical analysis loop. In case that the indentation
   error is to be treated by a token, the flag might have to be reset, such as
   in the following code fragment.

   .. block:: cpp
    
    mode MINE {
        ...
        on_indentation_error { 
            self_send1(QUEX_TKN_INDENTATION_ERROR, LexemeNull); 
            QUEX_NAME(error_code_clear)(&self); 
        }
        ...
    }

.. data:: on_indentation_bad

   Implicit Arguments: ``BadCharacter``

   In case that a character occurred in the indentation which was specified by
   the user as being *bad*. ``BadCharacter`` contains the inadmissible
   indentation character.

.. rubric:: Footnotes

.. [#f1] Lexical analysis is closely tied with the theory of state machines. 
         For that reason, the term 'incidence' has been chosen instead of 'event'
         which has a established meaning in the context of state machines.

.. [#f2] Buffer fillers and byte loaders must take care that this does not happen.
         POSIX conform byte loaders over sockets, for example, detect a terminating
         zero as part of the transmitted data and adapt the loaded number accordingly.

