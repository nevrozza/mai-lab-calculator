from abc import ABC, abstractmethod

from src.common.tokenization.tokenizator import Tokenizator
from src.common.tokenization.tokens import Token, tokens_to_expression


class Calculator(ABC):
    """Абстрактный класс для калькуляторов"""

    def __init__(self):
        self.tokens = []
        self.pos = 0

    @abstractmethod
    def solve(self, expr: str) -> int | float:
        pass

    def solve_and_print(self, expr: str):
        ans = self.solve(expr)
        print(f"{tokens_to_expression(self.tokens)} = {ans}")

    def _next(self):
        """Перемещает позицию на +1 [токен]"""
        self.pos += 1

    def _current_token(self) -> Token:
        """:return Возвращает текущий токен:"""
        return self.tokens[self.pos]

    @property
    @abstractmethod
    def _tokenizator(self) -> Tokenizator:
        """:return: Regex паттерн для деления выражения на элементы"""
        pass
