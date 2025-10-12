from src.common.calculator import Calculator
from src.common.tokenization.tokenizator import Tokenizator
from src.common.tokenization.tokens import TOKEN_TYPES
from src.common.utils.errors import CalcError
from src.common.utils.messages import debug
from src.m1.medium_tokenizator import MediumTokenizator


class CalculatorM1(Calculator):
    """
    Калькулятор для обработки выражений уровня M1 с использованием рекурсивного спуска.

    Поддерживает скобки и операции: +, -, *, /, ** (право-ассоц), //, %
    """

    @property
    def _tokenizator(self) -> Tokenizator:
        return MediumTokenizator()

    def solve(self, expr: str) -> int | float:
        """
        Запускает рекурсивный спуск (M1)

        Алгоритм:
            1) Инициализация
            2) Разбор выражения с _expr:
                expr() -> add() – сложение/вычитание:
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
        self.tokens = self._tokenizator.tokenize(expr)
        self.pos = 0
        result = self._expr()
        debug(type(result))
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
                case TOKEN_TYPES.FLOOR_DIV:  # TODO: ограничение, чтобы делить только для целых
                    result //= right
                case TOKEN_TYPES.MOD:  # TODO: ограничение, чтобы делить только для целых
                    result %= right
        return result

    def _pow(self) -> int | float:  # TODO: что насчёт ограничений | complex
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
                if self._current_token().type != TOKEN_TYPES.R_PARENTHESIS:
                    CalcError(
                        f"Ожидалось число или открывающая скобка. Получено {self._current_token()} | pos: {self.pos}")
                self._next()
                return result

            case _:
                raise CalcError(
                    f"Ожидалось число или открывающая скобка. Получено: {token} | pos: {self.pos}")
