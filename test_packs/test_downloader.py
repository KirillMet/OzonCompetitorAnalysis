from parser.link_parser import parse_links
from downloader.image_downloader import download_images


# Получаем ссылки из input/links.txt
cards = parse_links()


# Выводим что будем скачивать
print("\nНайденные карточки:")

for sku, links in cards.items():

    print(f"\nSKU: {sku}")

    for i, link in enumerate(links, 1):
        print(f"{i}. {link}")


print("\nНачинаем скачивание...\n")


# Запускаем загрузку
download_images(cards)


print("\nГотово!")