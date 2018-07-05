
TEST_FILES = \
	       strange_stream.exe  \
	       strange_wstream.exe \
		   bom.exe             \
		   bom-istream.exe
INCLUDE := -I$(HWUT_PATH) -I. -I../../../TESTS -I../../../

DEFS = -DQUEX_OPTION_ASSERTS $(INCLUDE) -ggdb 

all: $(TEST_FILES)

hwut-info:
	@echo $(TEST_FILES)

bom.exe: bom.c 
	gcc -DQUEX_OPTION_PLAIN_C_EXT \
		-DQUEX_NAMESPACE_MAIN_OPEN="" \
		-DQUEX_NAMESPACE_MAIN_CLOSE="" \
		$< -o $@ $(DEFS)

bom-istream.exe: bom.cpp 
	g++ \
		-DQUEX_NAMESPACE_MAIN_OPEN="" \
		-DQUEX_NAMESPACE_MAIN_CLOSE="" \
		-DQUEX_INLINE= \
		$(DEFS) $< -o $@

strange_stream.exe: strange_stream.cpp 
	g++ -DQUEX_TYPE_LEXATOM_EXT=uint8_t $(DEFS) $< -o $@

strange_wstream.exe: strange_wstream.cpp 
	g++ -DQUEX_TYPE_LEXATOM_EXT=wchar_t $(DEFS) $< -o $@

clean: 
	rm -rf $(TEST_FILES) ut
