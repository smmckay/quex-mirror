import quex.engine.codec_db.core as codec_db
from   quex.engine.state_machine.transformation.base import EncodingTrafo

from   quex.blackboard import setup as Setup
import os

class EncodingTrafoByTable(EncodingTrafo, list):
    """Provides the information about the relation of character codes in a 
    particular coding to unicode character codes. It is provided in the 
    following form:

           # Codec Values                 Unicode Values
           [ (Source0_Begin, Source0_End, TargetInterval0_Begin), 
             (Source1_Begin, Source1_End, TargetInterval1_Begin),
             (Source2_Begin, Source2_End, TargetInterval2_Begin), 
             ... 
           ]

    """
    def __init__(self, Codec=None, FileName=None, ExitOnErrorF=True):
        assert Codec is not None or FileName is not None

        if FileName is not None:
            file_name  = os.path.basename(FileName)
            file_name, \
            dumped_ext = os.path.splitext(file_name)
            codec_name = file_name.replace(" ", "_").replace("\t", "_").replace("\n", "_")
            file_name  = FileName
        else:
            codec_name, \
            file_name   = codec_db.get_file_name_for_codec_alias(Codec)

        source_set, drain_set = codec_db.load(self, file_name, ExitOnErrorF)
        EncodingTrafo.__init__(self, codec_name, source_set, drain_set)

        self._code_unit_error_range_db[0] = \
                drain_set.complement(Setup.buffer_encoding.lexatom_range)

    def do_transition(self, sm, FromSi, from_target_map, ToSi):
        """Translates to transition 'FromSi' --> 'ToSi' inside the state
        machine according to the translation table.

        If setup, the transition to 'BAD_LEXATOM' is added for invalid
        values of code units. 

        RETURNS: [0] True if complete, False else.
                 [1] True if transition needs to be removed from map.
        """
        number_set = from_target_map[ToSi]

        if number_set.transform_by_table(self): 
            assert not number_set.is_empty() # because .transform_by_table() -> True
            return True, False

        # 'FromSi' is a state that handles code unit '0'.
        # (With tables, there is actually only one code unit)
        self._code_unit_to_state_list_db[0].add(FromSi)
        print "#add2:", FromSi

        return False, number_set.is_empty()

    def do_NumberSet(self, number_set):
        """RETURNS: List of interval sequences that implement the number set.
        """
        transformed = number_set.transform_by_table(self)
        return [ 
            [ interval ]
            for interval in transformed.get_intervals(PromiseToTreatWellF=True) 
        ]


