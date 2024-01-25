import pytest

from dofu.module import Module, ModuleRegistrationManager

MRM = ModuleRegistrationManager


class TestModuleRegistration:
    @pytest.fixture(scope="function", autouse=True)
    def graph(self, registration_preserver):
        """
        Provide a clean registration env and graph for each test.
        """
        yield registration_preserver

    # noinspection PyUnusedLocal
    def test_register_module(self, graph):
        # first registration
        @Module.module("test")
        class TestModule(Module):
            pass

        assert TestModule in graph

        with pytest.raises(ValueError, match="module test .* already registered"):
            # duplicated registration
            @Module.module("test")
            class TestOtherModule(Module):
                pass

        assert TestModule in graph

    def test_register_module_with_dependency(self, graph):
        @Module.module("test")
        class TestModule(Module):
            pass

        @Module.module("other", requires=[TestModule])
        class TestOtherModule(Module):
            pass

        assert TestModule in graph
        assert TestOtherModule in graph
        assert graph.has_edge(TestOtherModule, TestModule)

        MRM.validate()

    def test_register_module_with_dependency_cycle(self, graph):
        class TestModule(Module):
            pass

        class TestOtherModule(Module):
            pass

        Module.module("test", requires=[TestOtherModule])(TestModule)
        Module.module("other", requires=[TestModule])(TestOtherModule)

        assert TestModule in graph
        assert TestOtherModule in graph
        assert graph.has_edge(TestOtherModule, TestModule)
        assert graph.has_edge(TestModule, TestOtherModule)

        with pytest.raises(ValueError, match=".*dependency cycle.*"):
            MRM.validate()

    def test_resolve_equip_blueprint(self, graph):
        @Module.module("test")
        class TestModule(Module):
            pass

        @Module.module("other", requires=[TestModule])
        class TestOtherModule(Module):
            pass

        @Module.module("another", requires=[TestOtherModule])
        class TestAnotherModule(Module):
            pass

        blueprint = MRM.resolve_equip_blueprint(["test"])
        assert blueprint == [TestModule]

        blueprint = MRM.resolve_equip_blueprint(["other"])
        assert blueprint == [TestModule, TestOtherModule]

        blueprint = MRM.resolve_equip_blueprint(["another"])
        assert blueprint == [TestModule, TestOtherModule, TestAnotherModule]

        blueprint = MRM.resolve_equip_blueprint(["test", "other"])
        assert blueprint == [TestModule, TestOtherModule]

        blueprint = MRM.resolve_equip_blueprint(["other", "test"])
        assert blueprint == [TestModule, TestOtherModule]

        blueprint = MRM.resolve_equip_blueprint(["test", "another"])
        assert blueprint == [TestModule, TestOtherModule, TestAnotherModule]

        blueprint = MRM.resolve_equip_blueprint(["another", "test"])
        assert blueprint == [TestModule, TestOtherModule, TestAnotherModule]

        @Module.module("one-more", requires=[TestModule, TestAnotherModule])
        class TestOneMoreModule(Module):
            pass

        blueprint = MRM.resolve_equip_blueprint(["one-more"])
        assert blueprint == [
            TestModule,
            TestOtherModule,
            TestAnotherModule,
            TestOneMoreModule,
        ]

        blueprint = MRM.resolve_equip_blueprint(["one-more", "test"])
        assert blueprint == [
            TestModule,
            TestOtherModule,
            TestAnotherModule,
            TestOneMoreModule,
        ]

        blueprint = MRM.resolve_equip_blueprint(["test", "one-more", "test"])
        assert blueprint == [
            TestModule,
            TestOtherModule,
            TestAnotherModule,
            TestOneMoreModule,
        ]

    def test_resolve_remove_blueprint(self, graph):
        @Module.module("test")
        class TestModule(Module):
            pass

        @Module.module("other", requires=[TestModule])
        class TestOtherModule(Module):
            pass

        @Module.module("another", requires=[TestOtherModule])
        class TestAnotherModule(Module):
            pass

        blueprint = MRM.resolve_remove_blueprint(["test"])
        assert blueprint == [TestAnotherModule, TestOtherModule, TestModule]

        blueprint = MRM.resolve_remove_blueprint(["other"])
        assert blueprint == [TestAnotherModule, TestOtherModule]

        blueprint = MRM.resolve_remove_blueprint(["another"])
        assert blueprint == [TestAnotherModule]

        blueprint = MRM.resolve_remove_blueprint(["test", "other"])
        assert blueprint == [TestAnotherModule, TestOtherModule, TestModule]

        blueprint = MRM.resolve_remove_blueprint(["other", "test"])
        assert blueprint == [TestAnotherModule, TestOtherModule, TestModule]

        blueprint = MRM.resolve_remove_blueprint(["test", "another"])
        assert blueprint == [TestAnotherModule, TestOtherModule, TestModule]

        blueprint = MRM.resolve_remove_blueprint(["another", "other"])
        assert blueprint == [TestAnotherModule, TestOtherModule]

        @Module.module("one-more", requires=[TestModule, TestAnotherModule])
        class TestOneMoreModule(Module):
            pass

        blueprint = MRM.resolve_remove_blueprint(["one-more"])
        assert blueprint == [TestOneMoreModule]

        blueprint = MRM.resolve_remove_blueprint(["one-more", "other"])
        assert blueprint == [TestOneMoreModule, TestAnotherModule, TestOtherModule]

        blueprint = MRM.resolve_remove_blueprint(["another", "one-more", "another"])
        assert blueprint == [TestOneMoreModule, TestAnotherModule]

    def test_module_meta_by_name(self, graph):
        @Module.module("test")
        class TestModule(Module):
            pass

        assert MRM.module_meta_by_name("test") is not None
        assert MRM.module_meta_by_name("test").name == "test"

        assert MRM.module_class_by_name("test") is not None
        assert MRM.module_class_by_name("test") == TestModule

        assert MRM.module_meta(TestModule)
        assert MRM.module_meta(TestModule) is not None
        assert MRM.module_meta(TestModule).name == "test"

        with pytest.raises(ValueError, match="module .* is not registered"):
            MRM.module_meta_by_name("other")
