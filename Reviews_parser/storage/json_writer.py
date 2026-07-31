"""
==================================================
Сохранение данных в JSON
==================================================

Назначение
----------

Модуль отвечает только за сохранение данных
в json-файл.

Он не знает:

    • что именно сохраняется
    • отзывы это или вопросы
    • откуда пришли данные

Можно использовать для любых структур.
"""

import json
import os


# ==================================================
# SAVE JSON
# ==================================================

def save_json(
    data,
    output_file
):
    """
    Сохраняет список или словарь в JSON.

    Parameters
    ----------
    data
        Любые данные Python
        (list, dict)

    output_file
        Полный путь до файла.

    Returns
    -------
    None
    """

    #
    # Создаем папку,
    # если ее еще нет.
    #
    directory = os.path.dirname(
        output_file
    )

    os.makedirs(
        directory,
        exist_ok=True
    )

    #
    # Сохраняем JSON.
    #
    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2
        )

    print()

    print("=" * 70)

    print(
        "Всего сохранено объектов:",
        len(data)
    )

    print("=" * 70)

    print()

    print("Файл сохранен:")

    print(output_file)