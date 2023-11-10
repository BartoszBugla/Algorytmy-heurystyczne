
# Poetry: Python packaging and dependency management made easy

Poetry helps you declare, manage and install dependencies of Python projects,
ensuring you have the right stack everywhere.

![Poetry Install](https://raw.githubusercontent.com/python-poetry/poetry/master/assets/install.gif)

Poetry replaces `setup.py`, `requirements.txt`, `setup.cfg`, `MANIFEST.in` and `Pipfile` with a simple `pyproject.toml`
based project format.


## Installation

Poetry supports multiple installation methods, including a simple script found at [install.python-poetry.org]. For full
installation instructions, including advanced usage of the script, alternate install methods, and CI best practices, see
the full [installation documentation].

## Documentation

[Documentation] for the current version of Poetry (as well as the development branch and recently out of support
versions) is available from the [official website].

## Run project backend

Install all necessary dependencies

```Bash
poetry install
```

Open development server

```Bash
poetry run python main.py
```

## Working with VSCode 

```Bash
poetry env info --path
```

Then click `cmd/ctrl + shift + p`, type `Python: Select Interpreter`, and paste the output of the previous command




