from pathlib import Path
import time
import json
import re


from parser.link_parser import parse_links
from downloader.image_downloader import download_images
from ocr.ocr_processor import process_ocr
from prompt_builder.builder import build_prompt
from ai.gpt_request import send_request
from excel_creator.excel_generator import create_excel
from result_creator.result_exporter import export_results



BASE_DIR = Path(__file__).parent



def check_file(path, name):

    if not path.exists():

        raise Exception(
            f"{name} не создан: {path}"
        )



def extract_json(text):

    """
    Поиск JSON внутри ответа GPT.
    GPT иногда добавляет текст до/после JSON.
    """

    # ищем объект JSON
    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL
    )


    if not match:

        return None


    json_text = match.group()


    try:

        return json.loads(
            json_text
        )

    except json.JSONDecodeError:

        return None




def save_json(data):

    json_file = (
        BASE_DIR /
        "response.json"
    )


    with open(
        json_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


    return json_file




def main():


    start_time = time.time()



    print("=" * 50)
    print("ЗАПУСК Ozon AI Analyzer")
    print("=" * 50)



    # ==============================
    # 1. Парсинг ссылок
    # ==============================


    print("\n[1/8] Парсинг ссылок...")


    cards = parse_links()


    if not cards:

        raise Exception(
            "Не найдены карточки"
        )


    print(
        f"Найдено SKU: {len(cards)}"
    )


    for sku, links in cards.items():

        print(
            sku,
            "-",
            len(links),
            "фото"
        )



    # ==============================
    # 2. Скачать изображения
    # ==============================


    print("\n[2/8] Скачивание изображений...")


    download_images(cards)


    images_folder = (
        BASE_DIR /
        "data" /
        "images"
    )


    check_file(
        images_folder,
        "Папка изображений"
    )


    print(
        "Загрузка изображений завершена"
    )



    # ==============================
    # 3. OCR
    # ==============================


    print("\n[3/8] Распознавание текста OCR...")


    process_ocr()


    ocr_folder = (
        BASE_DIR /
        "data" /
        "ocr"
    )


    check_file(
        ocr_folder,
        "Папка OCR"
    )


    print(
        "OCR завершен"
    )



    # ==============================
    # 4. Создание промта
    # ==============================


    print("\n[4/8] Формирование промта...")


    build_prompt()


    prompt_file = (
        BASE_DIR /
        "prompt_final.txt"
    )


    check_file(
        prompt_file,
        "Prompt"
    )


    print(
        "Prompt создан"
    )



    # ==============================
    # 5. GPT
    # ==============================


    print("\n[5/8] Анализ GPT...")


    send_request()


    response_file = (
        BASE_DIR /
        "response.txt"
    )


    check_file(
        response_file,
        "Ответ GPT"
    )


    print(
        "Ответ GPT получен"
    )



    # ==============================
    # 6. Проверка JSON
    # ==============================


    print("\n[6/8] Проверка JSON...")


    with open(
        response_file,
        "r",
        encoding="utf-8"
    ) as file:

        response_text = file.read()



    json_data = extract_json(
        response_text
    )



    if json_data is None:


        print(
            "JSON не найден."
        )

        print(
            "Excel создание пропущено."
        )


    else:


        json_file = save_json(
            json_data
        )


        print(
            "JSON создан:",
            json_file
        )



    # ==============================
    # 7. Excel
    # ==============================


    if json_data is not None:


        print("\n[7/8] Создание Excel...")


        create_excel(
            json_data
        )


        print(
            "Excel создан"
        )


    else:


        print(
            "\n[7/8] Excel пропущен"
        )



    print(
        "\nАнализ завершен"
    )


    print(
        "Время выполнения:",
        round(
            time.time() - start_time,
            2
        ),
        "сек."
    )

    # 8. Сохранение результата

    print("\n[8/8] Архивация результатов...")


    export_results()


    print(
        "Архивация завершена"
    )



if __name__ == "__main__":

    main()