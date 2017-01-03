Reset: mention 'byte_order_reversion' must be reset, manually.
       user_reset: user must free any resource, in case of failure.

Using 'reset memory' and later 'reset_ByteLoader' requires to check
for the 'buffer._memory.ownership' before reload! 
