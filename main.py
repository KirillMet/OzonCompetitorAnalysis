from pathlib import Path
import time


from parser.link_parser import parse_links
from downloader.image_downloader import download_images
from ocr.ocr_processor import process_ocr
from prompt_builder.builder import build_prompt
from ai.gpt_request import send_request



BASE_DIR = Path(__file__).parent



def check_file(path, name):

    if not path.exists():

        raise Exception(
            f"{name} не создан: {path}"
        )



def main():


    start_time = time.time()


    print("=" * 50)
    print("ЗАПУСК Ozon AI Analyzer")
    print("=" * 50)



    # 1. Парсинг ссылок

    print("\n[1/5] Парсинг ссылок...")


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



    # 2. Скачивание изображений

    print("\n[2/5] Скачивание изображений...")


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



    # 3. OCR

    print("\n[3/5] Распознавание текста OCR...")


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



    # 4. Создание промта

    print("\n[4/5] Формирование промта...")


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



    # 5. GPT

    print("\n[5/5] Анализ GPT...")


    answer = send_request()


    response_file = (
        BASE_DIR /
        "response.txt"
    )


    check_file(
        response_file,
        "Ответ GPT"
    )


    print(
        "\nАнализ завершен"
    )


    print(
        "Время выполнения:",
        round(time.time() - start_time, 2),
        "сек."
    )



if __name__ == "__main__":

    main()