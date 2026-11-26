from collections.abc import Callable

from .models import Commit
from .presets.banwords import BanwordResult, count_banwords


def check_banwords(
    commit: Commit,
    words: tuple[str, ...],
    *,
    condition: Callable[[int], bool],
    case_sensitive: bool = True,
) -> BanwordResult | None:
    """Вернуть срабатывание, если значение пресета удовлетворяет условию."""
    result = count_banwords(commit, words, case_sensitive=case_sensitive)
    return result if condition(result.value) else None
