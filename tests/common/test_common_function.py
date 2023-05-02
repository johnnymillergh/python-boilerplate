from loguru import logger
from pytest_mock import MockerFixture

from python_boilerplate.common.common_function import get_cpu_count, get_login_user


def test_get_cpu_count_when_cpu_count_is_none_then_returns_4(
    mocker: MockerFixture,
) -> None:
    # pytest-mock, patch, https://pytest-mock.readthedocs.io/en/latest/usage.html
    patch = mocker.patch("os.cpu_count", return_value=None)
    cpu_count = get_cpu_count()
    assert cpu_count == 4
    patch.assert_called_once()


def test_get_login_user(mocker: MockerFixture) -> None:
    # pytest-mock, spy, https://pytest-mock.readthedocs.io/en/latest/usage.html#spy
    import getpass

    spy = mocker.spy(getpass, "getuser")
    login_user = get_login_user()
    assert len(login_user) > 0
    logger.info(f"Current login user is [{login_user}]")
    assert len(spy.spy_return) > 0
    assert spy.call_count == 1
    spy.assert_called_once()


def test_get_login_user_when_exception_raised_then_returns_default_user(
    mocker: MockerFixture,
) -> None:
    patch = mocker.patch(
        "getpass.getuser", side_effect=Exception("Mocked exception: can't get user")
    )
    user = get_login_user()
    assert user == "default_user"
    patch.assert_called_once()
