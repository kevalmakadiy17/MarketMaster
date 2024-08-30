# MarketMaster

![Tests](https://github.com/wheelercj/marketmaster/actions/workflows/tests.yml/badge.svg)

Stock predictions made with [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity).

![graph menu](docs/images/graph%20menu.png)

## dev environment setup

0. Install [Python 3.10](https://www.python.org/downloads/release/python-3108/) if you haven't already.
1. Use `git clone https://github.com/wheelercj/MarketMaster.git` where you want the project's folder to appear and use `cd MarketMaster` to navigate into the new folder.
2. Create a virtual environment, such as with `py -3.10 -m venv venv` or `python3.10 -m venv venv`, and [activate the virtual environment](https://python.land/virtual-environments/virtualenv).
3. Install the app's dependencies with `pip install -r requirements-dev.txt`.
4. Set up the [pre-commit](https://pre-commit.com/) hooks with `pre-commit install`.

Now that the environment is set up, here are some new commands you can use:

* `briefcase dev` to run the app in dev mode. See [BeeWare Briefcase's docs](https://docs.beeware.org/en/latest/tutorial/tutorial-3.html) for more info if needed.
* `pytest` to run all the tests (except the GUI tests) locally in the current environment.
* `pytest src/tests_gui` to run the GUI tests locally in the current environment.
* `coverage report` to get a brief test coverage report, or `coverage html` for a detailed one.
* `pre-commit run --all-files` to run all the pre-commit hooks without committing.
* `pre-commit run hook-id-here --file file-path-here.py` to run one pre-commit hook on one file without committing.

## development

* When starting work on a new feature or other change, follow the steps in the "collaborating" section [here](https://wheelercj.github.io/notes/pages/20210907144216.html) to prevent changes from being lost.
* When a pre-commit hook fails, your options are:
    1. Follow the error message's suggestion.
    2. Add a comment to disable the pre-commit hook for specific parts of the code. See the [flake8](https://flake8.pycqa.org/en/latest/user/violations.html#in-line-ignoring-errors) and/or the [mypy](https://mypy.readthedocs.io/en/stable/common_issues.html#spurious-errors-and-locally-silencing-the-checker) docs for how to do this.
    3. Commit without running the hooks with `git commit --no-verify` for a local commit, but please fix the issue with an amend or a later commit before pushing.
* When bumping the app's version: do a global search for the current version because the version number is in multiple files.
* When adding, removing, or changing a dependency:
    * If it's a development dependency: update `requirements-dev.txt`.
    * If the dependency is for the app itself: update `requirements.txt` and the `requires` list under `[tool.briefcase.app.marketmaster]` in `pyproject.toml`.

## distribution

* `briefcase dev` to run the app in dev mode.
* `briefcase create` to create the app template.
* `briefcase update` to copy new changes into the platform directory.
* `briefcase update -d` to update the dependencies in the packaged app.
* `briefcase build` to compile the app.
* `briefcase run` to run the compiled app.
* `briefcase run -u` to update, build, and run the compiled app.
* `briefcase package` to create the app's installer for the current platform.
* `briefcase package -u` to update, build, and create the app's installer for the current platform.

## resources

* [intro to Python](https://wheelercj.github.io/notes/pages/20220109123727.html)
* [getting started with Git and GitHub](https://wheelercj.github.io/notes/pages/20210907144216.html)
* [Installing packages using pip and virtual environments – Python.org](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#installing-packages-using-pip-and-virtual-environments "Permalink to this headline")
* [Python import: Advanced Techniques and Tips – Real Python](https://realpython.com/python-import/#create-and-install-a-local-package)
* [Docstring formats – Real Python](https://realpython.com/documenting-python-code/#docstring-formats)
* [Plotting with PyQtGraph – Python GUIs](https://www.pythonguis.com/tutorials/pyside6-plotting-pyqtgraph/)
* [python packaging: basic setup.py and declarative metadata (intermediate) – Youtube](https://www.youtube.com/watch?v=GaWs-LenLYE&list=PLWBKAf81pmOaP9naRiNAqug6EBnkPakvY)
* [Packaging and distributing projects – Python.org](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#packaging-and-distributing-projects "Permalink to this headline")

### dependency docs

* [Python](https://docs.python.org/3/)
* [pytest](https://docs.pytest.org/en/6.2.x/contents.html)
* [pytest-qt](https://pytest-qt.readthedocs.io/en/latest/tutorial.html)
* [coverage](https://coverage.readthedocs.io/en/6.5.0/)
* [tox](https://tox.wiki/en/latest/)
* [PySide](https://doc.qt.io/qtforpython/index.html)
* [PyQtGraph](https://pyqtgraph.readthedocs.io/en/latest/)
* [BeeWare Briefcase](https://briefcase.readthedocs.io/en/latest/)
* [pre-commit](https://pre-commit.com/)
* [Black](https://black.readthedocs.io/en/stable/)
* [mypy](https://mypy.readthedocs.io/en/stable/)
* [flake8](https://flake8.pycqa.org/en/latest/)
* [FinanceDataReader API](https://github.com/financedata-org/FinanceDataReader)
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
* [NumPy](https://numpy.org/doc/1.23/)
* [pandas](https://pandas.pydata.org/pandas-docs/stable/)
* [SciPy](https://docs.scipy.org/doc/scipy/)
* [Matplotlib](https://matplotlib.org/)
* [scikit-learn](https://scikit-learn.org/stable/index.html)
