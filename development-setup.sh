
pushd quex/code_base/TESTS/test_environment/
python generate-TestAnalyzer.py C
python generate-TestAnalyzer.py C++
popd

pushd quex/output/core/TEST
python ../../../code_base/TESTS/code_base_instatiation.py ut
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
