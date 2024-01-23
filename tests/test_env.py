import re

from dofu import env


class TestRootInTests:
    def test_cache_root_in_tests(self):
        assert re.search(r"dofu-tests-cache", env.cache_root())

    def test_persistent_root(self):
        assert re.search(r"dofu-tests-cache.*.persistence", env.persistence_root())

    def test_user_home(self):
        assert re.search(r"dofu-tests-user-home", env.user_home())

    def test_xdg_config_root(self):
        assert re.search(r"dofu-tests-user-home.*.config", env.xdg_config_path())
