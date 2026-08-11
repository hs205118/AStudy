from copy import deepcopy
from typing import Any

def apply_json_patch(document: dict[str, Any], operations: list[dict[str, Any]]) -> dict[str, Any]:
    """Small RFC 6902 subset: add, replace, remove. Array append uses '-' token."""
    result = deepcopy(document)
    for op in operations:
        operation, path = op["op"], op["path"]
        if not path.startswith("/"):
            raise ValueError("Patch path must start with /")
        tokens = [t.replace("~1", "/").replace("~0", "~") for t in path[1:].split("/") if t != ""]
        if not tokens:
            raise ValueError("Root replacement is not supported")
        parent: Any = result
        for token in tokens[:-1]:
            parent = parent[int(token)] if isinstance(parent, list) else parent[token]
        key = tokens[-1]
        if operation in {"add", "replace"}:
            value = op.get("value")
            if isinstance(parent, list):
                if key == "-": parent.append(value)
                elif operation == "add": parent.insert(int(key), value)
                else: parent[int(key)] = value
            else: parent[key] = value
        elif operation == "remove":
            if isinstance(parent, list): parent.pop(int(key))
            else: parent.pop(key)
        else:
            raise ValueError(f"Unsupported patch operation: {operation}")
    return result
