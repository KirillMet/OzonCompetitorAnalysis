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
    "comments_result.json"
)


DEBUG_FILE = os.path.join(
    BASE_DIR,
    "comments_debug.json"
)



PRODUCT_URL = (
    "https://www.ozon.ru/product/"
    "issey-miyake-l-eau-d-issey-pour-homme-"
    "muzhskaya-tualetnaya-voda-75-ml-2142680228/"
    "?at=mqtkxLJrAhM8Eom3TMDPw9VCAqKKrhOmln2uAy25m2"
    "&sh=AOnqoPs0Iw"
)



EDGE_DEBUG_URL = (
    "http://localhost:9222"
)



MAX_SCROLLS = 100



# ==================================================
# ГЛОБАЛЬНЫЕ
# ==================================================

reviews = []


found_pages = set()





# ==================================================
# EDGE
# ==================================================

async def connect_edge():


    playwright = await async_playwright().start()


    browser = await playwright.chromium.connect_over_cdp(
        EDGE_DEBUG_URL
    )


    context = browser.contexts[0]


    if context.pages:

        page = context.pages[0]

    else:

        page = await context.new_page()



    return playwright, browser, page





# ==================================================
# ПОИСК КОММЕНТАРИЕВ
# ==================================================

async def add_listener(page):


    async def handler(response):


        url = response.url



        if (
            "entrypoint-api.bx/page/json/v2"
            not in url
        ):
            return



        if (
            "reviewshelfpaginator"
            not in url
        ):
            return



        if url in found_pages:

            return


        found_pages.add(url)



        print()
        print("=" * 80)
        print("НАЙДЕН API ОТЗЫВОВ")
        print(url)
        print("=" * 80)



        try:


            data = await response.json()



            #
            # сохраняем последний ответ для анализа
            #

            with open(
                DEBUG_FILE,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    data,
                    f,
                    ensure_ascii=False,
                    indent=2
                )



            extract_reviews(data)



        except Exception as e:


            print(
                "Ошибка JSON:",
                e
            )




    page.on(
        "response",
        handler
    )






# ==================================================
# ИЗВЛЕЧЕНИЕ
# ==================================================

def extract_reviews(data):


    """
    Ищем webListReviews
    """



    text = json.dumps(
        data,
        ensure_ascii=False
    )



    if "webListReviews" not in text:

        return



    find_reviews(
        data
    )







def find_reviews(obj):


    if isinstance(obj, dict):


        for key,value in obj.items():


            if key == "reviews" and isinstance(value,list):


                for review in value:

                    parse_review(
                        review
                    )



            else:

                find_reviews(
                    value
                )




    elif isinstance(obj,list):


        for item in obj:

            find_reviews(
                item
            )






def parse_review(review):


    if not isinstance(review,dict):

        return



    content = review.get(
        "content",
        {}
    )


    comment_text = content.get(
        "comment",
        ""
    )


    score = content.get(
        "score"
    )



    review_id = review.get(
        "uuid"
    )



    if not comment_text:

        return



    #
    # комментарии к отзыву
    #

    answers = []



    comments = review.get(
        "comments",
        {}
    )


    comment_list = comments.get(
        "list",
        []
    )



    for item in comment_list:


        answers.append(
            item
        )




    result = {

        "review_id": review_id,

        "review": comment_text,

        "rating": score,

        "comments_count":
            len(answers),

        "comments":
            answers

    }



    #
    # защита от дублей
    #

    ids = [
        x.get("review_id")
        for x in reviews
    ]



    if review_id not in ids:


        reviews.append(
            result
        )



        print()

        print(
            "ОТЗЫВ:"
        )

        print(
            comment_text
        )


        print(
            "Рейтинг:",
            score
        )


        print(
            "Комментариев:",
            len(answers)
        )







# ==================================================
# ОТКРЫТИЕ ТОВАРА
# ==================================================

async def open_product(page):


    print()

    print(
        "Текущая страница:"
    )


    print(
        page.url
    )



    if "ozon.ru/product" not in page.url:


        print(
            "Открываю товар..."
        )


        await page.goto(
            PRODUCT_URL,
            wait_until="domcontentloaded",
            timeout=90000
        )


    await page.wait_for_timeout(
        5000
    )







# ==================================================
# СКРОЛЛ
# ==================================================

async def scroll(page):


    print()

    print(
        "Начинаю поиск отзывов..."
    )



    for i in range(MAX_SCROLLS):


        print(
            "Скролл:",
            i+1
        )



        await page.mouse.wheel(
            0,
            700
        )


        await page.wait_for_timeout(
            2500
        )





# ==================================================
# SAVE
# ==================================================

def save():


    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:


        json.dump(
            reviews,
            f,
            ensure_ascii=False,
            indent=2
        )



    print()

    print("="*70)

    print(
        "Всего отзывов:",
        len(reviews)
    )


    print(
        "Сохранено:"
    )


    print(
        OUTPUT_FILE
    )






# ==================================================
# MAIN
# ==================================================

async def main():


    print("="*60)

    print(
        "OZON COMMENTS TEST"
    )

    print("="*60)



    playwright,browser,page = await connect_edge()



    print(
        "Edge подключен"
    )



    await add_listener(
        page
    )


    await open_product(
        page
    )



    await scroll(
        page
    )



    save()



    await browser.close()

    await playwright.stop()





if __name__ == "__main__":

    asyncio.run(
        main()
    )