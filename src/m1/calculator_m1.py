from src.common.calculator import Calculator
from src.common.tokenization.tokens import Token, TOKEN_TYPES
from src.common.utils.errors import CalcError
from src.common.utils.messages import debug


class CalculatorM1(Calculator):
    """
    Калькулятор для обработки выражений уровня M1 с использованием рекурсивного спуска.

    Поддерживает скобки и операции: +, -, *, /, ** (право-ассоц), //, %
    """

    def solve(self, tokens: list[Token]) -> int | float:
        self.tokens = tokens
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
        result = self._unary()

        while self._current_token().type in (TOKEN_TYPES.MUL, TOKEN_TYPES.DIV, TOKEN_TYPES.FLOOR_DIV, TOKEN_TYPES.MOD):
            operator = self._current_token()
            self._next()
            right = self._unary()

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
        result = self._primary()

        while self._current_token().type == TOKEN_TYPES.POW:
            self._next()
            degree = self._pow()  # Право-ассоц
            result **= degree
        return result

    def _unary(self) -> int | float:
        sign = 1
        while self._current_token().type in (TOKEN_TYPES.PLUS, TOKEN_TYPES.MINUS):
            if self._current_token().type == TOKEN_TYPES.MINUS:
                sign *= -1
            self._next()

        return sign * self._pow()  # TODO: check equals to the previous (02:55 now((

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
