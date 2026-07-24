from pathlib import Path


BASE_DIR = Path(__file__).parent.parent


OCR_FOLDER = BASE_DIR / "data" / "ocr"

TEMPLATE_FILE = (
    BASE_DIR /
    "prompts" /
    "prompt_template.txt"
)

OUTPUT_FILE = (
    BASE_DIR /
    "prompt_final.txt"
)



def collect_ocr_data():

    result = ""

    sku_folders = sorted(
        OCR_FOLDER.iterdir()
    )


    for index, sku_folder in enumerate(
        sku_folders
    ):


        if not sku_folder.is_dir():
            continue


        if index == 0:

            result += (
                f"\n\n"
                f"========================\n"
                f"МОЙ ТОВАР SKU: {sku_folder.name}\n"
                f"========================\n"
            )

        else:

            result += (
                f"\n\n"
                f"========================\n"
                f"КОНКУРЕНТ SKU: {sku_folder.name}\n"
                f"========================\n"
            )



        txt_files = sorted(
            sku_folder.glob("*.txt")
        )


        for txt_file in txt_files:


            text = txt_file.read_text(
                encoding="utf-8"
            )


            result += (
                f"\n\n"
                f"--- СЛАЙД {txt_file.stem} ---\n"
                f"{text}\n"
            )


    return result



def build_prompt():


    template = TEMPLATE_FILE.read_text(
        encoding="utf-8"
    )


    product_data = collect_ocr_data()


    final_prompt = template.replace(
        "{PRODUCT_DATA}",
        product_data
    )


    OUTPUT_FILE.write_text(
        final_prompt,
        encoding="utf-8"
    )


    print(
        "Создан:",
        OUTPUT_FILE
    )


    return final_prompt