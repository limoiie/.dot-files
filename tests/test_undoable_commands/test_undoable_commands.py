import os
import re
import shutil

from dofu import undoable_command as uc


class TestUCSymlink:
    def test_spec_tuple(self):
        assert uc.UCSymlink(src="a", dst="b").spec_tuple() == ("a", "b")

    def test_exec_undo(self, tmp_dir_with_a_dummy_file):
        tmp_dir, dummy_file = tmp_dir_with_a_dummy_file
        link_file = f"{dummy_file}.ln"

        # exec
        cmd = uc.UCSymlink(src=dummy_file, dst=link_file)
        ret = cmd.exec()
        assert ret.retcode == 0
        assert ret.stdout is None
        assert ret.stderr is None

        assert os.path.islink(link_file)

        # undo
        cmd.undo()

        assert not os.path.exists(link_file)
        assert os.path.exists(dummy_file)

    def test_exec_undo_with_missing_src(self, tmp_dir_with_a_dummy_file):
        tmp_dir, dummy_file = tmp_dir_with_a_dummy_file
        non_existing_file = f"{dummy_file}.non-existing"
        link_file = f"{dummy_file}.ln"

        # exec
        cmd = uc.UCSymlink(src=non_existing_file, dst=link_file)
        ret = cmd.exec()
        assert ret.retcode == 1
        assert isinstance(ret.stderr, (str, bytes))
        assert re.search(rb"Failed to ln -s.*not exists.*", ret.stderr)
        assert ret.stdout is None

    def test_exec_undo_with_existing_dst(self, tmp_dir_with_a_dummy_file):
        tmp_dir, dummy_file = tmp_dir_with_a_dummy_file
        link_file = f"{dummy_file}.ln"

        # exec
        cmd = uc.UCSymlink(src=dummy_file, dst=link_file)
        ret = cmd.exec()
        assert ret.retcode == 0
        assert ret.stdout is None
        assert ret.stderr is None

        assert os.path.islink(link_file)

        # exec again
        cmd = uc.UCSymlink(src=dummy_file, dst=link_file)
        ret = cmd.exec()
        assert ret.retcode == 1
        assert isinstance(ret.stderr, (str, bytes))
        assert re.search(rb"Failed to ln -s.*exists.*", ret.stderr)
        assert ret.stdout is None

    def test_exec_undo_with_removed_link(self, tmp_dir_with_a_dummy_file):
        tmp_dir, dummy_file = tmp_dir_with_a_dummy_file
        link_file = f"{dummy_file}.ln"

        # exec
        cmd = uc.UCSymlink(src=dummy_file, dst=link_file)
        ret = cmd.exec()
        assert ret.retcode == 0
        assert ret.stdout is None
        assert ret.stderr is None

        assert os.path.islink(link_file)

        # remove link
        os.unlink(link_file)

        # undo
        ret = cmd.undo()
        assert isinstance(ret, uc.ExecutionResult)
        assert ret.retcode == 1
        assert isinstance(ret.stderr, (str, bytes))
        assert re.search(rb"Failed to unlink.*not exists.*", ret.stderr)


