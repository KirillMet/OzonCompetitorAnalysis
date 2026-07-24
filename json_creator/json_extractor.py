from pathlib import Path
import json
import re


BASE_DIR = Path(__file__).parent.parent


INPUT_FILE = (
    BASE_DIR /
    "response.txt"
)


OUTPUT_FILE = (
    BASE_DIR /
    "response.json"
)



def extract_json(text):

    """
    Извлекает JSON из ответа GPT.
    Поддерживает JSON внутри ```json ... ```
    """

    # вариант с блоком ```json

    match = re.search(
        r"```json\s*(.*?)\s*```",
        text,
        re.DOTALL
    )


    if match:

        return match.group(1)



    # вариант без блока

    start = text.find("{")

    end = text.rfind("}")


    if start != -1 and end != -1:

        return text[start:end + 1]



    raise Exception(
        "JSON не найден в response.txt"
    )



def create_json():


    if not INPUT_FILE.exists():

        raise FileNotFoundError(
            f"Нет файла: {INPUT_FILE}"
        )



    text = INPUT_FILE.read_text(
        encoding="utf-8"
    )



    json_text = extract_json(
        text
    )



    try:

        data = json.loads(
            json_text
        )


    except json.JSONDecodeError as error:

        raise Exception(
            f"Ошибка JSON: {error}"
        )



    OUTPUT_FILE.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=4
        ),
        encoding="utf-8"
    )



    print(
        "JSON создан:",
        OUTPUT_FILE
    )


    return data



if __name__ == "__main__":

    create_json()