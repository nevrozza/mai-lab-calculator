from abc import ABC, abstractmethod

from src.common.tokenization.tokenizator import Tokenizator
from src.common.tokenization.tokens import Token, tokens_to_expression


class Calculator(ABC):
    """Абстрактный класс для калькуляторов"""

    def __init__(self, tag: str, tokenizator: Tokenizator):
        self.tag: str = tag
        self._tokens: list[Token] = []
        self._pos: int = 0
        self._tokenizator: Tokenizator = tokenizator

    @abstractmethod
    def solve(self, expr: str) -> int | float:
        pass

    def solve_and_print(self, expr: str):
        ans = self.solve(expr)
        print(f"{tokens_to_expression(self._tokens)} = {ans}")

    def _next(self):
        """Перемещает позицию на +1 [токен]"""
        self._pos += 1

    def _current_token(self) -> Token:
        """:return Возвращает текущий токен:"""
        return self._tokens[self._pos]
