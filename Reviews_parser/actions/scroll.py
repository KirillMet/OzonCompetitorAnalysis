"""
==================================================
Прокрутка страницы Ozon
==================================================

Назначение:
    Выполняет плавную прокрутку страницы.

Модуль полностью универсальный.

Он НЕ знает:

    • что парсим
    • отзывы это или комментарии
    • где хранятся найденные данные

Ему передается функция get_items_count(),
которая возвращает текущее количество
полученных страниц.

Если количество долго не меняется,
скролл автоматически завершается.
"""

from config import MAX_SCROLLS


# ==================================================
# SCROLL
# ==================================================

async def scroll_page(
    page,
    get_items_count
):
    """
    Универсальная прокрутка страницы.

    Parameters
    ----------
    page
        Playwright Page

    get_items_count
        Функция без параметров.

        Должна вернуть текущее количество
        уже найденных элементов.

        Например:

            lambda: len(reviews_pages)

    Returns
    -------
    None
    """

    print()
    print("=" * 60)
    print("Начинаю прокрутку страницы...")
    print("=" * 60)

    no_new_items = 0

    for scroll_number in range(MAX_SCROLLS):

        print()
        print(f"Скролл {scroll_number + 1}")

        #
        # Количество элементов
        # до прокрутки.
        #
        before = get_items_count()

        #
        # Плавный скролл.
        #
        for _ in range(8):

            await page.mouse.wheel(
                0,
                500
            )

            await page.wait_for_timeout(
                250
            )

        #
        # Ждем возможную загрузку API.
        #
        await page.wait_for_timeout(
            3000
        )

        #
        # Количество элементов
        # после прокрутки.
        #
        after = get_items_count()

        #
        # Если получили новые страницы.
        #
        if after > before:

            print(
                f"Получено новых страниц: {after - before}"
            )

            no_new_items = 0

        #
        # Если ничего нового.
        #
        else:

            no_new_items += 1

            print(
                f"Новых страниц нет ({no_new_items}/10)"
            )

        #
        # Иногда Ozon отвечает
        # через несколько секунд.
        #
        if no_new_items >= 10:

            print()
            print(
                "Ожидаю возможную дозагрузку..."
            )

            await page.wait_for_timeout(
                10000
            )

            #
            # Проверяем еще раз.
            #
            if get_items_count() == after:

                print()
                print(
                    "Новые страницы больше не появляются."
                )

                print(
                    "Прокрутка завершена."
                )

                break

            else:

                print(
                    "После ожидания появились новые страницы."
                )

                no_new_items = 0

    print()
    print("=" * 60)
    print("Прокрутка закончена.")
    print("=" * 60)