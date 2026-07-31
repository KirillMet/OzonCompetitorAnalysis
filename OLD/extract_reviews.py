import asyncio
import json
import os

from playwright.async_api import async_playwright


# ==================================================
# НАСТРОЙКИ
# ==================================================

BASE_DIR = r"C:\OzonDownloader"

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "reviews_raw.json"
)


PRODUCT_URL = (
    "https://www.ozon.ru/product/issey-miyake-l-eau-d-issey-pour-homme-muzhskaya-tualetnaya-voda-75-ml-2142680228/?at=mqtkxLJrAhM8Eom3TMDPw9VCAqKKrhOmln2uAy25m2&sh=AOnqoPs0Iw"
)


EDGE_DEBUG_URL = (
    "http://localhost:9222"
)


MAX_SCROLLS = 150



# ==================================================
# ГЛОБАЛЬНЫЕ ДАННЫЕ
# ==================================================

reviews_pages = []

found_urls = set()



# ==================================================
# EDGE CONNECT
# ==================================================

async def connect_edge():


    playwright = await async_playwright().start()


    browser = await playwright.chromium.connect_over_cdp(
        EDGE_DEBUG_URL
    )


    if not browser.contexts:

        raise Exception(
            "Edge context не найден"
        )


    context = browser.contexts[0]


    if context.pages:

        page = context.pages[0]

    else:

        page = await context.new_page()



    return playwright, browser, page




# ==================================================
# LISTENER API
# ==================================================

async def add_listener(page):


    async def response_handler(response):


        url = response.url



        if (
            "entrypoint-api.bx/page/json/v2"
            not in url
        ):
            return



        # берем только отзывы

        if (
            "reviewshelfpaginator"
            not in url
        ):
            return



        if url in found_urls:

            return



        found_urls.add(url)



        print()
        print("=" * 70)
        print("НАЙДЕН API ОТЗЫВОВ")
        print(url)
        print("=" * 70)



        try:

            data = await response.json()


            reviews_pages.append(
                data
            )


            print(
                "Добавлена страница:",
                len(reviews_pages)
            )


        except Exception as e:


            print(
                "Ошибка чтения JSON:",
                e
            )



    page.on(
        "response",
        response_handler
    )





# ==================================================
# OPEN PRODUCT
# ==================================================

async def open_product(page):


    print()

    print(
        "Текущая вкладка:"
    )

    print(
        page.url
    )



    if (
        "ozon.ru/product"
        not in page.url
    ):


        print(
            "Открываю карточку товара..."
        )


        await page.goto(
            PRODUCT_URL,
            wait_until="domcontentloaded",
            timeout=90000
        )


    else:


        print(
            "Карточка уже открыта"
        )



    await page.wait_for_timeout(
        5000
    )




# ==================================================
# SCROLL
# ==================================================

async def scroll_reviews(page):

    print()
    print("Начинаю прокрутку...")

    no_new_pages = 0

    for i in range(MAX_SCROLLS):

        print("Скролл:", i + 1)

        before = len(reviews_pages)

        # Плавный скролл как у обычного пользователя
        for _ in range(8):
            await page.mouse.wheel(0, 500)
            await page.wait_for_timeout(250)

        # Небольшая пауза на подгрузку
        await page.wait_for_timeout(3000)

        after = len(reviews_pages)

        if after > before:

            print(f"Получено новых страниц: {after - before}")

            no_new_pages = 0

        else:

            no_new_pages += 1

            print(
                f"Новых страниц нет ({no_new_pages}/10)"
            )

        # Даем Ozon дополнительное время,
        # иногда запрос приходит с задержкой
        if no_new_pages >= 10:

            print("Ожидаю возможную дозагрузку...")

            await page.wait_for_timeout(10000)

            if len(reviews_pages) == after:

                print("Новых страниц больше нет")

                break

            else:

                print("После ожидания появились новые страницы")

                no_new_pages = 0




# ==================================================
# SAVE
# ==================================================

def save_json():


    print()

    print("=" * 70)

    print(
        "Всего страниц:",
        len(reviews_pages)
    )

    print("=" * 70)



    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:


        json.dump(
            reviews_pages,
            f,
            ensure_ascii=False,
            indent=2
        )



    print()

    print(
        "Готово:"
    )

    print(
        OUTPUT_FILE
    )





# ==================================================
# MAIN
# ==================================================

async def main():


    print("=" * 60)
    print("OZON REVIEW SCRAPER")
    print("=" * 60)



    playwright, browser, page = await connect_edge()



    print()

    print(
        "Подключились к Edge"
    )



    await add_listener(
        page
    )



    await open_product(
        page
    )



    await scroll_reviews(
        page
    )



    save_json()



    await browser.close()

    await playwright.stop()





if __name__ == "__main__":

    asyncio.run(
        main()
    )