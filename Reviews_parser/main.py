"""
==================================================
OZON REVIEWS PARSER
==================================================

Главный файл запуска.

Pipeline:

RAW reviews
        |
        v
reviews_clean.json


RAW comments
        |
        v
comments_clean.json


reviews_clean
        +
comments_clean
        |
        v
reviews_with_comments.json


==================================================
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
    COMMENTS_RAW_FILE,
    COMMENTS_CLEAN_FILE,
    REVIEWS_WITH_COMMENTS_FILE,
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



from parser.comment_json_parser import (
    add_comments_listener,
    collect_comments_by_clicks,
    get_comments_data
)



from merge_reviews_comments import (
    merge_reviews_comments
)




# ==================================================
# STORAGE
# ==================================================

reviews_pages = []

comments_pages = []


found_review_urls = set()

found_comment_ids = set()


seen_review_cards = set()





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



        (
            playwright,
            browser,
            page
        ) = await connect_edge()



        print()

        print(
            "Edge подключен."
        )




        # ==================================================
        # REVIEW LISTENER
        # ==================================================

        await add_api_listener(

            page,

            storage=reviews_pages,

            found_urls=found_review_urls,

            url_contains=API_BASE,

            required_url_parts=[

                REVIEWS_CONTAINER

            ]

        )



        print()

        print(
            "Review listener установлен."
        )




        # ==================================================
        # COMMENT LISTENER
        # ==================================================

        await add_comments_listener(

            page,

            storage=comments_pages,

            found_ids=found_comment_ids

        )



        print()

        print(
            "Comment listener установлен."
        )




        # ==================================================
        # PRODUCT
        # ==================================================

        await open_product(

            page

        )





        # ==================================================
        # AFTER SCROLL CALLBACK
        # ==================================================

        async def after_scroll():


            print()

            print(
                "Проверка комментариев..."
            )



            await collect_comments_by_clicks(

                page,

                seen_review_cards

            )





        # ==================================================
        # SCROLL
        # ==================================================

        await scroll_page(

            page,

            get_items_count=lambda:

                len(reviews_pages),


            after_scroll=after_scroll

        )






        # ==================================================
        # SAVE RAW
        # ==================================================

        save_json(

            reviews_pages,

            OUTPUT_FILE

        )


        save_json(

            comments_pages,

            COMMENTS_RAW_FILE

        )



        print()

        print(
            "RAW JSON сохранены."
        )





        # ==================================================
        # CLEAN REVIEWS
        # ==================================================

        print()

        print(
            "Обработка отзывов..."
        )



        clean_reviews = extract_reviews(

            reviews_pages

        )



        save_json(

            clean_reviews,

            CLEAN_REVIEWS_FILE

        )



        print()

        print(
            "Отзывы:",
            len(clean_reviews)
        )






        # ==================================================
        # CLEAN COMMENTS
        # ==================================================

        print()

        print(
            "Обработка комментариев..."
        )



        clean_comments = get_comments_data(

            comments_pages

        )



        save_json(

            clean_comments,

            COMMENTS_CLEAN_FILE

        )



        print()

        print(
            "Комментарии:",
            len(clean_comments)
        )






        # ==================================================
        # MERGE
        # ==================================================

        print()

        print(
            "Объединение отзывов и комментариев..."
        )



        merged = merge_reviews_comments(

            clean_reviews,

            clean_comments

        )



        save_json(

            merged,

            REVIEWS_WITH_COMMENTS_FILE

        )



        print()

        print(
            "Объединено:",
            len(merged)
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