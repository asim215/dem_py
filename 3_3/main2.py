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


# Преобразование структуры history в строку str для пользователя
def history2str(hs) -> str:
    rs = ""
    for item in hs:
        rs += "дата: " + item.get("date", "-")
        rs += "\n#  текст: \"" + item.get("text", "-") + "\"\n"
    rs += "\n"
    return rs


# Информация для отладкий в терминал
def log(message):
    logging.info(f"{message.from_user.username}: {message.text}")


# Начало работы с ботом
@dp.message_handler(commands=['start', 'help'], state=StateMachine.user_info)
async def send_welcome(message: types.Message):
    # Исходные кнопки
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("/history")
    )
    await StateMachine.user_info.set()
    await message.reply("Привет.\n Я бот для тестирования, нахожусь\
        в разработке. (v0.0.1)", reply_markup=markup)
    await message.answer(f"Ваш id: {message.from_user.id}")
    log(message)


# Печать истории сообщений с пользователем
@dp.message_handler(commands=['history'], state=StateMachine.user_info)
async def history(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        history = data['history']
    await message.answer(f"Ваша история:\n{history2str(history)}")
    log(message)


# Эхо ввода и запись в историю
# Обработчик для каждого сообщения пользователя
@dp.message_handler(state=StateMachine.user_info)
async def echo(message: types.Message, state: FSMContext):
    # Эхо
    # await message.answer(message.text)
    # Запись истории сообщений
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
    log(message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
