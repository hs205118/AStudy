import pytest
from app.infrastructure.artifact_store import LocalArtifactStore

def test_put_get(tmp_path):
    store = LocalArtifactStore(tmp_path)
    uri, digest = store.put("run/a.txt", b"hello")
    assert store.get(uri) == b"hello"
    assert len(digest) == 64

def test_reject_path_traversal(tmp_path):
    store = LocalArtifactStore(tmp_path)
    with pytest.raises(ValueError): store.put("../escape", b"x")
