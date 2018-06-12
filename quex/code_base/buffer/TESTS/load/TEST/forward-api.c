/* PURPOSE: Testin Buffer_load_forward()
 *
 * Tests that the return values of the load forward functions are as expected
 * according to the buffer's state and the loader's capability. The focus of 
 * this test is NOT the adaption of the pointers.
 *
 * SCENARIOS:
 *            (1.a) Normal load 
 *                => E_LoadResult_DONE.
 *            (1.b) Lexeme starts at begin + (<=FallbackN) 
 *                => E_LoadResult_DONE
 *            (1.c) Lexeme starts at begin 
 *                => E_LoadResult_NO_SPACE_FOR_LOAD
 *            (1.d) Nothing loaded (loaded_n == 0)
 *                => E_LoadResult_NO_MORE_DATA
 *            (2.a) 1) no lexatom_loader, or
 *                  2) no byte byte_loader
 *                => E_LoadResult_NO_MORE_DATA
 *            (2.b) _read_p != input.end_p
 *                => '_read_p' pointed to buffer limit code, but it was 
 *                   not the buffer's limit
 *                => E_LoadResult_ENCODING_ERROR
 *            (2.c) Encoding Error from lexatom_loader/converter
 *                1) ICU
 *                2) IConv
 *                => E_LoadResult_ENCODING_ERROR
 *
 * E_LoadResult_NO_MORE_DATA => EOS must be set.
 *
 */
#define BufferElementN (QUEX_SETTING_BUFFER_MIN_FALLBACK_N + 5)

#include "commonly_pasted.c"
#include "ut/lib/buffer/lexatoms/LexatomLoader.i"
#include "ut/lib/buffer/lexatoms/LexatomLoader_Converter.i"
#include "ut/lib/buffer/lexatoms/converter/iconv/Converter_IConv"
#include "ut/lib/buffer/lexatoms/converter/iconv/Converter_IConv.i"
#include "ut/lib/buffer/lexatoms/converter/icu/Converter_ICU"
#include "ut/lib/buffer/lexatoms/converter/icu/Converter_ICU.i"

typedef enum {
    E_LexatomLoader_ICU,
    E_LexatomLoader_IConv,
    E_LexatomLoader_Plain,
    E_LexatomLoader_NoByteLoader,
    E_LexatomLoader_None,
} E_LexatomLoader;

static struct {
    QUEX_NAME(Buffer)             buffer;
    QUEX_NAME(ByteLoader_Memory)  byte_loader;
    QUEX_NAME(LexatomLoader)*     lexatom_loader;
    QUEX_NAME(Converter)*         converter;
    QUEX_TYPE_LEXATOM_EXT             memory[BufferElementN + 2]; 
    SomethingContainingABuffer_t  the_aux;
} self;

static void         self_setup(ptrdiff_t   LexemePOffset,  /* = LexemeP - Buffer's Front */    
                               ptrdiff_t   ReadPOffset,    /* = EndP - ReadP             */
                               bool        EmptyFileF,
                               E_LexatomLoader LexatomLoaderType, 
                               ptrdiff_t   ErrorCodePosition);
static E_LoadResult self_load(bool ConverterF);
static void         self_DONE();
static void         self_NO_SPACE_FOR_LOAD();
static void         self_NO_MORE_DATA();
static void         self_BAD_LEXATOM();

int
main(int argc, char**argv)
{
    if( argc > 1 && strcmp(argv[1], "--hwut-info") == 0 ) {
        printf("API: load_forward;\n");
        printf("CHOICES: DONE, NO_SPACE_FOR_LOAD, NO_MORE_DATA, BAD_LEXATOM;\n");
        return 0;
    }
    __quex_assert(QUEX_SETTING_BUFFER_MIN_FALLBACK_N == 2);

    hwut_if_choice("DONE")              self_DONE();
    hwut_if_choice("NO_SPACE_FOR_LOAD") self_NO_SPACE_FOR_LOAD();
    hwut_if_choice("NO_MORE_DATA")      self_NO_MORE_DATA();
    hwut_if_choice("BAD_LEXATOM")       self_BAD_LEXATOM();

    printf("<terminated: { verified: %i; overflow: %i; content_change: %i; }>\n",
           (int)common_verification_count, 
           (int)common_on_overflow_count, 
           (int)common_on_content_change_count);
    return 0;
}