class TestUCLink:
    def test_spec_tuple(self):
        assert uc.UCLink(src="a", dst="b").spec_tuple() == ("a", "b")

    def test_exec_undo(self, tmp_dir_with_a_dummy_file):
        tmp_dir, dummy_file = tmp_dir_with_a_dummy_file
        link_file = f"{dummy_file}.ln"

        assert os.stat(dummy_file).st_nlink == 1

        # exec
        cmd = uc.UCLink(src=dummy_file, dst=link_file)
        ret = cmd.exec()
        assert ret.retcode == 0
        assert ret.stdout is None
        assert ret.stderr is None

        assert not os.path.islink(link_file)
        assert os.stat(dummy_file).st_ino == os.stat(link_file).st_ino
        assert os.stat(dummy_file).st_nlink == os.stat(link_file).st_nlink == 2

        # undo
        cmd.undo()

        assert not os.path.exists(link_file)
        assert os.path.exists(dummy_file)

    def test_exec_undo_with_missing_src(self, tmp_dir_with_a_dummy_file):
        tmp_dir, dummy_file = tmp_dir_with_a_dummy_file
        non_existing_file = f"{dummy_file}.non-existing"
        link_file = f"{dummy_file}.ln"

        # exec
        cmd = uc.UCLink(src=non_existing_file, dst=link_file)
        ret = cmd.exec()
        assert ret.retcode == 1
        assert isinstance(ret.stderr, (str, bytes))
        assert re.search(rb"Failed to ln.*not exists.*", ret.stderr)
        assert ret.stdout is None

    def test_exec_undo_with_existing_dst(self, tmp_dir_with_a_dummy_file):
        tmp_dir, dummy_file = tmp_dir_with_a_dummy_file
        link_file = f"{dummy_file}.ln"

        # exec
        cmd = uc.UCLink(src=dummy_file, dst=link_file)
        ret = cmd.exec()
        assert ret.retcode == 0
        assert ret.stdout is None
        assert ret.stderr is None

        assert not os.path.islink(link_file)
        assert os.stat(dummy_file).st_ino == os.stat(link_file).st_ino
        assert os.stat(dummy_file).st_nlink == os.stat(link_file).st_nlink == 2

        # exec again
        cmd = uc.UCLink(src=dummy_file, dst=link_file)
        ret = cmd.exec()
        assert ret.retcode == 1
        assert isinstance(ret.stderr, (str, bytes))
        assert re.search(rb"Failed to ln.*exists.*", ret.stderr)
        assert ret.stdout is None

    def test_exec_undo_with_removed_link(self, tmp_dir_with_a_dummy_file):
        tmp_dir, dummy_file = tmp_dir_with_a_dummy_file
        link_file = f"{dummy_file}.ln"

        # exec
        cmd = uc.UCLink(src=dummy_file, dst=link_file)
        ret = cmd.exec()
        assert ret.retcode == 0
        assert ret.stdout is None
        assert ret.stderr is None

        assert not os.path.islink(link_file)
        assert os.stat(dummy_file).st_ino == os.stat(link_file).st_ino
        assert os.stat(dummy_file).st_nlink == os.stat(link_file).st_nlink == 2

        # remove link
        os.unlink(link_file)

        # undo
        ret = cmd.undo()
        assert isinstance(ret, uc.ExecutionResult)
        assert ret.retcode == 1
        assert isinstance(ret.stderr, (str, bytes))
        assert re.search(rb"Failed to unlink.*not exists.*", ret.stderr)


class TestBackupMv:
    def test_spec_tuple(self):
        assert uc.UCBackupMv(path="a").spec_tuple() == ("a",)

    def test_exec_undo(self, tmp_dir_with_a_dummy_file):
        tmp_dir, dummy_file = tmp_dir_with_a_dummy_file

        # exec
        cmd = uc.UCBackupMv(path=dummy_file)
        ret = cmd.exec()
        assert ret.retcode == 0
        assert ret.stdout is None
        assert ret.stderr is None

        assert not os.path.exists(dummy_file)
        assert os.path.exists(f"{dummy_file}.dofu.bak")

        # undo
        cmd.undo()

        assert os.path.exists(dummy_file)
        assert not os.path.exists(f"{dummy_file}.dofu.bak")

    def test_exec_undo_with_missing_src(self, tmp_dir_with_a_dummy_file):
        tmp_dir, dummy_file = tmp_dir_with_a_dummy_file
        non_existing_file = f"{dummy_file}.non-existing"

        # exec
        cmd = uc.UCBackupMv(path=non_existing_file)
        ret = cmd.exec()
        assert ret.retcode == 1
        assert isinstance(ret.stderr, (str, bytes))
        assert re.search(rb"Failed to backup mv.*not exists.*", ret.stderr)
        assert ret.stdout is None

    def test_exec_undo_with_existing_backup(self, tmp_dir_with_a_dummy_file):
        tmp_dir, dummy_file = tmp_dir_with_a_dummy_file
        backup_file = f"{dummy_file}.dofu.bak"

        # create backup file manually
        shutil.copy(dummy_file, backup_file)

        # exec
        cmd = uc.UCBackupMv(path=dummy_file)
        ret = cmd.exec()
        assert ret.retcode == 0
        assert ret.stdout is None
        assert ret.stderr is None

        assert not os.path.exists(dummy_file)
        assert os.path.exists(f"{dummy_file}.dofu.bak")
        assert os.path.exists(f"{dummy_file}.dofu.bak.bak")

        # undo
        cmd.undo()

        assert os.path.exists(dummy_file)
        assert os.path.exists(f"{dummy_file}.dofu.bak")
        assert not os.path.exists(f"{dummy_file}.dofu.bak.bak")


