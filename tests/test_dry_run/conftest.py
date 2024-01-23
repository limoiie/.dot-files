import os
import shutil
import tempfile

import pytest


def under_temp_workspace(*sub_dirs):
    return os.path.join(_temp_workspace, *sub_dirs)


@pytest.fixture(scope="session", autouse=True)
def temp_workspace():
    yield

    if os.path.exists(_temp_workspace):
        shutil.rmtree(_temp_workspace)


_temp_workspace = tempfile.mkdtemp(prefix="dofu-test-dry-run")


@pytest.fixture(scope="function")
def enable_dry_run():
    from dofu.options import Options

    old_value = Options.instance().dry_run
    Options.instance().dry_run = True
    yield
    Options.instance().dry_run = old_value


@pytest.fixture(scope="function")
def disable_dry_run():
    from dofu.options import Options

    old_value = Options.instance().dry_run
    Options.instance().dry_run = False
    yield
    Options.instance().dry_run = old_value
