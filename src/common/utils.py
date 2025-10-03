import colorama

from src.constants import IS_DEBUG_MODE, DEBUG_TAG, WARNING_TAG


class CalcError(Exception):
    """*Понятные ошибки калькулятора.*"""
    pass


def debug(message):
    """Debug Message"""
    if IS_DEBUG_MODE:
        tagged_print(color=colorama.Fore.CYAN, tag=DEBUG_TAG, message=message)


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
