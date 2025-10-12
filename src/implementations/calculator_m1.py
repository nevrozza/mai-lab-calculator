from src.common.calculator.calculator import Calculator
from src.common.tokenization.tokenizator import Tokenizator
from src.common.tokenization.tokens import TOKEN_TYPES, tokens_to_expression
from src.common.utils.errors import NotIntegerDivisionError, InvalidTokenError

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
        self._tokens = self._tokenizator.tokenize(expr)
        self._pos = 0
        result = self._expr()
        return result

    def _expr(self) -> int | float:
        return self._add()  # why, but ТЗ

    def _add(self) -> int | float:
        result = self._mul()

        while self._current_token().type in (TOKEN_TYPES.PLUS, TOKEN_TYPES.MINUS):
            sign = 1
            match self._current_token().type:
                case TOKEN_TYPES.PLUS:
                    sign = 1
                case TOKEN_TYPES.MINUS:
                    sign = -1

            self._next()
            result += sign * self._mul()

        return result

    def _mul(self) -> int | float:
        result = self._left_associated_unary()

        while self._current_token().type in (TOKEN_TYPES.MUL, TOKEN_TYPES.DIV, TOKEN_TYPES.FLOOR_DIV, TOKEN_TYPES.MOD):
            operator = self._current_token()
            self._next()
            right = self._left_associated_unary()

            match operator.type:
                case TOKEN_TYPES.MUL:
                    result *= right
                case TOKEN_TYPES.DIV:
                    result /= right
                case TOKEN_TYPES.FLOOR_DIV:
                    if right.is_integer():
                        result //= right
                    else:
                        raise NotIntegerDivisionError(operator.type.value)
                case TOKEN_TYPES.MOD:
                    if result.is_integer() and right.is_integer():
                        result %= right
                    else:
                        raise NotIntegerDivisionError(operator.type.value)
        return result

    def _pow(self) -> int | float: # | complex
        result = self._right_associated_unary()

        while self._current_token().type == TOKEN_TYPES.POW:
            self._next()
            degree = self._pow()  # Право-ассоц
            result **= degree
        return result

    def _right_associated_unary(self) -> int | float:
        sign = 1
        while self._current_token().type in (TOKEN_TYPES.PLUS, TOKEN_TYPES.MINUS):
            if self._current_token().type == TOKEN_TYPES.MINUS:
                sign *= -1
            self._next()

        return sign * self._primary()

    def _left_associated_unary(self) -> int | float:
        sign = 1
        while self._current_token().type in (TOKEN_TYPES.PLUS, TOKEN_TYPES.MINUS):
            if self._current_token().type == TOKEN_TYPES.MINUS:
                sign *= -1
            self._next()

        return sign * self._pow()

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
                    expr=tokens_to_expression(self._tokens),
                    pos=self._pos
                )
