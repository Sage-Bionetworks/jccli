jccli
=====

A command line client to manage `Jumpcloud <https://jumpcloud.com/>`__
identify provider service.

Getting Started
---------------

Install
~~~~~~~

.. code:: bash

   git clone https://github.com/Sage-Bionetworks/jccli.git && cd jccli && make build

Usage
~~~~~

.. code:: bash

   Usage: jccli [OPTIONS] COMMAND [ARGS]...

     Run jccli.

   Options:
     -k, --key TEXT  Jumpcloud API key
     -v, --verbose   Enable verbose output.
     --help          Show this message and exit.

   Commands:
     create-group  Create a Jumpcloud group
     create-user   Create a new Jumpcloud user
     delete-group  Delete a Jumpcloud group
     delete-user   Delete a jumpcloud user
     sync          Sync Jumpcloud with a data file
     version       Get the version.

Contributions
-------------

Contributions are welcome.

Requirements:

Install these utilities: \* `GNU
Make <https://www.gnu.org/software/make/>`__ \*
`pre-commit <https://pre-commit.com/#install>`__ \*
`Pandoc <https://pandoc.org/>`__

As a pre-deployment step we syntatically validate our code and
configurations with pre-commit.

Please install pre-commit, once installed the file validations will
automatically run on every commit. Alternatively you can manually
execute the validations by running ``pre-commit run --all-files``.

Resources
---------

Below are some handy resource links.

-  `Project Documentation <http://jccli.readthedocs.io/>`__
-  `Click <http://click.pocoo.org/5/>`__ is a Python package for
   creating beautiful command line interfaces in a composable way with
   as little code as necessary.
-  `Sphinx <http://www.sphinx-doc.org/en/master/>`__ is a tool that
   makes it easy to create intelligent and beautiful documentation,
   written by Geog Brandl and licnsed under the BSD license.
-  `pytest <https://docs.pytest.org/en/latest/>`__ helps you write
   better programs.
-  `GNU Make <https://www.gnu.org/software/make/>`__ is a tool which
   controls the generation of executables and other non-source files of
   a program from the program’s source files.

Authors
-------

-  **zaro0508** - *Initial work* -
   `github <https://github.com/zaro0508>`__

See also the list of
`contributors <https://github.com/zaro0508/jccli/contributors>`__ who
participated in this project.
