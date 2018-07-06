chmod a+rx TEST/valgrindi.sh

pushd quex/code_base/TESTS/
rm -rf test_c test_cpp 
python generate-TestAnalyzer.py C
python generate-TestAnalyzer.py C   emm
python generate-TestAnalyzer.py C   computed-gotos
python generate-TestAnalyzer.py C++ 
python generate-TestAnalyzer.py C++ emm
python generate-TestAnalyzer.py C++ computed-gotos
popd

pushd quex/output/core/TEST
rm -rf ut 
python ../../../code_base/TESTS/code_base_instatiation.py ut --lang-C
quex --co -o TestAnalyzer --odir ut --debug-exception --bet uint32_t --encoding unicode --language C
quex --co -o TestAnalyzer --odir ut --debug-exception --bet uint8_t  --encoding utf8    --language C
popd

#pushd quex/engine/loop/TEST
#rm -rf ut
#python ../../../code_base/TESTS/code_base_instatiation.py ut
#popd

pushd quex/output/languages/cpp/TEST
rm -rf ut
python ../../../../code_base/TESTS/code_base_instatiation.py  ut
cp ../../../../code_base/TESTS/test_cpp/TestAnalyzer-configuration ut
#quex --co -o TestAnalyzer --odir ut --debug-exception --bet uint32_t --encoding unicode
#quex --co -o TestAnalyzer --odir ut --debug-exception --bet uint8_t --encoding utf8
popd


pushd doc
#python command_line_options.py
popd

rm -f $(find -name "*.pyc")
pushd doc
make clean
popd
pushd demo
bash make_clean.sh > /dev/null 2>&1
popd

hwut make clean > /dev/null 2>&1

