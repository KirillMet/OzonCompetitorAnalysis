from pathlib import Path


BASE_DIR = Path(__file__).parent.parent


def parse_links(file_path=None):

    if file_path is None:
        file_path = BASE_DIR / "input" / "links.txt"


    cards = {}

    current_sku = None


    with open(file_path, "r", encoding="utf-8") as file:

        for line in file:

            line = line.strip()


            if not line:
                continue


            # SKU
            if not line.startswith("http"):

                current_sku = line
                cards[current_sku] = []


            # ссылка
            else:

                if current_sku:
                    cards[current_sku].append(line)


    return cards