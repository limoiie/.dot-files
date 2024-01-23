import pytest

# noinspection PyUnresolvedReferences
from tests.conftest import *


@pytest.fixture(scope="function")
def temp_workspace_with_a_dummy_file(tmp_path):
    dummy_file = tmp_path / "dummy_file"
    with open(dummy_file, "w") as f:
        f.write("dummy")

    return tmp_path, dummy_file
