import networkx as nx
import pytest

from dofu.module import ModuleRegistrationManager

# noinspection PyUnresolvedReferences
from tests.conftest import *

MRM = ModuleRegistrationManager


@pytest.fixture(scope="function")
def registration_preserver():
    """
    This fixture provides a clean module registration graph for each test.

    Any registration happened during the test will be removed after the test.
    """
    # noinspection PyProtectedMember
    original_graph = MRM._ModuleRegistrationManager__graph
    MRM._ModuleRegistrationManager__graph = nx.DiGraph()
    # noinspection PyProtectedMember
    yield MRM._ModuleRegistrationManager__graph
    MRM._ModuleRegistrationManager__graph = original_graph
