from dataclasses import dataclass

from ..models import AddedLine


@dataclass(frozen=True)
class BanwordMatch:
    word: str
    line: AddedLine
    occurrences: int


def find_banwords(
    lines: tuple[AddedLine, ...],
    words: tuple[str, ...],
    *,
    case_sensitive: bool = True,
) -> tuple[BanwordMatch, ...]:
    """Найти буквальные непересекающиеся вхождения каждого слова в строках."""
    if "" in words:
        raise ValueError("Banwords must not be empty")

    needles: dict[str, str] = {}
    for word in words:
        needles.setdefault(word if case_sensitive else word.casefold(), word)

    matches: list[BanwordMatch] = []
    for line in lines:
        text = line.text if case_sensitive else line.text.casefold()
        for needle, word in needles.items():
            occurrences = text.count(needle)
            if occurrences:
                matches.append(BanwordMatch(word, line, occurrences))

    return tuple(matches)
