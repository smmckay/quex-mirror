Introduction
------------

The quex program generates a lexical analyser that scans text and
identifies patterns. The result of this lexical analysis is a list of 
*tokens*. A token is a piece of atomic information directly relating to a
pattern, or an *incidence*. It consists of a type-identifier, i.e. the 
*token type*, and content which is extracted from the text fragment that
matched the pattern. 

Figure :ref:`(this) <fig-lexical-analyser>` shows the principle of lexical
analysis.  The lexical analyser receives a stream of characters "`if( x> 3.1 )
{ ...`" and produces a list of tokens that tells what the stream signifies. A first
token tells that there was an `if` statement, the second token tells
that there was an opening bracket, the third one tells that there was an
identifier with the content `x`, and so on. 
  
In compilers for serious programming languages the token stream is received by
a parser that interprets the given input according to a specific grammar.
However, for simple scripting languages this token stream might be treated
immediately. Using a lexical analyser generator for handcrafted ad-hoc
scripting languages has the advantage that it can be developed faster and it
is much easier and safer to provide flexibility and power. This is 
demonstrated in the following chapters.

.. _fig-lexical-analyser:

.. figure:: ../figures/lexical-analysis-process-text-to-path.* 
   
   Process of lexical analysis.

The following features distinguish quex from the traditional lexical
analysers such as lex or flex:

* *Ease*. A simple as well as a complicated lexical analyzer can 
  be specified in a very elegant and transparent manner. Do not get confused
  by the set of features and philosophies. If you do not use them, then
  simply skip the concerning sections of the text. Start from the ready-to-rumble
  examples in the `./demo` subdirectory.

* A generator for a directly *coded lexical analyzer* featuring
  pre- and post-condtions. The generated lexical analyzer is up to 2.5 times
  faster than an analyzer created by flex/lex.

* *Unicode*. The quex engine comes with a sophisticated buffer management which
  allows to specify converters as buffer fillers. At the time of this
  writing, the libraries 'iconv' and 'icu' for character code conversion
  are directly supported.
  
* Sophisticated lexical *modes* in which only exclusively specified
  patterns are active. In contrast to normal 'lex' modes they provide
  the following functionality:

  * Inheritance *relationships* between lexical analyser modes. This
    allows the systematic inclusion of patterns from other modes, as well as
    convenient transition control.

  * *Transition control*, i.e. restriction can be made to which mode
    a certain mode can exit or from which mode it can be entered. This 
    prevents the lexical analyser from accidentally dropping into an unwanted
    lexical analysis mode.

 * Mode *transition incidences*, i.e. incidence handlers can be defined for
   the incidences of exiting or entering from or to a particular mode.    
    
 * Indentation *incidences*, i.e it is possible to provide an incidence handler
   for the incidence of the first appearing non-white space in a line. This incidence
   handling happens quasi-paralel to the pattern matching.
  
* A default general purpose *token* class. Additionally, Quex
  provides an interface to run the lexical analyser with a user-defined token
  class.
  
* A *token queue* so that tokens can be communicated without returning
  from the analyser function.  The token queue is a key for the production of
  '*implicit tokens*', i.e.  tokens that do not relate directly to
  characters in an analysed character stream. Those tokens are derived from
  context. This again, is a key for defining redundancy reduced languages.
  
* Automatic *line* and *column numbering*.  The current line number and column
  number can be accessed at any time.  Quex investigates patterns and determines
  the most time efficient method to apply changes to column and line numbers.
  This results in an overhead for counting which is almost not measurable. 
  However, for fine tuning it might as well be turned off.

* *Include stack handling*. For languages where files include other files
  the quex engine provides a feature that allows to store the analyzer 
  state on a stack, continue analysis on the included file, and restore
  the analyzer state on return from the included file--without much fuss 
  for the end user.

* *Indentation Incidences*. As soon as a non-white space occurs after a newline
  a indentation incidence is fired, that allows convenient means to implement
  indentation based languages of the Python-like style.

* *Skippers*. For ranges, that are to be skipped, quex can implement 
  optimized small engines for skipping characters that are not of interest
  for lexical analysis. Examples, as the 'C/C++'-style comments '/*' to '*/'
  or '//' to newline.

* Automatic generation of transition graphs. Using the `--plot` command line
  option initiates quex to produce a graphical representation of the underlying
  state machines.

This text briefly explains the basic concepts of lexical analysis
in quex. Here, a short review is given on lexical analysis, but then it
concentrates on the introduction of the features mentioned above. The
subsequent chapter discusses a simple example of a complete application for
lexical analysis. The final chapter elaborates on the formal usage of
all features of quex. 


.. toctree::

   installation.txt
   license.txt
   naming.txt
   robustness.txt
