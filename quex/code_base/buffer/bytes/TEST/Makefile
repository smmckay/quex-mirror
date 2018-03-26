TESTS := test-FILE.exe \
	     test-POSIX.exe \
	     test-Memory.exe \
	     test-fstream.exe \
	     test-stringstream.exe \
		 segmented-input.exe

FLAGS    :=  -ggdb -Wall -Werror \
   	         -DTEST_FILE_SIZE=100 \
			 -DQUEX_NAMESPACE_MAIN_CLOSE='' \
			 -DQUEX_NAMESPACE_MAIN_OPEN='' \
			 -DQUEX_TYPE_STREAM_POSITION=long \
			 -I$(HWUT_PATH)/support/C \
			 -I$(QUEX_PATH) \
			 -I.

MORE := basic_functionality.c initial_position.c

all: $(TESTS)

hwut-info:
	@echo $(TESTS)

test-%.exe: test-%.c $(MORE) ut
	gcc $(FLAGS) -D__QUEX_OPTION_PLAIN_C $< $(MORE) -o $@

test-%.exe: test-%.cpp $(MORE) ut
	g++ $(FLAGS) $< $(MORE) -o $@

segmented-input.exe: segmented-input.c ut
	gcc $(FLAGS) -D__QUEX_OPTION_PLAIN_C $< -o $@

ut:
	python ../../../TESTS/code_base_instatiation.py ut analyzer compatibility buffer lexeme_converter

clean:
	rm -f *.exe
	rm -f tmp.*
