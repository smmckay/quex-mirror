/* -*- C++ -*-  vim: set syntax=cpp:
 * (C) 2007-2008 Frank-Rene Schaefer  */
#ifndef  QUEX_INCLUDE_GUARD__BUFFER__LEXATOMS__CONVERTER__CONVERTER_I
#define  QUEX_INCLUDE_GUARD__BUFFER__LEXATOMS__CONVERTER__CONVERTER_I

$$INC: buffer/lexatoms/converter/Converter$$
$$INC: quex/MemoryManager$$

QUEX_NAMESPACE_MAIN_OPEN

QUEX_INLINE bool
QUEX_NAME(Converter_construct)(QUEX_NAME(Converter)* me,
                               const char*  FromCodec, const char* ToCodec,
                               bool         (*initialize)(QUEX_NAME(Converter)*, 
                                                          const char* FromCodingName, 
                                                          const char* ToCodingName),  
                               bool         (*initialize_by_bom_id)(QUEX_NAME(Converter)*, 
                                                                    E_ByteOrderMark),
                               E_LoadResult (*convert)(QUEX_NAME(Converter)*, 
                                                       uint8_t**             source, const uint8_t*             SourceEnd, 
                                                       QUEX_TYPE_LEXATOM** drain,  const QUEX_TYPE_LEXATOM* DrainEnd),
                               void         (*delete_self)(QUEX_NAME(Converter)*),
                               ptrdiff_t    (*stomach_byte_n)(QUEX_NAME(Converter)*),
                               void         (*stomach_clear)(QUEX_NAME(Converter)*),
                               void         (*print_this)(QUEX_NAME(Converter)*))
/* If 'FromCodec == 0': The converter is expected to adapt to a BOM (byte order
 *                      mark *later*. 'initialize' is expected to mark the 
 *                      derived class' as 'not-initialized'.
 *                      In that case, the function '.initialize_by_bom_id' must 
 *                      be called before the converter is operational. That 
 *                      function may check, whether an initialization has been
 *                      done before.
 * 
 * RETURNS: true  -- construction succesful
 *          false -- else.                                                    */
{
    __quex_assert(0 != initialize);           /* All functions MUST be defined.    */
    __quex_assert(0 != initialize_by_bom_id); /* All functions MUST be defined.    */
    __quex_assert(0 != convert);
    __quex_assert(0 != delete_self);
    __quex_assert(0 != stomach_byte_n);
    __quex_assert(0 != stomach_clear);

    me->initialize           = initialize;
    me->initialize_by_bom_id = initialize_by_bom_id;
    me->convert              = convert;
    me->stomach_byte_n       = stomach_byte_n;
    me->stomach_clear        = stomach_clear;
    me->delete_self          = delete_self;
    me->print_this           = print_this;

    me->virginity_f          = true;
    me->byte_n_per_lexatom   = -1;         /* No fixed ratio 'byte_n/lexatom' */
    me->input_code_unit_size = -1;         /* Unknown input code unit size.   */

    /* Opens internally a conversion handle for the conversion from 'FromCodec'
     * to 'ToCodec'. Pass '0x0' as 'ToCodec' in order to indicate a conversion
     * to unicode of size sizeof(QUEX_TYPE_LEXATOM). 
     *
     * It is the task of the particular implementation to provide the 'ToCodec'
     * which is appropriate for sizeof(QUEX_TYPE_LEXATOM), i.e.  ASCII, UCS2,
     * UCS4.                                                                  */

    return initialize(me, FromCodec, ToCodec);
}

QUEX_INLINE void
QUEX_NAME(Converter_reset)(QUEX_NAME(Converter)* me)
{
    me->stomach_clear(me);
    me->virginity_f = true;
}

QUEX_INLINE void
QUEX_NAME(Converter_print_this)(QUEX_NAME(Converter)* me)
{
    QUEX_DEBUG_PRINT("      converter: ");
    if( ! me ) {
        QUEX_DEBUG_PRINT("<none>\n");
        return;
    }
    QUEX_DEBUG_PRINT("{\n");
    QUEX_DEBUG_PRINT1("        virginity_f:          %s;\n", E_Boolean_NAME(me->virginity_f));
    QUEX_DEBUG_PRINT1("        byte_n_per_lexatom:   %i;\n", (int)me->byte_n_per_lexatom);
    QUEX_DEBUG_PRINT1("        input_code_unit_size: %i;\n", (int)me->input_code_unit_size);
    if( me->print_this ) {
        me->print_this(me);
    }
    QUEX_DEBUG_PRINT("      }\n");
}


QUEX_NAMESPACE_MAIN_CLOSE

#endif /*  QUEX_INCLUDE_GUARD__BUFFER__LEXATOMS__CONVERTER__CONVERTER_I     */
