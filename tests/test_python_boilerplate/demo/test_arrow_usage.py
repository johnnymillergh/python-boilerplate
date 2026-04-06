import arrow
from loguru import logger
from pytest_benchmark.fixture import BenchmarkFixture

from python_boilerplate.demo.arrow_usage import convert_time_zone, string_to_datetime


def test_string_to_datetime() -> None:
    datetime = string_to_datetime("2022-01-01 15:15:00")
    assert datetime is not None
    tzinfo = datetime.tzinfo
    assert tzinfo is not None
    logger.info(f"Parsed time zone: {tzinfo}")
    now = arrow.now()
    assert datetime < now
    logger.info(f"Now: {now}, datetime: {datetime}")


def test_convert_time_zone() -> None:
    now = arrow.now()
    converted = convert_time_zone(now, "UTC")
    logger.info(f"Now: {now}, converted UTC: {converted}")
    assert converted is not None
    converted = convert_time_zone(converted, "+01:00")
    tzinfo = converted.tzinfo
    assert tzinfo is not None
    logger.info(f"Now: {now}, converted +01:00: {converted}")
    assert converted is not None
    converted = convert_time_zone(converted.shift(days=-1), "+02:00")
    logger.info(f"Now: {now}, converted +02:00: {converted}")
    assert converted is not None
    assert converted < now
    logger.info(f"Now: {now}, converted: {converted}")


def test_string_to_datetime_benchmark(benchmark: BenchmarkFixture) -> None:
    benchmark(string_to_datetime, "2022-01-01 15:15:00")
