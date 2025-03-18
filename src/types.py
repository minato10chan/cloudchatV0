from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class Message:
    role: str
    content: str

@dataclass
class ChatHistory:
    messages: List[Message]

@dataclass
class SearchResult:
    content: str
    metadata: Dict[str, Any]
    score: float

@dataclass
class DocumentMetadata:
    area: str
    major_category: str
    sub_category: str
    source: str
    filename: str
    upload_date: str
