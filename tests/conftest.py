import os
import shutil
import tempfile

import dotenv
import pytest

__all__ = [
    "load_dotenv",
    "mock_env",
    "temp_cache",
    "temp_user_home",
]


@pytest.fixture(scope="session", autouse=True)
def load_dotenv():
    """
    Load the dotenv file named '.env.tests' in the project root for tests.

    You may put the proxy settings in the dotenv file.
    """
    dotenv_path = dotenv.find_dotenv(".env.tests")
    if os.path.exists(dotenv_path):
        dotenv.load_dotenv(dotenv_path)


@pytest.fixture(scope="session", autouse=True)
def temp_cache():
    """
    Clean up the fake cache directory after the test session.

    The cache directory is overwritten by the test session for tests only,
    so we need to clean it up.
    """
    cache_root = tempfile.mkdtemp(prefix="dofu-tests-cache")

    yield cache_root

    if os.path.exists(cache_root):
        shutil.rmtree(cache_root)


@pytest.fixture(scope="session", autouse=True)
def temp_user_home():
    """
    Clean up the fake user home directory after the test session.

    The user home is overwritten by the test session for tests only,
    so we need to clean it up.
    """
    user_home_root = tempfile.mkdtemp(prefix="dofu-tests-user-home")

    yield user_home_root

    if os.path.exists(user_home_root):
        shutil.rmtree(user_home_root)


@pytest.fixture(scope="session", autouse=True)
def mock_env(temp_cache, temp_user_home):
    """
    Mock the env methods for tests.

    We need to overwrite the env like cache directory and user home for tests
    to prevent the tests from polluting the real cache and user home.
    """
    from dofu import env

    def __overwrite_cache_root_for_tests():
        if not os.path.exists(temp_cache):
            os.makedirs(temp_cache)
        return temp_cache

    def __overwrite_user_home():
        if not os.path.exists(temp_user_home):
            os.makedirs(temp_user_home)
        return temp_user_home

    # Mock the env methods for tests
    env.cache_root = __overwrite_cache_root_for_tests
    env.user_home = __overwrite_user_home
