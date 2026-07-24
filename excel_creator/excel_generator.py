from pathlib import Path
import json
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment


BASE_DIR = Path(__file__).parent.parent


JSON_FILE = (
    BASE_DIR /
    "response.json"
)


OUTPUT_FILE = (
    BASE_DIR /
    "analysis.xlsx"
)


def load_json():

    with open(
        JSON_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)



def create_excel(data):

    workbook = Workbook()

    sheet = workbook.active

    sheet.title = "Сравнение"


    # Ищем первый список объектов в JSON
    rows = None


    if isinstance(data, list):

        rows = data


    elif isinstance(data, dict):

        for value in data.values():

            if (
                isinstance(value, list)
                and len(value) > 0
                and isinstance(value[0], dict)
            ):

                rows = value
                break


    if rows is None:

        raise ValueError(
            "Не найден список объектов в JSON."
        )



    # Заголовки берутся автоматически из JSON
    headers = list(rows[0].keys())


    sheet.append(headers)



    # Жирный заголовок

    for cell in sheet[1]:

        cell.font = Font(
            bold=True
        )

        cell.alignment = Alignment(
            wrap_text=True,
            vertical="top"
        )



    # Заполняем строки

    for row in rows:

        excel_row = []


        for header in headers:

            value = row.get(
                header,
                ""
            )


            if isinstance(value, list):

                value = "\n\n".join(
                    str(item)
                    for item in value
                )


            elif isinstance(value, dict):

                value = json.dumps(
                    value,
                    ensure_ascii=False,
                    indent=2
                )


            elif value is None:

                value = ""


            excel_row.append(
                value
            )


        sheet.append(
            excel_row
        )



    # Перенос текста во всех ячейках

    for row in sheet.iter_rows():

        for cell in row:

            cell.alignment = Alignment(
                wrap_text=True,
                vertical="top"
            )
   

    # Автоматическая ширина столбцов

    for column_cells in sheet.columns:

        column_letter = (
            column_cells[0]
            .column_letter
        )


        max_length = 0


        for cell in column_cells:

            if cell.value is None:

                continue


            for line in str(cell.value).split("\n"):

                if len(line) > max_length:

                    max_length = len(line)



        sheet.column_dimensions[
            column_letter
        ].width = min(
            max(
                max_length + 3,
                20
            ),
            80
        )



    workbook.save(
        OUTPUT_FILE
    )


    print(
        "Excel создан:",
        OUTPUT_FILE
    )



def generate_excel():

    data = load_json()

    create_excel(
        data
    )



if __name__ == "__main__":

    generate_excel()