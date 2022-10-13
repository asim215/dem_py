import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup,\
    ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.files import JSONStorage

from settings import API_TOKEN

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = JSONStorage("states.json")
dp = Dispatcher(bot, storage=storage)


class StateMachine(StatesGroup):
    user_info = State()


def str_history(hs) -> str:
    rs = ""
    for item in hs:
        rs += "дата: " + item.get("date", "-")
        rs += "\n#  текст: \"" + item.get("text", "-") + "\"\n"
    rs += "\n"
    return rs


@dp.message_handler(commands=['start', 'help'], state=StateMachine.user_info)
async def send_welcome(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("/history")
    )
    await StateMachine.user_info.set()
    await message.reply("Hi!\nIt is a testing BOT. It is in development.",
                        reply_markup=markup)
    await message.answer(f"Your id is {message.from_user.id}")
    logging.info(f"{message.from_user.username}: {message.text}")


@dp.message_handler(commands=['history'], state=StateMachine.user_info)
async def history(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        history = data['history']

    # await message.answer(f"Ваша история:\n {' '.join(history)}")
    # await message.answer(f"Ваша история:\n {history}")
    # await message.answer(f"Ваша история:\n {[str() for item in history] history}")
    await message.answer(f"Ваша история:\n{str_history(history)}")
    logging.info(f"{message.from_user.username}: {message.text}")


@dp.message_handler(state=StateMachine.user_info)
async def echo(message: types.Message, state: FSMContext):
    await message.answer(message.text)
    async with state.proxy() as data:
        if "history" not in data:
            data["history"] = []
        # data["history"].append(message.text)
        data["history"].append(
            {
                # "user_id": message.from_user.id,
                "date": str(message.date),
                "text": message.text,
            }
        )
    logging.info(f"{message.from_user.username}: {message.text}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)