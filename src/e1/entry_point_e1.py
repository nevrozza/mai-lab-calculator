from src.common.utils.errors import CalcError
from src.common.utils.messages import error
from src.common.utils.terminal import default_calculator_entry_point
from src.e1.calculator_e1 import CalculatorE1


def entry_point_e1():
    calculator = CalculatorE1()
    default_calculator_entry_point("E1", callback_handler=lambda expr: _e1_callback_handler(calculator, expr))


def _e1_callback_handler(calculator: CalculatorE1, expr: str):
    try:
        calculator.solve_and_print(expr)
    except ZeroDivisionError:
        error("На ноль делить нельзя!")
    except CalcError as e:
        e.print_error()


if __name__ == "__main__":
    entry_point_e1()
