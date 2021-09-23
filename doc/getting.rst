Getting
#######

Requirements
------------

pyHDLParser requires either Python 2.7 or Python 3.x and no additional libraries.

The installation script depends on setuptools. The source is written in
Python 2.7 syntax but will convert cleanly to Python 3 when the installer
passes it through ``2to3``.

Download
--------

You can access the pyHDLParser Git repository from `Github <https://github.com/hdl/pyHDLParser>`_.
You can install direct from PyPI with the ``pip`` command if you have it available.

Installation
------------

pyHDLParser is a Python library.
You must have Python installed first to use it.
Most modern Linux distributions and OS/X have it available by default.
There are a number of options available for Windows.
If you don't already have a favorite, I recommend getting one of the `"full-stack" Python distros <http://www.scipy.org/install.html>`_ that are geared toward scientific computing such as Anaconda or Python(x,y).

You need to have the Python setuptools installed first.
If your OS has a package manager, it may be preferable to install setuptools through that tool.
Otherwise you can use Pip:

.. code-block:: sh

  > pip install setuptools

The easiest way to install pyHDLParser is from `PyPI <https://pypi.python.org/pypi/hdlparse>`_.

.. code-block:: sh

  > pip install --upgrade hdlparse

This will download and install the latest release, upgrading if you already have it installed.
If you don't have ``pip`` you may have the ``easy_install`` command available which can be used to install ``pip`` on
your system:

.. code-block:: sh

  > easy_install pip

You can also use ``pip`` to get the latest development code from Github:

.. code-block:: sh

  > pip install --upgrade https://github.com/hdl/pyHDLParser/tarball/master

If you manually downloaded a source package or created a clone with Git you can install with the following command run
from the base pyHDLParser directory:

.. code-block:: sh

  > python setup.py install

On Linux systems you may need to install with root privileges using the *sudo* command.

After a successful install the pyHDLParser library will be available.
