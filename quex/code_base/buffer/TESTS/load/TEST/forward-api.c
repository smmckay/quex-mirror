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
 *            (2.a) 1) no filler, or
 *                  2) no byte loader
 *                => E_LoadResult_NO_MORE_DATA
 *            (2.b) _read_p != input.end_p
 *                => '_read_p' pointed to buffer limit code, but it was 
 *                   not the buffer's limit
 *                => E_LoadResult_BAD_LEXATOM
 *            (2.c) Encoding Error from filler/converter
 *                1) ICU
 *                2) IConv
 *                => E_LoadResult_BAD_LEXATOM
 *
 * E_LoadResult_NO_MORE_DATA => EOS must be set.
 *
 */

#include "commonly_pasted.c"
#include <quex/code_base/buffer/lexatoms/LexatomLoader>

typedef enum {
    E_Converter_ICU,
    E_Converter_IConv,
    E_Converter_None
} E_Converter;

static struct {
    QUEX_NAME(Buffer)             buffer;
    QUEX_NAME(ByteLoader_Memory)  loader;
    QUEX_NAME(LexatomLoader)*     filler;
    QUEX_NAME(Converter)*         converter;
    QUEX_TYPE_LEXATOM             memory[32]; /* > anything ever needed.     */
} self;

static void         self_setup(ptrdiff_t   LexemePOffset,  /* = LexemeP - Buffer's Front */    
                               ptrdiff_t   ReadPOffset,    /* = EndP - ReadP             */
                               bool        EmptyFileF,
                               E_Converter Converter, 
                               ptrdiff_t   ErrorCodePosition);
static E_LoadResult self_load();
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

    return 0;
}

static void
self_setup(ptrdiff_t   LexemePOffset,  /* = LexemeP - Buffer's Front */    
           ptrdiff_t   ReadPOffset,    /* = EndP - ReadP             */
           bool        EmptyFileF,
           E_Converter Converter, 
           ptrdiff_t   ErrorCodePosition)
{
    size_t         tbuffer_size = 0;
    const uint8_t* content_begin, content_end;

    /* Converter ______________________________________________________________
     *                                                                       */
    switch( Converter ) {
    case E_Converter_ICU:
        self.converter = QUEX_NAME(Converter_ICU_new)("UTF-8", 0);
        content_begin  = &PseudoFileUTF8[0];
        content_end    = &PseudoFileUTF8[PSEUDO_FILE_UTF8_ELEMENT_N]; 
        tbuffer_size   = 7;
        break;

    case E_Converter_IConv:
        self.converter = QUEX_NAME(Converter_IConv_new)("UTF-8", 0);
        content_begin  = &PseudoFileUTF8[0];
        content_end    = &PseudoFileUTF8[PSEUDO_FILE_UTF8_ELEMENT_N]; 
        tbuffer_size   = 7;
        break;

    case E_Converter_None:
        self.converter = (QUEX_NAME(Converter)*)0; 
        content_begin  = &PseudoFile[0];
        content_end    = &PseudoFile[PSEUDO_FILE_ELEMENT_N]; 
        tbuffer_size   = 0;
        break;
    }

    /* Resource: Pseudo File __________________________________________________
     *                                                                       */
    if( EmptyFileF ) {
        QUEX_NAME(ByteLoader_Memory_construct)(&self.loader, (const uint8_t*)NULL, 0);
    }
    else {
        QUEX_NAME(ByteLoader_Memory_construct)(&self.loader, content_begin, content_end);
    }

    /* Lexatom Loader _________________________________________________________
     *                                                                       */
    self.filler = FillerF ? QUEX_NAME(LexatomLoader_new)(&self.loader.base, self.converter, tbuffer_size)
                          : 0;

    /* Buffer: Filler + Memory ________________________________________________
     *                                                                       */
    QUEX_NAME(Buffer_construct)(&self.buffer, self.filler,
                                &self.memory[0], BufferElementN,
                                (QUEX_TYPE_LEXATOM*)0, E_Ownership_EXTERNAL); 

    self.buffer.on_overflow       = common_on_overflow;
    self.buffer.on_content_change = common_on_content_change;


    /* Initialize: 'read_p' and 'lexeme_start_p' ______________________________
     *                                                                       */
    self.buffer._read_p         = &self.buffer.input.end_p[-ReadPOffset];
    self.buffer._lexeme_start_p = (LexemePOffset != - 1) ? &self.buffer._front[1] + LexemePOffset;
                                                         : self.buffer._read_p;
}

