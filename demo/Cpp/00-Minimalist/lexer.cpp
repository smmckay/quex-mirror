    #include <fstream>
    #include <iostream>

    #include "tiny/tiny"

    int main(int argc, char** argv)
    {         
        quex::Token*  token_p = 0x0;
        quex::tiny    tlex("example.txt", /* Converter */NULL);

        do {
            tlex.receive(&token_p);

            std::cout << token_p->type_id_name() << std::endl;

        } while(    token_p->id     != QUEX_TKN_TERMINATION 
                 && tlex.error_code == E_Error_None );
        
        return 0;
    }
