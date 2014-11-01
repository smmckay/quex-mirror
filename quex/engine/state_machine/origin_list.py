from quex.engine.state_machine.state_core_info import StateOperation
from quex.blackboard                           import E_PreContextIDs, E_IncidenceIDs

class OperationPot(object):
    __slots__ = ('__list')

    def __init__(self):
        self.__list = []

    @staticmethod
    def from_iterable(Iterable):
        result = OperationPot()
        result.merge(Iterable)
        return result

    @staticmethod
    def from_one(Operation):
        result = OperationPot()
        result.__list.append(Operation)
        return result

    def clone(self, ReplDbPreContext=None, ReplDbAcceptance=None):
        return OperationPot.from_iterable(x.clone(ReplDbPreContext=ReplDbPreContext, ReplDbAcceptance=ReplDbAcceptance) for x in self.__list)

    def get_list(self):
        return self.__list

    def __iter__(self):
        for x in self.__list:
            yield x

    def __len__(self):
        return len(self.__list)

    def take_out_FAILURE(self):
        L = len(self.__list)
        for i in xrange(L-1, -1, -1):
            if self.__list[i].acceptance_id() == E_IncidenceIDs.MATCH_FAILURE:
                del self.__list[i]

    def is_there_a_non_FAILURE(self):
        for origin in self.__list:
            if origin.acceptance_id() != E_IncidenceIDs.MATCH_FAILURE:
                return True
        return False

    def __add(self, Origin):
        """Check if origin has already been mentioned, else append the new origin.
        """
        # NOT: if not Origin.is_meaningful(): return
        #      We need even non-meaningful origins, to detect whether a state can be 
        #      combined with another during Hopcroft optimization.
            
        AcceptanceID = Origin.acceptance_id()
        if AcceptanceID != E_IncidenceIDs.MATCH_FAILURE:
            self.take_out_FAILURE()
        elif self.is_there_a_non_FAILURE():
            return

        for same in (origin for origin in self.__list if origin.acceptance_id() == AcceptanceID):
            same.merge(Origin)
            return
        self.__list.append(Origin.clone())

    def get_the_only_one(self):
        """Returns a origin that belongs to the list. If there is no origin on
           the list, then one is created and then returned.
        """
        L = len(self.__list)
        if   L == 0: 
            new_origin = StateOperation(E_IncidenceIDs.MATCH_FAILURE, -1L, AcceptanceF=False)
            self.__list.append(new_origin)
            # NOTE: Here the object is in a state where there is a 'nonsense origin'. It is
            #       expected from the caller to fix this.
            return new_origin

        assert L == 1, "Calling function not permitted on aggregated states. len(self.__list) == %s" % len(self.__list)
        return self.__list[0]

    def add(self, X, StateIndex=None, 
            StoreInputPositionF   = False, 
            AcceptanceF           = False, 
            RestoreInputPositionF = False, 
            PreContextID          = E_PreContextIDs.NONE):
        """Add the StateMachineID and the given StateIdx to the list of origins of 
           this state.
           NOTE: The rule is that by default the 'input_position_store_f' flag
                 follows the acceptance state flag (i.e. by default any acceptance
                 state stores the input position). Thus when an origin is  added
                 to a state that is an acceptance state, the 'input_position_store_f'
                 has to be raised for all incoming origins.      
        """
        assert type(X) == long or X == E_IncidenceIDs.MATCH_FAILURE or X.__class__ == StateOperation
        assert StateIndex is None or type(StateIndex) == long
        assert StoreInputPositionF is not None
            
        if isinstance(X.__class__, StateOperation):
            self.__add(X.clone())
        else:
            self.__add(StateOperation(AcceptanceID          = X, 
                                      StateIndex            = StateIndex, 
                                      AcceptanceF           = AcceptanceF,
                                      PreContextID          = PreContextID,
                                      StoreInputPositionF   = StoreInputPositionF, 
                                      RestoreInputPositionF = RestoreInputPositionF))

    def merge(self, OriginIterable):
        for origin in OriginIterable: 
            self.__add(origin)

    def set(self, OriginList, ArgumentIsYoursF=False):
        assert type(OriginList) == list
        if ArgumentIsYoursF: 
            self.__list = OriginList
            return
        self.__list = []
        self.merge(OriginList)

    def clear(self):
        self.__list = []

    def delete_dominated(self):
        """Simplification to make Hopcroft Minimization more efficient. The first unconditional
        acceptance makes any lower priorized acceptances meaningless. 

        This function is to be seen in analogy with the function 'get_acceptance_detector'. 
        Except for the fact that it requires the 'end of core pattern' markers of post
        conditioned patterns. If the markers are not set, the store input position commands
        are not called properly, and when restoring the input position bad bad things happen 
        ... i.e. segmentation faults.
        """
        # NOTE: Acceptance origins sort before non-acceptance origins
        self.__list.sort(key=lambda x: (not x.is_acceptance(), x.acceptance_id()))
        new_origin_list                  = []
        unconditional_acceptance_found_f = False
        for origin in self.__list:
            if not origin.is_acceptance():
                new_origin_list.append(origin)  # Out of consideration. 
                continue

            # Only append acceptance origins until the first unconditional acceptance.
            if not unconditional_acceptance_found_f:
                if origin.pre_context_id() == E_PreContextIDs.NONE:
                    unconditional_acceptance_found_f = True # prevent entering this part again
                new_origin_list.append(origin)

        self.__list = new_origin_list 

    def get_string(self, OriginalStatesF=True):

        txt = "" 
        if len(self.__list) == 0: 
            return txt + "\n"

        for origin in self.__list:
            if   origin.is_acceptance():                          break
            elif origin.pre_context_id() != E_PreContextIDs.NONE: break
            elif origin.input_position_store_f():                 break
            elif origin.input_position_restore_f():               break
        else:
            # All origins are 'harmless'. Sort by acceptance_id for the 'camera'.
            for origin in sorted(self.__list, key=lambda x: x.acceptance_id()):
                ostr = origin.get_string() 
                if ostr: txt += "%s, " % ostr
            txt = (txt[:-2] + "\n").replace("L","")     
            return txt

        # for origin in sorted(self.__list, key=attrgetter("state_machine_id")):
        for origin in self.__list:
            ostr = origin.get_string() 
            if ostr: txt += "%s, " % ostr
        txt = (txt[:-2] + "\n").replace("L","")     
        return txt
