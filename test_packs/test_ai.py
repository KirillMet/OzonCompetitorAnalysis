from ai.gpt_request import send_request



print(
    "Запуск AI анализа..."
)



answer = send_request()



print(
    "\nОтвет:\n"
)


print(
    answer[:2000]
)


print(
    "\nГотово"
)