import colorama
import os.path
from inspect import currentframe

from src.common.utils.terminal import TerminalConfig
from src.common.utils.vars import DEBUG_TAG, WARNING_TAG, ERROR_TAG


def debug(*message: object):
    """Debug tagged message"""
    if TerminalConfig.is_debug:
        tag = DEBUG_TAG

        # получаем скоуп, откуда вызвали функцию
        # https://stackoverflow.com/questions/12997687/how-to-get-python-caller-object-information
        current_frame = currentframe()
        if current_frame and current_frame.f_back:  # safe-call (?.) from kotlin
            caller_frame = current_frame.f_back
            function_name = caller_frame.f_code.co_name
            filename = os.path.basename(caller_frame.f_code.co_filename)  # to avoid `filename`.split("/")[-1]
            line_number = caller_frame.f_lineno
            tag += f" {filename}:{line_number} ({function_name})"

        tagged_print(colorama.Fore.CYAN, tag, *message)


def warning(*message: object):
    """Warning tagged message"""
    if TerminalConfig.is_warning:
        tagged_print(colorama.Fore.YELLOW, WARNING_TAG, *message)


def error(*message: object):
    """Error tagged message"""
    tagged_print(colorama.Fore.RED, ERROR_TAG, *message)


def tagged_print(color, tag: str, *message: object):
    """
    Вывод с цветным тегом
    :param color: Цвет тега
    :param tag: Текст тега
    :param message: Сообщение
    """
    formatted_message = " | ".join(str(m) for m in message)
    print(color + f"[{tag}]" + colorama.Fore.RESET + f" {formatted_message}")
