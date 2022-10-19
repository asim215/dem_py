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
# storage = MemoryStorage() 
dp = Dispatcher(bot, storage=storage)


class StateMachine(StatesGroup):
    q_started = State()


data_q = [
    {
        "text": "Вопрос 1",
        "answers": ["R10", "R11", "R12", "R13"]
    },
    {
        "text": "Вопрос 2",
        "answers": ["R20", "R21", "R22"]
    },
    {
        "text": "Вопрос 3",
        "answers": ["R30", "R31", "R32", "R33", "R34"]
    },
]


# 
def get_question_text(id):
    return data_q[id].get("text")


def gen_answers_markup(id):
    markup = InlineKeyboardMarkup()
    for i in range(len(data_q[id].get("answers"))):
        answer_t = data_q[id].get("answers")[i]
        markup.insert(InlineKeyboardButton(answer_t, callback_data=f"answer_{i}"))
    return markup


# Информация для отладкий в терминал
def log(message):
    logging.info(f"{message.from_user.username}: {message.text}")


# Начало работы с ботом
@dp.message_handler(commands=['start', 'help'], state="*")
async def send_welcome(message: types.Message):
    # Исходные кнопки
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
        KeyboardButton("Начать"),
        KeyboardButton("Позже"),
    )
    await message.reply("Привет.\n Я предлагаю вам пройти опрос.", reply_markup=markup)
    log(message)


@dp.message_handler(text="Начать", state="*")
async def start_quest(message: types.Message, state: FSMContext):
    await StateMachine.q_started.set()
    async with state.proxy() as data:
        data["current_question"] = 0
        data["answers"] = []

    await message.answer(get_question_text(0), reply_markup=gen_answers_markup(id))


# Обработка ответов
@dp.callback_query_handler(text_startswith="answer_", state=StateMachine.q_started)
async def bt_pressed(call: types.CallbackQuery, state: FSMContext):
    answer = int(call.data.split('_')[1])
    await call.message.edit_reply_markup(InlineKeyboardMarkup())
    async with state.proxy() as data:
        data["current_question"] += 1
        current_question = data["current_question"]
        data["answers"].append(answer)

    if current_question < len(data_q):
        # await call.message.answer()
        await call.message.answer(get_question_text(current_question),
                                  reply_markup=gen_answers_markup(current_question))
    else:
        async with state.proxy() as data:
            answers = data["answers"]
        print(f"User {call.form_user.username}: {answers}")
        await state.finish()
        markup = ReplyKeyboardMarkup().add(
            KeyboardButton("F")
        )
        # await call.message.answer("Thanks", reply_markup=markup)
        # await call.message.answer("Thanks", reply_markup=InlineKeyboardMarkup())
        await call.message.answer("Thanks", reply_markup=markup())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
