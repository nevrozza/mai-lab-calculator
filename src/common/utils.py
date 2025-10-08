import colorama
import os.path
from inspect import currentframe
from src.constants import IS_DEBUG_MODE, DEBUG_TAG, WARNING_TAG


class CalcError(Exception):
    """*Понятные ошибки калькулятора.*"""
    pass


def debug(message):
    """Debug Message"""
    if IS_DEBUG_MODE:
        tag = DEBUG_TAG

        # https://stackoverflow.com/questions/12997687/how-to-get-python-caller-object-information
        current_frame = currentframe()
        if current_frame and current_frame.f_back:  # safe-call (?.) from kotlin
            caller_frame = current_frame.f_back
            function_name = caller_frame.f_code.co_name
            filename = os.path.basename(caller_frame.f_code.co_filename)  # to avoid `filename`.split("/")[-1]
            line_number = caller_frame.f_lineno
            tag += f" {filename}:{line_number} ({function_name})"

        tagged_print(color=colorama.Fore.CYAN, tag=tag, message=message)


def warning(message):
    """Warning Message"""
    tagged_print(color=colorama.Fore.YELLOW, tag=WARNING_TAG, message=message)


def tagged_print(color, tag: str, message):
    """
    Вывод с цветным тегом
    :param color: цвет тега
    :param tag: текст тега
    :param message: сообщение
    """
    print(color + f"[{tag}]" + colorama.Fore.RESET + f" {message}")
