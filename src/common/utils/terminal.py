class TerminalConfig:
    """СИНГЛТОН для конфигурации терминала"""
    is_debug: bool = False
    is_warning: bool = True

    # https://sky.pro/media/osnovy-raboty-s-classmethod-i-staticmethod-v-python/?ysclid=mgmvem8tnx306327031
    @classmethod
    def toggle_debug(cls):
        cls.is_debug = not cls.is_debug
        if not cls.is_debug:
            print("дебаг отключён")
        else:
            print("дебаг включён")

    @classmethod
    def toggle_warning(cls):
        cls.is_warning = not cls.is_warning
        if not cls.is_warning:
            print("предупреждения отключены")
        else:
            print("предупреждения включены")


DEFAULT_HELP_MESSAGE = (
        f'{'-' * 20}\nhelp - вывести это сообщение\n:q - выход\n:d - в{'ы' if TerminalConfig.is_debug else ''}ключить дебаг' +
        f'\n:w - в{'ы' if TerminalConfig.is_warning else ''}ключить предупреждения\n{'-' * 20}')


def default_input_cycle(input_message: str, callback_handler):
    while True:
        inp = input(input_message)
        match inp.lower():
            case "help":
                print(DEFAULT_HELP_MESSAGE)
            case ":q":
                break
            case ":d":
                TerminalConfig.toggle_debug()
            case ":w":
                TerminalConfig.toggle_warning()
            case _:
                callback_handler(inp)
