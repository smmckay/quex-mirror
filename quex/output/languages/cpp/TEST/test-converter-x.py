#! /usr/bin/env python
import os
import sys
sys.path.append(os.environ["QUEX_PATH"])
import quex.output.analyzer.lexeme_converter as lexeme_converter
import quex.output.languages.core as languages
import quex.blackboard

if "--hwut-info" in sys.argv:
    print "Converter: Determine UTF-8 Range Map for Codec"
    print "CHOICES:   1, 2, 3;"

quex.blackboard.setup.language_db = languages.db["C++"]()

def test(Msg, ConversionInfoList):
    print
    print "(*) " + Msg
    print 
    conversion_info = []
    for x in ConversionInfoList:
        info = lexeme_converter.ConversionInfo(x[0], x[1], x[2], x[3])
        print "    " + repr(info)
        conversion_info.append(info)
    print
    txt = lexeme_converter.ConverterWriterUTF8().do(conversion_info, ProvidedConversionInfoF=True)
    print txt


if "1" in sys.argv:
    #             RangeIndex  CI_Begin_in_Unicode  CI_Begin   CI_Size
    ConvInfo = [ [1,          0x00000,             0x1000000, 20]] 
    test("Single Interval A", ConvInfo)
    ConvInfo = [ [2,          0x00080,             0x1000000, 20]] 
    test("Single Interval B", ConvInfo)
    ConvInfo = [ [3,          0x00800,             0x1000000, 20]] 
    test("Single Interval C", ConvInfo)
    ConvInfo = [ [4,          0x10000,             0x1000000, 20]] 
    test("Single Interval E", ConvInfo)

elif "2" in sys.argv:
    #             RangeIndex  CI_Begin_in_Unicode  CI_Begin   CI_Size
    ConvInfo = [ [1,          0,                   0x100000,  0x10], 
                 [2,          0x80,                0x200000,  0x10],
                 [3,          0x800,               0x300000,  0x10],
                 [4,          0x10000,             0x400000,  0x10] ]
    test("4 Intervals", ConvInfo)

elif "3" in sys.argv:
    TrafoInfo = [ [0,       0x81,     0x110000], 
                  [0x81,    0x801,    0x010081], 
                  [0x801,   0x10001,  0x020000], 
                  [0x10001, 0x100001, 0x000001] ]
    ConvInfo = lexeme_converter.ConverterWriterUTF8().get_conversion_table(TrafoInfo)
    ConvInfo = map(lambda x: [x.code_unit_n, 
                              x.codec_interval_begin_unicode, 
                              x.codec_interval_begin,
                              x.codec_interval_size], ConvInfo)
    test("Intervals over borders (all)", ConvInfo)

