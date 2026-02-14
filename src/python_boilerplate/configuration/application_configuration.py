import tomllib
from pathlib import Path
from typing import Final

from loguru import logger
from pyhocon import ConfigFactory

from python_boilerplate.common.common_function import (
    PROJECT_ROOT_PATH,
    get_resources_dir,
)

# `application_conf` contains the configuration for the application.
application_conf: Final = ConfigFactory.parse_file(get_resources_dir() / "application.conf")


def check_existence(file_path: Path) -> bool:
    return file_path.exists() and file_path.is_file()


_pyproject_toml_file = PROJECT_ROOT_PATH / "pyproject.toml"
if not check_existence(_pyproject_toml_file):
    logger.warning(f"File not found: {_pyproject_toml_file}")
    _pyproject_toml_file = Path(__file__).parent.parent.parent / "pyproject.toml"
    logger.warning(f"Fallback to: {_pyproject_toml_file}")
    if not check_existence(_pyproject_toml_file):
        logger.error(f"Fallback failed due to file not found: {_pyproject_toml_file}")
        raise FileNotFoundError(f"File not found: {_pyproject_toml_file}")
with _pyproject_toml_file.open("rb") as file:
    pyproject_toml: Final = tomllib.load(file)


def configure() -> None:
    """Configure application."""
    logger.warning(f"Application configuration loaded, {application_conf}, {pyproject_toml['project']['name']}")


if __name__ == "__main__":
    configure()
