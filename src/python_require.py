def assert_python_version():
    """
        Выкидывает ошибку, если версия Python не подходит
        kinda костыль для default venv
    """
    # https://stackoverflow.com/questions/11889932/specify-python-version-for-virtualenv-in-requirements-txt
    import sys
    cur_ver = sys.version_info[0:2]
    if cur_ver < (3, 10):  # match case construction
        cur_ver_str = f"{cur_ver[0]}.{cur_ver[1]}"
        raise Exception(f'Необходима версия Python >= 3.10. У Вас стоит {cur_ver_str}\n(match case contruction)')
