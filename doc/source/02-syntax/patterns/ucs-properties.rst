Unicode Properties
##################

Unicode :cite:`Unicode2015` is distinguished from other coding standards not
only with respect to its level of completeness including all possibly used
character sets. Moreover, much effort has been accomplished in categorizing
characters, providing terminology for concepts related to letter systems and
defining *character properties*.  The most important property for a lexical
analyzer is the 'code point', i.e. the integer value that represents a
character. However, there are other interesting properties that simplify the
description of regular expressions.

Unicode Standard Properties can be accessed through ``\P{..}`` expressions,
where the ``P`` stands for property. Properties can be divided into two
categories: 

.. describe:: Binary Properties, 

  i.e. properties that a character either has or has not. For example, a
  character is either a white space character or it is not. Sets of characters
  having a binary property ``binary_property`` can be accessed through
  ``\P{binary_property}``.
 
.. describe:: Non-Binary Properties, 

  i.e. properties that require a particular value related to it. For example,
  each character belongs to a certain script. A character belonging to the
  Greek script has the property 'Script=Greek'. Sets of characters that have a
  certain property setting can be accessed via ``\P{property=value}``.

The result of a ``\P{...}`` expression is always a *set of characters*.
Therefore, it cannot be used inside a quoted string expression.  For
convenience, the properties 'Name' and 'General_Category' are provided through
the shortcuts ``\N{...}`` and ``\G{...}``. Thus, ``\N{MIDDLE DOT}`` is a
shorthand for ``\P{Name=MIDDLE DOT}`` and ``\G{Uppercase_Letter}`` is a
shorthand for ``\P{General_Category=Uppercase_Letter}``. 

