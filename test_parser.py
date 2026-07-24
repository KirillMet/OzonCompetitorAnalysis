from pathlib import Path
from parser.link_parser import parse_links


BASE_DIR = Path(__file__).parent


cards = parse_links(
    BASE_DIR / "input" / "links.txt"
)


for sku, links in cards.items():

    print("\nSKU:", sku)

    for i, link in enumerate(links, 1):
        print(i, link)