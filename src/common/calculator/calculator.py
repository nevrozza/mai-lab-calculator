from abc import ABC, abstractmethod

from src.common.tokenization.tokenizator import Tokenizator
from src.common.tokenization.tokens import Token, tokens_to_expression, TOKEN_TYPES
from src.common.utils.errors import HardToCalculateExpression
from src.common.utils.messages import debug, warning
from src.common.utils.vars import TOKENS_LIMIT


class Calculator(ABC):
    """Абстрактный класс для калькуляторов"""

    def __init__(self, tag: str, tokenizator: Tokenizator):
        """
        :param tag: str - тег калькулятора (выводится в терминал)
        :param tokenizator: Tokenizator - токенизатор, который будет использоваться для разбиения выражения на токены
        """
        self.tag: str = tag
        self._tokens: list[Token] = []
        self._pos: int = 0
        self._tokenizator: Tokenizator = tokenizator

    def solve(self, expr: str) -> int | float:
        self._tokens = self._tokenizator.tokenize(expr)
        self._pos = 0

        if len(self._tokens) > TOKENS_LIMIT:
            raise HardToCalculateExpression

        return self._expr()

    @abstractmethod
    def _expr(self):
        pass

    def solve_and_print(self, expr: str):
        ans = self.solve(expr)
        if isinstance(ans, complex):
            warning("Получилось комплексное число!")
        elif ans.is_integer():
            ans = int(ans)
        elif isinstance(ans, float):
            ans = round(ans, 2)
        print(f"{tokens_to_expression(self._tokens)} = {ans}")

    def _next(self):
        """Перемещает позицию на +1 [токен]"""
        self._pos += 1

    def _current_token(self) -> Token:
        """:return Возвращает текущий токен:"""
        return self._tokens[self._pos]

    def _process_operations(self, next_method, operators, right_associative=False) -> int | float:
        """
        Универсальный метод для обработки операций (#), таких как a#b

        Смотреть ветку implementation/m1 (бесят повторения кода(()
        """
        result = next_method()

        while (token := self._current_token()).type in operators:
            debug(token)
            self._next()
            if right_associative:
                right = self._process_operations(next_method, operators)
            else:
                right = next_method()
            result = operators[token.type](result, right)

        return result

    def _process_unary_operations(self, next_method) -> int | float:
        """Метод для обработки унарных операций (можно определять next_method)"""
        sign = 1
        while self._current_token().type in (TOKEN_TYPES.PLUS, TOKEN_TYPES.MINUS):
            if self._current_token().type == TOKEN_TYPES.MINUS:
                sign *= -1
            self._next()
        return sign * next_method()
