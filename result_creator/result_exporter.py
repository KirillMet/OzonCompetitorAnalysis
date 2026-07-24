from pathlib import Path
import shutil
from datetime import datetime


BASE_DIR = Path(__file__).parent.parent


RESULT_DIR = (
    BASE_DIR /
    "RESULT"
)



FILES = [

    (
        "result.txt",
        "1_resultOCR.txt"
    ),

    (
        "prompt_final.txt",
        "2_prompt_final.txt"
    ),

    (
        "response.txt",
        "3_response.txt"
    ),

    (
        "analysis.xlsx",
        "4_analysis.xlsx"
    )

]



def create_result_folder():

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    folder = (
        RESULT_DIR /
        timestamp
    )

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return folder



def copy_results():

    result_folder = create_result_folder()


    print(
        "\nСоздание архива результата..."
    )


    for source_name, target_name in FILES:


        source = (
            BASE_DIR /
            source_name
        )


        if not source.exists():

            print(
                f"Пропуск: {source_name} не найден"
            )

            continue



        target = (
            result_folder /
            target_name
        )


        shutil.copy2(
            source,
            target
        )


        print(
            f"Скопирован: {source_name} -> {target_name}"
        )


    print(
        "\nРезультаты сохранены:"
    )

    print(
        result_folder
    )



def export_results():

    copy_results()



if __name__ == "__main__":

    export_results()