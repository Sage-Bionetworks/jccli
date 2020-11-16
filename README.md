# jccli

A command line client used to administrate the hosted
[Jumpcloud](https://jumpcloud.com/) identity provider service.

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
  -k, --key TEXT       JumpCloud API key (can also be set in config file or
                       use environmental variable: JC_API_KEY)

  -p, --profile TEXT   A user profile, as specified in the config file
                       [default: DEFAULT]

  -v, --verbosity LVL  Either CRITICAL, ERROR, WARNING, INFO or DEBUG
  --version            Show the version and exit.
  --help               Show this message and exit.

Commands:
  group  Command set for groups
  sync   Sync Jumpcloud with a data file
  user   Command set for users
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

### Configuration

JCCLI will look for an optional configuration file named `.jccli.ini` in the user's home directory. See [Python's
configparser](https://docs.python.org/3/library/configparser.html) for formatting specification. In short, `field =
"value"` pairs go under `[profile]` headers (replacing `profile` with the desired name of the profile), which can be
switched between using the `--profile` option. Currently, the only field that can be set is the `key` field, which can
be set to a JCCLI API key. Help text for optional arguments indicates whether they can be set in a user's config file.
If the user does not specify a `--profile`  it will default to `[DEFAULT]`.

For example:

```ini
[DEFAULT]
key = YOUR-KEY-HERE

[alt-account]
key = YOUR-OTHER-KEY-HERE
```

A user who has the above content in their `~/.jccli.ini` config file can use jccli with the key `YOUR-KEY-HERE` if they
don't specify a `--profile`; they can use the API key `YOUR-OTHER-KEY-HERE` if they specify `--profile alt-account`; or
they can use neither and pick a third key by using `--key YET-ANOTHER-KEY-HERE` (regardless of whether `--profile` is
specified).

### Settings precedence

JCCLI will look for settings (including API key, etc.) with the following order of precedence:
1. Optional arguments
2. Environmental variables
3. Selected profile in config file
4. `DEFAULT` profile in config file

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

JCCLI's test suite consists of unit tests and integration tests. The integration tests are designed to run on an actual
clean JumpCloud instance (see docstrings under `setup_class()` methods in `integration_tests/test_*.py` for details).
You can provide a key either by setting the environmental variable `JC_API_KEY`, or by setting the `key` field under the
section `[jccli-dev-testing]` in your `~/.jccli.ini` configuration file (See [Configuration](#Configuration) for
details).

We use [Travis-CI](https://travis-ci.org/) to automate our testing. This repo's Travis configuration is set up to run
the unit test suite (in `unit_tests/`) on every pull request and push, and to run the integration test suite (in
`integration_tests/`) only on a push.

### GitHub

Contributors are requested to use the following process (in the examples, we'll suppose that a user named `john-smith`
wants to fix some typos in the documentation):

1. Make a fork of JCCLI. E.g. `Sage-Bionetworks:jccli` &rarr; `john-smith:jccli`
2. Make a branch off of `master` named after a feature or issue. E.g. `john-smith:jccli/master` &rarr;
`john-smith:jccli/fix-typo-in-docs`
3. Make commits to that branch (in this example, `john-smith:jccli/fix-typo-in-docs`). When pushed to GitHub, they
should trigger Travis to run unit tests and integration tests. For the integration tests to pass, contributors need to
make sure that the `JC_API_KEY` environmental variable in their Travis CI environment is set to a
[Jumpcloud API Key](https://jumpcloud.com/demo) &mdash;specifically, one corresponding to a "clean" JumpCloud instance
(i.e. it should have no users, groups, etc.).
4. Make a pull request from the feature/issue branch on the fork (e.g. `john-smith:jccli/fix-typo-in-docs`) to
`Sage-Bionetworks:jccli/master`.
5. Wait for maintainers to review code and approve the pull request.

Maintainers should use the following process for reviewing and approving outside pull requests:

1. Examine proposed changes on GitHub. Pay special attention to hidden environment variables (as of write time,
`JC_API_KEY`) and make sure nothing in the changes could expose them or use them for unintended purposes. *If in doubt,
DO NOT proceed to the next step*.
2. Incorporate the changes into a new branch in our repo, e.g. create a branch `Sage-Bionetworks:jccli/fix-typo-in-docs`
and manually pull in the changes from `john-smith:jccli/fix-typo-in-docs`. Make a new tracking remote branch (i.e. `git
push --set-upstream origin fix-typo-in-docs`, or whatever the name of your remote is, instead of `origin`) and push to
it in order to trigger a Travis CI build. Make sure that the `integration-test` job ran and passed successfully.
3. Approve/merge the pull request and delete the feature branch made for testing purposes
(`Sage-Bionetworks:jccli/fix-types-in-docs`, in the example).

## Versioning
We try to follow [semantic versioning](https://semver.org/) as much as possble.
We use [bump2version](https://pypi.org/project/bump2version/) to help automate
versioning of this project.

To manually bump the version:
```
bumpversion patch --config-file setup.cfg
```

## Releasing

We have setup our CI to automate a release of this app.  To kick off the process just create
a tag (i.e v1.0.0) and push to the repo.  It is important to have the `v` in the tag and
the tag must be the same number as the current version.  Our CI will do the work of publishing
the app to pypi and then bumping to the next version for development.

## Resources

Below are some handy resource links.

* [Project Documentation](http://jccli.readthedocs.io/)
* [Click](http://click.pocoo.org/5/) is a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary.
* [Sphinx](http://www.sphinx-doc.org/en/master/) is a tool that makes it easy to create intelligent and beautiful documentation, written by Geog Brandl and licnsed under the BSD license.
* [pytest](https://docs.pytest.org/en/latest/) helps you write better programs.
* [GNU Make](https://www.gnu.org/software/make/) is a tool which controls the generation of executables and other non-source files of a program from the program's source files.
