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

    def test_call(self, capsys):
        ret = shutils.call("echo hello")
        assert ret == 0

        # the command is not executed, but printed
        assert capsys.readouterr().out == "echo hello ()\n"

    def test_run(self, capsys):
        ret = shutils.run("echo hello", capture_output=True)
        assert isinstance(ret, shutils.CompletedProcess)
        assert ret.returncode == 0
        assert ret.stdout is None
        assert ret.stderr is None

        # the command is not executed, but printed
        assert capsys.readouterr().out == "echo hello ()\n"

    def test_check_output(self, capsys):
        ret = shutils.check_output("echo hello")
        assert ret == b""

        # the command is not executed, but printed
        assert capsys.readouterr().out == "echo hello ()\n"

    def test_check_call(self, capsys):
        ret = shutils.check_call("echo hello")
        assert ret == 0

        # the command is not executed, but printed
        assert capsys.readouterr().out == "echo hello ()\n"


class TestDryRunFileUpdateGuarder:
    @pytest.fixture(autouse=True)
    def _enable_dry_run(self, enable_dry_run):
        pass

    def test_basic(self, capsys, tmp_path):
        dummy_file = tmp_path / "dummy.txt"
        dummy_file.write_text("hello\n")

        tmp_dummy_file = tmp_path / "dummy.txt.dofu.tmp"

        with shutils.file_update_guarder(dummy_file) as tmp_file:
            pathlib.Path(tmp_file).write_text("world\n")

        assert re.match(
            r"move .*.dummy.txt.dofu.tmp to .*dummy.txt", capsys.readouterr().out
        )

        # the tmp file was deleted
        assert not os.path.exists(tmp_dummy_file)
        # the original file is not changed
        assert os.path.exists(dummy_file)
        assert dummy_file.read_text() == "hello\n"

    def test_on_exception_when_no_update(self, capsys, tmp_path):
        dummy_file = tmp_path / "dummy.txt"
        dummy_file.write_text("hello\n")

        tmp_dummy_file = tmp_path / "dummy.txt.dofu.tmp"

        with pytest.raises(ValueError):
            with shutils.file_update_guarder(dummy_file):
                # no update
                raise ValueError("oops")

        assert capsys.readouterr().out == ""
        assert capsys.readouterr().err == ""

        # the tmp file was not created
        assert not os.path.exists(tmp_dummy_file)
        # the original file is not changed
        assert os.path.exists(dummy_file)
        assert dummy_file.read_text() == "hello\n"

    def test_on_exception_when_update(self, capsys, tmp_path):
        dummy_file = tmp_path / "dummy.txt"
        dummy_file.write_text("hello\n")

        tmp_dummy_file = tmp_path / "dummy.txt.dofu.tmp"

        with pytest.raises(ValueError):
            with shutils.file_update_guarder(dummy_file) as tmp_file:
                tmp_dummy_file.write_text("world\n")
                assert tmp_dummy_file.samefile(tmp_file)
                raise ValueError("oops")

        assert capsys.readouterr().out == ""
        assert capsys.readouterr().err == ""

        # the tmp file was not created
        assert not os.path.exists(tmp_dummy_file)
        # the original file is not changed
        assert os.path.exists(dummy_file)
        assert dummy_file.read_text() == "hello\n"


class TestDryRunInputFile:
    @pytest.fixture(autouse=True)
    def _enable_dry_run(self, enable_dry_run):
        pass

    def test_basic(self, capsys, tmp_path):
        dummy_file = tmp_path / "dummy.txt"
        dummy_file.write_text("hello\n")

        # the file is supposed to be updated inplace, if not dry run
        with shutils.input_file(dummy_file, inplace=True) as f:
            for line in f:
                sys.stdout.write(line.replace("hello", "world"))

        # the changes do not executed, but printed
        assert re.match(
            r"The file .* will be updated inplace as:\nworld", capsys.readouterr().out
        )

        # the original file is not changed
        assert os.path.exists(dummy_file)
        assert dummy_file.read_text() == "hello\n"
