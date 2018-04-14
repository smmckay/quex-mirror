
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

bom.exe: bom.c ut
	gcc -D__QUEX_OPTION_PLAIN_C \
		-DQUEX_NAMESPACE_MAIN_OPEN="" \
		-DQUEX_NAMESPACE_MAIN_CLOSE="" \
		$< -o $@ $(DEFS)

bom-istream.exe: bom.cpp ut
	g++ \
		-DQUEX_NAMESPACE_MAIN_OPEN="" \
		-DQUEX_NAMESPACE_MAIN_CLOSE="" \
		$(DEFS) $< -o $@

strange_stream.exe: strange_stream.cpp ut
	g++ -DQUEX_TYPE_LEXATOM=uint8_t $(DEFS) $< -o $@

strange_wstream.exe: strange_wstream.cpp ut
	g++ -DQUEX_TYPE_LEXATOM=wchar_t $(DEFS) $< -o $@

ut:
	python ../../code_base_instatiation.py ut

clean: 
	rm -rf $(TEST_FILES) ut
