from abc import ABC, abstractmethod

from src.common.tokenization.tokens import Token


class Calculator(ABC):
    """Абстрактный класс для калькуляторов"""
    def __init__(self):
        self.tokens = []
        self.pos = 0

    @abstractmethod
    def solve(self, tokens: list[Token]) -> int | float:
        pass

    def _next(self):
        """Перемещает позицию на +1 [токен]"""
        self.pos += 1

    def _current_token(self) -> Token:
        """:return Возвращает текущий токен:"""
        return self.tokens[self.pos]
