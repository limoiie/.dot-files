import logging
import os
import pathlib
import re
import sys

import pytest

from dofu import shutils


class TestDryRunSubprocess:
    @pytest.fixture(autouse=True)
    def _enable_dry_run(self, enable_dry_run):
        pass

    def test_call(self, caplog):
        with caplog.at_level(logging.INFO):
            ret = shutils.call("echo hello")
        assert ret == 0

        # the command is not executed, but printed
        assert '\n'.join(caplog.messages) == "echo hello ()"

    def test_run(self, caplog):
        with caplog.at_level(logging.INFO):
            ret = shutils.run("echo hello", capture_output=True)

        assert isinstance(ret, shutils.CompletedProcess)
        assert ret.returncode == 0
        assert ret.stdout is None
        assert ret.stderr is None

        # the command is not executed, but printed
        assert '\n'.join(caplog.messages) == "echo hello ()"

    def test_check_output(self, caplog):
        with caplog.at_level(logging.INFO):
            ret = shutils.check_output("echo hello")
        assert ret == b""

        # the command is not executed, but printed
        assert '\n'.join(caplog.messages) == "echo hello ()"

    def test_check_call(self, caplog):
        with caplog.at_level(logging.INFO):
            ret = shutils.check_call("echo hello")
        assert ret == 0

        # the command is not executed, but printed
        assert '\n'.join(caplog.messages) == "echo hello ()"


class TestDryRunFileUpdateGuarder:
    @pytest.fixture(autouse=True)
    def _enable_dry_run(self, enable_dry_run):
        pass

    def test_basic(self, caplog, tmp_path):
        dummy_file = tmp_path / "dummy.txt"
        dummy_file.write_text("hello\n")

        tmp_dummy_file = tmp_path / "dummy.txt.dofu.tmp"

        with caplog.at_level(logging.INFO):
            with shutils.file_update_guarder(dummy_file) as tmp_file:
                pathlib.Path(tmp_file).write_text("world\n")

        assert re.match(r".*mv .*dummy.txt.dofu.tmp .*dummy.txt", caplog.text)

        # the tmp file was deleted
        assert not os.path.exists(tmp_dummy_file)
        # the original file is not changed
        assert os.path.exists(dummy_file)
        assert dummy_file.read_text() == "hello\n"

    def test_on_exception_when_no_update(self, caplog, tmp_path):
        dummy_file = tmp_path / "dummy.txt"
        dummy_file.write_text("hello\n")

        tmp_dummy_file = tmp_path / "dummy.txt.dofu.tmp"

        with pytest.raises(ValueError):
            with caplog.at_level(logging.INFO):
                with shutils.file_update_guarder(dummy_file):
                    # no update
                    raise ValueError("oops")

        assert caplog.text == ""

        # the tmp file was not created
        assert not os.path.exists(tmp_dummy_file)
        # the original file is not changed
        assert os.path.exists(dummy_file)
        assert dummy_file.read_text() == "hello\n"

    def test_on_exception_when_update(self, caplog, tmp_path):
        dummy_file = tmp_path / "dummy.txt"
        dummy_file.write_text("hello\n")

        tmp_dummy_file = tmp_path / "dummy.txt.dofu.tmp"

        with pytest.raises(ValueError):
            with caplog.at_level(logging.INFO):
                with shutils.file_update_guarder(dummy_file) as tmp_file:
                    tmp_dummy_file.write_text("world\n")
                    assert tmp_dummy_file.samefile(tmp_file)
                    raise ValueError("oops")

        assert caplog.text == ""

        # the tmp file was not created
        assert not os.path.exists(tmp_dummy_file)
        # the original file is not changed
        assert os.path.exists(dummy_file)
        assert dummy_file.read_text() == "hello\n"


class TestDryRunInputFile:
    @pytest.fixture(autouse=True)
    def _enable_dry_run(self, enable_dry_run):
        pass

    def test_basic(self, capsys, caplog, tmp_path):
        dummy_file = tmp_path / "dummy.txt"
        dummy_file.write_text("hello\n")

        # the file is supposed to be updated inplace, if not dry run
        with caplog.at_level(logging.INFO):
            with shutils.input_file(dummy_file, inplace=True) as f:
                for line in f:
                    sys.stdout.write(line.replace("hello", "world"))

        # the changes do not executed, but printed
        assert re.match(r".*replace.* as:", caplog.text)
        assert capsys.readouterr().out == "world\n"

        # the original file is not changed
        assert os.path.exists(dummy_file)
        assert dummy_file.read_text() == "hello\n"
