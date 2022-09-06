![Python Boilerplate Social Image](./python_boilerplate.png)
[![GitHub release](https://img.shields.io/github/release/johnnymillergh/python_boilerplate.svg)](https://github.com/johnnymillergh/python_boilerplate/releases)
[![Github Actions workflow status](https://github.com/johnnymillergh/python_boilerplate/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/johnnymillergh/python_boilerplate/actions)
[![GitHub issues](https://img.shields.io/github/issues/johnnymillergh/python_boilerplate)](https://github.com/johnnymillergh/python_boilerplate/issues)
[![GitHub forks](https://img.shields.io/github/forks/johnnymillergh/python_boilerplate)](https://github.com/johnnymillergh/python_boilerplate/network)
[![GitHub stars](https://img.shields.io/github/stars/johnnymillergh/python_boilerplate)](https://github.com/johnnymillergh/python_boilerplate)
[![GitHub license](https://img.shields.io/github/license/johnnymillergh/python_boilerplate)](https://github.com/johnnymillergh/python_boilerplate/blob/master/LICENSE)
[![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/johnnymillergh/python_boilerplate.svg?style=popout)](https://github.com/johnnymillergh/python_boilerplate)
[![GitHub repo size](https://img.shields.io/github/repo-size/johnnymillergh/python_boilerplate.svg)](https://github.com/johnnymillergh/python_boilerplate)
[![Twitter](https://img.shields.io/twitter/url/https/github.com/johnnymillergh/python_boilerplate?style=social)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2Fjohnnymillergh%2Fpython_boilerplate)

# Python Boilerplate

**python_boilerplate** is a boilerplate project for Python. Based on template [sourcery-ai/python-best-practices-cookiecutter](https://github.com/sourcery-ai/python-best-practices-cookiecutter).

[Official Docker Image](https://github.com/johnnymillergh/python_boilerplate/pkgs/container/python_boilerplate%2Fpython_boilerplate)

## Features

Here is the highlights of **python_boilerplate**:

1. Inherited from modern and the latest Python technologies:

   `Python` - [![Python](https://img.shields.io/badge/Python-v3.10.6-blue)](https://www.python.org/downloads/release/python-3106/)

   `Pipenv` is to build and compile the project

2. Highly customizable data analysis with [pandas](https://pandas.pydata.org/), enhanced array operation with [NumPy](https://numpy.org/). Supports CSV, excel, JSON and so on

3. Data persistence with [peewee](http://docs.peewee-orm.com/en/latest/), [SQLite3](https://sqlite.org/index.html) as local database

4. Simple and flexible retry with [Tenacity](https://github.com/jd/tenacity)

5. Environment variable and configuration with [pyhocon](https://pythonhosted.org/pyhocon/_modules/pyhocon.html). Read `${ENVIRONMENT_VARIABLE}` when startup

6. Sensible and human-friendly approach to creating, manipulating, formatting and converting dates, times and timestamps with [Arrow](https://pypi.org/project/arrow/)

7. Generate fake data with [Faker](https://pypi.org/project/Faker/)

8. Testing with [pytest](https://docs.pytest.org/en/latest/), integrating [pytest-mock](https://pypi.org/project/pytest-mock/) for mocking, [pytest-cov](https://pypi.org/project/pytest-cov/) for code coverage analysis and [pyinstrument](https://github.com/joerick/pyinstrument) for Python stack profiler

9. Formatting with [black](https://github.com/psf/black)

10. Import sorting with [isort](https://github.com/timothycrosley/isort)

11. Static typing with [mypy](http://mypy-lang.org/)

12. Linting with [flake8](http://flake8.pycqa.org/en/latest/)

13. Git hooks that run all the above with [pre-commit](https://pre-commit.com/)

14. Deployment ready with [Docker](https://docker.com/)

15. Continuous Integration with [GitHub Actions](https://github.com/features/actions)

16. Loguru logging configuration. Log sample is like,

   ```
   2022-09-06 10:02:06.716 | ⚠️ WARNING  | MainThread      | python_boilerplate.repository.model.base_model.<module>:24 - SQLite database created. Path: [D:\Projects\PyCharmProjects\python_boilerplate\data\python_boilerplate.db], <peewee.SqliteDatabase object at 0x0000021CB40A8E80>
   2022-09-06 10:02:06.718 | ℹ️ INFO     | MainThread      | python_boilerplate.common.orm.peewee_table:16 - Registering peewee table: StartupLog
   2022-09-06 10:02:06.719 | 🐞 DEBUG    | MainThread      | peewee.execute_sql:3185 - ('CREATE TABLE IF NOT EXISTS "startup_log" ("id" INTEGER NOT NULL PRIMARY KEY, "current_user" VARCHAR(50) NOT NULL, "host" VARCHAR(50) NOT NULL, "command_line" TEXT NOT NULL, "current_working_directory" TEXT NOT NULL, "startup_time" DATETIME NOT NULL, "created_by" VARCHAR(50) NOT NULL, "created_time" DATETIME NOT NULL, "modified_by" VARCHAR(50) NOT NULL, "modified_time" DATETIME NOT NULL)', [])
   2022-09-06 10:02:06.882 | ℹ️ INFO     | MainThread      | python_boilerplate.<module>:35 - Application [python_boilerplate] started
   ```

## Usage

1. Clone or download this project.

   ```shell
   $ git clone https://github.com/johnnymillergh/python_boilerplater.git
   ```

2. Build with newest PyCharm.

3. Click the green triangle to Run.

## Setup

1. Setup the development environment

   ```shell
   # Install pipx if pipenv and cookiecutter are not installed
   $ python3 -m pip install pipx
   $ python3 -m pipx ensurepath
   
   # Install pipenv using pipx
   $ pipx install pipenv
   ```

2. Install dependencies

   ```shell
   $ pipenv install --dev
   ```

3. Setup pre-commit and pre-push hooks

   ```shell
   $ pipenv run pre-commit install -t pre-commit
   $ pipenv run pre-commit install -t pre-push
   ```

## Useful Commands

### Run Unit Tests

Run with pytest, analyze code coverage, generate HTML code coverage reports, fail the test if coverage percentage is unser 85%

```shell
$ pipenv run pytest --cov --cov-report html --cov-fail-under=85 --capture=no --log-cli-level=INFO
```

### Conventional Changelog CLI

1. Install global dependencies (optional if installed):

   ```shell
   $ npm install -g conventional-changelog-cli
   ```

2. This will *not* overwrite any previous changelogs. The above generates a changelog based on commits since the last semver tag that matches the pattern of "Feature", "Fix", "Performance Improvement" or "Breaking Changes".

   ```shell
   $ conventional-changelog -p angular -i CHANGELOG.md -s
   ```

3. If this is your first time using this tool and you want to generate all previous changelogs, you could do:

   ```shell
   $ conventional-changelog -p angular -i CHANGELOG.md -s -r 0
   ```

## CI (Continuous Integration)

- GitHub Actions is for building project and running tests.
- ~~[Travis CI](https://travis-ci.com/github/johnnymillergh/) is for publishing Docker Hub images of SNAPSHOT and RELEASE.~~

## Maintainers

[@johnnymillergh](https://github.com/johnnymillergh).

## Contributing

Feel free to dive in! [Open an issue](https://github.com/johnnymillergh/python_boilerplate/issues/new).

### Contributors

This project exists thanks to all the people who contribute. 

- Johnny Miller [[@johnnymillergh](https://github.com/johnnymillergh)]
- …


### Sponsors

Support this project by becoming a sponsor. Your logo will show up here with a link to your website. [[Become a sponsor](https://become-a-sponsor.org)]

## Credits

This package was created with Cookiecutter and the [sourcery-ai/python-best-practices-cookiecutter](https://github.com/sourcery-ai/python-best-practices-cookiecutter) project template.

Inspired by [How to set up a perfect Python project](https://sourcery.ai/blog/python-best-practices/).

## License

[Apache License](https://github.com/johnnymillergh/python_boilerplate/blob/master/LICENSE) © Johnny Miller

2021 - Present
