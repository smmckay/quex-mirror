TEST: Contexts 'begin-of-stream' and 'end-of-stream'.

This directory tests the lexer's ability to match dependent on the pre and post
contexts 'begin-of-stream' and 'end-of-stream'.  For that the lexer must
implement several different detectors with the correct precedence. Also, they
shall not mask-out unconditional patterns or patterns with other contexts.

Further, the 'begin-of-stream' and 'end-of-stream' are implicit in the context
conditions 'begin-of-line' and respectively 'end-of-line'. The tests evolve
around 'explicit' and 'implicit', i.e. lexers which explicitly define 
'begin-of-stream' and 'end-of-stream' as conditions, and those which define
them implicitly through 'begin/end of line'.

Tests evolve around a 'core pattern' LETTER which is setup with several
different contexts. The explicit and implicit definitions happen in the
files 'explicit.qx' and 'implicit.qx'.

Test files on which the analyzers run are the following:

"bos-eos.txt"     -- Together: 'begin-of-stream' and 'end-of-stream'.
"bos-and-eos.txt" -- Separate: 'begin-of-stream' and 'end-of-stream', 
                               + without context
                               + with other pre-context
                               + with other post-context
                               + with other pre- and post-context
"not-bos-eos.txt" -- Content that is not subject to 'begin-of-stream'
                     and 'end-of-stream' conditions.
            
"bos-x-x-eos.txt" -- 'begin-of-stream' together with 'normal post context'
                     'end-of-stream' together with 'normal post context'


"make.py" is used to generate those text files with special conditions
such as 'no newline at end of file'.
