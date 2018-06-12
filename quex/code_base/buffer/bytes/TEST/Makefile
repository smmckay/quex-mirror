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
			 -DQUEX_OPTION_ASSERTS_EXT \
			 -I$(HWUT_PATH)/support/C \
			 -I$(QUEX_PATH)/quex/code_base \
			 -I$(QUEX_PATH)/quex/code_base/TEST \
			 -I$(QUEX_PATH)/quex/code_base/TESTS \
			 -I.

MORE := basic_functionality.c initial_position.c

all: $(TESTS)

hwut-info:
	@echo $(TESTS)

test-%.exe: test-%.c $(MORE) 
	gcc $(FLAGS) -DQUEX_OPTION_PLAIN_C_EXT -DQUEX_INLINE= $< $(MORE) -o $@

test-%.exe: test-%.cpp $(MORE) 
	g++ $(FLAGS) -DQUEX_INLINE=inline $< $(MORE) -o $@

segmented-input.exe: segmented-input.c 
	gcc $(FLAGS) -DQUEX_OPTION_PLAIN_C_EXT -DQUEX_INLINE= $< -o $@

clean:
	rm -f *.exe
	rm -f tmp.*
