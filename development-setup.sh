
pushd quex/code_base/TESTS/test_environment/
rm -rf TestAnalyzer* lib
python generate-TestAnalyzer.py C
python generate-TestAnalyzer.py C++
popd

pushd quex/output/core/TEST
python ../../../code_base/TESTS/code_base_instatiation.py ut
popd
pushd quex/engine/loop/TEST
python ../../../code_base/TESTS/code_base_instatiation.py ut
popd
pushd quex/output/languages/cpp/TEST
python ../../../../code_base/TESTS/code_base_instatiation.py test_environment
cp ../../../../code_base/TESTS/test_environment/TestAnalyzer-configuration test_environment
popd


pushd doc
python command_line_options.py
popd

rm -f $(find -name "*.pyc")
pushd doc
make clean
popd
pushd demo
bash make_clean.sh > /dev/null 2>&1
popd

hwut make clean > /dev/null 2>&1
