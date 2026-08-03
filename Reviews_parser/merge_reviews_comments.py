"""
==================================================
OZON REVIEWS + COMMENTS MERGER
==================================================

Назначение
----------

Объединяет:

    reviews_clean.json

и

    comments_clean.json


В результат:

    reviews_with_comments.json


Структура результата:

[
    {
        "review_id": "...",
        "sku": 123456,
        "product_name": "...",
        "text": "...",

        "comments": [
            {
                "comment_id": "...",
                "text": "...",
                "author": "...",
                "date": "..."
            }
        ]
    }
]


НЕ отвечает за:

✘ получение API
✘ Playwright
✘ очистку данных
✘ парсинг отзывов


==================================================
"""


import json



from config import (
    CLEAN_REVIEWS_FILE,
    COMMENTS_CLEAN_FILE,
    REVIEWS_WITH_COMMENTS_FILE
)





# ==================================================
# LOAD
# ==================================================

def load_json(path):
    """
    Загружает JSON файл.
    """


    print()

    print(
        "Загрузка:"
    )

    print(
        path
    )


    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:


        return json.load(
            file
        )





# ==================================================
# SAVE
# ==================================================

def save_json(
    data,
    path
):
    """
    Сохраняет JSON.
    """


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

    print(
        "Сохранено:"
    )

    print(
        path
    )



    print()

    print(
        "Количество отзывов:",
        len(data)
    )





# ==================================================
# MERGE
# ==================================================

def merge_reviews_comments(
    reviews,
    comments
):
    """
    Добавляет комментарии
    внутрь соответствующего отзыва.

    Связь:

        comments.review_id

            ==

        reviews.review_id

    """



    comments_map = {}



    for comment in comments:


        review_id = comment.get(
            "review_id"
        )



        if not review_id:

            continue



        if review_id not in comments_map:


            comments_map[review_id] = []



        comments_map[review_id].append(
            comment
        )





    result = []



    for review in reviews:


        review_id = review.get(
            "review_id"
        )



        review_copy = dict(
            review
        )



        review_copy["comments"] = comments_map.get(

            review_id,

            []

        )



        result.append(
            review_copy
        )



    return result





# ==================================================
# MAIN
# ==================================================

def main():


    print()

    print(
        "=" * 60
    )

    print(
        "MERGE REVIEWS + COMMENTS"
    )

    print(
        "=" * 60
    )



    reviews = load_json(
        CLEAN_REVIEWS_FILE
    )


    comments = load_json(
        COMMENTS_CLEAN_FILE
    )



    print()

    print(
        "Отзывы:",
        len(reviews)
    )


    print(
        "Комментарии:",
        len(comments)
    )





    merged = merge_reviews_comments(

        reviews,

        comments

    )



    save_json(

        merged,

        REVIEWS_WITH_COMMENTS_FILE

    )



    print()

    print(
        "=" * 60
    )

    print(
        "ГОТОВО"
    )

    print(
        "=" * 60
    )





if __name__ == "__main__":


    main()