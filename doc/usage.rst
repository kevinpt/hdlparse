Usage
#####

The pyHDLParser library has two main modules :py:mod:`~hdlparse.vhdl_parser` and :py:mod:`~hdlparse.verilog_parser`.
You import one or both of them as needed.

.. code-block:: python

  import hdlparse.vhdl_parser as vhdl
  import hdlparse.verilog_parser as vlog

Within each module are extractor classes :py:class:`~hdlparse.vhdl_parser.VhdlExtractor` and
:py:class:`~hdlparse.verilog_parser.VerilogExtractor` that are the central mechanisms for using pyHDLParser.

.. code-block:: python

  vhdl_ex = vhdl.VhdlExtractor()
  vlog_ex = vlog.VerilogExtractor()


VHDL
====

The VHDL parser can extract a variety of different objects from sourec code.
It can be used to access package definitions and component declarations,type and subtype definitions, functions, and
procedures found within a package.
It will not process entity declarations or nested subprograms and types.

Extraction proceeds as follows:

.. code-block:: python

  with io.open(fname, 'rt', encoding='latin-1') as fh:
    code = fh.read()
  vhdl_objs = vhdl_ex.extract_objects_from_source(code)

  vhdl_objs = vhdl_ex.extract_objects(fname)

These will extract a list of all supported object types.
The result is a list of objects subclassed from :py:class:`~hdlparse.vhdl_parser.VhdlObject`.
You can pass an optional subclass of ``VhdlObject`` to filter the results for just that type.
Repeated calls are more efficient when using :py:meth:`~hdlparse.vhdl_parser.VhdlExtractor.extract_objects` which
maintains a cache of all previously parsed objects in the extractor.

.. code-block:: vhdl

  package example is
    component demo is
      generic (
        GENERIC1: boolean := false;
        GENERIC2: integer := 100
      );
      port (
        a, b : in std_ulogic := '1';
        c, d : out std_ulogic_vector(7 downto 0);
        e, f : inout unsigned(7 downto 0)
      );
    end component;
  end package;

Each port and generic is an instance of :py:class:`~hdlparse.vhdl_parser.VhdlParameter` containing the name, mode
(input, output, inout), and type.

.. code-block:: python

  import hdlparse.vhdl_parser as vhdl
  from hdlparse.vhdl_parser import VhdlComponent

  vhdl_ex = vhdl.VhdlExtractor()
  vhdl_comps = vhdl_ex.extract_objects('example.vhdl', VhdlComponent)

  for c in vhdl_comps:
    print('Component "{}":'.format(c.name))

    print('  Generics:')
    for p in c.generics:
      print('\t{:20}{:8} {}'.format(p.name, p.mode, p.data_type))

    print('  Ports:')
    for p in c.ports:
      print('\t{:20}{:8} {}'.format(p.name, p.mode, p.data_type ))

When run against the example code produces the following:

.. code-block: console

  Component "demo":
    Generics:
	  GENERIC1            in       boolean
	  GENERIC2            in       integer
    Ports:
	  a                   in       std_ulogic
	  b                   in       std_ulogic
	  c                   out      std_ulogic_vector(7 downto 0)
	  d                   out      std_ulogic_vector(7 downto 0)
	  e                   inout    unsigned(7 downto 0)
	  f                   inout    unsigned(7 downto 0)


VHDL arrays
-----------

It can be useful to know which data types are an array. The :py:class:`~hdlparse.vhdl_parser.VhdlExtractor` class will
keep track of all visited array type definitions it sees.
The :py:meth:`~hdlparse.vhdl_parser.VhdlExtractor.is_array` method lets you query the internal list to check if a type
is for an array.
All IEEE standard array types are supported by default.
Any subtypes derived from an array type will also be considered as arrays.

