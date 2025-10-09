from re import Pattern

from src.common.tokenization.tokenizator import Tokenizator
from src.common.tokenization.tokens import Token


class MediumTokenizator(Tokenizator):
    def tokenize(self, expr: str) -> list[Token]:
        return []

    @property
    def _token_regex(self) -> Pattern[str]:
        return Pattern()

    def _simplify_tokens(self) -> list[Token]:
        return []
