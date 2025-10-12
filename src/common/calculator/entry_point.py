from src.common.calculator.calculator import Calculator
from src.common.utils.errors import CalcError
from src.common.utils.messages import error
from src.common.utils.terminal import DEFAULT_HELP_MESSAGE, default_input_cycle


def calculator_entry_point(calculator: Calculator):
    """
    Точка входа для работы с калькулятором.

    Запускает интерактивный цикл ввода для вычисления математических выражений.
    Выводит справочное сообщение и обрабатывает пользовательский ввод.
    :param calculator: Калькулятор, с помощью которого будут производиться вычисления
    :return: Данная функция ничего не возвращает
    """
    help_message = f"{DEFAULT_HELP_MESSAGE}\n{calculator.tag} Введите выражение:"
    print(help_message)
    default_input_cycle(
        input_message='>>> ',
        callback_handler=lambda expr: _calculator_callback_handler(calculator, expr)
    )


def _calculator_callback_handler(calculator: Calculator, expr: str):
    """Обработчик callback-функции для вычисления выражений и обработки ошибок"""
    try:
        calculator.solve_and_print(expr)
    except ZeroDivisionError:
        error("На ноль делить нельзя!")
    except CalcError as e:
        e.print_error()
    except ValueError as e:
        if "Exceeds the limit" in str(e):
            error("Вышло слишком большое число =/")
        else:
            error(e)
