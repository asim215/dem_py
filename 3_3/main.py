"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup,\
    ReplyKeyboardMarkup, KeyboardButton
from settings import API_TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    markup = ReplyKeyboardMarkup().add(
        KeyboardButton("Main Button")
    )
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.", reply_markup=markup)
    logging.info(f"{message.from_user.username}: {message.text}")


# @dp.message_handler(regexp='(^cat[s]?$|puss)')
@dp.message_handler(regexp='(^dog[s|e]?$)')
async def doge(message: types.Message):
    with open('data/doge.jpg', 'rb') as photo:
        '''
        # Old fashioned way:
        await bot.send_photo(
            message.chat.id,
            photo,
            caption='Cats are here 😺',
            reply_to_message_id=message.message_id,
        )
        '''
        await message.reply_photo(photo, caption="Doge is here!")
        logging.info(f"{message.from_user.username}: {message.text}")


@dp.message_handler()
async def echo(message: types.Message):

    markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Кнопка А", callback_data="bt_a"),
        InlineKeyboardButton("Кнопка Б", callback_data="bt_b"),
        InlineKeyboardButton("Кнопка C", callback_data="jbt_1")
    )
    await message.answer(message.text, reply_markup=markup)
    logging.info(f"MYINFO{message.from_user.username}: {message.text}")


@dp.callback_query_handler(text_startswith="bt_")
async def bt_pressed(call: types.CallbackQuery):
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(
        "Кнопка GА",
        "Кнопка GБ",
        KeyboardButton("Button GC")
    )
    logging.info(f"MYINFO{call.from_user.username}: {call.data}")
    await call.message.answer(text=f"You pressed {call.data}", reply_markup=markup)
    await call.answer()


@dp.callback_query_handler(text_startswith="jbt_")
async def bt_pressed(call: types.CallbackQuery):
    markup = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("Button *"*100)
    )
    markup.row(
        KeyboardButton("ROW00"),
        KeyboardButton("ROW01")
    )
    # markup.row_width(2)
    markup.insert("test"*100)
    logging.info(f"MYINFO{call.from_user.username}: {call.data}")
    await call.message.answer(text=f"You pressed {call.data}", reply_markup=markup)
    await call.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)