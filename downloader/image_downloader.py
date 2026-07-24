from pathlib import Path
import requests


BASE_DIR = Path(__file__).parent.parent


IMAGES_DIR = BASE_DIR / "data" / "images"



def download_images(cards):

    for sku, urls in cards.items():

        sku_folder = IMAGES_DIR / sku

        sku_folder.mkdir(
            parents=True,
            exist_ok=True
        )


        for index, url in enumerate(urls, start=1):

            filename = (
                sku_folder /
                f"{index:02}.jpg"
            )


            response = requests.get(url)


            response.raise_for_status()


            with open(filename, "wb") as file:
                file.write(response.content)


            print(
                f"{sku}: скачан {filename.name}"
            )