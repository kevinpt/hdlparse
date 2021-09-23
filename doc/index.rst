pyHDLParser
###########

pyHDLParser is a simple package implementing a rudimentary parser for VHDL and Verilog.
It is not capable of fully parsing the entire language.
Rather, it is meant to extract enough key information from a source file to create generated documentation.

This library is used by the `Symbolator <https://github.com/hdl/symbolator>`_ diagram generator.

For VHDL this library can extract component, subprogram, type, subtype, and constant declarations from a package.
For Verilog it can extract module declarations (both 1995 and 2001 syntax).

.. toctree::

   about
   getting
   usage
   genindex
