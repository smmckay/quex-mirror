from   quex.engine.operations.operation_list      import Op

import quex.output.core.loop                      as     loop
import quex.engine.analyzer.engine_supply_factory as     engine
from   quex.engine.analyzer.door_id_address_label import DoorID
from   quex.engine.counter                        import CountActionMap
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
    ca_map        = Data["ca_map"]
    character_set = Data["character_set"]
    dial_db       = Data["dial_db"]
    assert isinstance(ca_map, CountActionMap)
    assert isinstance(character_set, NumberSet)

    ca_map = ca_map.pruned_clone(character_set)

    engine_type = None # Default
    if ReloadState: engine_type = ReloadState.engine_type

    on_loop_exit_door_id = DoorID.continue_without_on_after_match(dial_db)

    result,               \
    terminal_list,        \
    loop_map,             \
    door_id_beyond,       \
    required_register_set = loop.do(ca_map,
                                    OnLoopExitDoorId  = on_loop_exit_door_id,
                                    LexemeEndCheckF   = False,
                                    LexemeMaintainedF = False,
                                    EngineType        = engine_type,
                                    ReloadStateExtern = ReloadState, 
                                    dial_db           = dial_db)

    assert isinstance(result, list)
    return result, terminal_list, loop_map, required_register_set
