.. HdlParse documentation master file, created by
   sphinx-quickstart on Sun Oct 15 14:19:42 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

========
Hdlparse
========

Hdlparse is a simple package implementing a rudimentary parser for VHDL and Verilog. It is not capable of fully parsing the entire language. Rather, it is meant to extract enough key information from a source file to create generated documentation.

This library is used by the `Symbolator <https://github.com/kevinpt/symbolator>`_ diagram generator.

For VHDL this library can extract component, subprogram, type, subtype, and constant declarations from a package. For Verilog it can extract module declarations (both 1995 and 2001 syntax).


Requirements
------------

Hdlparse requires either Python 2.7 or Python 3.x and no additional libraries.

The installation script depends on setuptools. The source is written in
Python 2.7 syntax but will convert cleanly to Python 3 when the installer
passes it through ``2to3``.


Licensing
---------

Opbasm and the included VHDL source is licensed for free commercial and non-commercial use under the terms of the MIT license.


Download
--------

You can access the Hdlparse Git repository from `Github
<https://github.com/kevinpt/hdlparse>`_. You can install direct from PyPI with the ``pip``
command if you have it available.

Installation
------------

Hdlparse is a Python library. You must have Python installed first to use it. Most modern Linux distributions and OS/X have it available by default. There are a number of options available for Windows. If you don't already have a favorite, I recommend getting one of the `"full-stack" Python distros <http://www.scipy.org/install.html>`_ that are geared toward scientific computing such as Anaconda or Python(x,y).

You need to have the Python setuptools installed first. If your OS has a package manager, it may be preferable to install setuptools through that tool. Otherwise you can use Pip:

.. code-block:: sh

  > pip install setuptools

The easiest way to install Hdlparse is from `PyPI <https://pypi.python.org/pypi/hdlparse>`_.

.. code-block:: sh

  > pip install --upgrade hdlparse

This will download and install the latest release, upgrading if you already have it installed. If you don't have ``pip`` you may have the ``easy_install`` command available which can be used to install ``pip`` on your system:

.. code-block:: sh

  > easy_install pip


You can also use ``pip`` to get the latest development code from Github:

.. code-block:: sh

  > pip install --upgrade https://github.com/kevinpt/hdlparse/tarball/master

If you manually downloaded a source package or created a clone with Git you can install with the following command run from the base Hdlparse directory:

.. code-block:: sh

  > python setup.py install

On Linux systems you may need to install with root privileges using the *sudo* command.

After a successful install the Hdlparse library will be available.


Using Hdlparse
--------------

The Hdlparse library has two main modules :py:mod:`~hdlparse.vhdl_parser` and :py:mod:`~hdlparse.verilog_parser`. You import one or both of them as needed.

.. code-block:: python

  import hdlparse.vhdl_parser as vhdl
  import hdlparse.verilog_parser as vlog

Within each module are extractor classes :py:class:`~hdlparse.vhdl_parser.VhdlExtractor` and :py:class:`~hdlparse.verilog_parser.VerilogExtractor` that are the central mechanisms for using Hdlparse.

.. code-block:: python

  vhdl_ex = vhdl.VhdlExtractor()
  vlog_ex = vlog.VerilogExtractor()
  

VHDL
~~~~

The VHDL parser can extract a variety of different objects from source code. It can be used to access package definitions and component declarations,type and subtype definitions, functions, and procedures found within a package. It will not process entity declarations or nested subprograms and types.

Extraction proceeds as follows:

.. code-block:: python

  with io.open(fname, 'rt', encoding='latin-1') as fh:
    code = fh.read()
  vhdl_objs = vhdl_ex.extract_objects_from_source(code)

  vhdl_objs = vhdl_ex.extract_objects(fname)
  
These will extract a list of all supported object types. The result is a list of objects subclassed from :py:class:`~hdlparse.vhdl_parser.VhdlObject`. You can pass an optional subclass of ``VhdlObject`` to filter the results for just that type. Repeated calls are more efficient when using :py:meth:`~hdlparse.vhdl_parser.VhdlExtractor.extract_objects` which maintains a cache of all previously parsed objects in the extractor.

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

Each port and generic is an instance of :py:class:`~hdlparse.vhdl_parser.VhdlParameter` containing the name, mode (input, output, inout), and type.

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
~~~~~~~~~~~

It can be useful to know which data types are an array. The :py:class:`~hdlparse.vhdl_parser.VhdlExtractor` class will keep track of all visited array type definitions it sees. The :py:meth:`~hdlparse.vhdl_parser.VhdlExtractor.is_array` method lets you query the internal list to check if a type is for an array. All IEEE standard array types are supported by default. Any subtypes derived from an array type will also be considered as arrays.

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

Parsed array data can be saved to a file with :py:meth:`~hdlparse.vhdl_parser.VhdlExtractor.save_array_types` and restored with :py:meth:`~hdlparse.vhdl_parser.VhdlExtractor.load_array_types`. This lets you parse one set of files for type definitions and use the saved info for parsing other code at a different time.


Verilog
~~~~~~~

The Verilog parser is only able to extract module definitions with a port and optional parameter list. Verilog modules are extracted using the :py:meth:`~hdlparse.verilog_parser.VerilogExtractor.extract_objects` and :py:meth:`~hdlparse.verilog_parser.VerilogExtractor.extract_objects_from_source` methods. The latter is used when you have the code in a string. The former when you want to read the Veirlog source from a file. When parsing a file, a cache of objects is maintained so you can repeatedly call :py:meth:`~hdlparse.verilog_parser.VerilogExtractor.extract_objects` without reparsing the file.

.. code-block:: python

  with open(fname, 'rt') as fh:
    code = fh.read()
  vlog_mods = vlog_ex.extract_objects_from_source(code)

  vlog_mods = vlog_ex.extract_objects(fname)
  
The result is a list of extracted :py:class:`~hdlparse.verilog_parser.VerilogModule` objects. Each instance of this class has ``name``, ``generics``, and ``ports`` attributes. The ``name`` attribute is the name of the module. The ``generics`` attribute is a list of extracted parameters and ``ports`` is a list of the ports on the module.

.. code-block:: verilog

  module newstyle // This is a new style module def
  #(parameter real foo = 8, bar=1, baz=2,
  parameter signed [7:0] zip = 100)
  (
    input x, x2, inout y, y2_long_output,
    output wire [4:1] z, z2
  );
  endmodule

Each port and generic is an instance of :py:class:`~hdlparse.verilog_parser.VerilogParameter` containing the name, mode (input, output, inout), and type.

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


.. toctree::
   :hidden:
   :maxdepth: 2

   apidoc/modules


Indices and tables
------------------

* :ref:`genindex`
* :ref:`search`
