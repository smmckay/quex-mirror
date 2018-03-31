br_scan:
	quex -i scan.qx -o br_scan \
		 --token-class-file token.h --token-id-prefix BR_TKN_ \
		 --foreign-token-id-file gramma.h --token-class blackray::Token \
		 --debug-exception 

all \
check: br_scan
	g++ -Wall -Werror br_scan/br_scan.cpp example.cpp \
		-I. \
		-DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED \
		-o check 

mixMemberAssignWithManualTokenClass:
	quex -i scan-error.qx -o br_scan --token-class-file token.h --token-id-prefix BR_TKN_ --foreign-token-id-file gramma.h --token-class blackray::Token

tokenTypeAlongWithManualTokenClass:
	quex -i CppDefault.qx scan.qx -o br_scan --token-class-file token.h --token-id-prefix BR_TKN_ --foreign-token-id-file gramma.h --token-class blackray::Token

tokenTypeWithoutTokenClassSpecification:
	quex -i scan.qx -o br_scan --token-class-file token.h --token-id-prefix BR_TKN_ --foreign-token-id-file gramma.h  

clean:
	rm -rf check check tmp.txt br_scan*

