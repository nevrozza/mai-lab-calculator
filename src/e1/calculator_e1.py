from src.common.utils.errors import CalcError
from src.common.utils.messages import debug, warning
from src.e1.easy_tokenizator import EasyTokenizator
from src.common.tokenization.tokens import Token, TOKEN_TYPES


class CalculatorE1:
    """
    Калькулятор для обработки выражений уровня E1 с использованием рекурсивного спуска.

    Поддерживает базовые арифметические операции: +, -, *, /
    """

    def __init__(self):
        self.tokens = []
        self.pos = 0

    def solve(self, tokens: list[Token]) -> int | float:  # term + -
        """
        Запускает рекурсивный спуск по токенам

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

        :param tokens: Список токенов из EasyTokenizator
        :return: Результат вычисления выражения
        :raises ZeroDivisionError:  #TODO UnexpectedSym
        :raises CalcError:
        """
        self.tokens = tokens
        self.pos = 0
        result = self._expr()
        debug(self._current_token())  # print EOF  TODO: пока оставим, но мб не нужно это всё...
        return result

    def _expr(self) -> int | float:
        """см. solve()"""
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
        """см. solve()"""
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
        """см. solve()"""
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
        """Перемещает позицию на +1 [токен]"""
        self.pos += 1

    def _current_token(self) -> Token:
        """:return Возвращает текущий токен:"""
        return self.tokens[self.pos]


warning(CalculatorE1().solve(EasyTokenizator().tokenize("+10/4-5*2+7.5")))
# warning(CalculatorE1().solve(EasyTokenizator().tokenize("10 / 4 - -5 * 2")))  # !!
# warning(CalculatorE1().solve(EasyTokenizator().tokenize("10 / 4 - - -5 * 2")))  # !!
