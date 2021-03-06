.. _sec-multiple-lexical-analyzers:

Multiple Lexical Analyzers
==========================

This section discusses how to use multiple lexical analyzers generated by quex
in a single application without causing clashes. Since version 0.47.1 this
task has become very easy. The only requirement from the user's prespective is
that the lexical analyzers and the token classes need to live in separate
namespaces. The command line option ``-o, --engine, --analyzer-class`` allow
to specify a name of the analyzer class as well as its namepsace by means
of preceding ``::`` sequences, e.g.::

  > quex ... -o world::germany::baden::Fritzle ...

defines that the analyzer class is called ``Fritzle`` and is located in
namespace ``baden`` which is inside ``germany`` which is inside ``world``.  If
no namespace is specified, the class is located in namespace ``quex``.
Similarly, the token class can be specified by means of ``--token-class, --tc``::

  > quex ... -o castle::room::jewel_case::MyToken ...

specifies that the generated token class ``MyToken`` is inside the namespace
``castle``, which contains ``room``, which contains ``jewel_case``. If no namespace
is specified, then the token class is placed in the namespace of the 
lexical analyzer class. In any case, when migrating from a single to multiple
lexical analyzers, then your code must reflect this. For example, a code fragment
as

.. code-block:: cpp

   int main(int argc, char** argv) {
        ALexer     qlex("example.txt");
        ...
   }

should be adapted to something similar to

.. code-block:: cpp

   int main(int argc, char** argv) {
        namespace1::ALexer     a_lexer("example.a");
        namespace2::BLexer     b_lexer("example.b");
        ...
   }

In conclusion, the only thing that has to be made sure is that the generated
analyzers live in separate namespaces. All related entities of the analyzers
are then properly distinguished for compiling and linking.  Directory
``demo/012`` contains an example implementation of an application containing
three different analyzers with different numbers of bytes per character and
different decoders (ICU, IConv and engine encoding). 

Directory ``demo\012b`` contains an example with multiple lexical analyzers
using the same token class.  This subject is discusses in section
:ref:`sec-shared-token-class`.



