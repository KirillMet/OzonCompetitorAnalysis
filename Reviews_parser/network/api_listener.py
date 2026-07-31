"""
==================================================
Универсальный слушатель API Ozon
==================================================

Назначение
----------

Перехватывает все ответы браузера и сохраняет
только те JSON, которые подходят под заданные
условия.

Сам модуль НЕ знает:

    • что находится внутри JSON
    • отзывы это или вопросы
    • как потом их разбирать

Он только:

    ✔ фильтрует URL
    ✔ читает JSON
    ✔ сохраняет найденные страницы

Благодаря этому его можно использовать
для любого API Ozon.
"""


# ==================================================
# API LISTENER
# ==================================================

async def add_api_listener(
    page,
    storage,
    found_urls,
    url_contains=None,
    required_url_parts=None,
    print_requests=True
):
    """
    Подключает обработчик всех API ответов.

    Parameters
    ----------
    page
        Playwright Page

    storage
        Список, куда складываются найденные JSON.

    found_urls
        Множество уже обработанных URL.

    url_contains
        Главная часть URL.

        Например:

            entrypoint-api.bx/page/json/v2

    required_url_parts
        Дополнительные обязательные строки.

        Например:

            [
                "reviewshelfpaginator"
            ]

        или

            [
                "questions"
            ]

    print_requests
        Показывать найденные запросы.
    """

    if required_url_parts is None:
        required_url_parts = []

    async def response_handler(response):

        url = response.url

        #
        # Проверяем главный фильтр.
        #
        if url_contains:

            if url_contains not in url:
                return

        #
        # Проверяем дополнительные условия.
        #
        for part in required_url_parts:

            if part not in url:
                return

        #
        # Уже обрабатывали.
        #
        if url in found_urls:
            return

        found_urls.add(url)

        if print_requests:

            print()
            print("=" * 70)
            print("НАЙДЕН API")
            print(url)
            print("=" * 70)

        try:

            data = await response.json()

            storage.append(data)

            if print_requests:

                print(
                    "Добавлена страница:",
                    len(storage)
                )

        except Exception as e:

            print()

            print(
                "Ошибка чтения JSON:"
            )

            print(e)

    page.on(
        "response",
        response_handler
    )