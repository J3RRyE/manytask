from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class AddedLine:
    path: str
    number: int
    text: str


@dataclass(frozen=True)
class Job:
    id: int
    name: str
    status: str
    ref: str | None = None
    url: str | None = None


@dataclass(frozen=True, kw_only=True)
class Commit:
    """Коммит студента. None для added_lines или jobs означает отсутствие данных об этой части коммита."""

    sha: str
    repository: str
    student: str
    branches: tuple[str, ...] = ()
    task: str | None = None
    committed_at: datetime | None = None
    url: str | None = None
    files: Mapping[str, str] = field(default_factory=dict)
    added_lines: tuple[AddedLine, ...] | None = None
    jobs: tuple[Job, ...] | None = None
    metadata: Mapping[str, object] = field(default_factory=dict)
