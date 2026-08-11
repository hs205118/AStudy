import hashlib
from pathlib import Path
from typing import Protocol

class ArtifactStore(Protocol):
    def put(self, key: str, content: bytes) -> tuple[str, str]: ...
    def get(self, uri: str) -> bytes: ...

class LocalArtifactStore:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def put(self, key: str, content: bytes) -> tuple[str, str]:
        safe = Path(key)
        if safe.is_absolute() or ".." in safe.parts:
            raise ValueError("Unsafe artifact key")
        destination = (self.root / safe).resolve()
        if self.root not in destination.parents:
            raise ValueError("Artifact path escapes root")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)
        return str(destination), hashlib.sha256(content).hexdigest()

    def get(self, uri: str) -> bytes:
        path = Path(uri).resolve()
        if self.root != path and self.root not in path.parents:
            raise ValueError("Artifact path escapes root")
        return path.read_bytes()
