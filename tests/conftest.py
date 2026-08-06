import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture
def client():
    original_activities = copy.deepcopy(app_module.activities)
    app_module.activities = copy.deepcopy(original_activities)

    with TestClient(app_module.app) as test_client:
        yield test_client

    app_module.activities = copy.deepcopy(original_activities)
