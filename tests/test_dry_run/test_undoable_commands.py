import os
import re

import pytest

from dofu import undoable_command as uc
from tests.test_undoable_commands.conftest import tmp_dir_with_a_dummy_file


class TestDryRunUCSymlink:
    @pytest.fixture(autouse=True)
    def _enable_dry_run(self, enable_dry_run):
        pass

    def test_exec_undo(self, capsys, tmp_dir_with_a_dummy_file):
        tmp_dir, dummy_file = tmp_dir_with_a_dummy_file
        link_file = f"{dummy_file}.ln"

        # exec
        cmd = uc.UCSymlink(src=dummy_file, dst=link_file)
        ret = cmd.exec()
        assert ret.retcode == 0
        assert ret.stdout is None
        assert ret.stderr is None

        # ln -s not executed, but printed
        assert not os.path.exists(link_file)
        assert re.match(
            r"ln -s .*dummy_file to .*dummy_file.ln", capsys.readouterr().out
        )

        # undo
        cmd.undo()

        assert re.match(r"unlink .*dummy_file.ln", capsys.readouterr().out)

        assert not os.path.exists(link_file)
        assert os.path.exists(dummy_file)


class TestDryRunUCLink:
    @pytest.fixture(autouse=True)
    def _enable_dry_run(self, enable_dry_run):
        pass

    def test_exec_undo(self, capsys, tmp_dir_with_a_dummy_file):
        tmp_dir, dummy_file = tmp_dir_with_a_dummy_file
        link_file = f"{dummy_file}.ln"

        # exec
        cmd = uc.UCLink(src=dummy_file, dst=link_file)
        ret = cmd.exec()
        assert ret.retcode == 0
        assert ret.stdout is None
        assert ret.stderr is None

        # ln not executed, but printed
        assert not os.path.exists(link_file)
        assert re.match(r"ln .*dummy_file to .*dummy_file.ln", capsys.readouterr().out)

        # undo
        cmd.undo()

        assert re.match(r"unlink .*dummy_file.ln", capsys.readouterr().out)

        assert not os.path.exists(link_file)
        assert os.path.exists(dummy_file)


class TestDryRunUCBackupMv:
    @pytest.fixture(autouse=True)
    def _enable_dry_run(self, enable_dry_run):
        pass

    def test_exec_undo(self, capsys, tmp_dir_with_a_dummy_file):
        tmp_dir, dummy_file = tmp_dir_with_a_dummy_file
        backup_file = f"{dummy_file}.dofu.bak"

        # exec
        cmd = uc.UCBackupMv(path=dummy_file)
        ret = cmd.exec()
        assert ret.retcode == 0
        assert ret.stdout is None
        assert ret.stderr is None

        # mv not executed, but printed
        assert not os.path.exists(backup_file)
        assert re.match(
            r"mv .*dummy_file .*dummy_file.dofu.bak", capsys.readouterr().out
        )

        # undo
        cmd.undo()

        assert re.match(
            r"mv .*dummy_file.dofu.bak .*dummy_file", capsys.readouterr().out
        )

        assert not os.path.exists(backup_file)
        assert os.path.exists(dummy_file)


class TestDryRunUCMkdir:
    @pytest.fixture(autouse=True)
    def _enable_dry_run(self, enable_dry_run):
        pass

    def test_exec_undo(self, capsys, tmp_dir_with_a_dummy_file):
        tmp_dir, dummy_file = tmp_dir_with_a_dummy_file
        new_dir = f"{tmp_dir}/nested/sub/dir"

        # exec
        cmd = uc.UCMkdir(path=new_dir)
        ret = cmd.exec()
        assert ret.retcode == 0
        assert ret.stdout is None
        assert ret.stderr is None

        # mkdir not executed, but printed
        assert not os.path.exists(new_dir)
        assert re.match(r"mkdir -p .*nested/sub/dir", capsys.readouterr().out)

        # mick the creating
        os.makedirs(new_dir)

        # undo
        cmd.undo()

        # not undo the creation, but printed
        assert os.path.exists(new_dir)
        assert re.match(
            r""
            r"rm -r .*nested/sub/dir.*"
            r"rm -r .*nested/sub.*"
            r"rm -r .*nested",
            capsys.readouterr().out,
            re.DOTALL | re.MULTILINE,
        )


class TestDryRunUCMove:
    @pytest.fixture(autouse=True)
    def _enable_dry_run(self, enable_dry_run):
        pass

    def test_exec_undo(self, capsys, tmp_dir_with_a_dummy_file):
        tmp_dir, dummy_file = tmp_dir_with_a_dummy_file
        dst_file = f"{dummy_file}.mv"

        # exec
        cmd = uc.UCMove(src=dummy_file, dst=dst_file)
        ret = cmd.exec()
        assert ret.retcode == 0
        assert ret.stdout is None
        assert ret.stderr is None

        # mv not executed, but printed
        assert not os.path.exists(dst_file)
        assert re.match(r"mv .*dummy_file .*dummy_file.mv", capsys.readouterr().out)

        # mick the moving
        os.rename(dummy_file, dst_file)
        assert os.path.exists(dst_file)

        # undo
        cmd.undo()

        # not undo the creation, but printed
        assert os.path.exists(dst_file)
        assert re.match(r"mv .*dummy_file.mv .*dummy_file", capsys.readouterr().out)


class TestDryRunUCReplaceLine:
    @pytest.fixture(autouse=True)
    def _enable_dry_run(self, enable_dry_run):
        pass

    def test_exec_undo(self, capsys, tmp_dir_with_a_dummy_file):
        tmp_dir, dummy_file = tmp_dir_with_a_dummy_file

        # exec
        cmd = uc.UCReplaceLine(path=dummy_file, pattern="dummy", repl="DUMMY")
        ret = cmd.exec()
        assert ret.retcode == 0
        assert ret.stdout is None
        assert ret.stderr is None

        # mv not executed, but printed
        assert re.match(
            r"The file .* will be updated inplace as:\nDUMMY", capsys.readouterr().out
        )

        # mick the replacing
        dummy_file.write_text("DUMMY\n")

        # undo
        cmd.undo()

        # not undo the creation, but printed
        assert re.match(
            r"The file .* will be updated inplace as:\ndummy", capsys.readouterr().out
        )
        assert os.path.exists(dummy_file)
        assert dummy_file.read_text() == "DUMMY\n"
