import asyncio, time, random


async def hello(delay: int, message: str):
    await asyncio.sleep(delay)
    print(f"Задержка: {delay}, Сообщение: {message}")
    return {"delay": delay}


async def main():
    tasks = tuple(asyncio.Task(hello(random.randint(1, 5), "hello")) for _ in range(10))

    # for task in tasks:
    #     await task

    # results = await asyncio.gather(*tasks)
    # print(f"Results: {results}")


    # tasks_on_wait = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    # await asyncio.sleep(1)
    # done, pending = tasks_on_wait
    #
    # for task in done:
    #     print(task.result())
    #
    # done_new, pending_new = await asyncio.wait(pending, timeout=1)
    #
    # for task in done_new:
    #     print(task.result())

    for task in asyncio.as_completed(tasks):
        print(await task)
    # task1 = asyncio.Task(hello(3, "hello"))
    # task2 = asyncio.Task(hello(2, "hello"))
    # task3 = asyncio.Task(hello(1, "hello"))

    # await task1
    # await task2
    # await task3

    print("Задачи выполнены")


if __name__ == "__main__":
    asyncio.run(main())