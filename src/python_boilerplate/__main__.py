import atexit
import os
import platform
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

from loguru import logger
from tzlocal import get_localzone

from python_boilerplate.common.common_function import get_module_name
from python_boilerplate.configuration.application_configuration import (
    configure as configure_application,
)
from python_boilerplate.configuration.application_configuration import pyproject_toml
from python_boilerplate.configuration.apscheduler_configuration import (
    cleanup as apscheduler_clean,
)
from python_boilerplate.configuration.apscheduler_configuration import (
    configure as configure_apscheduler,
)
from python_boilerplate.configuration.loguru_configuration import (
    configure as configure_loguru,
)
from python_boilerplate.configuration.peewee_configuration import (
    configure as configure_peewee,
)
from python_boilerplate.configuration.thread_pool_configuration import (
    cleanup as thread_pool_cleanup,
)
from python_boilerplate.configuration.thread_pool_configuration import (
    configure as configure_thread_pool,
)
from python_boilerplate.data_migration.data_migration import init_db_data
from python_boilerplate.message.email import cleanup as email_cleanup
from python_boilerplate.message.email import init_smtp
from python_boilerplate.repository.model.startup_log import StartupLog
from python_boilerplate.repository.startup_log_repository import (
    retain_startup_log,
    save,
    update_latest,
)
from python_boilerplate.repository.trace_log_repository import retain_trace_log

__start_time = time.perf_counter()


def startup() -> None:
    """Call this function to start the application and do all the preparations and configurations."""
    logger.info(
        f"Starting {get_module_name()} using Python {platform.python_version()} on "
        f"{platform.node()} with PID {os.getpid()} ({Path(__file__).parent})"
    )

    # Configuration
    configure_application()
    configure_loguru()
    configure_peewee()
    configure_thread_pool()
    configure_apscheduler()

    # Initialization
    init_smtp()
    init_db_data()

    # Saving startup log
    # Cannot save startup log in parallel, because the ThreadPoolExecutor won't be able to start another future
    # once the MainThread will end very soon.
    save(StartupLog(command_line=" ".join(sys.argv)))

    elapsed = time.perf_counter() - __start_time
    logger.info(f"Started {get_module_name()}@{pyproject_toml['project']['version']} in {timedelta(seconds=elapsed)}")


@atexit.register
def finalize() -> None:
    """Register `finalize()` function to be executed upon normal program termination."""
    logger.warning(f"Stopping {get_module_name()}, releasing system resources")
    # Retain logs, in case the size of the SQLite database will be increasing like crazy.
    retain_startup_log()
    retain_trace_log()
    # Shutdown tread pool and other connections
    thread_pool_cleanup()
    email_cleanup()
    apscheduler_clean()
    update_latest()
    __end_elapsed = time.perf_counter() - __start_time
    logger.info(f"Stopped {get_module_name()}, running for {timedelta(seconds=__end_elapsed)} in total")


def main() -> None:
    logger.info(
        f"Current module: {get_module_name()}, tzname: {datetime.now().astimezone().tzname()}, "
        f"localzone: {get_localzone()}"
    )


if __name__ == "__main__":
    startup()
    main()
