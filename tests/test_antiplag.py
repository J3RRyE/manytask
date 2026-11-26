import pytest

from manytask.antiplag.checks import check_banwords
from manytask.antiplag.functions.find_banwords import BanwordMatch
from manytask.antiplag.models import AddedLine, Commit, Job


def test_banword_check_applies_condition_and_keeps_evidence() -> None:
    added_line = AddedLine("src/solution.cpp", 42, "eval(x) + eval(y) + Eval(z)")
    commit = Commit(
        sha="abc",
        repository="students/alice",
        student="alice",
        branches=("submit/string",),
        task="string",
        url="https://gitlab.example/students/alice/-/commit/abc",
        files={"src/solution.cpp": "eval(existing);\neval(x) + eval(y) + Eval(z)\nreturn 0;"},
        added_lines=(added_line, AddedLine("src/solution.cpp", 43, "return 0;")),
        jobs=(Job(id=1, name="grade", status="success"),),
    )

    finding = check_banwords(commit, ("eval(",), condition=lambda value: value > 0)

    assert finding is not None
    assert finding.commit_sha == "abc"
    assert finding.repository == commit.repository
    assert finding.commit_url == commit.url
    assert finding.value == 2
    assert finding.matches == (BanwordMatch("eval(", added_line, 2),)
    assert check_banwords(commit, ("eval(",), condition=lambda value: value > 2) is None


def test_banword_check_counts_case_insensitive_terms_once() -> None:
    added_line = AddedLine("solution.cpp", 1, "Eval(x)")
    commit = Commit(sha="abc", repository="students/alice", student="alice", added_lines=(added_line,))

    finding = check_banwords(commit, ("eval(", "EVAL("), condition=lambda value: value > 0, case_sensitive=False)

    assert finding is not None
    assert finding.matches == (BanwordMatch("eval(", added_line, 1),)


def test_banword_check_distinguishes_empty_diff_from_unavailable_diff() -> None:
    empty = Commit(sha="empty", repository="students/alice", student="alice", added_lines=())
    missing = Commit(sha="missing", repository="students/alice", student="alice")

    assert check_banwords(empty, ("eval(",), condition=lambda value: value > 0) is None

    with pytest.raises(ValueError, match="Diff is unavailable for commit missing"):
        check_banwords(missing, ("eval(",), condition=lambda value: value > 0)
