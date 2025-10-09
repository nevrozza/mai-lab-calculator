from src.common.calculator import Calculator
from src.common.tokenization.tokens import Token


class CalculatorM1(Calculator):
    """
    Калькулятор для обработки выражений уровня M1 с использованием рекурсивного спуска.

    Поддерживает скобки и операции: +, -, *, /, **, //, %
    """
    def solve(self, tokens: list[Token]) -> int | float:
        return 0
