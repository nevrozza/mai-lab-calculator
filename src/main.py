from colorama import Fore, init

from src.common.utils.terminal import default_input_cycle, DEFAULT_HELP_MESSAGE
from src.e1.entry_point_e1 import entry_point_e1


def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """
    init()  # Colorama

    print(DEFAULT_HELP_MESSAGE)

    labs_line = (Fore.GREEN + "E1" + " /"
                 + Fore.RED + "/ " + "M1" + Fore.MAGENTA + " | " + "КАЗИК" + Fore.RESET)

    default_input_cycle(
        input_message=f"Введите вариант лабубы:\n{labs_line}\n",
        callback_handler=_main_input_callback_handler
    )


def _main_input_callback_handler(variant: str):
    match variant.upper():
        case "E1":
            entry_point_e1()
        case "M1":
            return False  # break
        case "КАЗИК":
            return False  # break
        case _:
            print("Такой лабубы нет... Попробуйте ещё раз\n" + "=" * 40)


if __name__ == "__main__":
    main()
