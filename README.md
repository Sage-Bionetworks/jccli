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
  group  Group of commands for Jumpcloud groups :param ctx: :param key:...
  sync   Sync Jumpcloud with a data file
  user   User group of functions :param ctx: context object :return:
```


```bash
> jccli --key XXXXXXXXXX61d2 user get --username jsmith
{
  "id": "9ba6cc40d82ee45d5f73da2e",
  "account_locked": false,
  "activated": true,
  "firstname": "Joe",
  "job_title": "",
  "lastname": "Smith",
  ..
  ..
}
```


## Contributions

Contributions are welcome.

### Requirements

Install these utilities:
* [GNU Make](https://www.gnu.org/software/make/)
* [pre-commit](https://pre-commit.com/#install)
* [Pandoc](https://pandoc.org/)

### Process

Before making a commit, you should syntactically validate your code and configurations with pre-commit.

You can set up pre-commit hooks to automatically be run before every commit by running: `pre-commit install`.
Alternatively, you can manually execute the validations by running `pre-commit run --all-files`.

#### Tests

JCCLI's test suite consists of unit tests and integration tests. The integration tests depend on the environment
variable `JC_API_KEY`, which should be a Jumpcloud API key corresponding to a blank Jumpcloud instance which can be used
for testing purposes.

We use [Travis-CI](https://travis-ci.org/) to automate our testing. This repo's Travis configuration is set up to run
the unit test suite (in `unit_tests/`) on every push and pull request, and to run the integration test suite (in
`integration_tests/`) whenever a push or pull request is made to the `master` branch (regardless of the repo and its
owner).

### GitHub

Contributors are requested to first make a Pull Request to a non-master branch in the `Sage-Bionetworks/jccli` repo, and
then have the changes merged into `master` from there.

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
