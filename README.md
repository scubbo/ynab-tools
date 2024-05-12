# ynab-tools

[![PyPI](https://img.shields.io/pypi/v/ynab-tools.svg)](https://pypi.org/project/ynab-tools/)
[![Changelog](https://img.shields.io/github/v/release/scubbo/ynab-tools?include_prereleases&label=changelog)](https://github.com/scubbo/ynab-tools/releases)
[![Tests](https://github.com/scubbo/ynab-tools/actions/workflows/test.yml/badge.svg)](https://github.com/scubbo/ynab-tools/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/scubbo/ynab-tools/blob/master/LICENSE)

Tools for use with YNAB ("You Need A Budget")

## Installation

Install this tool using `pip`:
```bash
pip install ynab-tools
```
## Usage

For help, run:
```bash
ynab-tools --help
```
You can also use:
```bash
python -m ynab_tools --help
```
## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd ynab-tools
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
