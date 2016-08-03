"""PURPOSE: 

      Given two state machines A and T, determine whether A ends with T.

"""
import quex.engine.state_machine.check.outrun    as outrun
import quex.engine.state_machine.algebra.reverse as reverse

def do(A, T):
    """Checks: (1) whether there are sequence that match 'T' and the end of 'A'.
               (2) whether there are sequences that do not match 'T' and still
                   match the end of 'A'.

    RETURNS: [0] True, ALL ending sequences of 'A' match 'T'.
                 False, else.
             [1] True, if there are some ending sequences of 'A' that match 'T'.
                 False, else.
    """
    Ar = reverse.do(A)
    Tr = reverse.do(T)
    
    common_tail_exists_f   = __common_exists(Ar, Tr)
    uncommon_tail_exists_f = __uncommon_exists(Ar, Tr)

    return common_tail_exists_f and not uncommon_tail_exists_f, \
           common_tail_exists_f

def common_exists(A, T):
    """RETURNS: True, if there are sequence that match 'T' and may appear
                      as ending sequences of 'A'.
                False, else.
    """
    Ar = reverse.do(A)
    Tr = reverse.do(T)
    return __common_exists(Ar, Tr)

def uncommon_exists(A, T): 
    """RETURNS: True, if there are sequence that do NOT match 'T' but may appear
                      as ending sequences of 'A'.
                False, else.
    """
    Ar = reverse.do(A)
    Tr = reverse.do(T)
    return __uncommon_exists(Ar, Tr)

def __common_exists(Ar, Tr):
    """RETURNS: True, if there are sequence that match 'T' and may appear
                      as ending sequences of 'A'.
                False, else.
    """
    collector = outrun.Step1_Walker(Tr, Ar)
    collector.do([(Ar.init_state_index, Tr.init_state_index)])

    # collector.result: List of pairs (Ti_si, Ai_si) 
    # 
    #   Ti_si = index of acceptance state in 'Tr' that has been reached.
    #   Ai_si = index of state in 'Ar' that was reached when walking
    #           along the path to 'Ti_si'.
    # 
    # => If there is a result, then a sequence that matches 'T' exists which
    #    is a terminating sequence of 'A'
    return len(collector.result) != 0

def __uncommon_exists(Ar, Tr): 
    """Detect paths in Ar that divert from Tr starting from
       the acceptance states collected in step 1.
    """
    detector = outrun.Step2_Walker(Tr, Ar)

    # Start searching for diversion from the critical acceptance states in Tr.
    detector.do([(Ar.init_state_index, Tr.init_state_index)])

    # detector.result: True  -- if there are paths in Ar that divert
    #                  False -- if all paths from acceptance states in Tr are 
    #                           also in Ar.
    return detector.result

