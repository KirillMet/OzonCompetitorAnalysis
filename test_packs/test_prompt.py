from prompt_builder.builder import build_prompt


print(
    "Формирование промта..."
)


prompt = build_prompt()


print(
    "\nПервые 1000 символов:\n"
)


print(
    prompt[:1000]
)


print(
    "\nГотово"
)