static void
self_setup(ptrdiff_t       LexemePOffset,  /* = LexemeP - Buffer's Front */    
           ptrdiff_t       ReadPOffset,    /* = EndP - ReadP             */
           bool            EmptyFileF,
           E_LexatomLoader LexatomLoaderType, 
           ptrdiff_t       ErrorCodePosition)
{
    self.the_aux.buffer = &self.buffer;

    /* Byte Loader on Pseudo File ______________________________________________
     *                                                                        */
    if( EmptyFileF ) {
        QUEX_NAME(ByteLoader_Memory_construct)(&self.byte_loader, (const uint8_t*)NULL, 0);
    }
    else if(    LexatomLoaderType == E_LexatomLoader_IConv 
             || LexatomLoaderType == E_LexatomLoader_ICU ) {
        QUEX_NAME(ByteLoader_Memory_construct)(&self.byte_loader, 
                                               &PseudoFileUTF8[0],
                                               &PseudoFileUTF8[PSEUDO_FILE_UTF8_ELEMENT_N]);
    }
    else {
        QUEX_NAME(ByteLoader_Memory_construct)(&self.byte_loader, 
                                               (const uint8_t*)&PseudoFile[0],
                                               (const uint8_t*)&PseudoFile[PSEUDO_FILE_ELEMENT_N]);
    }

    /* LexatomLoaderType _______________________________________________________
     *                                                                        */
    switch( LexatomLoaderType ) {
    case E_LexatomLoader_ICU:
        self.converter      = QUEX_NAME(Converter_ICU_new)("UTF-8", 0);
        self.lexatom_loader = QUEX_NAME(LexatomLoader_new)(&self.byte_loader.base, 
                                                           self.converter);
        break;

    case E_LexatomLoader_IConv:
        self.converter      = QUEX_NAME(Converter_IConv_new)("UTF-8", 0);
        self.lexatom_loader = QUEX_NAME(LexatomLoader_new)(&self.byte_loader.base, 
                                                           self.converter);
        break;

    case E_LexatomLoader_Plain:
        self.converter      = (QUEX_NAME(Converter)*)0; 
        self.lexatom_loader = QUEX_NAME(LexatomLoader_new)(&self.byte_loader.base, 
                                                           self.converter);
        break;

    case E_LexatomLoader_NoByteLoader:
        self.converter      = (QUEX_NAME(Converter)*)0; 
        self.lexatom_loader = QUEX_NAME(LexatomLoader_new)(&self.byte_loader.base, 
                                                           self.converter);
        self.lexatom_loader->byte_loader = (QUEX_NAME(ByteLoader)*)0;
        break;

    case E_LexatomLoader_None:
        self.lexatom_loader = (QUEX_NAME(LexatomLoader)*)0;
        break;
    }

    /* Lexatom Loader __________________________________________________________
     *                                                                        */

    /* Buffer: Filler + Memory _________________________________________________
     *                                                                        */
    QUEX_NAME(Buffer_construct)(&self.buffer, self.lexatom_loader,
                                &self.memory[0], BufferElementN,
                                (QUEX_TYPE_LEXATOM_EXT*)0, E_Ownership_EXTERNAL,
                                (QUEX_NAME(Buffer)*)0); 

    QUEX_NAME(Buffer_callbacks_set)(&self.buffer,
                                         common_on_content_change,
                                         common_on_overflow,
                                         &self.the_aux);

    /* Initial load ___________________________________________________________
     *                                                                       */
    self_load(   LexatomLoaderType == E_LexatomLoader_IConv 
              || LexatomLoaderType == E_LexatomLoader_ICU );

    /* Initialize: 'read_p' and 'lexeme_start_p' _______________________________
     *                                                                        */
    self.buffer._read_p         = QUEX_MAX(&self.buffer._memory._front[1], 
                                           &self.buffer.input.end_p[-ReadPOffset]);
    self.buffer._lexeme_start_p = (LexemePOffset != - 1) ? &self.buffer._memory._front[1 + LexemePOffset]
                                                         : self.buffer._read_p;
    self.buffer._lexeme_start_p = QUEX_MIN(self.buffer._lexeme_start_p, 
                                           &self.buffer.input.end_p[-1]);
    self.buffer._lexeme_start_p = QUEX_MAX(self.buffer._lexeme_start_p, 
                                           &self.buffer._memory._front[1]);

}

