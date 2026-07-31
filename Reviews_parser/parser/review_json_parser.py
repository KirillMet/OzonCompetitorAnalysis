"""
==================================================
OZON REVIEW JSON PARSER
==================================================

Назначение
----------

Преобразует сырой ответ API Ozon:

    reviews_raw.json

в очищенный список отзывов:

    reviews_clean.json


Отвечает за:

    ✔ поиск блоков отзывов
    ✔ связывание отзывов с товарами
    ✔ очистку данных
    ✔ нормализацию структуры
    ✔ подготовку данных для анализа


НЕ отвечает за:

    ✘ получение данных из браузера
    ✘ API запросы
    ✘ Excel
    ✘ AI анализ


Pipeline:

Edge
 |
 v
api_listener.py
 |
 v
reviews_raw.json
 |
 v
review_json_parser.py
 |
 v
reviews_clean.json

==================================================
"""


import json

from datetime import datetime


from config import (
    OUTPUT_FILE,
    CLEAN_REVIEWS_FILE
)



# ==================================================
# FILES
# ==================================================

# Входной файл.
# Это сырой JSON, полученный listener'ом.

INPUT_FILE = OUTPUT_FILE




# ==================================================
# DATE
# ==================================================

def unix_to_date(ts):
    """
    Конвертация Unix timestamp
    в читаемую дату.
    """

    if not ts:
        return None


    try:

        return datetime.fromtimestamp(
            ts
        ).strftime(
            "%Y-%m-%d %H:%M:%S"
        )


    except Exception:

        return None




# ==================================================
# LOAD
# ==================================================

def load_json(path):
    """
    Загружает JSON файл.

    Возвращает:
        list | dict
    """

    print()

    print(
        "Загрузка файла:"
    )

    print(path)



    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:


        data = json.load(
            file
        )



    print()

    print(
        "Тип данных:",
        type(data).__name__
    )


    if isinstance(
        data,
        list
    ):

        print(
            "Количество страниц:",
            len(data)
        )


    return data




# ==================================================
# SAVE
# ==================================================

