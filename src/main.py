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

    e_labs = ["E1", "E2", "E3", "E4"]
    m_labs = ["M1", "M2", "M3", "M4"]

    labs_line = (Fore.GREEN + ' '.join([e for e in e_labs]) + " /"
                 + Fore.RED + "/ " + ' '.join([m for m in m_labs]) + Fore.RESET)

    variant = input("Введите вариант лабубы:\n"
                    + labs_line + "\n"
                    ).upper()
    print(variant)  # TODO: чтоб не ругался pre-commit


if __name__ == "__main__":
    main()
