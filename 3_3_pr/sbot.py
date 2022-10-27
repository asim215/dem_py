# Бот с состояниями Finite State Machine
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.files import JSONStorage

from settings import API_TOKEN

logging.basicConfig(level=logging.DEBUG)


# Иницализация бота, диспетчера
bot = Bot(token=API_TOKEN)
storage = JSONStorage("states.json")
dp = Dispatcher(bot, storage=storage)


# Объявление состояний
class StateMachine(StatesGroup):
    main = State()
    password_create = State()
    password_check = State()
    history_show = State()
    history_clear = State()


# Преобразование структуры history в строку
def history2str(hs) -> str:
    rs = ""
    for item in hs:
        rs += "дата: " + item.get("date", "-")
        rs += "\n#  текст: \"" + item.get("text", "-") + "\"\n"
    rs += "\n"
    return rs


# Информация о сообщениях и состоянии в логах
async def log(message, state):
    logging.info(f"{message.from_user.username}: {message.text}: {await state.get_state()}")


# Начало работы с ботом
@dp.message_handler(commands=['start', 'help'], state="*")
async def send_welcome(message: types.Message):
    # Глобальные кнопки
    markup_g = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("/history_show"),
        KeyboardButton("/history_clear"),
        KeyboardButton("/password_create"),
        KeyboardButton("/user_del"),
    )
    await message.reply(f"Привет, {message.from_user.username}.\nЯ эхо бот для тестирования состояний.",
                        reply_markup=markup_g)
    await message.answer(f"Ваш id: {message.from_user.id}")
    await StateMachine.main.set()
    await main_menu(message)


async def main_menu(message: types.Message):
    # Доступные команды
    commands = [
        "Показать историю сообщений: /history_show",
        "Очистить историю сообщений: /history_clear",
        "Создать новый пароль: /password_create",
        "Удалить данные пользователя: /user_del",
    ]
    str_com = "\n".join(commands)
    await message.answer(f"Пожалуйста введите или выберете команду:\n{str_com}")


# Начало создания нового пароля
@dp.message_handler(commands=['password_create'], state=StateMachine.main)
async def password_create(message: types.Message, state: FSMContext):
    # print("password_create")
    await message.answer("Пожалуйста введите новый пароль.")
    await StateMachine.password_create.set()
    await log(message, state)


# Сохранение нового пароля
@dp.message_handler(state=StateMachine.password_create)
async def password_save(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text
        await message.answer(f"Ваш пароль сохранен как: \"{message.text}\"")
    await StateMachine.main.set()
    await main_menu(message)
    await log(message, state)


# Начало печати истории сообщений с пользователем
@dp.message_handler(commands=['history_show'], state=StateMachine.main)
async def history_c(message: types.Message, state: FSMContext):
    await message.answer("Для вывода истории сообщений введите Ваш пароль.")
    await StateMachine.password_check.set()
    await log(message, state)


# Проверка пароля
@dp.message_handler(state=StateMachine.password_check)
async def password_check(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pd = data.get('password', None)
    if message.text == pd:
        await message.answer("Пароль введен корректно.")
        await StateMachine.history_show.set()
        await history_show(message, state)
    elif pd is None:
        await message.answer("Пароль не создан, необходимо создать пароль.")
        await password_create(message, state)
    else:
        await message.answer("Неправильный пароль.")
        await StateMachine.main.set()
        await main_menu(message)
    await log(message, state)


# Печать истории сообщений с пользователем
# @dp.message_handler(state=StateMachine.history_show)
async def history_show(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        history = data.get('history', None)
    if history is not None:
        await message.answer(f"Ваша история:\n{history2str(history)}")
    else:
        await message.answer("Ваша история сообщений пуста")
    await StateMachine.main.set()
    await main_menu(message)
    await log(message, state)


# Очиска истории с подтверждением пароля
@dp.message_handler(commands=['history_clear'], state=StateMachine.main)
async def history_clear(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        del data['history']
    await message.answer("Ваша история очищена.")
    await main_menu(message)
    await log(message, state)


# Удаление данных пользователя
@dp.message_handler(commands=['user_del'], state=StateMachine.main)
async def user_del(message: types.Message, state: FSMContext):
    await state.reset_data()
    await message.answer("Данные пользователя удалены")
    await main_menu(message)
    await log(message, state)


# Эхо ввода и запись в историю
# Обработчик для сообщений пользователя
@dp.message_handler(state=StateMachine.main)
async def echo(message: types.Message, state: FSMContext):
    # Эхо
    await message.answer(message.text)
    # Запись истории сообщений
    async with state.proxy() as data:
        if "history" not in data:
            data["history"] = []
        # Добавление даты и сообщения
        data["history"].append(
            {
                "date": str(message.date),
                "text": message.text,
            }
        )
    await log(message, state)


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
