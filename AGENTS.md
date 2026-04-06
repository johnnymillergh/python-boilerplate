# AGENTS.md

Guidelines for AI agents working in this repository.

## Build & Run Commands

| Task | Command |
|------|---------|
| Install deps | `uv sync --extra test --extra dev --extra linter` |
| Run application | `uv run python -m python_boilerplate` |
| Lint (ruff) | `uv run ruff check .` |
| Lint auto-fix | `uv run ruff check --fix .` |
| Format | `uv run ruff format .` |
| Type check | `uv run mypy` |
| Install mypy stubs | `uv run mypy --install-types` |
| All tests | `uv run pytest --cov -n auto --benchmark-disable` |
| Single test file | `uv run pytest tests/test_python_boilerplate/common/test_profiling.py` |
| Single test func | `uv run pytest tests/test_python_boilerplate/common/test_profiling.py -k test_elapsed_time` |
| Tests with logging | `uv run pytest --log-cli-level=DEBUG --capture=no <path>` |
| Benchmarks only | `uv run pytest --capture=no --log-cli-level=ERROR -n 0 --benchmark-only` |
| Pre-commit (all) | `uv run pre-commit run --all-files` |

## Project Structure

```
src/
  python_boilerplate/
    __init__.py              # freeze_support() call for PyInstaller
    __main__.py              # Application entry point
    common/                  # Shared utilities (decorators, helpers)
    configuration/           # App config, thread pool, logging, scheduler, DB
    data_migration/          # Database migration scripts
    demo/                    # Example/demo scripts
    message/                 # Messaging (email)
    repository/              # Data access layer (peewee ORM models + repos)
    resources/               # Static resources (HOCON config files)
    template/                # Jinja2 templates
tests/
  conftest.py                # Global fixtures (auto_profile with pyinstrument)
  test_python_boilerplate/   # Mirrors src/ structure exactly
    common/
    configuration/
    demo/
    message/
    repository/
    template/
```

Source lives in `src/` (setuptools `package-dir = {"" = "src"}`). Tests mirror the source tree under `tests/test_python_boilerplate/`.

## Tool Configuration

- **Python**: >=3.13.1, <3.14 (`target-version = "py313"`)
- **Package manager**: uv (with `uv.lock`)
- **Linter/Formatter**: Ruff 0.15.x (`lint.select = ["ALL"]` with specific ignores)
- **Type checker**: mypy (strict mode, pydantic plugin)
- **Test runner**: pytest with pytest-xdist (`-n auto`), pytest-cov, pytest-mock, pytest-asyncio, pytest-benchmark
- **Pre-commit hooks**: ruff import sort, ruff check --fix, ruff format, mypy, pytest (pre-commit stage), pytest-cov (pre-push stage)
- **Line length**: 120 characters
- **Indent**: 4 spaces, UTF-8, LF line endings

## Code Style

### Imports

Imports are organized in three groups separated by blank lines, sorted by ruff (`I001`):

```python
# 1. Standard library
import functools
import time
from collections.abc import Callable
from typing import Any

# 2. Third-party
from loguru import logger

# 3. Local (absolute imports only, no relative imports)
from python_boilerplate.common.common_function import json_serial
```

- Use `from collections.abc import Callable, Coroutine` (NOT `from typing import Callable`)
- Relative imports are banned (`ban-relative-imports = "all"` in ruff config)
- `__init__.py` files are mostly empty (no re-exports)

### Type Annotations

- All functions MUST have return type annotations (mypy `disallow_untyped_defs = true`)
- Use PEP 695 type parameter syntax for generic functions: `def foo[T](x: T) -> T:` (NOT `TypeVar`)
- Use `typing.Any` when dynamic types are unavoidable
- Use `typing.Final` for module-level constants
- Use `TYPE_CHECKING` guard for import-only types: `if TYPE_CHECKING: from _pytest.nodes import Node`
- Use `X | Y` union syntax (NOT `Union[X, Y]` or `Optional[X]`)

### Naming Conventions

- Files: `snake_case.py`
- Functions/variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE` with `Final` annotation
- Test files: `test_<module_name>.py` mirroring source structure
- Test functions: `test_<what_is_tested>` or `test_<what_is_tested>_<scenario>`

### Docstrings

Sphinx/reST style with `:param:` and `:return:` directives:

```python
def get_login_user() -> str:
    """
    Get current login user who is using the OS.

    :param username: the username to look up
    :return: the username
    """
```

- Opening `"""` on same line as summary for single-line docstrings
- Opening `"""` on first line with summary for multi-line docstrings
- One blank line between summary and `:param` block (when description exists)

### Error Handling

- Catch specific exceptions, log with `logger.exception()` or `logger.error()`
- Re-raise after logging: `raise e` (do not swallow)
- Use `pytest.raises` for testing expected exceptions
- Pattern: try/execute/except-log-raise/finally-cleanup

```python
try:
    return func(*arg, **kwarg)
except Exception as e:
    logger.warning(f"Captured exception. {e}")
    raise e
finally:
    cleanup()
```

### Logging

- Use `loguru.logger` exclusively (NOT stdlib `logging`)
- f-string formatting in log messages: `logger.info(f"Result: {value}")`
- Available levels: TRACE, DEBUG, INFO, WARNING, ERROR

### Decorators

This codebase makes heavy use of function decorators in `src/python_boilerplate/common/`:

- `@async_function` - Run sync function in thread pool, returns `Future`
- `@async_function_wrapper` - Add done_callback to async function
- `@elapsed_time(level="INFO")` - Profile function timing
- `@async_elapsed_time(level="INFO")` - Profile async function timing
- `@mem_profile()` / `@cpu_profile()` - Resource profiling
- `@peewee_table` - Register ORM table class
- `@trace` / `@async_trace` - Function call tracing to DB
- `@debounce(wait)` / `@throttle(limit)` - Rate limiting

### Testing

- Test files mirror source: `src/.../foo.py` -> `tests/test_python_boilerplate/.../test_foo.py`
- Use `pytest.fixture` for setup; `conftest.py` has `auto_profile` fixture (runs pyinstrument on every test)
- Use `pytest-mock` (`MockerFixture`) for mocking/spying
- Async tests use `@pytest.mark.asyncio`
- Name pattern: `--pytest-test-first` enforced (functions must start with `test_`)
- Coverage target: 90% (enforced in pre-push hook)

### Ruff Ignored Rules

Key intentionally-ignored lint rules (do NOT "fix" these patterns):

- `ANN401` - `typing.Any` is allowed in `*args`/`**kwargs`
- `D100-D104,D106` - Missing docstrings in public modules/classes/functions are allowed
- `EM101,EM102` - String literals in exceptions are OK
- `PLR2004` - Magic values in comparisons are OK
- `COM812` - Trailing commas are not enforced
- `S311` - Pseudo-random generators are OK
- `TRY003,TRY201` - Exception message style is relaxed

Test files (`tests/*`) additionally ignore: `ANN` (annotations), `ARG` (unused args), `INP001`, `S101` (assert).

## CI Pipeline

GitHub Actions (`python-ci-with-uv.yml`) runs on push to main/develop/feature/release/hotfix branches:

1. `uv run ruff check .` (no `--fix` in CI - must pass clean)
2. `uv run mypy` (after installing types)
3. `uv run pytest --quiet --cov --cov-report term -n auto --benchmark-disable`
4. `uv run pytest --benchmark-only` (benchmarks separate)
5. Application smoke test

Note: CI runs `ruff check` WITHOUT `--fix`. Code must pass lint cleanly before push.
