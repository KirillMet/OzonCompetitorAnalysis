import json


FILE = r"C:\OzonDownloader\reviews_raw.json"


with open(FILE, encoding="utf-8") as f:
    data = json.load(f)


for page in data:

    widgets = page.get(
        "widgetStates",
        {}
    )

    for key, value in widgets.items():

        if "webListReviews" in key:

            print("=" * 80)
            print(key)

            widget = json.loads(value)


            print(
                widget.keys()
            )


            print(
                json.dumps(
                    widget,
                    ensure_ascii=False,
                    indent=2
                )[:5000]
            )

            exit()