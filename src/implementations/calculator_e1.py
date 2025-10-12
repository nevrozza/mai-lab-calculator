from src.common.calculator.calculator import Calculator
from src.common.tokenization.tokenizator import Tokenizator
from src.common.tokenization.tokens import TOKEN_TYPES, tokens_to_expression
from src.common.utils.errors import InvalidTokenError, CalcError
from src.common.utils.messages import debug
from src.common.utils.operators import BASIC_OPERATORS, MUL_DIV_OPERATORS
from src.common.utils.vars import EASY_TOKEN_RE


class CalculatorE1(Calculator):
    """
    Калькулятор для обработки выражений уровня E1 с использованием рекурсивного спуска.

    Поддерживает базовые арифметические операции: +, -, *, /
    """

    def __init__(self):
        super().__init__("[E1]", Tokenizator(EASY_TOKEN_RE))

    def solve(self, expr: str) -> int | float:  # term + -
        """
        Запускает рекурсивный спуск по токенам (E1)

        Алгоритм:
            1) Инициализация
            2) Разбор выражения c _expr:
                expr() — сложение/вычитание:
                    - Левый операнд (result) = term()
                    - Обработка в цикле +=term() или -=term() к result
                term() – умножение/деление:
                    - Левый операнд (result) = factor()
                    - Обработка в цикле *=factor() или /=factor() к result
                factor() - числа/унарные знаки:
                    - Обрабатывает 2 токена, если есть не обработанный знак выше перед числом
                    - Иначе обрабатывает только 1 (само число)

        :param expr: Выражение для вычисления
        :return: Результат вычисления выражения
        """
        return super().solve(expr)

    def _expr(self) -> int | float:
        """
        Обрабатывает сложение и вычитание
        Подробнее: см. solve()
        """
        return self._process_operations(
            next_method=self._term,
            operators=BASIC_OPERATORS
        )

    def _term(self) -> int | float:  # factor * /
        """
        Обрабатывает умножение и деление
        см. solve()
        """
        return self._process_operations(
            next_method=self._factor,
            operators=MUL_DIV_OPERATORS
        )

    def _factor(self) -> int | float:  # +-num
        """см. solve()"""
        token = self._current_token()
        debug(token)

        signs = {
            TOKEN_TYPES.PLUS: 1,
            TOKEN_TYPES.MINUS: -1
        }

        sign = 1
        if token.type in signs:
            sign = signs[token.type]
            self._next()
            token = self._current_token()

        if token.type != TOKEN_TYPES.NUM:
            raise InvalidTokenError(
                expr=tokens_to_expression(self._tokens),
                pos=self._pos
            )
        else:
            self._next()
            if token.value is not None:
                return sign * token.value
            else:
                # лол, сверху проверка на число... не знаю, как заставить его поверить, что value != None
                raise CalcError("pre-commit был прав...")
