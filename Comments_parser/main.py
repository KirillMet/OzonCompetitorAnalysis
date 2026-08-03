import asyncio


from config import (
    PRODUCT_URL,
    COMMENTS_RAW_FILE,
    SEPARATOR
)


from browser.edge import connect_edge


from actions.product import open_product


from actions.scroll import scroll_page


from network.comments_listener import (
    add_comments_listener,
    save_comments_pages
)


from parser.html_search import (
    search_review_ids
)



async def main():

    print(SEPARATOR)
    print("OZON COMMENTS ANALYZER")
    print(SEPARATOR)
    print()


    playwright = None
    browser = None


    try:


        #
        # Подключение к Edge
        #
        playwright, browser, page = await connect_edge()


        print()
        print(
            "Edge подключен"
        )


        #
        # Буфер API ответов
        #
        comments_pages = []


        #
        # Ставим listener заранее
        #
        await add_comments_listener(
            page,
            comments_pages
        )


        #
        # Открываем товар
        #
        print(
            "Открываю товар..."
        )


        await open_product(
            page,
            PRODUCT_URL
        )


        print()
        print(
            "Карточка открыта"
        )


        #
        # Скролл отзывов
        #
        print()
        print(
            "Начинаю прокрутку..."
        )


        await scroll_page(
            page
        )


        print()
        print(
            "Прокрутка закончена"
        )


        #
        # Сохранение API
        #
        save_comments_pages(
            comments_pages,
            COMMENTS_RAW_FILE
        )


        #
        # Поиск UUID
        #
        html = await page.content()


        print()
        print(
            "Ищу идентификаторы отзывов..."
        )


        search_review_ids(
            html
        )


        print()
        print(
            "Анализ завершен"
        )


    finally:


        print()
        print(
            "Закрываю соединение с Edge..."
        )


        if browser:

            await browser.close()


        if playwright:

            await playwright.stop()


        print(
            "Готово."
        )



if __name__ == "__main__":

    asyncio.run(
        main()
    )