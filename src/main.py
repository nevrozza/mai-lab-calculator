import colorama
from colorama import Fore


def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """
    colorama.init()

    labs_line = (Fore.GREEN + "E1" + " /"
                 + Fore.RED + "/ " + "M1" + Fore.MAGENTA + " | " + "КАЗИК" + Fore.RESET)

    variant = input("Введите вариант лабубы:\n"
                    + labs_line + "\n"
                    ).upper()
    print(variant)  # TODO: чтоб не ругался pre-commit


if __name__ == "__main__":
    main()