def save_json(
    data,
    path
):
    """
    Сохраняет результат обработки.
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

    print(path)

    print()

    print(
        "Количество объектов:",
        len(data)
    )

    # ==================================================
# HELPERS
# ==================================================

def get_pages(data):
    """
    Приводит входные данные
    к единому формату списка страниц.

    Ozon может вернуть:

        dict

    или:

        [
            dict,
            dict
        ]
    """

    if isinstance(
        data,
        list
    ):

        return data


    return [
        data
    ]




def safe_json_load(value):
    """
    Безопасная загрузка JSON
    из widgetStates.

    Ozon хранит часть данных
    как строку JSON внутри JSON.
    """

    if not isinstance(
        value,
        str
    ):

        return None


    try:

        return json.loads(
            value
        )


    except Exception:

        return None




# ==================================================
# PRODUCTS
# ==================================================

def extract_products(data):
    """
    Извлекает информацию о товарах.

    Отзывы содержат только itemId.

    Название, фото и варианты
    находятся в блоках products.
    """


    products = {}



    pages = get_pages(
        data
    )



    for page in pages:


        if not isinstance(
            page,
            dict
        ):

            continue



        widget_states = page.get(
            "widgetStates",
            {}
        )



        if not isinstance(
            widget_states,
            dict
        ):

            continue




        for value in widget_states.values():


            block = safe_json_load(
                value
            )



            if not isinstance(
                block,
                dict
            ):

                continue



            block_products = block.get(
                "products"
            )



            if not block_products:

                continue



            if not isinstance(
                block_products,
                dict
            ):

                continue



            products.update(
                block_products
            )



    print()

    print(
        "Найдено товаров:",
        len(products)
    )



    return products




# ==================================================
# PRODUCT VARIANTS
# ==================================================

def extract_variants(product):
    """
    Извлекает характеристики варианта товара.

    Например:

    {
        "Объем": "75 мл",
        "Цвет": "Черный"
    }
    """


    result = {}



    if not isinstance(
        product,
        dict
    ):

        return result



    variants = product.get(
        "variants",
        []
    )



    if not isinstance(
        variants,
        list
    ):

        return result



    for item in variants:


        if not isinstance(
            item,
            dict
        ):

            continue



        name = item.get(
            "name"
        )


        value = item.get(
            "value"
        )



        if name:

            result[name] = value



    return result

# ==================================================
# MEDIA
# ==================================================

def extract_photos(content):
    """
    Извлекает ссылки на фотографии отзыва.
    """

    photos_raw = content.get(
        "photos",
        []
    )


    if not isinstance(
        photos_raw,
        list
    ):

        return []



    photos = []


    for photo in photos_raw:


        if not isinstance(
            photo,
            dict
        ):

            continue



        url = photo.get(
            "url"
        )


        if url:

            photos.append(
                url
            )



    return photos




def extract_videos(content):
    """
    Извлекает ссылки на видео отзыва.
    """

    videos_raw = content.get(
        "videos",
        []
    )


    if not isinstance(
        videos_raw,
        list
    ):

        return []



    videos = []


    for video in videos_raw:


        if not isinstance(
            video,
            dict
        ):

            continue



        url = video.get(
            "url"
        )


        if url:

            videos.append(
                url
            )



    return videos




# ==================================================
# REVIEW PARSER
# ==================================================

def parse_review(
    review,
    products
):
    """
    Преобразует один отзыв Ozon
    в нормальную структуру.

    Parameters
    ----------
    review:
        сырой отзыв Ozon

    products:
        словарь товаров

    Returns
    -------
    dict
    """



    if not isinstance(
        review,
        dict
    ):

        return None




    content = review.get(
        "content",
        {}
    )


    if not isinstance(
        content,
        dict
    ):

        content = {}




    sku = review.get(
        "itemId"
    )



    product = products.get(
        str(sku),
        {}
    )



    if not isinstance(
        product,
        dict
    ):

        product = {}




    author = review.get(
        "author",
        {}
    )


    if not isinstance(
        author,
        dict
    ):

        author = {}




    usefulness = review.get(
        "usefulness",
        {}
    )


    if not isinstance(
        usefulness,
        dict
    ):

        usefulness = {}




    comment = content.get(
        "comment",
        ""
    )


    if not isinstance(
        comment,
        str
    ):

        comment = ""




    photos = extract_photos(
        content
    )


    videos = extract_videos(
        content
    )



    useful = usefulness.get(
        "useful",
        0
    )


    unuseful = usefulness.get(
        "unuseful",
        0
    )



    if not isinstance(
        useful,
        int
    ):

        useful = 0



    if not isinstance(
        unuseful,
        int
    ):

        unuseful = 0




    return {


        "review_id":

            review.get(
                "uuid"
            ),



        "sku":

            sku,



        "product_name":

            product.get(
                "name",
                ""
            ),



        "product_image":

            product.get(
                "coverImage",
                ""
            ),



        "date":

            unix_to_date(
                review.get(
                    "publishedAt"
                )
            ),



        "author":

            author.get(
                "firstName",
                ""
            ),



        "rating":

            content.get(
                "score"
            ),



        "text":

            comment,



        "text_length":

            len(
                comment
            ),



        "positive":

            content.get(
                "positive",
                ""
            ),



        "negative":

            content.get(
                "negative",
                ""
            ),



        "photos":

            photos,



        "videos":

            videos,



        "has_photos":

            bool(
                photos
            ),



        "has_videos":

            bool(
                videos
            ),



        "likes":

            useful,



        "dislikes":

            unuseful,



        "usefulness_score":

            useful - unuseful,



        "verified_purchase":

            review.get(
                "isItemPurchased",
                False
            ),



        "is_purchased":

            review.get(
                "isItemPurchased",
                False
            ),



        "order_type":

            review.get(
                "OrderType"
            ),



        "context_questions":

            content.get(
                "contextQuestions",
                []
            ),



        "variant":

            extract_variants(
                product
            )

    }

# ==================================================
# REVIEWS
# ==================================================

def extract_reviews(data):
    """
    Извлекает все отзывы
    из страниц API Ozon.

    Возвращает:
        list[dict]
    """

    reviews_result = []

    seen_ids = set()


    products = extract_products(
        data
    )


    pages = get_pages(
        data
    )


    total_pages = len(
        pages
    )



    statistics = {

        "pages": total_pages,

        "raw_reviews": 0,

        "duplicates": 0,

        "photos": 0,

        "videos": 0

    }



    for index, page in enumerate(
        pages,
        start=1
    ):


        if not isinstance(
            page,
            dict
        ):

            continue



        widget_states = page.get(
            "widgetStates",
            {}
        )



        if not isinstance(
            widget_states,
            dict
        ):

            continue




        for value in widget_states.values():


            block = safe_json_load(
                value
            )



            if not isinstance(
                block,
                dict
            ):

                continue



            reviews = block.get(
                "reviews"
            )



            if not isinstance(
                reviews,
                list
            ):

                continue



            statistics["raw_reviews"] += len(
                reviews
            )



            for raw_review in reviews:


                review_id = raw_review.get(
                    "uuid"
                )



                #
                # Защита от дублей
                #
                if review_id:


                    if review_id in seen_ids:

                        statistics["duplicates"] += 1

                        continue


                    seen_ids.add(
                        review_id
                    )



                review = parse_review(
                    raw_review,
                    products
                )



                if not review:

                    continue



                if review["has_photos"]:

                    statistics["photos"] += 1



                if review["has_videos"]:

                    statistics["videos"] += 1



                reviews_result.append(
                    review
                )



        print(
            f"Обработана страница {index}/{total_pages}"
        )



    print()

    print("=" * 60)

    print(
        "СТАТИСТИКА"
    )

    print("=" * 60)


    for key, value in statistics.items():

        print(
            f"{key}: {value}"
        )



    print()

    print(
        "Уникальных отзывов:",
        len(reviews_result)
    )


    return reviews_result





# ==================================================
# MAIN
# ==================================================

def main():


    print()

    print("=" * 60)

    print(
        "OZON REVIEW CONVERTER"
    )

    print("=" * 60)



    data = load_json(
        INPUT_FILE
    )



    reviews = extract_reviews(
        data
    )



    print()

    print(
        "Всего обработано отзывов:",
        len(reviews)
    )



    save_json(
        reviews,
        CLEAN_REVIEWS_FILE
    )



    print()

    print("=" * 60)

    print(
        "ГОТОВО"
    )

    print("=" * 60)




if __name__ == "__main__":

    main()