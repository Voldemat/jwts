import pytest


@pytest.fixture
def test_data() -> dict[str, str | bool]:
    return {"ok": True, "data": "test-data"}
