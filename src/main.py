import colorama
from colorama import Fore

from src.python_require import assert_python_version


def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """
    assert_python_version()
    colorama.init()

    labs_line = (Fore.GREEN + "E1" + " /"
                 + Fore.RED + "/ " + "M1" + Fore.MAGENTA + " | " + "КАЗИК" + Fore.RESET)

    variant = input("Введите вариант лабубы:\n"
                    + labs_line + "\n"
                    ).upper()
    print(variant)  # TODO: чтоб не ругался pre-commit


if __name__ == "__main__":
    main()