class TestMkdir:
    def test_spec_tuple(self):
        assert uc.UCMkdir(path="a").spec_tuple() == ("a",)

    def test_exec_undo(self, tmp_path):
        path_to_make = tmp_path / "nested" / "sub" / "dir"
        assert not os.path.exists(path_to_make)

        # exec
        cmd = uc.UCMkdir(path=path_to_make)
        ret = cmd.exec()
        assert ret.retcode == 0
        assert ret.stdout is None
        assert ret.stderr is None

        assert os.path.exists(path_to_make)

        # undo
        cmd.undo()

        assert not os.path.exists(path_to_make)  # ./nested/sub/dir
        assert not os.path.exists(path_to_make.parent)  # ./nested/sub
        assert not os.path.exists(path_to_make.parent.parent)  # ./nested
        assert os.path.exists(path_to_make.parent.parent.parent)  # ./

    def test_exec_undo_with_existing_dir(self, tmp_path):
        path_to_make = tmp_path / "nested" / "sub" / "dir"
        assert not os.path.exists(path_to_make)

        # exec
        cmd = uc.UCMkdir(path=path_to_make)
        ret = cmd.exec()
        assert ret.retcode == 0
        assert ret.stdout is None
        assert ret.stderr is None

        assert os.path.exists(path_to_make)

        # exec again
        again_cmd = uc.UCMkdir(path=path_to_make)
        ret = again_cmd.exec()
        assert ret.retcode == 0
        assert ret.stdout is None
        assert ret.stderr is None

        assert os.path.exists(path_to_make)

        # undo
        assert again_cmd.undo() is None

        assert os.path.exists(path_to_make)

        assert cmd.undo() is None

        assert not os.path.exists(path_to_make)  # ./nested/sub/dir
        assert not os.path.exists(path_to_make.parent)  # ./nested/sub
        assert not os.path.exists(path_to_make.parent.parent)  # ./nested
        assert os.path.exists(path_to_make.parent.parent.parent)  # ./


class TestMove:
    def test_spec_tuple(self):
        assert uc.UCMove(src="a", dst="b").spec_tuple() == ("a", "b")

    def test_exec_undo(self, tmp_dir_with_a_dummy_file):
        tmp_dir, src_file = tmp_dir_with_a_dummy_file
        dst_file = f"{src_file}.mv"

        # exec
        cmd = uc.UCMove(src=src_file, dst=dst_file)
        ret = cmd.exec()
        assert ret.retcode == 0
        assert ret.stdout is None
        assert ret.stderr is None

        assert not os.path.exists(src_file)
        assert os.path.exists(dst_file)

        # undo
        cmd.undo()

        assert os.path.exists(src_file)
        assert not os.path.exists(dst_file)

    def test_exec_undo_with_missing_src(self, tmp_dir_with_a_dummy_file):
        tmp_dir, src_file = tmp_dir_with_a_dummy_file
        non_existing_file = f"{src_file}.non-existing"
        dst_file = f"{src_file}.mv"

        # exec
        cmd = uc.UCMove(src=non_existing_file, dst=dst_file)
        ret = cmd.exec()
        assert ret.retcode == 1
        assert isinstance(ret.stderr, (str, bytes))
        assert re.search(rb"Failed to mv.*not exists.*", ret.stderr)
        assert ret.stdout is None

    def test_exec_undo_with_existing_dst(self, tmp_dir_with_a_dummy_file):
        tmp_dir, src_file = tmp_dir_with_a_dummy_file
        dst_file = f"{src_file}.mv"

        # exec
        cmd = uc.UCMove(src=src_file, dst=dst_file)
        ret = cmd.exec()
        assert ret.retcode == 0
        assert ret.stdout is None
        assert ret.stderr is None

        assert not os.path.exists(src_file)
        assert os.path.exists(dst_file)

        # exec again
        cmd = uc.UCMove(src=src_file, dst=dst_file)
        ret = cmd.exec()
        assert ret.retcode == 1
        assert isinstance(ret.stderr, (str, bytes))
        assert re.search(rb"Failed to mv.*exists.*", ret.stderr)
        assert ret.stdout is None


class TestReplaceLine:
    def test_spec_tuple(self):
        cmd = uc.UCReplaceLine(path="a", pattern="b", new_line="c")
        assert cmd.spec_tuple() == ("a", "b", "c")

    def test_exec_undo(self, tmp_dir_with_a_dummy_file):
        tmp_dir, dummy_file = tmp_dir_with_a_dummy_file

        with open(dummy_file) as f:
            origin_content = f.read()

        # exec
        cmd = uc.UCReplaceLine(path=dummy_file, pattern="dummy", new_line="DUMMY")
        ret = cmd.exec()
        assert ret.retcode == 0
        assert ret.stdout is None
        assert ret.stderr is None

        with open(dummy_file) as f:
            assert f.read() == "DUMMY"

        # undo
        cmd.undo()

        with open(dummy_file) as f:
            assert f.read() == origin_content

    def test_exec_undo_with_missing_src(self, tmp_dir_with_a_dummy_file):
        tmp_dir, dummy_file = tmp_dir_with_a_dummy_file
        non_existing_file = f"{dummy_file}.non-existing"

        # exec
        cmd = uc.UCReplaceLine(path=non_existing_file, pattern="dummy", new_line="DUMMY")
        ret = cmd.exec()
        assert ret.retcode == 1
        assert isinstance(ret.stderr, (str, bytes))
        assert re.search(rb"Failed to replace line.*not exists.*", ret.stderr)
        assert ret.stdout is None
