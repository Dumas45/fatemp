import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ParentInput:
    name: str
    items: int


@dataclass
class ChildInput:
    name: str
    records: list[int]


@dataclass
class ChildResult:
    name: str
    processed: int
    checksum: int


@dataclass
class ParentResult:
    name: str
    workflow_id: str
    prepared_records: list[int]
    child: ChildResult
