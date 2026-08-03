import asyncio



async def open_product(
        page,
        product_url
):

    print()
    print("Открываю карточку товара...")
    print()


    #
    # Переходим на товар
    #
    await page.goto(
        product_url,
        wait_until="domcontentloaded",
        timeout=60000
    )


    #
    # Ждем загрузку динамических блоков Ozon
    #
    await asyncio.sleep(
        5
    )


    print(
        "Карточка готова к работе."
    )