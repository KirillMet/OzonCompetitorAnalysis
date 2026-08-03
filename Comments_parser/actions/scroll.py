"""
Простая прокрутка страницы Ozon.

Используется для загрузки отзывов в DOM.
"""

import asyncio

from config import (
    MAX_SCROLLS,
    SCROLL_DELTA,
    SCROLL_STEP_DELAY,
    SCROLL_PAGE_DELAY
)



async def scroll_page(page):


    print()

    print("=" * 60)
    print("Начинаю прокрутку страницы...")
    print("=" * 60)



    for i in range(
        MAX_SCROLLS
    ):


        print(
            f"Скролл {i+1}"
        )


        for _ in range(8):

            await page.mouse.wheel(
                0,
                SCROLL_DELTA
            )

            await asyncio.sleep(
                SCROLL_STEP_DELAY / 1000
            )


        await asyncio.sleep(
            SCROLL_PAGE_DELAY / 1000
        )



    print()

    print(
        "Прокрутка завершена."
    )