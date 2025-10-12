from re import Pattern

from src.common.tokenization.tokenizator import Tokenizator
from src.common.tokenization.tokens import Token
from src.common.utils.messages import debug, warning
from src.common.utils.vars import EASY_TOKEN_RE


class EasyTokenizator(Tokenizator):
    """
    Токенизатор для Easy задачек
    """

    def tokenize(self, expr: str) -> list[Token]:
        self._reinit(expr)

        while (element := self._get_next_element()) is not None:
            self._add_token(element)

        debug(expr)
        debug(self.tokens)

        simplified_tokens = self._validate_and_simplify_tokens()
        debug(f"После упрощения: ${simplified_tokens}")

        if self.warning_messages:
            warning(*self.warning_messages)

        return simplified_tokens

    @property
    def _token_regex(self) -> Pattern[str]:
        return EASY_TOKEN_RE
