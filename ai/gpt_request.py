from pathlib import Path

from openai import OpenAI

from config import API_KEY



BASE_DIR = Path(__file__).parent.parent


PROMPT_FILE = (
    BASE_DIR /
    "prompt_final.txt"
)


RESPONSE_FILE = (
    BASE_DIR /
    "response.txt"
)



client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.vsegpt.ru/v1"
)



def send_request():


    if not PROMPT_FILE.exists():

        raise FileNotFoundError(
            f"Нет файла: {PROMPT_FILE}"
        )



    prompt = PROMPT_FILE.read_text(
        encoding="utf-8"
    )



    print(
        "Отправляем запрос в GPT..."
    )



    response = client.chat.completions.create(

        model="openai/gpt-4o-mini",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0
    )



    answer = (
        response
        .choices[0]
        .message
        .content
    )



    RESPONSE_FILE.write_text(
        answer,
        encoding="utf-8"
    )


    print(
        "Ответ сохранен:",
        RESPONSE_FILE
    )


    return answer