DFA Plots
===================

Quex has the ability to produce transition graphs for the state machines that
result from the regular expressions of its modes. It outputs the structure of
state machines in the '.dot' format. This format can be used to produce
graphics using the tool 'graphviz' from AT\&T Labs :ref:`cite dot`
http://www.graphviz.org. Please install this package before any attempt to
produce transition graphs. 

The plot of transition graphs is initiated with the command line argument
``--language dot`` followed by a string that indicates the graphic format, e.g.

.. code-block:: bash

   > quex -i core.qx --language dot

will produce transition graphs of all state machines that would result from
descriptions in ``core.qx``. As a result of this operation a set of files is
created that carry the extension of the graphic format. The basenames of the
files are related to the mode from which its content results. The characters
on the state transitions can be either displayed as UTF8 characters or
in hexadecimal notation, if the command line option ``--character-display``
is provided, e.f.

.. code-block:: bash

   > quex -i core.qx --language dot --character-display hex

displays the characters as hexadecimal numbers of their Unicode Code Points. 
Once, those files have been generated, the dot utility can be called to produce
state machine plots, e.g.

.. code-block:: bash

   > dot -Tsvg -oMyfile.svg MY_MODE.dot

generates an SVG file from the file that quex produced 'MY_MODE.dot'. 
An example of a state machine plot can be viewed
in :ref:`Sample plot <fig-sample-plot>`.

.. _fig-sample-plot:

.. figure:: ../../figures/ONE_AND_ONLY.*

   Sample plot of a simple state machine.
