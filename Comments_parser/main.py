import asyncio
import json
import os
import hashlib

from playwright.async_api import async_playwright


# ==================================================
# НАСТРОЙКИ
# ==================================================

EDGE_DEBUG_URL = "http://localhost:9222"

PRODUCT_URL = (
    "https://www.ozon.ru/product/"
    "issey-miyake-l-eau-d-issey-pour-homme-"
    "muzhskaya-tualetnaya-voda-75-ml-2142680228/"
    "?at=mqtkxLJrAhM8Eom3TMDPw9VCAqKKrhOmln2uAy25m2"
    "&sh=AOnqoPs0Iw"
)


OUTPUT_FILE = (
    r"C:\OzonDownloader\Reviews_parser\data\comments_raw.json"
)


MAX_SCROLLS = 100


# ==================================================
# ГЛОБАЛЬНЫЕ ДАННЫЕ
# ==================================================

found_requests = []

processed_reviews = set()

found_comment_uuids = set()

seen_review_cards = set()



# ==================================================
# EDGE
# ==================================================

async def connect_edge():

    playwright = await async_playwright().start()


    browser = await playwright.chromium.connect_over_cdp(
        EDGE_DEBUG_URL
    )


    if not browser.contexts:
        raise Exception(
            "Нет контекста Edge"
        )


    context = browser.contexts[0]


    if context.pages:

        page = context.pages[0]

    else:

        page = await context.new_page()


    return playwright, browser, page



# ==================================================
# API LISTENER
# ==================================================

async def add_comments_listener(page):


    async def handler(response):


        if "rpGetCommentsByReviewUuid" not in response.url:

            return



        request_data = None


        try:

            request_data = json.loads(
                response.request.post_data
            )

        except Exception:

            return



        review_uuid = request_data.get(
            "reviewUuid"
        )


        if not review_uuid:

            return



        if review_uuid in processed_reviews:

            return



        processed_reviews.add(
            review_uuid
        )



        try:

            data = await response.json()

        except Exception:

            return



        comments = data.get(
            "comments",
            []
        )



        found_requests.append(
            {
                "request": request_data,
                "data": data
            }
        )



        os.makedirs(
            os.path.dirname(OUTPUT_FILE),
            exist_ok=True
        )



        with open(
            OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as f:


            json.dump(
                found_requests,
                f,
                ensure_ascii=False,
                indent=2
            )



        for comment in comments:


            uuid = comment.get(
                "uuid"
            )


            if uuid in found_comment_uuids:

                continue



            found_comment_uuids.add(
                uuid
            )



            print()

            print("=" * 80)

            print(
                "НОВЫЙ КОММЕНТАРИЙ"
            )

            print("=" * 80)


            print(
                "REVIEW UUID:",
                review_uuid
            )


            print(
                "COMMENT UUID:",
                uuid
            )


            print(
                "TEXT:",
                comment.get(
                    "comment",
                    ""
                )
            )


            print("=" * 80)



    page.on(
        "response",
        handler
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
# HASH КАРТОЧКИ ОТЗЫВА
# ==================================================

async def get_review_card_hash(element):


    try:


        html = await element.evaluate(
            """
            el => {

                let node = el;

                for(let i=0;i<6;i++){

                    if(!node.parentElement)
                        break;

                    node=node.parentElement;
                }

                return node.outerHTML;
            }
            """
        )


        return hashlib.md5(
            html.encode(
                "utf-8"
            )
        ).hexdigest()



    except Exception:

        return None



# ==================================================
# КЛИКИ
# ==================================================

async def collect_comments_by_clicks(page):


    empty_scrolls = 0



    for scroll in range(
        MAX_SCROLLS
    ):


        print()

        print(
            f"СКРОЛЛ #{scroll + 1}"
        )



        links = await page.locator(
            "text=/Комментар/i"
        ).all()



        print(
            "Найдено кнопок:",
            len(links)
        )



        clicked = 0



        for link in links:


            try:


                if not await link.is_visible():

                    continue



                box = await link.bounding_box()



                if not box:

                    continue



                if box["y"] < 0:

                    continue



                card_hash = await get_review_card_hash(
                    link
                )



                if not card_hash:

                    continue



                if card_hash in seen_review_cards:

                    continue



                seen_review_cards.add(
                    card_hash
                )



                print()

                print(
                    "Клик по новой карточке:",
                    card_hash
                )



                await link.scroll_into_view_if_needed()



                await page.wait_for_timeout(
                    500
                )



                await link.click(
                    timeout=5000
                )



                await page.wait_for_timeout(
                    3000
                )


                clicked += 1



            except Exception as e:


                print(
                    "Ошибка:",
                    e
                )



        print(
            "Новых кликов:",
            clicked
        )



        if clicked == 0:

            empty_scrolls += 1

        else:

            empty_scrolls = 0



        if empty_scrolls >= 5:

            break



        await page.mouse.wheel(
            0,
            1200
        )


        await page.wait_for_timeout(
            2000
        )



# ==================================================
# MAIN
# ==================================================

async def main():


    print("=" * 60)

    print(
        "COMMENTS CLICK COLLECTOR"
    )

    print("=" * 60)



    playwright, browser, page = await connect_edge()



    print(
        "Edge подключен"
    )



    await add_comments_listener(
        page
    )


    await open_product(
        page
    )


    await collect_comments_by_clicks(
        page
    )



    await page.wait_for_timeout(
        5000
    )



    print()

    print("=" * 60)

    print(
        "API запросов:",
        len(found_requests)
    )


    print(
        "Комментариев:",
        len(found_comment_uuids)
    )


    print(
        "Карточек:",
        len(seen_review_cards)
    )


    print("=" * 60)



    await browser.close()

    await playwright.stop()



if __name__ == "__main__":

    asyncio.run(main())