static E_LoadResult
self_load(bool ConverterF)
{
    size_t             PositionRegisterN = 5;
    QUEX_TYPE_LEXATOM_EXT* (position_register[5]);
    BufferBefore_t     before;
    E_LoadResult       verdict;
    ptrdiff_t          delta;

    before_setup(&before, &self.buffer, position_register);

    verdict = QUEX_NAME(Buffer_load_forward)(&self.buffer, 
                                             &position_register[0], 
                                             PositionRegisterN);
    delta   = before.read_p - self.buffer._read_p;

    hwut_verify(delta >= 0);
    if( verdict != E_LoadResult_ENCODING_ERROR ) {
        before_check_consistency(&before, delta, verdict, &self.buffer, position_register, ConverterF);
    }

    return verdict;
}

static void
self_DONE()
{
    ptrdiff_t lexeme_p_offset;

    /* (1.a) Normal load 
     *     => E_LoadResult_DONE. */
    self_setup(/* LexemePOffset     */ -1,
               /* ReadPOffset       */ 0,
               /* EmptyFile         */ false,
               /* LexatomLoaderType */ E_LexatomLoader_Plain,
               /* ErrorCodePosition */ -1);
    hwut_verify(self_load(false) == E_LoadResult_DONE);

    for(lexeme_p_offset  = QUEX_SETTING_BUFFER_MIN_FALLBACK_N + 1;
        lexeme_p_offset <= BufferElementN - 2;
        ++lexeme_p_offset) 
    {
        self_setup(/* LexemePOffset     */ lexeme_p_offset,
                   /* ReadPOffset       */ 0,
                   /* EmptyFile         */ false,
                   /* LexatomLoaderType */ E_LexatomLoader_Plain,
                   /* ErrorCodePosition */ -1);
        hwut_verify(self_load(false) == E_LoadResult_DONE);
    }

#   if 0
    for(lexeme_p_offset  = QUEX_SETTING_BUFFER_MIN_FALLBACK_N + 1;
        lexeme_p_offset <= BufferElementN - 2;
        ++lexeme_p_offset) 
    {
        self_setup(/* LexemePOffset     */ lexeme_p_offset,
                   /* ReadPOffset       */ 0,
                   /* EmptyFile         */ false,
                   /* LexatomLoaderType */ E_LexatomLoader_ICU,
                   /* ErrorCodePosition */ -1);
        hwut_verify(self_load(false) == E_LoadResult_DONE);
    }

    for(lexeme_p_offset  = QUEX_SETTING_BUFFER_MIN_FALLBACK_N + 1;
        lexeme_p_offset <= BufferElementN - 2;
        ++lexeme_p_offset) 
    {
        self_setup(/* LexemePOffset     */ lexeme_p_offset,
                   /* ReadPOffset       */ 0,
                   /* EmptyFile         */ false,
                   /* LexatomLoaderType */ E_LexatomLoader_IConv,
                   /* ErrorCodePosition */ -1);
        hwut_verify(self_load(false) == E_LoadResult_DONE);
    }
#   endif
}

static void
self_NO_SPACE_FOR_LOAD()
{    
    ptrdiff_t lexeme_p_offset;

    /* (1.b) Lexeme starts at begin + (<=FallbackN) 
     *     => E_LoadResult_DONE */
    for(lexeme_p_offset  = 0;
        lexeme_p_offset <= QUEX_SETTING_BUFFER_MIN_FALLBACK_N;
        ++lexeme_p_offset) 
    {
        self_setup(/* LexemePOffset     */ lexeme_p_offset,
                   /* ReadPOffset       */ 0,
                   /* EmptyFile         */ false,
                   /* LexatomLoaderType */ E_LexatomLoader_Plain,
                   /* ErrorCodePosition */ -1);
        hwut_verify(self_load(false) == E_LoadResult_OVERFLOW);
    }
}

