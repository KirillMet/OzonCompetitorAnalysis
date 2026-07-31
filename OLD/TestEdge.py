from playwright.sync_api import sync_playwright
import time


CDP_URL = "http://127.0.0.1:9222"

# сюда вставь артикул для поиска
ARTICLE = "3272158539"


def main():

    print("Подключение к Edge...")

    with sync_playwright() as p:

        browser = p.chromium.connect_over_cdp(
            CDP_URL
        )

        print("Подключено")

        context = browser.contexts[0]

        print(
            "Вкладок:",
            len(context.pages)
        )

        page = context.pages[0]


        print("Текущий URL:")
        print(page.url)


        # открываем поиск Ozon
        search_url = (
            f"https://www.ozon.ru/search/?text={ARTICLE}"
        )

        print()
        print("Ищем:")
        print(search_url)


        page.goto(
            search_url,
            wait_until="domcontentloaded",
            timeout=60000
        )


        print()
        print("После поиска:")
        print("URL:", page.url)
        print("TITLE:", page.title())


        time.sleep(5)


        # сохраняем скрин
        page.screenshot(
            path="ozon_search.png",
            full_page=True
        )


        print()
        print("Ссылки товаров:")


        links = page.locator(
            "a[href*='/product/']"
        )


        count = links.count()

        print(
            "Найдено:",
            count
        )


        for i in range(min(count, 10)):

            href = links.nth(i).get_attribute(
                "href"
            )

            print(
                href
            )


        input(
            "\nEnter для выхода..."
        )


if __name__ == "__main__":
    main()