from   quex.engine.operations.operation_list      import Op

import quex.output.core.loop                      as     loop
import quex.engine.analyzer.engine_supply_factory as     engine
from   quex.engine.analyzer.door_id_address_label import DoorID
from   quex.engine.counter                        import CountBase
from   quex.engine.misc.interval_handling         import NumberSet
from   quex.blackboard                            import Lng

def do(Data, ReloadState):
    """Fast implementation of character set skipping machine.
    ________________________________________________________________________
    As long as characters of a given character set appears it iterates: 

                                 input in Set
                                   .--<---.
                                  |       |
                              .-------.   |
                   --------->( SKIPPER )--+----->------> RESTART
                              '-------'       input 
                                            not in Set

    ___________________________________________________________________________
    NOTE: The 'TerminalSkipRange' takes care that it transits immediately to 
    the indentation handler, if it ends on 'newline'. This is not necessary
    for 'TerminalSkipCharacterSet'. Quex refuses to work on 'skip sets' when 
    they match common lexemes with the indentation handler.
    ___________________________________________________________________________

    Precisely, i.e. including counter and reload actions:

    START
      |
      |    .----------------------------------------------.
      |    |.-------------------------------------------. |
      |    ||.----------------------------------------. | |
      |    |||                                        | | |
      |    |||  .-DoorID(S, a)--.    transition       | | |
      |    || '-|  gridstep(cn) |       map           | | |        
      |    ||   '---------------'\    .------.        | | |        
      |    ||   .-DoorID(S, b)--. '->-|      |        | | |       
      |    |'---|  ln += 1      |--->-| '\t' +-->-----' | |      
      |    |    '---------------'     |      |          | |     
      |    |    .-DoorID(S, c)--.     | ' '  +-->-------' |   
      |    '----|  cn += 1      |--->-|      |            |   
      |         '---------------'     | '\n' +-->---------'              
      |                               |      |                  .-DropOut ------.        
      |         .-DoorID(S, 0)--.     | else +-->---------------| on_exit       |                                
      '------>--| on_entry      |--->-|      |                  '---------------'        
                '---------------'     |  BLC +-->-.  
                                  .->-|      |     \                 Reload State 
                .-DoorID(S, 1)--./    '------'      \             .-----------------.
           .----| after_reload  |                    \          .---------------.   |
           |    '---------------'                     '---------| before_reload |   |
           |                                                    '---------------'   |
           '-----------------------------------------------------|                  |
                                                         success '------------------'     
                                                                         | failure      
                                                                         |            
                                                                  .---------------.       
                                                                  | End of Stream |       
                                                                  '---------------'                                                                   

    NOTE: If dynamic character size codings, such as UTF8, are used as engine codecs,
          then the single state may actually be split into a real state machine of
          states.
    """
    counter_db    = Data["counter_db"]
    character_set = Data["character_set"]
    assert isinstance(counter_db, CountBase)
    assert isinstance(character_set, NumberSet)

    ca_map = counter_db.count_command_map
    ca_map = ca_map.pruned_clone(character_set)

    engine_type = None # Default
    if ReloadState: engine_type = ReloadState.engine_type

    result,               \
    loop_map,             \
    door_id_beyond,       \
    required_register_set = loop.do(ca_map,
                                    OnLoopExitDoorId  = DoorID.continue_without_on_after_match(),
                                    LexemeEndCheckF   = False,
                                    LexemeMaintainedF = False,
                                    EngineType        = engine_type,
                                    ReloadStateExtern = ReloadState) 

    assert isinstance(result, list)
    return result, loop_map, required_register_set
