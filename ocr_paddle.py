import os

# отключаем oneDNN ошибку Paddle
os.environ["FLAGS_use_onednn"] = "0"

from paddleocr import PaddleOCR
from pathlib import Path


BASE_DIR = Path(__file__).parent

IMAGE_FOLDER = BASE_DIR / "downloads"

RESULT_FILE = BASE_DIR / "result.txt"


ocr = PaddleOCR(
    lang="ru",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False
)


def main():

    images = list(
        IMAGE_FOLDER.glob("*.jpg")
    )


    if not images:
        print("Нет JPG файлов")
        return


    print(
        f"Найдено изображений: {len(images)}"
    )


    all_text = []


    for image in images:

        print(
            "Обработка:",
            image.name
        )


        result = ocr.predict(
            str(image)
        )


        text_lines = []


        for page in result:

            if "rec_texts" in page:

                for line in page["rec_texts"]:

                    text_lines.append(
                        line
                    )


        all_text.append(
            "\n".join(
                [
                    "=" * 40,
                    image.name,
                    "=" * 40,
                    *text_lines,
                    ""
                ]
            )
        )


    RESULT_FILE.write_text(
        "\n".join(all_text),
        encoding="utf-8"
    )


    print(
        "Готово:",
        RESULT_FILE
    )



if __name__ == "__main__":
    main()