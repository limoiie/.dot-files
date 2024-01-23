import os

import dotenv
import pytest

__all__ = [
    'load_dotenv',
]


@pytest.fixture(scope="session", autouse=True)
def load_dotenv():
    dotenv_path = dotenv.find_dotenv('.env.tests')
    if os.path.exists(dotenv_path):
        dotenv.load_dotenv(dotenv_path)
