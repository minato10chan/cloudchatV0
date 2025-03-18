from typing import List, Dict, Any

class TextData:
    def __init__(self, content: str, metadata: Dict[str, Any] = None):
        self.content = content
        self.metadata = metadata or {}

class VectorData:
    def __init__(self, vector: List[float], metadata: Dict[str, Any] = None):
        self.vector = vector
        self.metadata = metadata or {}