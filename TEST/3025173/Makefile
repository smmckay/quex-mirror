br_scan:
	quex -i scan.qx -o br_scan \
		 --token-class-file token.h --token-id-prefix BR_TKN_ \
		 --foreign-token-id-file gramma.h --token-class blackray::Token \
		 --no-string-accumulator \
		 --debug-exception 

all \
check: br_scan
	g++ -Wall -Werror br_scan.cpp example.cpp \
		-I$(QUEX_PATH) -I. \
		-DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED \
		-o check 

mixMemberAssignWithManualTokenClass:
	quex -i scan-error.qx -o br_scan --token-class-file token.h --token-id-prefix BR_TKN_ --foreign-token-id-file gramma.h --token-class blackray::Token

tokenTypeAlongWithManualTokenClass:
	quex -i CppDefault.qx scan.qx -o br_scan --token-class-file token.h --token-id-prefix BR_TKN_ --foreign-token-id-file gramma.h --token-class blackray::Token

tokenTypeWithoutTokenClassSpecification:
	quex -i scan.qx -o br_scan --token-class-file token.h --token-id-prefix BR_TKN_ --foreign-token-id-file gramma.h  

clean:
	rm -f check
	rm -f check
	rm -f tmp.txt
	rm -f br_scan*

