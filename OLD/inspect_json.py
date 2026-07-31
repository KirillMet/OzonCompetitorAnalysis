import json
from datetime import datetime


INPUT_FILE = r"C:\OzonDownloader\reviews_raw.json"
OUTPUT_FILE = r"C:\OzonDownloader\reviews_clean.json"


# ==================================================
# DATE
# ==================================================

def unix_to_date(ts):

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
# LOAD / SAVE
# ==================================================

def load_json(path):

    print(
        f"Загрузка файла:\n{path}"
    )

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)


    print(
        f"Тип данных: {type(data).__name__}"
    )


    if isinstance(data, list):

        print(
            f"Страниц в файле: {len(data)}"
        )


    return data




def save_json(data, path):

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )


    print(
        f"Сохранено:\n{path}"
    )



# ==================================================
# PRODUCTS
# ==================================================

def extract_products(data):

    products = {}


    pages = (
        data
        if isinstance(data, list)
        else [data]
    )


    for page in pages:


        widget_states = page.get(
            "widgetStates",
            {}
        )


        if not isinstance(widget_states, dict):
            continue



        for value in widget_states.values():


            if not isinstance(value, str):

                continue


            if '"products"' not in value:

                continue



            try:

                obj = json.loads(
                    value
                )


                products.update(
                    obj.get(
                        "products",
                        {}
                    ) or {}
                )


            except Exception:

                continue



    print(
        f"Найдено вариантов товаров: {len(products)}"
    )


    return products




# ==================================================
# REVIEWS
# ==================================================

def extract_reviews(data):


    reviews_result = []


    products = extract_products(
        data
    )


    pages = (
        data
        if isinstance(data, list)
        else [data]
    )


    total_pages = len(
        pages
    )



    for index, page in enumerate(
        pages,
        start=1
    ):


        widget_states = page.get(
            "widgetStates",
            {}
        )


        if not isinstance(widget_states, dict):

            continue



        for value in widget_states.values():


            if not isinstance(value, str):

                continue


            if '"reviews"' not in value:

                continue



            try:

                block = json.loads(
                    value
                )

            except Exception:

                continue



            reviews = block.get(
                "reviews",
                []
            )


            if not isinstance(reviews, list):

                continue



            for r in reviews:


                if not isinstance(r, dict):

                    continue



                content = r.get(
                    "content",
                    {}
                )


                if not isinstance(content, dict):

                    content = {}



                sku = r.get(
                    "itemId"
                )



                product = products.get(
                    str(sku)
                )



                variant = {}



                if isinstance(product, dict):


                    variants = product.get(
                        "variants",
                        []
                    )


                    if not isinstance(
                        variants,
                        list
                    ):

                        variants = []



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

                            variant[name] = value




                # =========================
                # PHOTOS SAFE
                # =========================

                photos_raw = content.get(
                    "photos",
                    []
                )


                if not isinstance(
                    photos_raw,
                    list
                ):

                    photos_raw = []



                photos = [

                    p.get(
                        "url"
                    )

                    for p in photos_raw

                    if isinstance(
                        p,
                        dict
                    )
                    and p.get(
                        "url"
                    )

                ]



                # =========================
                # VIDEOS SAFE
                # =========================

                videos_raw = content.get(
                    "videos",
                    []
                )


                if not isinstance(
                    videos_raw,
                    list
                ):

                    videos_raw = []



                videos = [

                    v.get(
                        "url"
                    )

                    for v in videos_raw

                    if isinstance(
                        v,
                        dict
                    )
                    and v.get(
                        "url"
                    )

                ]



                usefulness = r.get(
                    "usefulness",
                    {}
                )


                if not isinstance(
                    usefulness,
                    dict
                ):

                    usefulness = {}



                author = r.get(
                    "author",
                    {}
                )


                if not isinstance(
                    author,
                    dict
                ):

                    author = {}



                comment = content.get(
                    "comment",
                    ""
                )


                if not isinstance(
                    comment,
                    str
                ):

                    comment = ""



                context_questions = content.get(
                    "contextQuestions",
                    []
                )


                if not isinstance(
                    context_questions,
                    list
                ):

                    context_questions = []



                review = {


                    "review_id":

                        r.get(
                            "uuid"
                        ),



                    "sku":

                        sku,



                    "product_name":

                        product.get(
                            "name",
                            ""
                        )
                        if isinstance(product, dict)
                        else "",



                    "product_image":

                        product.get(
                            "coverImage",
                            ""
                        )
                        if isinstance(product, dict)
                        else "",



                    "date":

                        unix_to_date(
                            r.get(
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

                        len(
                            photos
                        ) > 0,



                    "has_videos":

                        len(
                            videos
                        ) > 0,



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



                    "usefulness_score":

                        usefulness.get(
                            "useful",
                            0
                        )
                        -
                        usefulness.get(
                            "unuseful",
                            0
                        ),



                    "verified_purchase":

                        r.get(
                            "isItemPurchased",
                            False
                        ),



                    "is_purchased":

                        r.get(
                            "isItemPurchased",
                            False
                        ),



                    "order_type":

                        r.get(
                            "OrderType"
                        ),



                    "context_questions":

                        context_questions,



                    "variant":

                        variant

                }



                reviews_result.append(
                    review
                )



        print(
            f"Обработана страница {index}/{total_pages}"
        )



    return reviews_result




# ==================================================
# MAIN
# ==================================================

def main():


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



    print(
        f"\nНайдено отзывов: {len(reviews)}"
    )



    save_json(
        reviews,
        OUTPUT_FILE
    )



    print("=" * 60)

    print(
        "ГОТОВО"
    )

    print("=" * 60)




if __name__ == "__main__":

    main()