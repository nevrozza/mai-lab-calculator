from src.common.calculator.calculator import Calculator
from src.common.tokenization.tokenizator import Tokenizator
from src.common.tokenization.tokens import TOKEN_TYPES
from src.common.utils.errors import InvalidTokenError
from src.common.utils.operators import BASIC_OPERATORS, MUL_DIV_OPERATORS, FLOOR_DIV_OPERATOR, MOD_OPERATOR, \
    POW_OPERATOR

from src.common.utils.vars import MEDIUM_TOKEN_RE


class CalculatorM1(Calculator):
    """
    Калькулятор для обработки выражений уровня M1 с использованием рекурсивного спуска.

    Поддерживает скобки и операции: +, -, *, /, ** (право-ассоц), //, %
    """

    def __init__(self):
        super().__init__("[M1]", Tokenizator(MEDIUM_TOKEN_RE))

    def solve(self, expr: str) -> int | float:
        """
        Запускает рекурсивный спуск (M1)

        Алгоритм:
            1) Инициализация
            2) Разбор выражения с _expr:
                _expr() -> add() – сложение/вычитание:
                    - Левый операнд (result) = mul()
                    - Обработка в цикле +=mul() или -=mul() к result
                mul() - умножение/деление/остаток:
                    - Левый операнд (result) = left_associated_unary()
                    - Обработка в цикле (*|/|//|%)=left_associated_unary()
                left_associated_unary() - унарные знаки для ВСЕГО выражения:
                    - Обрабатывает последовательности унарных +/-
                    - Вызывает pow() для дальнейшего разбора
                pow() – степень (право-ассоц.):
                    - Левый операнд (result) = right_associated_unary()
                    - Обработка в цикле **pow() к result
                right_associated_unary() — унарные знаки только для ОСНОВАНИЯ степени:
                    - Обрабатывает последовательности унарных +/-
                    - Вызывает primary() для получения числа
                primary() — числа и скобки:
                    - Обрабатывает числа или выражения в скобках

        ВАЖНО:
            - -2**2 = -4 (унарные знаки ДО степени имеют НИЗКИЙ приоритет) // _left_associated_unary()
            - 2**-1 = 0.5 (унарные знаки В степени имеют ВЫСОКИЙ приоритет) // _right_associated_unary()
            - 2**3**2 = 2**(3**2) = 512 (правая ассоциативность в степени)
        :param expr:
        :return:
        """
        return super().solve(expr)

    def _expr(self) -> int | float:
        return self._add()  # why, but ТЗ

    def _add(self) -> int | float:
        return self._process_operations(
            next_method=self._mul,
            operators=BASIC_OPERATORS
        )

    def _mul(self) -> int | float:
        return self._process_operations(
            next_method=self._left_associated_unary,
            operators={
                **MUL_DIV_OPERATORS,
                **FLOOR_DIV_OPERATOR,
                **MOD_OPERATOR
            }
        )

    def _pow(self) -> int | float | complex:
        return self._process_operations(
            next_method=self._right_associated_unary,
            operators=POW_OPERATOR,
            right_associative=True
        )

    def _right_associated_unary(self) -> int | float:
        return self._process_unary_operations(self._primary)

    def _left_associated_unary(self) -> int | float:
        return self._process_unary_operations(self._pow)

    def _primary(self):  # -> int | float
        match (token := self._current_token()).type:
            case TOKEN_TYPES.NUM:
                self._next()
                return token.value
            case TOKEN_TYPES.L_PARENTHESIS:
                self._next()
                result = self._expr()
                self._next()
                return result
            case _:
                raise InvalidTokenError(
                    tokens=self._tokens,
                    pos=self._pos
                )
