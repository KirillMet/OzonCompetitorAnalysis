import os

# отключаем oneDNN ошибку Paddle
os.environ["FLAGS_use_onednn"] = "0"


from pathlib import Path
from paddleocr import PaddleOCR


# корень проекта
BASE_DIR = Path(__file__).parent.parent


IMAGE_FOLDER = BASE_DIR / "data" / "images"

OCR_FOLDER = BASE_DIR / "data" / "ocr"



ocr = PaddleOCR(
    lang="ru",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False
)



def recognize_image(image_path):

    result = ocr.predict(
        str(image_path)
    )


    text_lines = []


    for page in result:

        if "rec_texts" in page:

            for line in page["rec_texts"]:

                text_lines.append(
                    line
                )


    return "\n".join(text_lines)



def process_ocr():


    if not IMAGE_FOLDER.exists():

        print(
            "Нет папки:",
            IMAGE_FOLDER
        )

        return



    sku_folders = sorted(
        IMAGE_FOLDER.iterdir()
    )


    for sku_folder in sku_folders:


        if not sku_folder.is_dir():
            continue



        print(
            "\nSKU:",
            sku_folder.name
        )



        output_folder = (
            OCR_FOLDER /
            sku_folder.name
        )


        output_folder.mkdir(
            parents=True,
            exist_ok=True
        )



        images = sorted(
            sku_folder.glob("*.jpg")
        )



        if not images:

            print(
                "Нет изображений"
            )

            continue



        for image in images:


            print(
                "Обработка:",
                image.name
            )


            text = recognize_image(
                image
            )



            output_file = (
                output_folder /
                f"{image.stem}.txt"
            )


            output_file.write_text(
                text,
                encoding="utf-8"
            )



            print(
                "Сохранено:",
                output_file
            )