# jccli

A command line client to manage [Jumpcloud](https://jumpcloud.com/)
identify provider service.

## Getting Started

### Install

```bash
pip install git+https://github.com/Sage-Bionetworks/jccli
```

### Usage

```bash
Usage: jccli [OPTIONS] COMMAND [ARGS]...

  Run jccli.

Options:
  -k, --key TEXT       Jumpcloud API key
  -v, --verbosity LVL  Either CRITICAL, ERROR, WARNING, INFO or DEBUG
  --version            Show the version and exit.
  --help               Show this message and exit.

Commands:
  create-group  Create a Jumpcloud group
  create-user   Create a new Jumpcloud user
  delete-group  Delete a Jumpcloud group
  delete-user   Delete a jumpcloud user
  sync          Sync Jumpcloud with a data file
```

## Contributions

Contributions are welcome.

Requirements:

Install these utilities:
* [GNU Make](https://www.gnu.org/software/make/)
* [pre-commit](https://pre-commit.com/#install)
* [Pandoc](https://pandoc.org/)

As a pre-deployment step we syntatically validate our code and configurations with pre-commit.

Please install pre-commit, once installed the file validations will automatically
run on every commit. Alternatively you can manually execute the validations by running
`pre-commit run --all-files`.


## Resources

Below are some handy resource links.

* [Project Documentation](http://jccli.readthedocs.io/)
* [Click](http://click.pocoo.org/5/) is a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary.
* [Sphinx](http://www.sphinx-doc.org/en/master/) is a tool that makes it easy to create intelligent and beautiful documentation, written by Geog Brandl and licnsed under the BSD license.
* [pytest](https://docs.pytest.org/en/latest/) helps you write better programs.
* [GNU Make](https://www.gnu.org/software/make/) is a tool which controls the generation of executables and other non-source files of a program from the program's source files.


## Authors

* **zaro0508** - *Initial work* - [github](https://github.com/zaro0508)

See also the list of [contributors](https://github.com/zaro0508/jccli/contributors) who participated in this project.
