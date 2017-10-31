TODO:: Review and Rewrite this section
======================================


.. intersection({Pattern} \Any*{Pattern})  # => patterns Q that end with Q
.. intersection({Pattern} {Pattern}\Any*)  # => patterns Q that start with Q

.. intersection({Pattern} \Any*\Not{Pattern})  # => patterns Q that do not end with Q
.. intersection({Pattern} \Not{Pattern}\Any*)  # => patterns Q that do not start with Q


.. describe:: \\CutBegin{ P Q } -- Cut Beginning (BL)

   Prune P in front, so that ``\CutBegin{ P Q }`` starts right after what Q 
   would match. 

   Example::

              \CutBegin{"otto_mueller" "otto"} --> "_mueller"

.. note:: 

     ``\CutBegin`` cuts only *one appearance* of a lexeme from Q *at the
     beginning* of P; but it does not mean that the result cannot match a
     lexeme starting with a lexeme from Q. Let P match Lp = {xx, xy} while Q
     matches Lq = {x}, then ``\CutBegin{P Q}`` only cuts the first appearance
     of 'x' and the resulting set of lexemes is {x, y}. It contains 'x'
     which is a lexeme matched by Q.

.. note::

     When dealing with repeated expressions the rules of ``\CutBegin``
     may surprise at the first glance. Consider for example::

           \CutBegin{[0-9]+ 0}
    
     which only cuts out the first occurence of 0.  There is an infinite number
     of lexemes in ``[0-9]+`` having '0' as second character--which becomes now
     the first. Thus the above expression is equivalent to ``[0-9]+`` itself.  To
     delete ``0`` totally from ``[0-9]+`` it is necessary to write::

           \CutBegin{[0-9]+ 0+}



.. describe:: \\CutEnd{ P Q } -- Cut End (BL)

   Prune P at back, so that \\CutEnd{ P Q } ends right before Q would match. 
   Example::

              \CutEnd{"otto_mueller" "mueller"} --> "otto_"

\\CutBegin{P \Not{Q}}
\\CutBegin{P \Not{Q}}
.. describe:: \\NotBegin{ P Q } -- Complement Begin (BS)

   Matches those lexemes of P which do not start with lexemes that match Q.

.. describe:: \\NotEnd{ P Q } -- Complement End (BS)

   Matches those lexemes of P which do not end with lexemes that match Q.

.. describe:: \\NotIn{ P Q } -- Complement End (BS)

   Matches those lexemes of P which do not contain lexemes that match Q.

-----------------------
