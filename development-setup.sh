
pushd quex/code_base/extra/test_environment/
python generate-TestAnalyzer.py C
python generate-TestAnalyzer.py C++
popd

pushd doc
python command_line_options.py
popd
