from src.common.tokens.tokenization import easy_tokenize
from src.common.tokens.tokens import Token, TOKEN_TYPES
from src.common.utils import CalcError, debug, warning


class CalculatorE1:
    """
    Калькулятор для E1

    кидает: ZeroDivisionError и кастомные CalcError #TODO UnexpectedSym
    """

    def __init__(self):
        self.tokens = []
        self.pos = 0

    def solve(self, tokens: list[Token]) -> int | float:  # term + -
        """
        Запускает рекурсивный спуск по токенам
        :param tokens: список токенов из easy_tokenize
        ":return: решение"
        """
        self.tokens = tokens
        self.pos = 0
        result = self._expr()
        debug(self._current_token())
        return result

    def _expr(self) -> int | float:
        result = self._term()
        while self._current_token().type in (TOKEN_TYPES.PLUS, TOKEN_TYPES.MINUS):
            debug(self._current_token())
            sign_mul = 0
            match self._current_token().type:
                case TOKEN_TYPES.PLUS:
                    sign_mul = 1
                case TOKEN_TYPES.MINUS:
                    sign_mul = -1

            self._next()
            result += sign_mul * self._term()
        return result

    def _term(self) -> int | float:  # factor * /
        result = self._factor()

        while self._current_token().type in (TOKEN_TYPES.MUL, TOKEN_TYPES.DIV):
            debug(self._current_token())
            match self._current_token().type:
                case TOKEN_TYPES.MUL:
                    self._next()
                    result *= self._factor()
                case TOKEN_TYPES.DIV:
                    self._next()
                    div = self._factor()
                    result /= div

        return result

    def _factor(self) -> int | float:  # +-num
        token = self._current_token()
        debug(token)
        sign = 1
        if token.type in (TOKEN_TYPES.PLUS, TOKEN_TYPES.MINUS):
            match token.type:
                case TOKEN_TYPES.PLUS:
                    sign = 1
                case TOKEN_TYPES.MINUS:
                    sign = -1
            self._next()
            token = self._current_token()

        if token.type != TOKEN_TYPES.NUM:
            raise CalcError(f"Ожидалось число, получено: {token}")
        self._next()
        if token.value is not None:
            return sign * token.value
        else:
            raise CalcError("Unexpected error")  # TODO

    def _next(self):
        self.pos += 1

    def _current_token(self) -> Token:
        return self.tokens[self.pos]


warning(CalculatorE1().solve(easy_tokenize("10 / 4 + -5 * 2")))
warning(CalculatorE1().solve(easy_tokenize("10 / 4 - -5 * 2")))  # !!
warning(CalculatorE1().solve(easy_tokenize("10 / 4 - - -5 * 2")))  # !!
