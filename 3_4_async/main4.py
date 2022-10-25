import asyncio, time, random

messages = ("Ингридиенты ссыпаются на плиту", "Пицца жарится", "Пицца готова")

async def hello(delay: int = 30, message: str = "hello"):
    # await asyncio.sleep(delay)
    for message in messages:
        print(message)
        await asyncio.sleep(3)
    print(f"Задержка: {delay}, Сообщение: {message}")
    return {"delay": delay}


async def main():
    after_five_minutes = asyncio.Task(hello())
    for i in range(1, 6):
        print(f"Море волнуется {i}")
        await asyncio.sleep(1)
    await after_five_minutes
    print("Задачи выполнены")


if __name__ == "__main__":
    asyncio.run(main())