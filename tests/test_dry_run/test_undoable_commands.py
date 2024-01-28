import logging
import os
import re

import pytest

from dofu import undoable_commands as ucs
from tests.test_undoable_commands.conftest import tmp_dir_with_a_dummy_file


class TestDryRunUCSymlink:
    @pytest.fixture(autouse=True)
    def _enable_dry_run(self, enable_dry_run):
        pass

    def test_exec_undo(self, caplog, tmp_dir_with_a_dummy_file):
        tmp_dir, dummy_file = tmp_dir_with_a_dummy_file
        link_file = f"{dummy_file}.ln"

        # exec
        cmd = ucs.UCSymlink(src=dummy_file, dst=link_file)
        caplog.clear()
        with caplog.at_level(logging.INFO):
            ret = cmd.exec()
        assert ret.retcode == 0
        assert ret.stdout is None
        assert ret.stderr is None

        # ln -s not executed, but printed
        assert not os.path.exists(link_file)
        assert re.match(
            r"ln -s .*dummy_file .*dummy_file.ln", "\n".join(caplog.messages)
        )

        # undo
        caplog.clear()
        with caplog.at_level(logging.INFO):
            cmd.undo()

        assert re.match(r"unlink .*dummy_file.ln", "\n".join(caplog.messages))

        assert not os.path.exists(link_file)
        assert os.path.exists(dummy_file)


class TestDryRunUCLink:
    @pytest.fixture(autouse=True)
    def _enable_dry_run(self, enable_dry_run):
        pass

    def test_exec_undo(self, caplog, tmp_dir_with_a_dummy_file):
        tmp_dir, dummy_file = tmp_dir_with_a_dummy_file
        link_file = f"{dummy_file}.ln"

        # exec
        cmd = ucs.UCLink(src=dummy_file, dst=link_file)
        caplog.clear()
        with caplog.at_level(logging.INFO):
            ret = cmd.exec()
        assert ret.retcode == 0
        assert ret.stdout is None
        assert ret.stderr is None

        # ln not executed, but printed
        assert not os.path.exists(link_file)
        assert re.match(r"ln .*dummy_file .*dummy_file.ln", "\n".join(caplog.messages))

        # undo
        caplog.clear()
        with caplog.at_level(logging.INFO):
            cmd.undo()

        assert re.match(r"unlink .*dummy_file.ln", "\n".join(caplog.messages))

        assert not os.path.exists(link_file)
        assert os.path.exists(dummy_file)


class TestDryRunUCBackupMv:
    @pytest.fixture(autouse=True)
    def _enable_dry_run(self, enable_dry_run):
        pass

    def test_exec_undo(self, caplog, tmp_dir_with_a_dummy_file):
        tmp_dir, dummy_file = tmp_dir_with_a_dummy_file
        backup_file = f"{dummy_file}.dofu.bak"

        # exec
        cmd = ucs.UCBackupMv(path=dummy_file)
        caplog.clear()
        with caplog.at_level(logging.INFO):
            ret = cmd.exec()
        assert ret.retcode == 0
        assert ret.stdout is None
        assert ret.stderr is None

        # mv not executed, but printed
        assert not os.path.exists(backup_file)
        assert re.match(
            r"mv .*dummy_file .*dummy_file.dofu.bak", "\n".join(caplog.messages)
        )

        # undo
        caplog.clear()
        with caplog.at_level(logging.INFO):
            cmd.undo()

        assert re.match(
            r"mv .*dummy_file.dofu.bak .*dummy_file", "\n".join(caplog.messages)
        )

        assert not os.path.exists(backup_file)
        assert os.path.exists(dummy_file)


class TestDryRunUCMkdir:
    @pytest.fixture(autouse=True)
    def _enable_dry_run(self, enable_dry_run):
        pass

    def test_exec_undo(self, caplog, tmp_dir_with_a_dummy_file):
        tmp_dir, dummy_file = tmp_dir_with_a_dummy_file
        new_dir = f"{tmp_dir}/nested/sub/dir"

        # exec
        cmd = ucs.UCMkdir(path=new_dir)
        caplog.clear()
        with caplog.at_level(logging.INFO):
            ret = cmd.exec()
        assert ret.retcode == 0
        assert ret.stdout is None
        assert ret.stderr is None

        # mkdir not executed, but printed
        assert not os.path.exists(new_dir)
        assert re.match(r"mkdir -p .*nested/sub/dir", "\n".join(caplog.messages))

        # mick the creating
        os.makedirs(new_dir)

        # undo
        caplog.clear()
        with caplog.at_level(logging.INFO):
            cmd.undo()

        # not undo the creation, but printed
        assert os.path.exists(new_dir)
        assert re.match(
            r"" r"rm -r .*nested/sub/dir.*" r"rm -r .*nested/sub.*" r"rm -r .*nested",
            "\n".join(caplog.messages),
            re.DOTALL | re.MULTILINE,
        )


class TestDryRunUCMove:
    @pytest.fixture(autouse=True)
    def _enable_dry_run(self, enable_dry_run):
        pass

    def test_exec_undo(self, caplog, tmp_dir_with_a_dummy_file):
        tmp_dir, dummy_file = tmp_dir_with_a_dummy_file
        dst_file = f"{dummy_file}.mv"

        # exec
        cmd = ucs.UCMove(src=dummy_file, dst=dst_file)
        caplog.clear()
        with caplog.at_level(logging.INFO):
            ret = cmd.exec()
        assert ret.retcode == 0
        assert ret.stdout is None
        assert ret.stderr is None

        # mv not executed, but printed
        assert not os.path.exists(dst_file)
        assert re.match(r"mv .*dummy_file .*dummy_file.mv", "\n".join(caplog.messages))

        # mick the moving
        os.rename(dummy_file, dst_file)
        assert os.path.exists(dst_file)

        # undo
        caplog.clear()
        with caplog.at_level(logging.INFO):
            cmd.undo()

        # not undo the creation, but printed
        assert os.path.exists(dst_file)
        assert re.match(r"mv .*dummy_file.mv .*dummy_file", "\n".join(caplog.messages))


class TestDryRunUCReplaceLine:
    @pytest.fixture(autouse=True)
    def _enable_dry_run(self, enable_dry_run):
        pass

    def test_exec_undo(self, caplog, capsys, tmp_dir_with_a_dummy_file):
        tmp_dir, dummy_file = tmp_dir_with_a_dummy_file

        # exec
        cmd = ucs.UCAppendLine(path=dummy_file, pattern="dummy", repl="DUMMY")
        caplog.clear()
        with caplog.at_level(logging.INFO):
            ret = cmd.exec()
        assert ret.retcode == 0
        assert ret.stdout is None
        assert ret.stderr is None

        # mv not executed, but printed
        assert re.match(r"update.* as:", "\n".join(caplog.messages))
        assert capsys.readouterr().out == "DUMMY"

        # mick the replacing
        dummy_file.write_text("DUMMY\n")

        # undo
        caplog.clear()
        with caplog.at_level(logging.INFO):
            cmd.undo()

        # not undo the creation, but printed
        assert re.match(r"update.* as:", "\n".join(caplog.messages))
        assert capsys.readouterr().out == "dummy"
        assert os.path.exists(dummy_file)
        assert dummy_file.read_text() == "DUMMY\n"
