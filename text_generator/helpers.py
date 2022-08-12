import string
from typing import Iterable

punctuation = set(string.punctuation)


def join_punctuation(iterable: Iterable[str]) -> str:
    return "".join(
        word if set(word) <= punctuation else " " + word for word in iterable
    ).lstrip()
