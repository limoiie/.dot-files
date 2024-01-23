import os.path
import subprocess

import pytest

from dofu import shutils


class TestSubprocess:
    def test_call(self, capfd):
        ret = shutils.call("echo hello", shell=True)
        assert ret == 0
        assert capfd.readouterr().out == "hello\n"

    def test_call_wrong_command(self):
        # wrong command
        with pytest.raises(FileNotFoundError):
            shutils.call("echo hello")

    def test_call_but_return_nonzero(self, capfd):
        # correct command but return non-zero
        ret = shutils.call("echo hello; exit 1", shell=True)
        assert ret == 1
        assert capfd.readouterr().out == "hello\n"

    def test_run(self):
        ret = shutils.run("echo hello", shell=True, capture_output=True)
        assert isinstance(ret, shutils.CompletedProcess)
        assert ret.returncode == 0
        assert ret.stdout == b"hello\n"
        assert ret.stderr == b""

    def test_run_wrong_command(self):
        # wrong command
        with pytest.raises(FileNotFoundError):
            shutils.run("echo hello")

    def test_run_but_return_nonzero(self):
        # correct command but return non-zero
        ret = shutils.run("echo hello; exit 1", shell=True, capture_output=True)
        assert isinstance(ret, shutils.CompletedProcess)
        assert ret.returncode == 1
        assert ret.stdout == b"hello\n"
        assert ret.stderr == b""

    def test_check_output(self):
        ret = shutils.check_output("echo hello", shell=True)
        assert ret == b"hello\n"

    def test_check_output_wrong_command(self):
        # wrong command
        with pytest.raises(FileNotFoundError):
            shutils.check_output("echo hello")

    def test_check_call(self, capfd):
        ret = shutils.check_call("echo hello", shell=True)
        assert ret == 0
        assert capfd.readouterr().out == "hello\n"

    def test_check_call_wrong_command(self):
        # wrong command
        with pytest.raises(FileNotFoundError):
            shutils.check_call("echo hello")

    def test_check_call_but_return_nonzero(self, capfd):
        # correct command but return non-zero
        with pytest.raises(subprocess.CalledProcessError):
            shutils.check_call("echo hello; exit 1", shell=True)
        assert capfd.readouterr().out == "hello\n"


class TestFileUpdateGuarder:
    def test_basic(self, tmp_path):
        dummy_file = tmp_path / "dummy.txt"
        dummy_file.write_text("hello\n")

        tmp_dummy_file = tmp_path / 'dummy.txt.dofu.tmp'

        with shutils.file_update_guarder(dummy_file) as tmp_file:
            tmp_dummy_file.write_text("world\n")
            assert tmp_dummy_file.samefile(tmp_file)

        assert dummy_file.read_text() == "world\n"

    def test_on_exception_when_no_update(self, tmp_path, capfd):
        dummy_file = tmp_path / "dummy.txt"
        dummy_file.write_text("hello\n")

        tmp_dummy_file = tmp_path / 'dummy.txt.dofu.tmp'

        with pytest.raises(ValueError):
            with shutils.file_update_guarder(dummy_file):
                # nothing to do
                raise ValueError("oops")

        assert capfd.readouterr().out == ""
        assert os.path.exists(dummy_file)
        assert dummy_file.read_text() == "hello\n"
        assert not os.path.exists(tmp_dummy_file)

    def test_on_exception_when_update(self, tmp_path, capfd):
        dummy_file = tmp_path / "dummy.txt"
        dummy_file.write_text("hello\n")

        tmp_dummy_file = tmp_path / 'dummy.txt.dofu.tmp'

        with pytest.raises(ValueError):
            with shutils.file_update_guarder(dummy_file) as tmp_file:
                tmp_dummy_file.write_text("world\n")
                assert tmp_dummy_file.samefile(tmp_file)
                raise ValueError("oops")

        assert capfd.readouterr().out == ""
        assert os.path.exists(dummy_file)
        assert dummy_file.read_text() == "hello\n"
        assert not os.path.exists(tmp_dummy_file)


def test_commands_exists(capfd):
    assert shutils.do_commands_exist("echo")
    assert shutils.do_commands_exist("echo", "ls")
    assert not shutils.do_commands_exist("haha")
    assert not shutils.do_commands_exist("echo", "haha")
    capfd.readouterr()
