import json
import re


from storage.json_writer import save_json
from config import COMMENTS_IDS_FILE



UUID_PATTERN = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
    re.I
)



def search_review_ids(
    json_files
):
    """
    Поиск UUID отзывов.

    json_files:
        список JSON файлов с ответами API
    """

    print()

    print(
        "-" * 60
    )

    print(
        "Поиск UUID отзывов"
    )


    found_ids = set()



    for file_path in json_files:


        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)



        except Exception as e:

            print(
                "Ошибка чтения JSON:",
                file_path,
                e
            )

            continue



        #
        # Превращаем JSON в текст
        #
        text = json.dumps(
            data,
            ensure_ascii=False
        )


        #
        # Ищем UUID
        #
        ids = UUID_PATTERN.findall(
            text
        )


        for uid in ids:

            found_ids.add(
                uid
            )



    result = list(
        found_ids
    )



    print()

    print(
        f"Найдено UUID: {len(result)}"
    )



    for uid in result[:10]:

        print(
            uid
        )



    #
    # Сохраняем ID отзывов
    #
    save_json(
        result,
        COMMENTS_IDS_FILE
    )



    print()

    print(
        "UUID сохранены:"
    )

    print(
        COMMENTS_IDS_FILE
    )


    return result