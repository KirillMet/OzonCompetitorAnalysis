import requests
from pathlib import Path


# ===== НАСТРОЙКИ =====

BASE_DIR = Path(__file__).parent

URL_FILE = BASE_DIR / "urls.txt"

DOWNLOAD_FOLDER = BASE_DIR / "downloads"


# =====================


def load_urls():
    """
    Читаем список ссылок из txt
    """

    if not URL_FILE.exists():
        raise FileNotFoundError(
            "Файл urls.txt не найден"
        )

    with open(
        URL_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        urls = [
            line.strip()
            for line in file
            if line.strip()
        ]

    return urls



def create_folder():
    """
    Создает папку если ее нет
    """

    DOWNLOAD_FOLDER.mkdir(
        exist_ok=True
    )



def download_image(url, number):
    """
    Скачивание одного изображения
    """

    headers = {
        "User-Agent":
            "Mozilla/5.0"
    }


    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )


    response.raise_for_status()


    filename = (
        DOWNLOAD_FOLDER /
        f"{number}.jpg"
    )


    with open(
        filename,
        "wb"
    ) as file:

        file.write(
            response.content
        )


    print(
        f"Скачано: {filename.name}"
    )



def main():

    urls = load_urls()


    print(
        f"Найдено ссылок: {len(urls)}"
    )


    create_folder()


    for index, url in enumerate(
        urls,
        start=1
    ):

        try:

            download_image(
                url,
                index
            )


        except Exception as e:

            print(
                f"Ошибка {url}: {e}"
            )


    print("Готово")



if __name__ == "__main__":
    main()