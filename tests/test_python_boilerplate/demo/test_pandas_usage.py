from collections.abc import Hashable, Iterable
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
import pytest
from loguru import logger

from python_boilerplate.common.profiling import cpu_profile, elapsed_time, mem_profile
from python_boilerplate.demo.pandas_usage import (
    data_generation,
    look_for_sony_published_games,
    pandas_data_structure_date_range,
    pandas_data_structure_series,
    sony_published_video_games_path,
    video_games,
)

if TYPE_CHECKING:
    from pandas import DataFrame, DatetimeIndex, Series

# https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html#minutes-to-pandas


@elapsed_time("INFO")
@mem_profile("INFO")
@cpu_profile("INFO")
def test_pandas_data_structure_series() -> None:
    series: Series = pandas_data_structure_series()
    assert series.dtype == np.dtype("float64")
    assert len(series) == 6
    logger.info(f"series:\n{series}")


@elapsed_time("INFO")
@mem_profile("INFO")
@cpu_profile("INFO")
def test_pandas_data_structure_date_range() -> None:
    dates: DatetimeIndex = pandas_data_structure_date_range()
    assert dates.dtype == np.dtype("datetime64[us]")
    assert len(dates) == 6
    date1 = dates.array[0].date()
    logger.info(f"date 1: {date1}")
    logger.info(f"dates:\n{dates}")


@elapsed_time("INFO")
@mem_profile("INFO")
@cpu_profile("INFO")
def test_pandas_reading_csv() -> None:
    """
    Read a csv file.

    See the CSV & text files https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-read-csv-table
    """
    logger.info(f"video_games:\n{video_games}")
    logger.info(f"Head of video_games:\n{video_games.head()}")
    logger.info(f"Tail of video_games:\n{video_games.tail()}")
    logger.info(f"video_games.columns:\n{video_games.columns}")
    logger.info(f"video_games.index:\n{video_games.index}")
    logger.info(f"video_games.info():\n{video_games.info()}")
    logger.info(f"video_games.iloc[1]:\n{video_games.iloc[1]}")
    iterable_video_games: Iterable[tuple[Hashable, Series]] = video_games.iterrows()
    for index, row in iterable_video_games:
        logger.info(f"index: {index}, title: {row['Title']}")
        if index == 5:
            break
    assert video_games is not None
    assert video_games.iloc[1]["Release.Console"] == "Sony PSP"


@elapsed_time("INFO")
@mem_profile("INFO")
@cpu_profile("INFO")
def test_look_for_sony_published_games() -> None:
    sony_published_games: DataFrame = look_for_sony_published_games()
    assert sony_published_games is not None
    assert len(sony_published_games) == 9
    assert Path(sony_published_video_games_path).exists(), "CSV file NOT exists!"


@elapsed_time("INFO")
@mem_profile("INFO")
@cpu_profile("INFO")
def test_data_generation() -> None:
    try:
        data_generation()
    except Exception as ex:
        pytest.fail(f"{data_generation} raised an exception {ex}")
