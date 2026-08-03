"""
browser/edge.py

Модуль отвечает только за подключение к уже запущенному
Microsoft Edge через Playwright CDP.

В модуле нет никакой логики парсинга Ozon.
Его единственная задача — вернуть объект страницы,
с которым дальше работают остальные модули.
"""

from playwright.async_api import async_playwright

from config import EDGE_DEBUG_URL


async def connect_edge():
    """
    Подключение к уже открытому Edge.

    Edge должен быть заранее запущен с параметром:

        --remote-debugging-port=9222

    Возвращает:

        playwright
        browser
        page
    """

    print()
    print("Запуск Playwright...")

    playwright = await async_playwright().start()

    print("Подключение к Edge...")

    browser = await playwright.chromium.connect_over_cdp(
        EDGE_DEBUG_URL
    )

    #
    # Проверяем, что браузер действительно содержит контекст.
    #
    if not browser.contexts:

        raise Exception(
            "Не найден ни один Context в Edge."
        )

    context = browser.contexts[0]

    #
    # Если вкладки уже существуют —
    # используем первую.
    #
    if context.pages:

        page = context.pages[0]

        print("Используется существующая вкладка.")

    #
    # Если вкладок нет —
    # создаём новую.
    #
    else:

        page = await context.new_page()

        print("Создана новая вкладка.")

    print()
    print("Успешное подключение к Edge.")
    print("Текущий URL:")
    print(page.url)

    return (
        playwright,
        browser,
        page
    )


async def close_browser(
    playwright,
    browser
):
    """
    Корректное завершение работы Playwright.
    """

    print()
    print("Закрываю соединение с Edge...")

    await browser.close()

    await playwright.stop()

    print("Готово.")