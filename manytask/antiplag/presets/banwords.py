from dataclasses import dataclass

from ..functions.find_banwords import BanwordMatch, find_banwords
from ..models import Commit


@dataclass(frozen=True)
class BanwordResult:
    commit_sha: str
    repository: str
    commit_url: str | None
    matches: tuple[BanwordMatch, ...]

    @property
    def value(self) -> int:
        return sum(match.occurrences for match in self.matches)


def count_banwords(commit: Commit, words: tuple[str, ...], *, case_sensitive: bool = True) -> BanwordResult:
    """Подсчитать вхождения в добавленных строках коммита."""
    if commit.added_lines is None:
        raise ValueError(f"Diff is unavailable for commit {commit.sha}")

    return BanwordResult(
        commit_sha=commit.sha,
        repository=commit.repository,
        commit_url=commit.url,
        matches=find_banwords(commit.added_lines, words, case_sensitive=case_sensitive),
    )
