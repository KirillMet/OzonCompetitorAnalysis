import json
import os


# ==================================================
# LISTENER
# ==================================================

async def add_comments_listener(
    page,
    comments_pages
):
    """
    Устанавливает перехват сетевых запросов Ozon.

    Все найденные API ответы добавляются
    в список comments_pages.
    """

    async def handle_response(response):

        url = response.url

        if (
            "entrypoint-api.bx/page/json/v2" in url
            and "reviews" in url
        ):

            print()
            print("=" * 80)
            print("НАЙДЕН COMMENTS API")
            print(url)
            print("=" * 80)


            try:

                data = await response.json()


                comments_pages.append(
                    {
                        "url": url,
                        "json": data
                    }
                )


                print(
                    "JSON добавлен"
                )


            except Exception as e:

                print(
                    f"Ошибка чтения JSON: {e}"
                )


    page.on(
        "response",
        handle_response
    )


    print(
        "Comments research listener установлен."
    )



# ==================================================
# SAVE
# ==================================================

def save_comments_pages(
    comments_pages,
    filename
):
    """
    Сохраняет пойманные API ответы в JSON.
    """


    try:

        os.makedirs(
            os.path.dirname(filename),
            exist_ok=True
        )


        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                comments_pages,
                f,
                ensure_ascii=False,
                indent=4
            )


        print()
        print(
            "JSON сохранен:"
        )
        print(
            filename
        )


    except Exception as e:

        print(
            f"Ошибка сохранения JSON: {e}"
        )