from re import Pattern

from src.common.tokenization.tokenizator import Tokenizator
from src.common.tokenization.tokens import Token, TOKEN_TYPES
from src.common.utils.messages import debug
from src.common.utils.vars import MEDIUM_TOKEN_RE


class MediumTokenizator(Tokenizator):
    def tokenize(self, expr: str) -> list[Token]:
        self._reinit(expr)

        while (element := self._get_next_element()) is not None:
            self._add_token(element)

        self.tokens.append(Token(TOKEN_TYPES.EOF))  # TODO: рассмотреть его необходимость

        debug(expr)
        debug(self.tokens)

        # simplified_tokens = self._simplify_tokens()
        # debug(f"После упрощения: ${simplified_tokens}")
        #
        # if simplified_tokens != self.tokens:
        #     warning("Выражение было упрощено")

        return self.tokens

    @property
    def _token_regex(self) -> Pattern[str]:
        return MEDIUM_TOKEN_RE

    def _simplify_tokens(self) -> list[Token]:
        return []