static E_LoadResult
self_load()
{
    size_t             PositionRegisterN = 5;
    QUEX_TYPE_LEXATOM* (position_register[5]);
    BufferBefore_t     before;
    E_LoadResult       verdict;
    ptrdiff_t          delta;

    before_setup(&before, buffer, position_register);

    verdict = QUEX_NAME(Buffer_load_forward)(buffer, &position_register[0], 
                                             PositionRegisterN);
    delta   = before.read_p - buffer->_read_p;

    hwut_verify(delta >= 0);
    before_check_consistency(&before, delta, verdict, buffer, position_register);

    return verdict;
}

static void
self_DONE()
{
    /* (1.a) Normal load 
     *     => E_LoadResult_DONE. */
    self_setup(/* LexemePOffset     */ -1,
               /* ReadPOffset       */ 0,
               /* EmptyFile         */ false,
               /* Converter         */ E_Converter_None);
    /* ErrorCodePosition */ position);
    hwut_verify(load() == E_LoadResult_DONE);

    /* (1.b) Lexeme starts at begin + (<=FallbackN) 
     *     => E_LoadResult_DONE */
    for(lexeme_p_offset  = 1;
        lexeme_p_offset <= QUEX_SETTING_BUFFER_MIN_FALLBACK_N;
        ++lexeme_p_offset) 
    {
        self_setup(/* LexemePOffset     */ lexeme_p_offset,
                   /* ReadPOffset       */ 0,
                   /* EmptyFile         */ false);
        /* Converter         */ E_Converter_None);
        /* ErrorCodePosition */ position);
        hwut_verify(load() == E_LoadResult_DONE);
    }
}

static void
self_NO_SPACE_FOR_LOAD()
{    
    /* (1.c) Lexeme starts at begin 
     *     => E_LoadResult_NO_SPACE_FOR_LOAD */
    self_setup(/* LexemePOffset */ 0,
               /* ReadPOffset   */ 0,
               /* EmptyFile     */ false);
    /* Converter     */ E_Converter_None);
    /* ErrorCodePosition */ position);
    hwut_verify(load() == E_LoadResult_NO_SPACE_FOR_LOAD);
}

static void
self_NO_MORE_DATA()
{
    /* (1.d) Nothing loaded (loaded_n == 0)
     *     => E_LoadResult_NO_MORE_DATA */
    self_setup(/* LexemePOffset */-1, 
               /* ReadPOffset   */ 0,
               /* EmptyFile     */ true);
    /* Converter     */ E_Converter_None);
    /* ErrorCodePosition */ position);
    hwut_verify(load() == E_LoadResult_NO_MORE_DATA);

    /* (2.a) 1) no filler, or
     *       2) no byte loader
     *     => E_LoadResult_NO_MORE_DATA */
    self_setup(/* LexemePOffset */-1, 
               /* ReadPOffset   */ 0,
               /* EmptyFile     */ false,
               /* Converter     */ E_Converter_None);
    /* ErrorCodePosition */ position);
    hwut_verify(load() == E_LoadResult_NO_MORE_DATA);

    self_setup(/* LexemePOffset     */-1,
               /* ReadPOffset       */ 0,
               /* EmptyFile         */ false,
               /* Converter         */ E_Converter_None,
               /* ErrorCodePosition */ position);
    hwut_verify(load() == E_LoadResult_NO_MORE_DATA);
}

static void
self_BAD_LEXATOM()
{
    /* (2.b) _read_p != input.end_p
     *     => '_read_p' pointed to buffer limit code, but it was 
     *        not the buffer's limit
     *     => E_LoadResult_BAD_LEXATOM */
    for(read_p_offset = 1; read_p_offset < buffer_size, ++read_p_offset) {
        self_setup(/* LexemePOffset     */-1, 
                   /* ReadPOffset       */ read_p_offset,
                   /* EmptyFile         */ false);
        /* Converter         */ E_Converter_None,
            /* ErrorCodePosition */ position);
        hwut_verify(load() == E_LoadResult_BAD_LEXATOM);
    }

    /* (2.c) Encoding Error from filler/converter
     *     1) ICU
     *     2) IConv
     *     => E_LoadResult_BAD_LEXATOM */
    for(position = 0; position < utf8_file_size; ++position) 
    {
        self_setup(/* LexemePOffset     */ -1, 
                   /* ReadPOffset       */ 0,
                   /* EmptyFile         */ false,
                   /* Converter         */ E_Converter_ICU,
                   /* ErrorCodePosition */ position);
        hwut_verify(load() == E_LoadResult_BAD_LEXATOM);
        self_setup(/* LexemePOffset     */ -1, 
                   /* ReadPOffset       */ 0,
                   /* EmptyFile         */ false,
                   /* Converter         */ E_Converter_IConv,
                   /* ErrorCodePosition */ position);
        hwut_verify(load() == E_LoadResult_BAD_LEXATOM);
    }
}

