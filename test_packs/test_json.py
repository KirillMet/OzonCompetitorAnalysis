from json_creator.json_extractor import create_json


print(
    "Извлечение JSON..."
)


data = create_json()


print(
    "Количество строк:",
    len(
        data["comparison_table"]
    )
)


print(
    "Готово"
)