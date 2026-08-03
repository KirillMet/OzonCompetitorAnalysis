"""
==================================================
OZON SCROLL ACTION
==================================================

Управляет прокруткой страницы.

Не знает о:

✘ reviews
✘ comments
✘ JSON
✘ API


После каждого шага скролла
может вызвать внешний callback.

Используется pipeline:

scroll
 |
 v
review listener
 |
 v
after_scroll()
 |
 v
comment collector


==================================================
"""


import asyncio


from config import MAX_SCROLLS





async def scroll_page(
    page,
    get_items_count=None,
    after_scroll=None
):
    """
    Основной скроллер.

    Parameters
    ----------

    page:
        Playwright page


    get_items_count:
        функция проверки количества
        найденных элементов


    after_scroll:
        async callback,
        который вызывается
        после каждого шага


    """



    previous_count = 0


    empty_scrolls = 0





    for scroll_number in range(
        MAX_SCROLLS
    ):



        print()

        print(
            f"СКРОЛЛ #{scroll_number + 1}"
        )



        # ------------------------------------------
        # Ждем загрузку API после скролла
        # ------------------------------------------


        await page.mouse.wheel(

            0,

            1200

        )



        await page.wait_for_timeout(

            3000

        )




        # ------------------------------------------
        # Проверяем количество найденных страниц
        # ------------------------------------------


        current_count = 0



        if get_items_count:


            current_count = get_items_count()



        print(

            "Найдено API страниц:",

            current_count

        )





        # ------------------------------------------
        # CALLBACK
        # ------------------------------------------

        if after_scroll:


            try:


                await after_scroll()



            except Exception as e:


                print()

                print(
                    "Ошибка after_scroll:"
                )

                print(e)






        # ------------------------------------------
        # Проверка остановки
        # ------------------------------------------


        if current_count == previous_count:


            empty_scrolls += 1


        else:


            empty_scrolls = 0




        previous_count = current_count





        if empty_scrolls >= 5:


            print()

            print(
                "Новых данных нет."
            )


            break






        await asyncio.sleep(

            1

        )




    print()

    print(
        "Скролл завершен."
    )