Unicode 8.0 provides more than 17000 character names. To review the complete
list the standard literature may be referred [#f1]_ . Note also, that names as
defined in Unicode 1.0 can be accessed through the 'Unicode_1_Name' property.
This property also contains names of control functions according to ISO 6429
:cite:`ISO1992_6429`.  Section :ref:`sec:appendix-property-general-category`
provides detailed information about the property ``General_Category``. At this
place, information about likely-to-be-used properties is listed. 

As an option to facilitate the specification of property values, wildcards may
be used inside the property expressions. The ``*``, ``?`` and simple character
sets such as as ``[AEIOUX-Z]`` for the characters ``A``, ``E``, ``I``, ``O``,
``U``, ``X``, ``Y``, and ``Z``. If the first character is an ``!`` then the
complementary character set is considered.  This is conform with Unix file name
matching :ref:`Robbins1995practical`.  

The following item list exposes some of the supported Unicode Character
Properties.  The current version of Quex is based on Unicode 8.0. It uses the
raw databases as provided by the Unicode Consortium and it is likely that 
the property system of any later standard is integrated as soon as it is in a
major state [#f2]_ . 

Unicode Character Properties are used to define *sets of characters* to be
matched during lexical analysis. This excludes some properties from
consideration, namely the properties tagged as `string` property types and the
'quick-check' properties (Unicode Technical Report UCS #15). The expressions in
brackets are the aliases that may be used as a shorthand for the full name of
the property.

.. describe:: Binary Properties

    ASCII_Hex_Digit(AHex), Alphabetic(Alpha), Bidi_Control(Bidi_C), Bidi_Mirrored(Bidi_M), Composition_Exclusion(CE), Dash(Dash), Default_Ignorable_Code_Point(DI), Deprecated(Dep), Diacritic(Dia), Expands_On_NFC(XO_NFC), Expands_On_NFD(XO_NFD), Expands_On_NFKC(XO_NFKC), Expands_On_NFKD(XO_NFKD), Extender(Ext), Full_Composition_Exclusion(Comp_Ex), Grapheme_Base(Gr_Base), Grapheme_Extend(Gr_Ext), Grapheme_Link(Gr_Link), Hex_Digit(Hex), Hyphen(Hyphen), IDS_Binary_Operator(IDSB), IDS_Trinary_Operator(IDST), ID_Continue(IDC), ID_Start(IDS), Ideographic(Ideo), Join_Control(Join_C), Logical_Order_Exception(LOE), Lowercase(Lower), Math(Math), Noncharacter_Code_Point(NChar), Other_Alphabetic(OAlpha), Other_Default_Ignorable_Code_Point(ODI), Other_Grapheme_Extend(OGr_Ext), Other_ID_Continue(OIDC), Other_ID_Start(OIDS), Other_Lowercase(OLower), Other_Math(OMath), Other_Uppercase(OUpper), Pattern_Syntax(Pat_Syn), Pattern_White_Space(Pat_WS), Quotation_Mark(QMark), Radical(Radical), STerm(STerm), Soft_Dotted(SD), Terminal_Punctuation(Term), Unified_Ideograph(UIdeo), Uppercase(Upper), Variation_Selector(VS), White_Space(WSpace), XID_Continue(XIDC), XID_Start(XIDS), 

.. describe:: Non-Binary Properties

    Age(age), Bidi_Class(bc), Bidi_Mirroring_Glyph(bmg), Block(blk), Canonical_Combining_Class(ccc), Case_Folding(cf), Decomposition_Mapping(dm), Decomposition_Type(dt), East_Asian_Width(ea), FC_NFKC_Closure(FC_NFKC), General_Category(gc), Grapheme_Cluster_Break(GCB), Hangul_Syllable_Type(hst), ISO_Comment(isc), Joining_Group(jg), Joining_Type(jt), Line_Break(lb), Lowercase_Mapping(lc), NFC_Quick_Check(NFC_QC), NFD_Quick_Check(NFD_QC), NFKC_Quick_Check(NFKC_QC), NFKD_Quick_Check(NFKD_QC), Name(na), Numeric_Type(nt), Numeric_Value(nv), Script(sc), Sentence_Break(SB), Simple_Case_Folding(sfc), Simple_Lowercase_Mapping(slc), Simple_Titlecase_Mapping(stc), Simple_Uppercase_Mapping(suc), Special_Case_Condition(scc), Titlecase_Mapping(tc), Unicode_1_Name(na1), Unicode_Radical_Stroke(URS), Uppercase_Mapping(uc), Word_Break(WB), 

Binary properties can simply be applied using an expression such as
``\P{ID_Start}``, which results in the set of characters that can build the
beginning of an identifier in usual programming languages. Non-binary
properties require values and are specified in the form ``\P{Property=Value}``.
The supported values for each non-binary property are the following:

.. describe:: Age

    ``1.1``, ``2.0``, ``2.1``, ``3.0``, ``3.1``, ``3.2``, ``4.0``, ``4.1``, ``5.0``...

.. describe:: Bidi_Class

    ``Arabic_Letter(AL)``, ``Arabic_Number(AN)``, ``Boundary_Neutral(BN)``, ``Common_Separator(CS)``, ``European_Number(EN)``, ``European_Separator(ES)``, ``European_Terminator(ET)``, ``Left_To_Right(L)``, ``Left_To_Right_Embedding(LRE)``, ``Left_To_Right_Override(LRO)``, ``Nonspacing_Mark(NSM)``, ``Other_Neutral(ON)``, ``Paragraph_Separator(B)``, ``Pop_Directional_Format(PDF)``, ``Right_To_Left(R)``, ``Right_To_Left_Embedding(RLE)``, ``Right_To_Left_Override(RLO)``, ``Segment_Separator(S)``, ``White_Space(WS)``.

.. describe:: Bidi_Mirroring_Glyph

    (not supported)

.. describe:: Block

    ``Aegean_Numbers``, ``Alphabetic_Presentation_Forms``, ``Ancient_Greek_Musical_Notation``, ``Ancient_Greek_Numbers``, ``Arabic``, ``Arabic_Presentation_Forms-A``, ``Arabic_Presentation_Forms-B``, ``Arabic_Supplement``, ``Armenian``, ``Arrows``, ``Balinese``, ``Basic_Latin``, ``Bengali``, ``Block_Elements``, ``Bopomofo``, ``Bopomofo_Extended``, ``Box_Drawing``, ``Braille_Patterns``, ``Buginese``, ``Buhid``, ``Byzantine_Musical_Symbols``, ``CJK_Compatibility``, ``CJK_Compatibility_Forms``, ``CJK_Compatibility_Ideographs``, ``CJK_Compatibility_Ideographs_Supplement``, ``CJK_Radicals_Supplement``, ``CJK_Strokes``, ``CJK_Symbols_and_Punctuation``, ``CJK_Unified_Ideographs``, ``CJK_Unified_Ideographs_Extension_A``, ``CJK_Unified_Ideographs_Extension_B``, ``Cherokee``, ``Combining_Diacritical_Marks``, ``Combining_Diacritical_Marks_Supplement``, ``Combining_Diacritical_Marks_for_Symbols``, ``Combining_Half_Marks``, ``Control_Pictures``, ``Coptic``, ``Counting_Rod_Numerals``, ``Cuneiform``, ``Cuneiform_Numbers_and_Punctuation``, ``Currency_Symbols``, ``Cypriot_Syllabary``, ``Cyrillic``, ``Cyrillic_Supplement``, ``Deseret``, ``Devanagari``, ``Dingbats``, ``Enclosed_Alphanumerics``, ``Enclosed_CJK_Letters_and_Months``, ``Ethiopic``, ``Ethiopic_Extended``, ``Ethiopic_Supplement``, ``General_Punctuation``, ``Geometric_Shapes``, ``Georgian``, ``Georgian_Supplement``, ``Glagolitic``, ``Gothic``, ``Greek_Extended``, ``Greek_and_Coptic``, ``Gujarati``, ``Gurmukhi``, ``Halfwidth_and_Fullwidth_Forms``, ``Hangul_Compatibility_Jamo``, ``Hangul_Jamo``, ``Hangul_Syllables``, ``Hanunoo``, ``Hebrew``, ``High_Private_Use_Surrogates``, ``High_Surrogates``, ``Hiragana``, ``IPA_Extensions``, ``Ideographic_Description_Characters``, ``Kanbun``, ``Kangxi_Radicals``, ``Kannada``, ``Katakana``, ``Katakana_Phonetic_Extensions``, ``Kharoshthi``, ``Khmer``, ``Khmer_Symbols``, ``Lao``, ``Latin-1_Supplement``, ``Latin_Extended-A``, ``Latin_Extended-B``, ``Latin_Extended-C``, ``Latin_Extended-D``, ``Latin_Extended_Additional``, ``Letterlike_Symbols``, ``Limbu``, ``Linear_B_Ideograms``, ``Linear_B_Syllabary``, ``Low_Surrogates``, ``Malayalam``, ``Mathematical_Alphanumeric_Symbols``, ``Mathematical_Operators``, ``Miscellaneous_Mathematical_Symbols-A``, ``Miscellaneous_Mathematical_Symbols-B``, ``Miscellaneous_Symbols``, ``Miscellaneous_Symbols_and_Arrows``, ``Miscellaneous_Technical``, ``Modifier_Tone_Letters``, ``Mongolian``, ``Musical_Symbols``, ``Myanmar``, ``NKo``, ``New_Tai_Lue``, ``Number_Forms``, ``Ogham``, ``Old_Italic``, ``Old_Persian``, ``Optical_Character_Recognition``, ``Oriya``, ``Osmanya``, ``Phags-pa``, ``Phoenician``, ``Phonetic_Extensions``, ``Phonetic_Extensions_Supplement``, ``Private_Use_Area``, ``Runic``, ``Shavian``, ``Sinhala``, ``Small_Form_Variants``, ``Spacing_Modifier_Letters``, ``Specials``, ``Superscripts_and_Subscripts``, ``Supplemental_Arrows-A``, ``Supplemental_Arrows-B``, ``Supplemental_Mathematical_Operators``, ``Supplemental_Punctuation``, ``Supplementary_Private_Use_Area-A``, ``Supplementary_Private_Use_Area-B``, ``Syloti_Nagri``, ``Syriac``, ``Tagalog``, ``Tagbanwa``, ``Tags``, ``Tai_Le``, ``Tai_Xuan_Jing_Symbols``, ``Tamil``, ``Telugu``, ``Thaana``, ``Thai``, ``Tibetan``, ``Tifinagh``, ``Ugaritic``, ``Unified_Canadian_Aboriginal_Syllabics``, ``Variation_Selectors``, ``Variation_Selectors_Supplement``, ``Vertical_Forms``, ``Yi_Radicals``, ``Yi_Syllables``, ``Yijing_Hexagram_Symbols(n/a)``.

.. describe:: Canonical_Combining_Class

    ``0``, ``1``, ``10``, ``103``, ``107``, ``11``, ``118``, ``12``, ``122``, ``129``, ``13``, ``130``, ``132``, ``14``, ``15``, ``16``, ``17``, ``18``, ``19``, ``20``, ``202``, ``21``, ``216``, ``218``, ``22``, ``220``, ``222``, ``224``, ``226``, ``228``, ``23``, ``230``, ``232``, ``233``, ``234``, ``24``, ``240``, ``25``, ``26``, ``27``, ``28``, ``29``, ``30``, ``31``, ``32``, ``33``, ``34``, ``35``, ``36``, ``7``, ``8``, ``84``, ``9``, ``91``.

.. describe:: Case_Folding

    (not supported)

.. describe:: Decomposition_Mapping

    (not supported)

.. describe:: Decomposition_Type

    ``Canonical(can)``, ``Circle(enc)``, ``Compat(com)``, ``Final(fin)``, ``Font(font)``, ``Fraction(fra)``, ``Initial(init)``, ``Isolated(iso)``, ``Medial(med)``, ``Narrow(nar)``, ``Nobreak(nb)``, ``Small(sml)``, ``Square(sqr)``, ``Sub(sub)``, ``Super(sup)``, ``Vertical(vert)``, ``Wide(wide)``.

.. describe:: East_Asian_Width

    ``A``, ``F``, ``H``, ``N``, ``Na``, ``W``.

.. describe:: FC_NFKC_Closure

    (not supported)

.. describe:: General_Category

    ``Close_Punctuation(Pe)``, ``Connector_Punctuation(Pc)``, ``Control(Cc)``, ``Currency_Symbol(Sc)``, ``Dash_Punctuation(Pd)``, ``Decimal_Number(Nd)``, ``Enclosing_Mark(Me)``, ``Final_Punctuation(Pf)``, ``Format(Cf)``, ``Initial_Punctuation(Pi)``, ``Letter_Number(Nl)``, ``Line_Separator(Zl)``, ``Lowercase_Letter(Ll)``, ``Math_Symbol(Sm)``, ``Modifier_Letter(Lm)``, ``Modifier_Symbol(Sk)``, ``Nonspacing_Mark(Mn)``, ``Open_Punctuation(Ps)``, ``Other_Letter(Lo)``, ``Other_Number(No)``, ``Other_Punctuation(Po)``, ``Other_Symbol(So)``, ``Paragraph_Separator(Zp)``, ``Private_Use(Co)``, ``Space_Separator(Zs)``, ``Spacing_Mark(Mc)``, ``Surrogate(Cs)``, ``Titlecase_Letter(Lt)``, ``Uppercase_Letter(Lu)``.

.. describe:: Grapheme_Cluster_Break

    ``CR(CR)``, ``Control(CN)``, ``Extend(EX)``, ``L(L)``, ``LF(LF)``, ``LV(LV)``, ``LVT(LVT)``, ``T(T)``, ``V(V)``.

.. describe:: Hangul_Syllable_Type

    ``L``, ``LV``, ``LVT``, ``T``, ``V``.

.. describe:: ISO_Comment

    ``*``, ``Abkhasian``, ``Adrar_yaj``, ``Aristeri_keraia``, ``Assamese``, ``Byelorussian``, ``Dasia``, ``Dexia_keraia``, ``Dialytika``, ``Enn``, ``Enotikon``, ``Erotimatiko``, ``Faliscan``, ``German``, ``Greenlandic``, ``Icelandic``, ``Kaeriten``, ``Kanbun_Tateten``, ``Khutsuri``, ``Maatham``, ``Mandarin_Chinese_first_tone``, ``Mandarin_Chinese_fourth_tone``, ``Mandarin_Chinese_light_tone``, ``Mandarin_Chinese_second_tone``, ``Mandarin_Chinese_third_tone``, ``Merpadi``, ``Naal``, ``Oscan``, ``Oxia,_Tonos``, ``Patru``, ``Psili``, ``Rupai``, ``Sami``, ``Serbocroatian``, ``Tuareg_yab``, ``Tuareg_yaw``, ``Ukrainian``, ``Umbrian``, ``Varavu``, ``Varia``, ``Varudam``, ``Vietnamese``, ``Vrachy``, ``a``, ``aa``, ``ae``, ``ai``, ``ang_kang_ye``, ``ang_kang_yun``, ``anusvara``, ``ardhacandra``, ``ash_*``, ``au``, ``b_*``, ``bb_*``, ``bha``, ``break``, ``bs_*``, ``bub_chey``, ``c_*``, ``candrabindu``, ``cha``, ``chang_tyu``, ``che_go``, ``che_ta``, ``che_tsa_chen``, ``chu_chen``, ``colon``, ``d_*``, ``danda``, ``dd_*``, ``dda``, ``ddha``, ``deka_chig``, ``deka_dena``, ``deka_nyi``, ``deka_sum``, ``dena_chig``, ``dena_nyi``, ``dena_sum``, ``dha``, ``di_ren_*``, ``dong_tsu``, ``dorje``, ``dorje_gya_dram``, ``double_danda``, ``drilbu``, ``drul_shey``, ``du_ta``, ``dzu_ta_me_long_chen``, ``dzu_ta_shi_mig_chen``, ``e``, ``escape``, ``g_*``, ``gg_*``, ``gha``, ``golden_number_17``, ``golden_number_18``, ``golden_number_19``, ``gs_*``, ``gug_ta_ye``, ``gug_ta_yun``, ``gup``, ``gya_tram_shey``, ``h_*``, ``halfwidth_katakana-hiragana_semi-voiced_sound_mark``, ``halfwidth_katakana-hiragana_voiced_sound_mark``, ``harpoon_yaz``, ``hdpe``, ``hlak_ta``, ``honorific_section``, ``hwair``, ``i``, ``ii``, ``independent``, ``j_*``, ``je_su_nga_ro``, ``jha``, ``ji_ta``, ``jj_*``, ``k_*``, ``ka_sho_yik_go``, ``ka_shog_gi_go_gyen``, ``kha``, ``kur_yik_go``, ``kuruka``, ``kuruka_shi_mik_chen``, ``kyu_pa``, ``l_*``, ``lakkhang_yao``, ``lazy_S``, ``lb_*``, ``ldpe``, ``lg_*``, ``lh_*``, ``line-breaking_hyphen``, ``lm_*``, ``lp_*``, ``ls_*``, ``lt_*``, ``m_*``, ``mai_taikhu``, ``mai_yamok``, ``mar_tse``, ``mathematical_use``, ``n_*``, ``nam_chey``, ``nan_de``, ``ng_*``, ``nge_zung_gor_ta``, ``nge_zung_nyi_da``, ``nh_*``, ``nikkhahit``, ``nj_*``, ``nna``, ``norbu``, ``norbu_nyi_khyi``, ``norbu_shi_khyi``, ``norbu_sum_khyi``, ``not_independent``, ``nukta``, ``nyam_yig_gi_go_gyen``, ``nyi_da_na_da``, ``nyi_shey``, ``nyi_tsek_shey``, ``o``, ``oe``, ``or_shuruq``, ``other``, ``p_*``, ``paiyan_noi``, ``pause``, ``pema_den``, ``pete``, ``pha``, ``phurba``, ``pp``, ``ps``, ``pug``, ``punctuation_ring``, ``pvc``, ``r_*``, ``ren_*``, ``ren_di_*``, ``ren_ren_*``, ``ren_tian_*``, ``repha``, ``rinchen_pung_shey``, ``s_*``, ``sara_ai_mai_malai``, ``sara_ai_mai_muan``, ``sara_uue``, ``section``, ``sha``, ``shey``, ``ss_*``, ``ssa``, ``t_*``, ``tamatart``, ``ter_tsek``, ``ter_yik_go_a_thung``, ``ter_yik_go_wum_nam_chey_ma``, ``ter_yik_go_wum_ter_tsek_ma``, ``tha``, ``tian_ren_*``, ``trachen_char_ta``, ``tru_chen_ging``, ``tru_me_ging``, ``tsa_tru``, ``tsek``, ``tsek_shey``, ``tsek_tar``, ``tta``, ``ttha``, ``u``, ``uu``, ``virama``, ``visarga``, ``vocalic_l``, ``vocalic_ll``, ``vocalic_r``, ``vocalic_rr``, ``yang_ta``, ``yar_tse``, ``yik_go_dun_ma``, ``yik_go_kab_ma``, ``yik_go_pur_shey_ma``, ``yik_go_tsek_shey_ma``.

.. describe:: Joining_Group

    ``Ain``, ``Alaph``, ``Alef``, ``Beh``, ``Beth``, ``Dal``, ``Dalath_Rish``, ``E``, ``Fe``, ``Feh``, ``Final_Semkath``, ``Gaf``, ``Gamal``, ``Hah``, ``Hamza_On_Heh_Goal``, ``He``, ``Heh``, ``Heh_Goal``, ``Heth``, ``Kaf``, ``Kaph``, ``Khaph``, ``Knotted_Heh``, ``Lam``, ``Lamadh``, ``Meem``, ``Mim``, ``Noon``, ``Nun``, ``Pe``, ``Qaf``, ``Qaph``, ``Reh``, ``Reversed_Pe``, ``Sad``, ``Sadhe``, ``Seen``, ``Semkath``, ``Shin``, ``Swash_Kaf``, ``Syriac_Waw``, ``Tah``, ``Taw``, ``Teh_Marbuta``, ``Teth``, ``Waw``, ``Yeh``, ``Yeh_Barree``, ``Yeh_With_Tail``, ``Yudh``, ``Yudh_He``, ``Zain``, ``Zhain(n/a)``.

.. describe:: Joining_Type

    ``C``, ``D``, ``R``, ``T``.

.. describe:: Line_Break

    ``AI``, ``AL``, ``B2``, ``BA``, ``BB``, ``BK``, ``CB``, ``CL``, ``CM``, ``CR``, ``EX``, ``GL``, ``H2(H2)``, ``H3(H3)``, ``HY``, ``ID``, ``IN``, ``IS``, ``JL(JL)``, ``JT(JT)``, ``JV(JV)``, ``LF``, ``NL``, ``NS``, ``NU``, ``OP``, ``PO``, ``PR``, ``QU``, ``SA``, ``SG``, ``SP``, ``SY``, ``WJ``, ``XX``, ``ZW``.

.. describe:: Lowercase_Mapping

    (not supported)

.. describe:: NFC_Quick_Check

    (not supported)

.. describe:: NFD_Quick_Check

    (not supported)

.. describe:: NFKC_Quick_Check

    (not supported)

.. describe:: NFKD_Quick_Check

    (not supported)

.. describe:: Name

    (see Unicode Standard Literature)

.. describe:: Numeric_Type

    ``Decimal(De)``, ``Digit(Di)``, ``Numeric(Nu)``.

.. describe:: Numeric_Value

    ``0``, ``1``, ``2``, ``3``, ``4``, ``5``, ``6``, ``7``, ``8``, ``9``.

.. describe:: Script

    ``Arabic(Arab)``, ``Armenian(Armn)``, ``Balinese(Bali)``, ``Bengali(Beng)``, ``Bopomofo(Bopo)``, ``Braille(Brai)``, ``Buginese(Bugi)``, ``Buhid(Buhd)``, ``Canadian_Aboriginal(Cans)``, ``Cherokee(Cher)``, ``Common(Zyyy)``, ``Coptic(Copt)``, ``Cuneiform(Xsux)``, ``Cypriot(Cprt)``, ``Cyrillic(Cyrl)``, ``Deseret(Dsrt)``, ``Devanagari(Deva)``, ``Ethiopic(Ethi)``, ``Georgian(Geor)``, ``Glagolitic(Glag)``, ``Gothic(Goth)``, ``Greek(Grek)``, ``Gujarati(Gujr)``, ``Gurmukhi(Guru)``, ``Han(Hani)``, ``Hangul(Hang)``, ``Hanunoo(Hano)``, ``Hebrew(Hebr)``, ``Hiragana(Hira)``, ``Inherited(Qaai)``, ``Kannada(Knda)``, ``Katakana(Kana)``, ``Kharoshthi(Khar)``, ``Khmer(Khmr)``, ``Lao(Laoo)``, ``Latin(Latn)``, ``Limbu(Limb)``, ``Linear_B(Linb)``, ``Malayalam(Mlym)``, ``Mongolian(Mong)``, ``Myanmar(Mymr)``, ``New_Tai_Lue(Talu)``, ``Nko(Nkoo)``, ``Ogham(Ogam)``, ``Old_Italic(Ital)``, ``Old_Persian(Xpeo)``, ``Oriya(Orya)``, ``Osmanya(Osma)``, ``Phags_Pa(Phag)``, ``Phoenician(Phnx)``, ``Runic(Runr)``, ``Shavian(Shaw)``, ``Sinhala(Sinh)``, ``Syloti_Nagri(Sylo)``, ``Syriac(Syrc)``, ``Tagalog(Tglg)``, ``Tagbanwa(Tagb)``, ``Tai_Le(Tale)``, ``Tamil(Taml)``, ``Telugu(Telu)``, ``Thaana(Thaa)``, ``Thai(Thai)``, ``Tibetan(Tibt)``, ``Tifinagh(Tfng)``, ``Ugaritic(Ugar)``, ``Yi(Yiii)``.

.. describe:: Sentence_Break

    ``ATerm(AT)``, ``Close(CL)``, ``Format(FO)``, ``Lower(LO)``, ``Numeric(NU)``, ``OLetter(LE)``, ``STerm(ST)``, ``Sep(SE)``, ``Sp(SP)``, ``Upper(UP)``.

.. describe:: Simple_Case_Folding

    (not supported)

.. describe:: Simple_Lowercase_Mapping

    (not supported)

.. describe:: Simple_Titlecase_Mapping

    (not supported)

.. describe:: Simple_Uppercase_Mapping

    (not supported)

.. describe:: Special_Case_Condition

    (not supported)

.. describe:: Titlecase_Mapping

    (not supported)

.. describe:: Unicode_1_Name

    (see Unicode Standard Literature)

.. describe:: Unicode_Radical_Stroke

    (not supported)

.. describe:: Uppercase_Mapping

    (not supported)

.. describe:: Word_Break

    ``ALetter(LE)``, ``ExtendNumLet(EX)``, ``Format(FO)``, ``Katakana(KA)``, ``MidLetter(ML)``, ``MidNum(MN)``, ``Numeric(NU)``.


.. rubric:: Footnotes

.. [#f1] Alternatively, the file ``UnicodeData.txt`` that comes with the quex
         application contains equally all possible character names.

.. [#f2] Section :ref:`sec:update-unicode-db` explains how other (newer)
         versions of the Unicode Database may be applied. 
