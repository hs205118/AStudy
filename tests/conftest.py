import os
from pathlib import Path
import pytest

@pytest.fixture
def isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("TRD_DATABASE_URL", f"sqlite:///{tmp_path}/test.db")
    monkeypatch.setenv("TRD_ARTIFACT_ROOT", str(tmp_path / "artifacts"))
    return tmp_path
