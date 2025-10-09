from re import Pattern

from src.common.tokens.regex import EASY_TOKEN_RE
from src.common.tokens.tokenizators.Tokenizator import Tokenizator
from src.common.tokens.tokens import Token, TOKEN_TYPES
from src.common.utils import debug, warning


class EasyTokenizator(Tokenizator):
    """
    Токенизатор для Easy задачек
    """

    def tokenize(self, expr: str) -> list[Token]:
        self._reinit(expr)

        while (element := self._get_next_element()) is not None:
            self._add_token(element)

        self.tokens.append(Token(TOKEN_TYPES.EOF))  # TODO: рассмотреть его необходимость

        debug(expr)
        debug(self.tokens)

        simplified_tokens = self._simplify_tokens()
        debug(f"После упрощения: ${simplified_tokens}")

        if simplified_tokens != self.tokens:
            warning("Выражение было упрощено")

        return simplified_tokens

    @property
    def _token_regex(self) -> Pattern[str]:
        return EASY_TOKEN_RE

    # noinspection PyMethodMayBeStatic
    def _simplify_tokens(self) -> list[Token]:
        result = []
        i = 0

        while i < len(self.tokens):
            current_type = self.tokens[i].type

            if current_type in (TOKEN_TYPES.PLUS, TOKEN_TYPES.MINUS):
                """
                Обрабатываем ситуации аля
                '---' -> '-'
                '+-' -> '-'
                '--' -> '+'
                """
                sign = 1
                while i < len(self.tokens) and self.tokens[i].type in (TOKEN_TYPES.PLUS, TOKEN_TYPES.MINUS):
                    if self.tokens[i].type == TOKEN_TYPES.MINUS:
                        sign *= -1
                    i += 1
                if sign == -1:
                    result.append(Token(TOKEN_TYPES.MINUS))
                elif result:  # Добавляем плюс, только если он НЕ в начале выражения
                    result.append(Token(TOKEN_TYPES.PLUS))
            else:
                result.append(self.tokens[i])
                i += 1

        return result
