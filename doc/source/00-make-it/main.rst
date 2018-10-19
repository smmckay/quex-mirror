Make It!
########

.. epigraph::

    Grau, teurer Freund, ist alle Theorie und grün des Lebens goldner Baum.
    *(German: All theory is gray, my dear friend, but green is the golden tree of activity)*

    -- Mephisto, the devil, in "Faust", J. W. von Geothe (1748-1832)

While tolerating an arbitrary level of ignorance, this section demonstrates how
to make things work.  Here is a minimalist analyzer description for Quex.

    .. code-block:: cpp 
       :caption: tiny.qx

        token { OP_EQUAL; NUMBER; IDENTIFIER; }

        mode ONE_AND_ONLY
        {   
            <<EOF>>     => QUEX_TKN_TERMINATION;

            [ \t\r\n]+  {}  
            [0-9]+      => QUEX_TKN_NUMBER(Lexeme);
            [_a-zA-Z]+  => QUEX_TKN_IDENTIFIER(Lexeme);
        }   

The `token` section defines token identifier names.  The `mode` section
contains a list of pattern-action pairs. Upon 'end-of-file' the token
``QUEX_TKN_TERMINATION`` is sent. Nothing happens upon the occurrence of white
space. ``QUEX_TKN_NUMBER`` is sent, when a number occurs
``QUEX_TKN_IDENTIFIER`` signalizes a bunch of letters.  Let the aforementioned
content be stored in a file ``tiny.qx``. With the command line::

  > quex -i tiny.qx -o tiny --language C

a lexical analyzer is generated in the subdirectory ``tiny``. Here is some code
that uses it. 

  .. code-block:: cpp
     :caption: lexer.c

     #include <stdio.h>
     #include "tiny/tiny.h"

     int main(int argc, char** argv)
     {
         tiny_Token* token_p = 0x0;
         tiny        tlex;

         tiny_from_file_name(&tlex, "example.txt", /* Converter */NULL);

         while( tlex.error_code == E_Error_None ) {
             tlex.receive(&tlex, &token_p);
             printf("%s", tiny_map_token_id_to_name(token_p->id));
             if( token_p->id == QUEX_TKN_TERMINATION ) break;
             printf(": %s\n", token_p->text);
         } 

         tiny_destruct(&tlex);
         return 0;
     }

This is a C-example, where the constructor ``tiny_from_file_name()`` and the
destructor ``tiny_destruct()`` are called explicitly. A ``while`` loop iterates
over the incoming tokens produced from the input file ``example.txt``. It ends
when an error occurs or the terminating token arrives. Inside the loop,
function ``tlex.receive()`` initiates an analysis step and receives a token
pointed to by ``token_p``. Let the code be stored in ``lexer.c``. Then, the
command line::

	> gcc lexer.c tiny/tiny.c -I. -o lexer 

produces an application ``lexer``. Given a text file ``example.txt`` with
the content below::

    99 red balloons

and typing on the command line::

    > ./lexer 

delivers the output::

    NUMBER: 99
    IDENTIFIER: red
    IDENTIFIER: balloons
    <TERMINATION>

Done. Using C++ instead of C, one needs to omit the ``--language C`` option 
in the Quex call, i.e.::

  > quex -i tiny.qx -o tiny 

The code fragment to be stored in a file ``lexer.cpp`` would be

.. code-block:: cpp
   :caption: lexer.cpp

    #include <iostream>
    #include "tiny/tiny"

    int main(int argc, char** argv)
    {         
        tiny_Token*  token_p = 0x0;
        tiny         tlex("example.txt", /* Converter */NULL);

        while( tlex.error_code == E_Error_None ) {
            tlex.receive(&token_p);
            std::cout << token_p->id_name();
            if( token_p->id == QUEX_TKN_TERMINATION ) break;
            std::cout << ": " << token_p->text << std::endl;
        }
        return 0;
    }

It may be compiled with::

    > g++ lexer.cpp tiny/tiny.cpp -I. -o lexer 

The same invocation as before causes the same results as before. Done. 

The aforementioned examples for C and C++ were copy-pasted from the demos.
Indeed, the demo subdirectories contain a variety of functional applications.
Each one has its nitty-gritty problems solved.  They are perfect starting
points for someone's own particular project. 

The Demos
=========

The subdirectories of the distribution's directory ``demo/`` contains a set of
example applications for each programming language. The following list associates
the directory names with the subject on which the example elaborates.

00-Minimalist/:
  The example explained in this section.

01-Trivial/:
  A trivial example that goes slightly beyond the minimal.

02-ModesAndStuff/:
  Modes, mode transitions, mode inheritance.

03-Indentation/:
  Parsing scopes based on indentation (such as in Python).

04-ConvertersAndBOM/: 
  Character encoding conversions using ICU and IConv. The byte-order-make (BOM).
  
05-LexerForC/:
  A lexer for the C programming language.

06-Include/:
  Including files during lexical analysis.

07-TrailingPostContext/:
  Dealing with the *dangerous trailing context*.

08-DeletionAndPriorityMark/:
  Reordering pattern-action pairs in the mode inheritance hierarchy.

09-WithBisonParser/:
  Connecting a Quex lexical analyzer to a Bison generated parser.

10-SocketsAndTerminal/:
  Feeding through sockets and by the console.

11-ManualBufferFilling/:
  Feeding the buffer manually, rather than relying on input streams.

12-EngineEncoding/:
  Encoding an engine, rather than using converted input.

13-MultipleLexers/:
  Using multiple lexical analyzers in one application.

14-MultipleLexersSameToken/:
  Using a generated token class in multiple lexical analyzers.

Each directory contains a ``Makefile`` and a ``CMakeLists.txt`` file.
For UNIX users, that means that typing::

  > make

is sufficient to produce a functional application. In other cases,
many IDEs can actually read ``CMakeLists.txt`` directly. Else, the
``-G`` option lets ``cmake`` generate the desired build environment,
for example::
  
  > cmake -G "Visual Studio 14 2015 ARM"

generates a build environment for Visual Studio™ for ARM™ devices. 

Summary
=======

The goal of this chapter was to enable the reader to quickly draw benefit from
Quex.  However, what we have learned from "Faust" is that the temptations of
functional ignorance are evil in nature. The following chapters shall pave the
way of virtue providing insights to safely contain lexical analyzer generation.
 
.. epigraph::

    العِلمُ قَبلَ القَولِ وَ العَملِ
    *(Arabic: Science must always preceed speech and action)*

    -- Famous chapter title in "As Saheeh", M. Al Bukhary (810-870)