.. code-block:: python

  import hdlparse.vhdl_parser as vhdl

  vhdl_ex = vhdl.VhdlExtractor()

  code = '''
  package foobar is
    type custom_array is array(integer range <>) of boolean;
    subtype custom_subtype is custom_array(1 to 10);
  end package;
  '''
  vhdl_comps = vhdl_ex.extract_objects(code)

  # These all return true:
  print(vhdl_ex.is_array('unsigned'))
  print(vhdl_ex.is_array('custom_array'))
  print(vhdl_ex.is_array('custom_subtype'))

Parsed array data can be saved to a file with :py:meth:`~hdlparse.vhdl_parser.VhdlExtractor.save_array_types` and
restored with :py:meth:`~hdlparse.vhdl_parser.VhdlExtractor.load_array_types`.
This lets you parse one set of files for type definitions and use the saved info for parsing other code at a different
time.


Verilog
=======

The Verilog parser is only able to extract module definitions with a port and optional parameter list.
Verilog modules are extracted using the :py:meth:`~hdlparse.verilog_parser.VerilogExtractor.extract_objects` and
:py:meth:`~hdlparse.verilog_parser.VerilogExtractor.extract_objects_from_source` methods.
The latter is used when you have the code in a string.
The former when you want to read the Veirlog source from a file.
When parsing a file, a cache of objects is maintained so you can repeatedly call
:py:meth:`~hdlparse.verilog_parser.VerilogExtractor.extract_objects` without reparsing the file.

.. code-block:: python

  with open(fname, 'rt') as fh:
    code = fh.read()
  vlog_mods = vlog_ex.extract_objects_from_source(code)

  vlog_mods = vlog_ex.extract_objects(fname)

The result is a list of extracted :py:class:`~hdlparse.verilog_parser.VerilogModule` objects.
Each instance of this class has ``name``, ``generics``, and ``ports`` attributes.
The ``name`` attribute is the name of the module.
The ``generics`` attribute is a list of extracted parameters and ``ports`` is a list of the ports on the module.

.. code-block:: verilog

  module newstyle // This is a new style module def
  #(parameter real foo = 8, bar=1, baz=2,
  parameter signed [7:0] zip = 100)
  (
    input x, x2, inout y, y2_long_output,
    output wire [4:1] z, z2
  );
  endmodule

Each port and generic is an instance of :py:class:`~hdlparse.verilog_parser.VerilogParameter` containing the name, mode
(input, output, inout), and type.

.. code-block:: python

  import hdlparse.verilog_parser as vlog

  vlog_ex = vlog.VerilogExtractor()
  vlog_mods = vlog_ex.extract_objects_from_source('example.v')

  for m in vlog_mods:
    print('Module "{}":'.format(m.name))

    print('  Parameters:')
    for p in m.generics:
      print('\t{:20}{:8}{}'.format(p.name, p.mode, p.data_type))

    print('  Ports:')
    for p in m.ports:
      print('\t{:20}{:8}{}'.format(p.name, p.mode, p.data_type))


When run against the example code produces the following:

.. code-block:: console

  Module "newstyle":
    Parameters:
	  foo                 in      real
	  bar                 in      real
	  baz                 in      real
	  zip                 in      signed [7:0]
    Ports:
	  x                   input
	  x2                  input
	  y                   inout
	  y2_long_output      inout
	  z                   output  wire [4:1]
	  z2                  output  wire [4:1]


Reference
=========

.. automodule:: hdlparse
    :members:
    :undoc-members:
    :show-inheritance:

hdlparse\.minilexer
-------------------

.. automodule:: hdlparse.minilexer
    :members:
    :undoc-members:
    :show-inheritance:

hdlparse\.verilog\_parser
-------------------------

.. automodule:: hdlparse.verilog_parser
    :members:
    :undoc-members:
    :show-inheritance:

hdlparse\.vhdl\_parser
----------------------

.. automodule:: hdlparse.vhdl_parser
    :members:
    :undoc-members:
    :show-inheritance:
