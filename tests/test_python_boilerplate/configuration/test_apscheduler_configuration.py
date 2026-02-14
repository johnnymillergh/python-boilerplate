import sys
from time import sleep

import pytest
from apscheduler.triggers.cron import CronTrigger
from loguru import logger
from pytest_mock import MockerFixture, MockFixture

from python_boilerplate.configuration.apscheduler_configuration import (
    cleanup,
    configure,
    scheduler,
)


def test_configure() -> None:
    try:
        configure()
    except Exception as ex:
        pytest.fail(f"{configure} raised an exception {ex}")


@scheduler.scheduled_job(trigger=CronTrigger.from_crontab("* * * * *"))
def timed_job() -> None:
    logger.info("This is a timed job")


def timed_job_with_args(a_int: int, a_string: str) -> None:
    logger.info(f"This is a timed job with args: {a_int}, {a_string}")


def test_scheduler_when_adding_in_interval_job(mocker: MockFixture) -> None:
    if not scheduler.running:
        scheduler.start()
    timed_job_spy = mocker.spy(sys.modules[__name__], "timed_job")
    timed_job_with_args_spy = mocker.spy(sys.modules[__name__], "timed_job_with_args")
    try:
        scheduler.add_job(func=timed_job, trigger="interval", seconds=1)
        scheduler.add_job(func=timed_job_with_args, trigger="interval", seconds=1, args=(200, "OK"))
        sleep(5)
    except Exception as ex:
        pytest.fail(f"{scheduler} raised an exception. {ex}")
    assert timed_job_spy.call_count <= 5
    assert timed_job_with_args_spy.call_count <= 5


def test_cleanup(mocker: MockerFixture) -> None:
    # pytest-mock, patch an object, https://pytest-mock.readthedocs.io/en/latest/usage.html
    executor_patch = mocker.patch.object(scheduler, "shutdown")
    cleanup()
    executor_patch.assert_called_once()
