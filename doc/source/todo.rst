Reset: mention 'byte_order_reversion' must be reset, manually.
       user_reset: user must free any resource, in case of failure.

Using 'reset memory' and later 'reset_ByteLoader' requires to check
for the 'buffer._memory.ownership' before reload! 

-- Function: 'collect_user_owned_memory()' to be called before
             reset/include_pop/destructor.

-- Including: Buffer splits, so that frequent inclusion does not require
              allocation of huge amounts of buffers.

-- Reset: user_reset must destruct newly created resources and 
                     mark them 'absent' in case of failure.

-- ByteLoader->input_handle_ownership => prevent closure/freeing of handle
