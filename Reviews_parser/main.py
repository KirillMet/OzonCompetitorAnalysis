"""
==================================================
OZON REVIEWS PARSER
==================================================

Главный файл запуска.

Отвечает за:

    1. Подключение к Edge
    2. Установку API listener
    3. Открытие товара
    4. Прокрутку страницы
    5. Сохранение raw JSON
    6. Очистку отзывов
    7. Сохранение clean JSON

Вся логика находится в модулях.
"""


import asyncio



# ==================================================
# CONFIG
# ==================================================

from config import (
    API_BASE,
    REVIEWS_CONTAINER,
    OUTPUT_FILE,
    CLEAN_REVIEWS_FILE,
    TITLE_SEPARATOR
)



# ==================================================
# MODULES
# ==================================================

from browser.edge import (
    connect_edge,
    close_browser
)


from actions.product import (
    open_product
)


from actions.scroll import (
    scroll_page
)


from network.api_listener import (
    add_api_listener
)


from storage.json_writer import (
    save_json
)


from parser.review_json_parser import (
    extract_reviews
)




# ==================================================
# GLOBAL STORAGE
# ==================================================

# сырые ответы API Ozon

reviews_pages = []


# обработанные URL API

found_urls = set()




# ==================================================
# MAIN
# ==================================================

async def main():


    print(TITLE_SEPARATOR)

    print(
        "OZON REVIEWS PARSER"
    )

    print(TITLE_SEPARATOR)



    playwright = None

    browser = None



    try:



        # ------------------------------------------
        # EDGE CONNECT
        # ------------------------------------------

        (
            playwright,
            browser,
            page
        ) = await connect_edge()



        print()

        print(
            "Edge подключен."
        )




        # ------------------------------------------
        # API LISTENER
        # ------------------------------------------

        await add_api_listener(

            page,

            storage=reviews_pages,

            found_urls=found_urls,

            url_contains=API_BASE,

            required_url_parts=[
                REVIEWS_CONTAINER
            ]

        )



        print()

        print(
            "API listener установлен."
        )




        # ------------------------------------------
        # PRODUCT
        # ------------------------------------------

        await open_product(
            page
        )




        # ------------------------------------------
        # SCROLL
        # ------------------------------------------

        await scroll_page(

            page,

            get_items_count=lambda:
                len(reviews_pages)

        )




        # ------------------------------------------
        # SAVE RAW JSON
        # ------------------------------------------

        save_json(

            reviews_pages,

            OUTPUT_FILE

        )



        print()

        print(
            "RAW JSON сохранен."
        )




        # ------------------------------------------
        # PARSE CLEAN REVIEWS
        # ------------------------------------------

        print()

        print(
            "Начинаю обработку отзывов..."
        )



        clean_reviews = extract_reviews(
            reviews_pages
        )



        print()

        print(
            "Очищенных отзывов:",
            len(clean_reviews)
        )



        save_json(

            clean_reviews,

            CLEAN_REVIEWS_FILE

        )



        print()

        print(
            "CLEAN JSON сохранен."
        )




        print()

        print(
            "Парсинг полностью завершен."
        )




    except Exception as e:


        print()

        print(
            "ОШИБКА:"
        )

        print(e)




    finally:


        if browser:


            await close_browser(
                playwright,
                browser
            )




# ==================================================
# START
# ==================================================

if __name__ == "__main__":


    asyncio.run(
        main()
    )