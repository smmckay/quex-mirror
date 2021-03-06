Settings
--------

Following settings can be made on the command line:

.. cmacro:: QUEX_SETTING_LEXATOM_LOADER_SEEK_BUFFER_SIZE

   For seeking in character streams a temporary buffer is required. By means
   of this macro its size can be specified.

.. cmacro:: QUEX_SETTING_BUFFER_LEXATOM_BUFFER_BORDER

   The buffer limit code is by default 0x0. If it is intended that this character
   code appears inside patterns, then it need to be reset by this setting.

.. cmacro:: QUEX_SETTING_BUFFER_FALLBACK_N

   Buffers in quex keep a certain fall-back region when loading new content into
   the buffer. This prevents the lexer from reloading backwards if the input pointer
   is navigated below the current reload position. Note, that this has only effect
   in case of manual navigation of the input pointer, or in scanners with pre-conditions.

.. cmacro:: QUEX_SETTING_BUFFER_SIZE

   The size of a buffer on which the quex engine does its analysis. The larger the
   buffer, the less reloads are required. But at a certain buffer size (usually about
   32Kb) an increase in buffer size does not show measurable performance increase.
   
   The buffer size *must* be greater or equal the largest conceivable lexeme that the
   lexer can match.

.. cmacro:: QUEX_SETTING_ICU_PIVOT_BUFFER_SIZE

   When using IBM's ICU library for character conversion (command line option ``--icu``),
   the intermediate buffer size is determined by this setting.

.. cmacro:: QUEX_SETTING_MODE_STACK_SIZE

   Defines the size of the mode stack. It defines the number of 'sub mode
   calls' that can be done via the ``.push_mode`` and ``.pop_mode`` member
   functions. See also section :ref:`sec-mode-transitions`.

.. cmacro:: QUEX_SETTING_TOKEN_QUEUE_SIZE

   Defines the initial number of elements of the token queue--if it is 
   enable (see also command line option ``--no-token-queue``)

.. cmacro:: QUEX_SETTING_TOKEN_QUEUE_SAFETY_BORDER

   Defines the size of the safety border. In other words, this corresponds to the 
   maximum number of tokens to be sent caused by a pattern match '-1'. If each
   pattern sends only one token, it can be set safely to zero.

.. cmacro:: QUEX_SETTING_LEXATOM_LOADER_CONVERTER_BUFFER_SIZE

   When using a converter (``--icu`` or ``--iconv``) this is the size of the 
   buffer where the original stream data is read into.

.. cmacro:: QUEX_SETTING_OUTPUT_TEMPORARY_UTF8_STRING_BUFFER_SIZE

   When printing the ``text`` content of the default token type, it can be converted
   to UTF8. The conversion requires a temporary buffer whose size is defined by
   means of this macro.
