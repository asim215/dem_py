# Модификация эхо бота
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup,\
    ReplyKeyboardMarkup, KeyboardButton
from settings import API_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# Логи в консоль
# - Сообщения
def log_m(msg):
    logging.info(f"{msg.from_user.username}: {msg.text}")


# - Вызов
def log_c(call):
    logging.info(f"Кнопка нажата {call.from_user.username}: {call.data}")


# Начало
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("Главная кнопка")
    )
    await message.reply("Привет. Это Эхобот. Созданный с помощью aiogram.",
                        reply_markup=markup)
    log_m(message)


# Вывод изображения собаки
# Отлавливает через регулярное выражение
@dp.message_handler(regexp='(^dog[s|e]?$)')
async def doge(message: types.Message):
    with open('data/doge.jpg', 'rb') as photo:
        await message.reply_photo(photo, caption="Собачка здесь!")
        log_m(message)


# Эхо
@dp.message_handler()
async def echo(message: types.Message):
    # Добавление кнопок к эхо сообщению
    markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Кнопка А", callback_data="bt_a"),
        InlineKeyboardButton("Кнопка Б", callback_data="bt_b"),
        InlineKeyboardButton("Кнопка J1", callback_data="jbt_1"),
        InlineKeyboardButton("Кнопка J2", callback_data="jbt_2"),
    )
    await message.answer(message.text, reply_markup=markup)
    log_m(message)


# Реакция на нажатие кнопок bt
@dp.callback_query_handler(text_startswith="bt_")
async def bt_pressed(call: types.CallbackQuery):
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(
        # Задание глобальной кноки с помощью текста
        "Кнопка GА",
        "Кнопка GБ",
        # С помощью конструктора KB
        KeyboardButton("Button GC")
    )
    log_c(call)
    await call.message.answer(text=f"Вы нажали {call.data}", reply_markup=markup)
    await call.answer()


# Реакция на нажатие кнопок jbt
@dp.callback_query_handler(text_startswith="jbt_")
async def jbt_pressed(call: types.CallbackQuery):
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(
        # Кнопка с большим количеством текста
        KeyboardButton("МногоТекста"*100)
    )
    # Таблица 3х3 из 3 строк и 3 столбцов кнопок
    markup.row(
        KeyboardButton("Row00"),
        KeyboardButton("Row01"),
        KeyboardButton("Row02"),
    )
    markup.row(
        KeyboardButton("Row10"),
        KeyboardButton("Row11"),
        KeyboardButton("Row12"),
    )
    markup.row(
        KeyboardButton("Row20"),
        KeyboardButton("Row21"),
        KeyboardButton("Row22"),
    )
    log_c(call)
    await call.message.answer(text=f"Вы нажали {call.data}", reply_markup=markup)
    await call.answer()


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)