#! /usr/bin/env python
import sys
import os
from StringIO import StringIO
sys.path.append(os.environ["QUEX_PATH"])
from   quex.input.files.token_type        import TokenTypeDescriptor
import quex.output.languages.cpp.token_class          as token_class
import quex.input.files.token_type          as parser
import quex.output.languages.core as languages
import quex.blackboard         as blackboard

blackboard.setup.buffer_element_size     = 1
blackboard.setup.output_token_class_file = ""
blackboard.setup.token_class_name        = ""
blackboard.setup.token_class_name_space  = ""
blackboard.setup.token_class_name_safe   = ""
blackboard.setup.language_db             = languages.db["C++"]()

if "--hwut-info" in sys.argv:
    print "Token Class Template"
    print "HAPPY: line [0-9]+;"
    sys.exit(0)

def test(Txt):
    sh = StringIO(Txt)
    sh.name = "a string"
    descriptor = parser.parse(sh)
    blackboard.token_type_definition = descriptor
    txt, txt_i = token_class._do(descriptor)
    print txt

test0 = "{ "
test1 = \
"""
{
   name = europa::deutschland::baden_wuertemberg::ispringen::MeinToken;
   distinct {
       my_name  :  std::string;
       numbers  :  std::vector<int>;
   }
   union {
       { 
          number       : float;
          index        : short;
       }
       { 
          x            : int16_t;
          y            : int16_t;
       }
       stream_position : uint32_t;
       who_is_that     : uint16_t;
   }
   constructor {
       this = is = a = constructor;
   }
   inheritable;
   destructor {
       this = is = a = destructor;
   }
   take_text {
       return true;
   }
   copy {
       this = is = a = copy-code;
   }
}
"""
test(test1)

