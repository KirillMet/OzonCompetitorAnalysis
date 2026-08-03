"""
==================================================
Парсер отзывов Ozon
==================================================

Из comments_raw.json извлекает реальные отзывы.

Ищет структуры отзывов внутри API JSON:
- uuid
- text
- rating
- author
- date
- advantages
- disadvantages

Сохраняет:

data/comments_clean.json

Формат:

[
    {
        "id": "...",
        "rating": 5,
        "text": "...",
        "advantages": "...",
        "disadvantages": "...",
        "date": "...",
        "author": "..."
    }
]

"""

import json


from storage.json_writer import save_json


from config import COMMENTS_CLEAN_FILE



# ==================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ==================================================


def recursive_find_reviews(
    obj
):
    """
    Рекурсивный поиск объектов,
    похожих на отзывы.
    """

    found = []


    if isinstance(
        obj,
        dict
    ):


        #
        # Проверяем текущий объект
        #
        if is_review_object(obj):

            found.append(
                obj
            )


        #
        # Продолжаем поиск внутри
        #
        for value in obj.values():

            found.extend(
                recursive_find_reviews(
                    value
                )
            )



    elif isinstance(
        obj,
        list
    ):


        for item in obj:

            found.extend(
                recursive_find_reviews(
                    item
                )
            )


    return found





def is_review_object(
    obj
):
    """
    Проверяет,
    похож ли dict на отзыв.
    """


    if not isinstance(
        obj,
        dict
    ):

        return False



    keys = set(
        obj.keys()
    )



    #
    # Минимальные признаки отзыва
    #
    has_uuid = (
        "uuid" in keys
        or
        "id" in keys
    )


    has_text = any(
        key in keys
        for key in [
            "text",
            "content",
            "comment"
        ]
    )


    has_rating = any(
        key in keys
        for key in [
            "rating",
            "score",
            "stars"
        ]
    )


    return (
        has_uuid
        and
        (
            has_text
            or
            has_rating
        )
    )






def get_value(
    obj,
    keys
):
    """
    Получение значения
    по списку возможных ключей.
    """


    for key in keys:

        if key in obj:

            return obj[key]


    return None







def normalize_review(
    obj
):
    """
    Приведение отзыва
    к единому формату.
    """


    review = {

        "id": get_value(
            obj,
            [
                "uuid",
                "id"
            ]
        ),

        "rating": get_value(
            obj,
            [
                "rating",
                "score",
                "stars"
            ]
        ),

        "text": get_value(
            obj,
            [
                "text",
                "content",
                "comment"
            ]
        ),

        "advantages": get_value(
            obj,
            [
                "advantages",
                "pros"
            ]
        ),

        "disadvantages": get_value(
            obj,
            [
                "disadvantages",
                "cons"
            ]
        ),

        "date": get_value(
            obj,
            [
                "published_at",
                "created_at",
                "date"
            ]
        ),

        "author": get_value(
            obj,
            [
                "author",
                "userName",
                "name"
            ]
        )

    }


    return review






# ==================================================
# MAIN PARSER
# ==================================================


def parse_reviews(
    raw_file
):
    """
    Главная функция парсинга отзывов.

    raw_file:
        comments_raw.json
    """


    print()

    print(
        "=" * 60
    )

    print(
        "Парсинг отзывов"
    )

    print(
        "=" * 60
    )



    #
    # Загружаем API ответы
    #
    with open(
        raw_file,
        "r",
        encoding="utf-8"
    ) as file:

        pages = json.load(
            file
        )



    reviews = []



    #
    # Обходим страницы API
    #
    for page in pages:


        api_json = page.get(
            "json"
        )


        if not api_json:

            continue



        objects = recursive_find_reviews(
            api_json
        )


        for obj in objects:


            review = normalize_review(
                obj
            )


            #
            # Отбрасываем пустые
            #
            if not review["id"]:

                continue



            reviews.append(
                review
            )





    #
    # Удаляем дубли
    #
    unique = {}



    for review in reviews:

        unique[
            review["id"]
        ] = review




    result = list(
        unique.values()
    )



    print()

    print(
        "Найдено отзывов:",
        len(result)
    )



    save_json(
        result,
        COMMENTS_CLEAN_FILE
    )



    return result