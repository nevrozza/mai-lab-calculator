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
        return result

    def _expr(self) -> int | float:
        return self._add()  # why, but ТЗ

    def _add(self) -> int | float:
        result = self._mul()

        while self._current_token().type in (TOKEN_TYPES.PLUS, TOKEN_TYPES.MINUS):
            debug(self._current_token())
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
        result = self._pow()

        while self._current_token().type in (TOKEN_TYPES.MUL, TOKEN_TYPES.DIV, TOKEN_TYPES.FLOOR_DIV, TOKEN_TYPES.MOD):
            operator = self._current_token()
            self._next()
            right = self._pow()

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

    def _pow(self) -> int | float:  # TODO: что насчёт ограничений
        result = self._unary()

        while self._current_token().type == TOKEN_TYPES.POW:
            self._next()
            exp = self._pow()  # Право-ассоц
            result **= exp
        return result

    def _unary(self) -> int | float:
        if self._current_token().type in (TOKEN_TYPES.PLUS, TOKEN_TYPES.MINUS):
            operator = self._current_token()
            self._next()
            right = self._unary()  # Рекурсия для ситуаций лайк -(10-20) => -(-10) = 10
            if operator == TOKEN_TYPES.PLUS:
                return right
            else:
                return -right

        else:
            return self._primary()

    def _primary(self):  # -> int | float
        match (token := self._current_token()):
            case TOKEN_TYPES.NUM:
                self._next()
                return token.value
            case TOKEN_TYPES.L_PARENTHESIS:
                self._next()
                result = self._expr()
                if self._current_token() != TOKEN_TYPES.R_PARENTHESIS:
                    CalcError(
                        f"Ожидалось число или открывающая скобка. Получено {self._current_token()} / pos: {self.pos}")
                self._next()
                return result
            case _:
                CalcError("Ожидалось число или открывающая скобка")