static void
self_NO_MORE_DATA()
{
    /* (1.d) Nothing loaded (loaded_n == 0)
     *     => E_LoadResult_NO_MORE_DATA */
    self_setup(/* LexemePOffset     */-1, 
               /* ReadPOffset       */ 0,
               /* EmptyFile         */ true,
               /* LexatomLoaderType */ E_LexatomLoader_Plain,
               /* ErrorCodePosition */ -1);
    hwut_verify(self_load(false) == E_LoadResult_NO_MORE_DATA);

    /* (2.a) 1) no lexatom_loader, or
     *       2) no byte byte_loader
     *     => E_LoadResult_NO_MORE_DATA */
    self_setup(/* LexemePOffset     */-1, 
               /* ReadPOffset       */ 0,
               /* EmptyFile         */ false,
               /* LexatomLoaderType */ E_LexatomLoader_None,
               /* ErrorCodePosition */ -1);
    hwut_verify(self_load(false) == E_LoadResult_NO_MORE_DATA);

    self_setup(/* LexemePOffset     */-1,
               /* ReadPOffset       */ 0,
               /* EmptyFile         */ false,
               /* LexatomLoaderType */ E_LexatomLoader_NoByteLoader,
               /* ErrorCodePosition */ -1);
    hwut_verify(self_load(false) == E_LoadResult_NO_MORE_DATA);
}

static void
self_BAD_LEXATOM()
{
    ptrdiff_t read_p_offset;
    ptrdiff_t position;
    uint8_t   backup_byte;

    /* (2.b) _read_p != input.end_p
     *     => '_read_p' pointed to buffer limit code, but it was 
     *        not the buffer's limit
     *     => E_LoadResult_ENCODING_ERROR */
    for(read_p_offset = 1; read_p_offset < BufferElementN; ++read_p_offset) {
        self_setup(/* LexemePOffset     */-1, 
                   /* ReadPOffset       */ read_p_offset,
                   /* EmptyFile         */ false,
                   /* LexatomLoaderType */ E_LexatomLoader_Plain,
                   /* ErrorCodePosition */ -1);
        hwut_verify(self_load(false) == E_LoadResult_ENCODING_ERROR);
    }

    /* (2.c) Encoding Error from lexatom_loader/converter
     *     1) ICU (does not work!)
     *     2) IConv
     *     => E_LoadResult_ENCODING_ERROR */
    for(position = 0; position < PSEUDO_FILE_UTF8_ELEMENT_N; ++position) 
    {
        backup_byte = PseudoFileUTF8[position]; 
        PseudoFileUTF8[position] = 0xFF; /* Is never ok in UTF8 */

        self_setup(/* LexemePOffset     */ -1, 
                   /* ReadPOffset       */ 0,
                   /* EmptyFile         */ false,
                   /* LexatomLoaderType */ E_LexatomLoader_IConv,
                   /* ErrorCodePosition */ position);

        while( self.buffer.input.lexatom_index_end_of_stream == -1 ) {
            self.buffer._read_p         = QUEX_MIN(self.buffer._memory._back,
                                                   self.buffer.input.end_p);
            self.buffer._lexeme_start_p = &self.buffer._read_p[-1];
 
            if( self_load(true) == E_LoadResult_ENCODING_ERROR) break;
        }

        PseudoFileUTF8[position] = backup_byte;
    }

#   if 0
    for(position = 0; position < PSEUDO_FILE_UTF8_ELEMENT_N; ++position) 
    {
        backup_byte = PseudoFileUTF8[position]; 
        PseudoFileUTF8[position] = 0xFF; /* Is never ok in UTF8 */
        self_setup(/* LexemePOffset     */ -1, 
                   /* ReadPOffset       */ 0,
                   /* EmptyFile         */ false,
                   /* LexatomLoaderType */ E_LexatomLoader_ICU,
                   /* ErrorCodePosition */ position);

        while( self.buffer.input.lexatom_index_end_of_stream == -1 ) {
            self.buffer._read_p         = QUEX_MIN(self.buffer._memory._back,
                                                   self.buffer.input.end_p);
            self.buffer._lexeme_start_p = &self.buffer._read_p[-1];
            if( self_load(true) == E_LoadResult_ENCODING_ERROR) break;
        }

        PseudoFileUTF8[position] = backup_byte;
    }
#   endif
}

