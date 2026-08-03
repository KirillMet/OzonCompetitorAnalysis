"""
==================================================
OZON COMMENT JSON PARSER
==================================================

Назначение
----------

1. Слушает API Ozon комментариев:

    rpGetCommentsByReviewUuid


2. Сохраняет RAW:

    comments_raw.json


3. Преобразует RAW:

    comments_clean.json


Pipeline:

Review API
    |
    v
reviews_raw.json
    |
    v
reviews_clean.json


Комментарии:

Клик "Комментарии"
    |
    v
rpGetCommentsByReviewUuid
    |
    v
comments_raw.json
    |
    v
comments_clean.json


==================================================
"""


import json
import hashlib

from datetime import datetime

from config import (
    DATA_DIR
)


# ==================================================
# FILES
# ==================================================

COMMENTS_RAW_FILE = DATA_DIR + r"\comments_raw.json"

COMMENTS_CLEAN_FILE = DATA_DIR + r"\comments_clean.json"



# ==================================================
# DATE
# ==================================================

def unix_to_date(timestamp):

    if not timestamp:
        return None


    try:

        return datetime.fromtimestamp(
            timestamp
        ).strftime(
            "%Y-%m-%d %H:%M:%S"
        )


    except Exception:

        return None



# ==================================================
# SAVE
# ==================================================

def save_json(data, path):

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


    print()
    print("Сохранено:")
    print(path)

    print(
        "Объектов:",
        len(data)
    )



# ==================================================
# LOAD
# ==================================================

def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)



# ==================================================
# COMMENT LISTENER
# ==================================================

async def add_comments_listener(
    page,
    storage,
    found_ids
):
    """
    Слушает API комментариев Ozon.
    """



    async def handler(response):


        if (
            "rpGetCommentsByReviewUuid"
            not in response.url
        ):

            return



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




        try:

            data = await response.json()


        except Exception:

            return




        comments = data.get(
            "comments",
            []
        )



        if not comments:

            return




        new_comments = []



        for comment in comments:


            comment_uuid = comment.get(
                "uuid"
            )



            if not comment_uuid:

                continue



            if comment_uuid in found_ids:

                continue



            found_ids.add(
                comment_uuid
            )



            new_comments.append(
                comment
            )




        if not new_comments:

            return




        storage.append(
            {

                "review_uuid":

                    review_uuid,


                "request":

                    request_data,


                "comments":

                    new_comments,


                "raw":

                    data

            }
        )



        print()
        print("=" * 70)

        print(
            "НАЙДЕНЫ КОММЕНТАРИИ"
        )

        print(
            "Review:",
            review_uuid
        )

        print(
            "Количество:",
            len(new_comments)
        )

        print("=" * 70)




    page.on(
        "response",
        handler
    )



# ==================================================
# HASH REVIEW CARD
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
            html.encode("utf-8")
        ).hexdigest()



    except Exception:

        return None




# ==================================================
# CLICK COMMENTS
# ==================================================

async def collect_comments_by_clicks(
    page,
    seen_review_cards,
    max_scrolls=20
):


    empty_scrolls = 0



    for _ in range(max_scrolls):


        links = await page.locator(
            "text=/Комментар/i"
        ).all()



        clicked = 0



        for link in links:


            try:


                if not await link.is_visible():

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



                await link.scroll_into_view_if_needed()



                await page.wait_for_timeout(
                    500
                )



                await link.click(
                    timeout=5000
                )



                await page.wait_for_timeout(
                    2000
                )


                clicked += 1



            except Exception as e:

                print(
                    "Ошибка клика:",
                    e
                )




        if clicked == 0:

            empty_scrolls += 1

        else:

            empty_scrolls = 0




        if empty_scrolls >= 3:

            break




        await page.mouse.wheel(
            0,
            1000
        )



        await page.wait_for_timeout(
            1500
        )



# ==================================================
# CLEAN COMMENTS PARSER
# ==================================================

def get_comments_data(raw_data):
    """
    RAW comments_raw.json
    ->
    comments_clean.json
    """



    result = []

    seen = set()



    for block in raw_data:


        review_uuid = block.get(
            "review_uuid"
        )



        comments = block.get(
            "comments",
            []
        )



        for comment in comments:


            comment_id = comment.get(
                "uuid"
            )



            if not comment_id:

                continue



            if comment_id in seen:

                continue



            seen.add(
                comment_id
            )



            author = comment.get(
                "author",
                {}
            )



            usefulness = comment.get(
                "usefulness",
                {}
            )



            result.append(
                {

                    "comment_id":

                        comment_id,


                    "review_id":

                        review_uuid,


                    "sku":

                        comment.get(
                            "itemId"
                        ),


                    "date":

                        unix_to_date(
                            comment.get(
                                "createdAt"
                            )
                        ),



                    "author":

                        author.get(
                            "firstName",
                            ""
                        ),



                    "text":

                        comment.get(
                            "comment",
                            ""
                        ),



                    "likes":

                        usefulness.get(
                            "useful",
                            0
                        ),



                    "dislikes":

                        usefulness.get(
                            "unuseful",
                            0
                        ),



                    "is_official":

                        bool(
                            author.get(
                                "clientOfficial"
                            )
                        )

                }
            )



    return result



# ==================================================
# MAIN CLEAN
# ==================================================

def create_comments_clean():


    print()
    print("=" * 70)

    print(
        "COMMENT CLEAN PARSER"
    )

    print("=" * 70)



    raw = load_json(
        COMMENTS_RAW_FILE
    )



    clean = get_comments_data(
        raw
    )



    save_json(
        clean,
        COMMENTS_CLEAN_FILE
    )



    print()
    print("ГОТОВО")



# ==================================================
# START
# ==================================================

if __name__ == "__main__":

    create_comments_clean()