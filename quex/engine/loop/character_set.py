import quex.engine.loop.core                      as     loop
from   quex.engine.analyzer.door_id_address_label import DoorID
from   quex.engine.counter                        import CountActionMap
from   quex.engine.misc.interval_handling         import NumberSet

def do(CaMap, CharacterSet, ReloadState, dial_db):
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
    assert isinstance(CaMap, CountActionMap)
    assert isinstance(CharacterSet, NumberSet)

    if ReloadState: engine_type = ReloadState.engine_type
    else:           engine_type = None

    on_loop_exit_door_id = DoorID.continue_without_on_after_match(dial_db)

    analyzer_list,         \
    terminal_list,         \
    loop_map,              \
    door_id_loop,          \
    required_register_set, \
    run_time_counter_f     = loop.do(CaMap.pruned_clone(CharacterSet),
                                     OnLoopExitDoorId  = on_loop_exit_door_id,
                                     EngineType        = engine_type,
                                     ReloadStateExtern = ReloadState, 
                                     dial_db           = dial_db)
    assert not run_time_counter_f

    return analyzer_list, \
           terminal_list, \
           loop_map, \
           required_register_set
