from src.common.tokens.regex import EASY_TOKEN_RE
from src.common.tokens.tokenizators.Tokenizator import Tokenizator
from src.common.tokens.tokens import Token, TOKEN_TYPES
from src.common.utils import debug, warning


class EasyTokenizator(Tokenizator):
    """
    *docstring*
    """

    def tokenize(self, expr: str) -> list[Token]:
        """
        # TODO дока
        Используется для задачек Easy
        :param expr: выражение для токенизации
        :return: список токенов
        """

        self._reinit(expr)

        while (element := self._get_next_element()) is not None:
            self._add_to_tokens(element)

        self.tokens.append(Token(TOKEN_TYPES.EOF))

        debug(expr)
        debug(self.tokens)
        simplified_tokens = self._simplify_tokens()
        debug(f"После упрощения: ${simplified_tokens}")

        if simplified_tokens != self.tokens:
            warning("Выражение было упрощено")

        return simplified_tokens

    # noinspection PyMethodMayBeStatic
    def _simplify_tokens(self) -> list[Token]:
        """
        O(N), клянусь
        :param tokens:
        :return:
        """
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
                else:
                    result.append(Token(TOKEN_TYPES.PLUS))
            else:
                result.append(self.tokens[i])
                i += 1

        return result

    def _get_token_regex(self):
        """"""
        return EASY_TOKEN_RE
