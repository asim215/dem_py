from .messages import get_message_text, main_keyboard

import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from aiogram.contrib.fsm_storage.files import JSONStorage

from .settings import API_TOKEN

logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=API_TOKEN)

storage = JSONStorage("states.json")

dp = Dispatcher(bot, storage=storage)

# get_intent_callback = lambda text: "intent_not_found"


# analog
def get_intent_callback(text):
    return "intent_not_found"


class StateMachine(StatesGroup):
    main_state = State()


# Start
@dp.message_handler(commands=['start', 'help'], state="*")
async def send_welcome(message: types.Message):
    await StateMachine.main_state.set()
    await message.reply(get_message_text("hello"), reply_markup=main_keyboard)

    logging.info(f"{message.from_user.username}: {message.text}")


# Обработка сообщений пользователя
@dp.message_handler(state=StateMachine.main_state)
async def main_state_handler(message: types.Message, state: FSMContext):
    # Передать сообщение пользователя и получить намерение
    intent = get_intent_callback(message.text)

    messages_from_intent = {
        "парковка": "intent_parking",
        "время": "intent_time",
        "забронировать": "intent_reservation",
        "услуги": "intent_services",
        "номера": "intent_rooms",
    }

    # Если намерение в присутствует в базе, то выдать текст сообщения
    if intent in messages_from_intent:
        await message.answer(get_message_text(messages_from_intent[intent]))
    else:
        # Иначе сообщение об отсутствии подходящего намерения
        await message.answer(get_message_text("intent_none"))

    logging.info(f"{message.from_user.username}: ({intent}) {message.text}")


# Запуск бота
def run_bot(_get_intent_callback):
    if _get_intent_callback is not None:
        global get_intent_callback
        get_intent_callback = _get_intent_callback
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    run_bot(get_intent_callback)