from src.common.tokenization.tokens import Token, TOKEN_TYPES
from src.common.utils.errors import NoNumbersError, InvalidExprStartError, InvalidParenthesisError, \
    FloatTogetherError


class TokensValidator:
    """Валидатор и упроститель выражений"""

    def __init__(self):
        self._tokens: list[Token] = []
        self._i: int = 0
        self._result: list[Token] = []
        self._parenthesis_stack: list[str] = []
        self.warning_messages: set[str] = set()

    def _reinit(self, tokens: list[Token]):
        self._tokens = tokens
        self._result.clear()
        self._parenthesis_stack.clear()
        self.warning_messages.clear()
        self._i = 0

    def validate_and_simplify_tokens(self, tokens: list[Token]) -> list[Token]:
        """
        Валидирует и упрощает токены согласно правилам математики:
            - Обрабатывает последовательность унарных операторов
            - Обрабатывает числа с пробелами
            - Добавляет поддержку неявного умножения
            - Проверяет баланс скобок (через стек)
            - Очищает результат от лишних операторов

        Примеры:
            - "---" -> "-"
            - "+-"  -> "-"
            - "++"  -> "+"
            - "2(2)"-> "2*(2)"
            - "2+"  -> "2"

        O(N), клянусь

        SRP нарушено, чтобы была только 1 проходка
        :param tokens: Необработанные токены
        :return: Список токенов с упрощением
        """
        self._reinit(tokens)
        self._validate_initial_tokens()

        while self._i < len(self._tokens):
            self._process_token()

        self._check_final_parenthesis()
        self._cleanup_result()
        return self._result

    def _validate_initial_tokens(self):
        """
        Проверяет начальные условия валидности выражения.

        Условия:
        - Выражение должно содержать хотя бы одно число
        - Выражение должно начинаться с допустимого токена
        """

        if TOKEN_TYPES.NUM not in [t.type for t in self._tokens]:
            raise NoNumbersError

        first_token_type = self._tokens[self._i].type

        valid_starts = (TOKEN_TYPES.PLUS, TOKEN_TYPES.MINUS, TOKEN_TYPES.NUM, TOKEN_TYPES.L_PARENTHESIS)
        if first_token_type not in valid_starts:
            raise InvalidExprStartError(first_token_type.value)

    def _process_token(self):
        """Обрабатывает текущий токен в один проход (запускается из цикла)"""
        token = self._tokens[self._i]

        # Баланс скобок
        self._process_parenthesis(token)

        # Проверка неявного умножения перед обработкой токена
        if self._needs_implicit_mul(token):
            self._result.append(Token(TOKEN_TYPES.MUL))

        if token.type in (TOKEN_TYPES.PLUS, TOKEN_TYPES.MINUS):
            self._process_unary_operators()
        elif token.type == TOKEN_TYPES.NUM:
            self._process_numbers(token)
        else:
            self._process_usual_token(token)

    def _process_parenthesis(self, token: Token):
        if token.type == TOKEN_TYPES.L_PARENTHESIS:
            self._parenthesis_stack.append(TOKEN_TYPES.L_PARENTHESIS.value)
        elif token.type == TOKEN_TYPES.R_PARENTHESIS:
            if not self._parenthesis_stack:
                raise InvalidParenthesisError(has_extra_closing=True)
            self._parenthesis_stack.pop()

    def _process_unary_operators(self):
        """Упрощает последовательности операторов +-"""
        sign = 1
        simplified_count = 0

        while self._i < len(self._tokens) and self._tokens[self._i].type in (TOKEN_TYPES.PLUS, TOKEN_TYPES.MINUS):
            if self._tokens[self._i].type == TOKEN_TYPES.MINUS:
                sign *= -1
            simplified_count += 1
            self._i += 1

        if simplified_count > 1:
            self.warning_messages.add("Выражение было упрощено")

        if sign == -1:
            self._result.append(Token(TOKEN_TYPES.MINUS))
        elif self._result:  # Плюс только если не в начале выражения
            self._result.append(Token(TOKEN_TYPES.PLUS))

    def _process_numbers(self, token: Token):
        """Обрабатывает числа с пробелом 2 2 -> 22"""
        number_value = token.value
        self._i += 1

        while (self._i < len(self._tokens) and
               self._tokens[self._i].type == TOKEN_TYPES.NUM):
            next_num = self._tokens[self._i]
            if isinstance(number_value, float) or isinstance(next_num.value, float):
                raise FloatTogetherError(number_value, next_num.value)
            else:
                number_value = int(str(number_value) + str(next_num.value))
                self.warning_messages.add("Пробел между числами убран")
            self._i += 1

        self._result.append(Token(TOKEN_TYPES.NUM, number_value))

    def _needs_implicit_mul(self, token: Token) -> bool:
        """Проверяет нужно ли добавить неявное умножение // 2(2) = 4"""
        if not self._result:
            return False
        last_token = self._result[-1]

        return (
                (last_token.type in (TOKEN_TYPES.NUM, TOKEN_TYPES.R_PARENTHESIS)) and
                (token.type in (TOKEN_TYPES.L_PARENTHESIS, TOKEN_TYPES.NUM))
        )

    def _process_usual_token(self, token: Token):
        self._result.append(token)
        self._i += 1

    def _check_final_parenthesis(self):
        """Проверяет баланс скобок после обработки всех токенов."""
        if self._parenthesis_stack:
            raise InvalidParenthesisError(has_extra_closing=False)

    def _cleanup_result(self):
        """
        Выполняет финальную очистку результата:
            - Удаляет лишние операторы в конце выражения
            - Добавляет EOF
        """

        extra_operators = (TOKEN_TYPES.PLUS, TOKEN_TYPES.MINUS, TOKEN_TYPES.MUL, TOKEN_TYPES.DIV)
        while self._result and self._result[-1].type in extra_operators:
            self.warning_messages.add("Удалены лишние операторы в конце")
            self._result.pop()
        self._result.append(Token(TOKEN_TYPES.EOF))
