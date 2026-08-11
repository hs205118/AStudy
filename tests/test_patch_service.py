from app.services.patch_service import apply_json_patch

def test_patch_replace_and_add():
    result = apply_json_patch({"a": 1, "items": []}, [{"op": "replace", "path": "/a", "value": 2}, {"op": "add", "path": "/items/-", "value": "x"}])
    assert result == {"a": 2, "items": ["x"]}
