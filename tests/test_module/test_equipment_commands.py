import os.path
import subprocess

import pytest

from dofu import equipment as eqp, module, undoable_commands as ucs


class TestEquipmentSyncCommands:
    @pytest.fixture(scope="function", autouse=True)
    def graph(self, registration_preserver):
        """
        This fixture is responsible to provide a clean graph for each test.

        Any registration happened during the test will be removed after the test.
        """
        yield registration_preserver

    @pytest.fixture(scope="function")
    def prepare_module(self, tmp_path):
        """
        Prepare a module with a git repo requirement for testing sync.
        """

        # noinspection PyUnusedLocal
        @module.Module.module("test-one-module")
        class TestOneModule(module.Module):
            _package_requirements = []
            _gitrepo_requirements = []
            _command_requirements = [
                ucs.UCMkdir(
                    path=tmp_path / "test-config-dir",
                ),
                ucs.UCSymlink(
                    src=tmp_path / "test-config-dir",
                    dst=tmp_path / "test-config-link",
                ),
                ucs.UCBackupMv(
                    tmp_path / "test-config-dir",
                ),
            ]

        yield TestOneModule

    def test_sync(self, capfd, tmp_path, prepare_module):
        # install test-one-module
        mngr = eqp.ModuleEquipmentManager()
        mngr.sync(["test-one-module"])
        meta = mngr.meta["test-one-module"]

        assert len(meta.transactions) == 1
        assert meta.len_commands == 3

        assert not os.path.exists(tmp_path / "test-config-dir")
        assert os.path.islink(tmp_path / "test-config-link")
        assert os.path.isdir(tmp_path / "test-config-dir.dofu.bak")

    def test_rollback_lazily(self, capfd, tmp_path, prepare_module):
        # install test-one-module
        mngr = eqp.ModuleEquipmentManager()
        mngr.sync(["test-one-module"])
        meta = mngr.meta["test-one-module"]

        itr = iter(meta.rollback_lazily())
        next(itr)
        # assert the backup-mv is rolled back
        assert os.path.isdir(tmp_path / "test-config-dir")
        assert os.path.islink(tmp_path / "test-config-link")
        assert not os.path.exists(tmp_path / "test-config-dir.dofu.bak")

        next(itr)
        # assert the link is rolled back
        assert os.path.isdir(tmp_path / "test-config-dir")
        assert not os.path.exists(tmp_path / "test-config-link")
        assert not os.path.exists(tmp_path / "test-config-dir.dofu.bak")

        next(itr)
        # assert the mkdir is rolled back
        assert not os.path.exists(tmp_path / "test-config-dir")
        assert not os.path.exists(tmp_path / "test-config-link")
        assert not os.path.exists(tmp_path / "test-config-dir.dofu.bak")

    def test_sync_with_common_steps(self, tmp_path, prepare_module):
        # install test-one-module
        mngr = eqp.ModuleEquipmentManager()
        mngr.sync(["test-one-module"])

        # change the commands while preserving the first two steps
        prepare_module._command_requirements.pop()
        prepare_module._command_requirements.append(
            ucs.UCMove(
                tmp_path / "test-config-link",
                tmp_path / "test-config-moved",
            )
        )
        mngr.sync(["test-one-module"])
        meta = mngr.meta["test-one-module"]

        # assert the transactions are traced correctly
        assert meta.len_commands == 3
        assert len(meta.transactions) == 2
        assert meta.transactions[0].len == 3
        assert meta.transactions[0].effect_len == 2
        assert meta.transactions[1].len == 1
        assert meta.transactions[1].effect_len == 1

        # assert the sync works correctly:
        # - the backup-mv from test-config-dir to test-config.dir.dofu.bak is rolled back
        # - the test-config-link is moved to test-config-moved
        assert os.path.exists(tmp_path / "test-config-dir")
        assert not os.path.exists(tmp_path / "test-config-link")
        assert not os.path.exists(tmp_path / "test-config-dir.dofu.bak")
        assert os.path.islink(tmp_path / "test-config-moved")

    def test_sync_with_error_inner_rollback(self, tmp_path, prepare_module):
        # install test-one-module
        mngr = eqp.ModuleEquipmentManager()
        mngr.sync(["test-one-module"])
        meta = mngr.meta["test-one-module"]

        # mock the env broken -- some traced file is deleted for unknown reason
        # this will cause the second command failed to roll back
        os.unlink(tmp_path / "test-config-link")

        # clear all the config commands
        prepare_module._command_requirements.clear()

        with pytest.raises(subprocess.CalledProcessError, match="non-zero exit"):
            mngr.sync(["test-one-module"])

        # assert the broken command is still here
        assert meta.len_commands == 2
        assert (
            meta.transactions[-1].status
            == eqp.ModuleEquipmentTransactionStatus.FAILED_ROLLBACK
        )

    def test_sync_with_error_inner_transaction(self, tmp_path, prepare_module):
        # install test-one-module
        mngr = eqp.ModuleEquipmentManager()
        mngr.sync(["test-one-module"])

        # mock the env broken -- some traced file is deleted for unknown reason
        # this will cause the following command failed
        os.unlink(tmp_path / "test-config-link")

        # change the commands while preserving the first two steps
        prepare_module._command_requirements.append(
            ucs.UCMove(
                tmp_path / "test-config-link",
                tmp_path / "test-config-moved",
            )
        )
        with pytest.raises(subprocess.CalledProcessError, match="non-zero exit"):
            mngr.sync(["test-one-module"])

        meta = mngr.meta["test-one-module"]
        assert meta.len_commands == 3
        assert len(meta.transactions) == 1
