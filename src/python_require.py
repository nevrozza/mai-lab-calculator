def assert_python_version():
    """
    Выкидывает AssertionError, если версия Python не подходит
    kinda костыль для default venv
    :return: Данная функция ничего не возвращает
    """
    # https://stackoverflow.com/questions/11889932/specify-python-version-for-virtualenv-in-requirements-txt
    import sys
    cur_ver = sys.version_info[0:2]
    assert cur_ver >= (3, 10), (
        f"""
        Необходима версия Python >= 3.10. У Вас стоит {cur_ver[0]}.{cur_ver[1]}
        (match case contruction)
        """
    )
