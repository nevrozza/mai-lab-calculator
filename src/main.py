import colorama
from colorama import Fore

from src.python_require import assert_python_version


def main() -> None:
    assert_python_version()
    colorama.init()
    # easy_tokenize()
    # print(get_token_type("24").value * 2)
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """
    # target, degree = map(int, input("Введите два числа разделенные пробелом: ").split(" "))
    #
    # result = power_function(target=target, power=degree)
    #
    # print(result)

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
