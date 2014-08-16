"""
Let N be the number of intervals in a trigger set. For example,
      For a trigger set '[0:4) [10:12)' N would be '2'.

Let E be the extend of a trigger set, i.e. the number of code points 
      that it contains. The trigger set '[0:4) [10:12)' has an 
      extend of '12', i.e. the numbers from 0 to 11 (12 is excluded).

Let C be the computation cost for an operation.
 
Let M be the memory cost for an operation.

(i) Cost of Bisectioning _______________________________________________

    Example:

        if x > 64:
            if x < 16:
                if x == 4: jump state1
            else:
                jump state2
        else:
            jump state2

    C = log2(N) * (cmp + jump)
    M = log2(N) * (cmp + jump)

(ii) Branch Tables / Switch Statements _________________________________

     Branch tables are generated by the compiler from 'switch' statements
     with 'x' containing the value to branch upon:

         (1) x = validate x in range   # x = 0 if not in range
         (2) i = x * sizeof(goto)
         (3) jump $(next + i)          # goto address in 'next[i]'

        next: bad_state
              state_1
              state_2
              ...

     Thus, the resulting cost is:

          (1) Two comparisons, if 'x' does not cover a byte range.
              (this includes a conditional jump)
          (2) shift operation (times '4' = << 2, for example)
          (3) addition + referencing + jump

     C = 1 * (2 * cmp + jump + shift + add + ref + jump)
     M = E * (2 * cmp + jump + shift + add + ref + jump)

     where 'C' is indenpendent of 'E' and 'N', but M linear with E.


(iii) Linear Comparison (forward/backward) _____________________________

         if x == value1: goto state_1
         if x == value2: goto state_2
         ...
         else:           goto state_else

      C = N / 2 * (cmp + jump)
      M = N * (cmp + jump)

      where 'N' is the number of values in the given interval where
      the target differs from 'state_else'.

HEURISTIC: _____________________________________________________________

   (1) If interval can be interpreted as set of 'exceptional' transitions
       where the number of exceptions N <= N_linear, the implement trigger
       map as Linear Comparison (iii).

   (2) 
"""
from   quex.engine.misc.enum import Enum
from   math                  import log

E_Type = Enum("SWITCH_CASE", "BISECTION", "COMPARISON_SEQUENCE", "TRANSITION")

def get(TriggerMap, 
        size_all_intervals=None, 
        size_all_drop_out_intervals=None):
    """See file 'solution-new.py' for an approach of a more sophisticated
       implementation.
    """
    TriggerSetN = len(TriggerMap)

    if TriggerSetN == 1:
        return E_Type.TRANSITION

    if size_all_intervals is None:
        size_all_intervals          = 0
        size_all_drop_out_intervals = 0
        for interval, target in TriggerMap:
            if target.drop_out_f(): size_all_drop_out_intervals += interval.size()
            size_all_intervals += interval.size()

    if size_all_intervals - size_all_drop_out_intervals == 0:
        # No drop-outs
        return E_Type.BISECTION

    p = log(len(TriggerMap), 2) / (size_all_intervals - size_all_drop_out_intervals)

    if p > 0.03 and size_all_drop_out_intervals < 512: 
        return E_Type.SWITCH_CASE

    if len(TriggerMap) > 5: 
        return E_Type.BISECTION
    else:
        return E_Type.COMPARISON_SEQUENCE

