from abc import ABC, abstractmethod

from src.common.tokens.tokens import Token, TOKEN_TYPES
from src.common.utils import CalcError


class Tokenizator(ABC):
    """docstring"""

    def __init__(self):
        self.tokens: list[Token] = []
        self.pos: int = 0
        self.expr: str = ""

    @abstractmethod
    def tokenize(self, expr: str) -> list[Token]:
        """

        :param expr:
        """
        pass

    def _reinit(self, expr: str):
        """"""
        if not expr.strip():
            raise CalcError("Пустой ввод")
        self.tokens.clear()
        self.pos = 0
        self.expr = expr

    def _add_to_tokens(self, element: str):
        """Fuckin' refactoring"""
        """
        :param element: число или символ
        :return: список токенов (2 токена, если есть унарный минус)
        """

        element = element.replace(",", ".")
        if element.replace("-", "").replace(".", "").isdigit():
            value = float(element) if '.' in element else int(element)
            num_token = Token(TOKEN_TYPES.NUM, abs(value))
            if value < 0:
                self.tokens += [Token(TOKEN_TYPES.MINUS), num_token]  # Handler for unary minus
            else:
                self.tokens.append(num_token)
        else:
            self.tokens.append(Token(TOKEN_TYPES(element)))

    def _get_next_element(self) -> str | None:
        """"""
        if self.pos >= len(self.expr):  # for `outside` while cycle
            return None

        matched = self._get_token_regex().match(self.expr, self.pos)
        if not matched:
            raise CalcError(f"Некорректный ввод около: '{self.expr[self.pos:]}'")

        element = matched.group(1)
        self.pos = matched.end()
        return element

    @abstractmethod
    def _get_token_regex(self):
        """"""
        pass

    @abstractmethod
    def _simplify_tokens(self) -> list[Token]:
        """"""
        pass
