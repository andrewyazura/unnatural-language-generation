import tokenize_uk
from typing import Generator


def tokenize_text(text: str) -> Generator[str, None, None]:
    yield from map(lambda s: s.lower(), tokenize_uk.tokenize_words(text))
