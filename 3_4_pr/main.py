import re
import os
from aiogram.utils import callback_data

import database
from database import UsersTable, PizzaTable, OrdersTable, FileTable
from messages import get_message, main_keyboard

import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    InputMediaPhoto

from aiogram.contrib.fsm_storage.files import JSONStorage

# from messages import get_message
from settings import API_TOKEN

logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=API_TOKEN)

storage = JSONStorage("states.json")

dp = Dispatcher(bot, storage=storage)


class StateMachine(StatesGroup):
    main = State()
    registered = State()
    register_waiting_phone = State()
    register_waiting_email = State()
    register_waiting_address = State()
    order_waiting_count = State()
    order_waiting_address = State()
    order_waiting_accept = State()
    order_in_work = State()


def log(message: types.Message):
    logging.info(f"{message.from_user.username}: {message.text}")


async def send_photo(message, filename, caption=None, reply_markup=None):
    file_id = FileTable.get_file_id_by_file_name(filename)
    if file_id is None:
        # upload_file
        with open(filename, 'rb') as photo:
            result = await message.answer_photo(
                photo,
                caption=caption,
                reply_markup=reply_markup
            )
            file_id = result.photo[0].file_id
            FileTable.create(telegram_file_id=file_id, file_name=filename)
    else:
        await bot.send_photo(
            message.from_user.id,
            file_id,
            caption=caption,
            reply_markup=reply_markup
        )


async def send_media_group(
        message, filenames, aption=None, reply_markup=None):
    files = []
    for filename in filenames:
        file_id = FileTable.get_file_id_by_file_name(filename)
        if file_id is None:
            with open(filename, 'rb') as photo:
                files.append(InputMediaPhoto(photo, caption))
        else:
            files.append(InputMediaPhoto(file_id, caption))

    await bot.send_media_group(
        message.from_user.id,
        files
    )


async def get_files_pizza():
    return os.listdir("data/pizza/")


# Начальное состояние
@dp.message_handler(commands=['start', 'help'], state="*")
async def send_welcome(message: types.Message):
    telegram_id = message.from_user.id
    user = UsersTable.get_or_none(telegram_id=telegram_id)

    if user is None:
        await StateMachine.register_waiting_phone.set()
        await message.reply(get_message("hello"))
    else:
        await StateMachine.registered.set()
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)\
            .add("Войти", "Удалить аккаунт")
        await message.reply(get_message("registered"), reply_markup=markup)
    log(message)


# Отправка меню в виде галереи фото
@dp.message_handler(commands='mediagroup', state="*")
async def send_mediagroup_handler(message: types.Message):
    await send_media_group(message,
                           filenames=get_files_pizza(),
                           # filenames=["data/pizza_1.jpg", "data/pizza_2.jpg", "data/pizza_3.jpg"],
                           caption="TEXT")
    log(message)


# Вход или удаление зарегистрированного пользователя
@dp.message_handler(state=StateMachine.registered)
async def handle_registered(message: types.Message, state: FSMContext):
    if message.text == "Удалить аккаунт":
        # Удаление пользователя из БД
        telegram_id = message.from_user.id
        UsersTable.delete_user_by_telegram_id(telegram_id=telegram_id)
        # Регистрация нового пользователя
        await StateMachine.register_waiting_phone.set()
        await message.reply(get_message("hello"))
    else:
        # Успешный вход
        await state.finish()
        await StateMachine.main.set()
        await message.answer(get_message("enter_ok"), reply_markup=main_keyboard)
    log(message)


# Добавление телефона
@dp.message_handler(state=StateMachine.register_waiting_phone)
async def handle_phone(message: types.Message, state: FSMContext):
    if re.fullmatch("[0-9]{10,}", message.text):
        async with state.proxy() as data:
            data["phone"] = message.text
        await message.reply(get_message("phone_ok"))
        await StateMachine.register_waiting_email.set()
    else:
        await message.reply(get_message("phone_bad"))
    log(message)


# Добавление email
@dp.message_handler(state=StateMachine.register_waiting_email)
async def handle_email(message: types.Message, state: FSMContext):
    if re.fullmatch(".*@.*", message.text):
        async with state.proxy() as data:
            data["email"] = message.text
        markup = ReplyKeyboardMarkup(resize_keyboard=True).add("Пропустить")
        await message.reply(get_message("email_ok"), reply_markup=markup)
        await StateMachine.register_waiting_address.set()
    else:
        await message.reply(get_message("email_bad"))
    log(message)


# Добавление адреса
@dp.message_handler(state=StateMachine.register_waiting_address)
async def handle_address(message: types.Message, state: FSMContext):
    if message.text != "":
        async with state.proxy() as data:
            data["address"] = message.text if message.text != "Пропустить" else "Не указан"
            user_info = data
        await message.reply(get_message("address_ok"), reply_markup=main_keyboard)

        # Добавляем пользователя в таблицу
        UsersTable.add_user(
            name=f"{message.from_user.first_name} {message.from_user.last_name}",
            telegram_id=message.from_user.id,
            phone=user_info["phone"],
            email=user_info["email"],
            address=user_info["address"]
        )

        await state.finish()
        await StateMachine.main.set()
    else:
        await message.reply(get_message("address_bad"))
    log(message)


# Обработка главного состояния
@dp.message_handler(state=StateMachine.main)
async def main_state_handler(message: types.Message, state: FSMContext):
    if message.text == "Меню":
        # Вывести меню
        for pizza in PizzaTable.get_menu():
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("Заказать",
                       callback_data=f"order_pizza_{pizza.pizza_id}"))

            await send_photo(
                message,
                f'data/pizza/{pizza.pizza_id}.jpg',
                caption=get_message("pizza_show",
                                    name=pizza.name,
                                    type=pizza.type,
                                    desc=pizza.desc,
                                    price=pizza.price),
                reply_markup=markup
            )

    elif message.text == "Заказ":
        pass
    log(message)


# Начало заказа выбранной пиццы
@dp.callback_query_handler(text_startswith="order_pizza_", state=StateMachine.main)
async def order_pizza_handler(call: types.CallbackQuery, state: FSMContext):
    pizza_id = call.data.split('_')[2]
    print("\n-----inside pizza handler", pizza_id)
    
    async with state.proxy() as data:
        data["order_pizza_id"] = pizza_id

    pizza: PizzaTable = PizzaTable.get(pizza_id=pizza_id)
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

    markup.add("отменить")
    markup.add("1", "2", "3", "4", "5", "10", "15")

    await call.message.answer(get_message("order_get_count", name=pizza.name), reply_markup=markup)
    await StateMachine.order_waiting_count.set()
    await call.answer()


# Получить количество
@dp.message_handler(state=StateMachine.order_waiting_count)
async def order_waiting_count_handler(message: types.Message, state: FSMContext):
    if message.text == "отменить":
        # Вернуться в начало
        await state.finish()
        await StateMachine.main.set()
    elif re.fullmatch("[0-9]{1,2}", message.text):
        # Извлечение количества
        count = int(message.text)
        current_address = UsersTable.get(telegram_id=message.from_user.id).address
        async with state.proxy() as data:
            data["order_count"] = count
            data["order_address"] = current_address
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add("отменить", "подтвердить")
        await message.answer(get_message("order_get_address", address=current_address), reply_markup=markup)
        await StateMachine.order_waiting_address.set()
    log(message)


@dp.message_handler(state=StateMachine.order_waiting_address)
async def order_waiting_address_handler(message: types.Message, state: FSMContext):
    if message.text == "отменить":
        # Возврат в начальное состояние
        await state.finish()
        await StateMachine.main.set()
        return
    elif message.text != "подтвердить":
        # Сохранить новый адрес
        async with state.proxy() as data:
            data["order_address"] = message.text

    async with state.proxy() as data:
        address = data["order_address"]
        count = data["order_count"]
        pizza_id = data["order_pizza_id"]

    pizza: PizzaTable = PizzaTable.get(pizza_id=pizza_id)
    # Итого к оплате
    price = count * pizza.price
    async with state.proxy() as data:
        data["order_price"] = price
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("отменить", "подтвердить")

    await message.answer(
        get_message("order_accept", name=pizza.name, count=count, price=price, address=address),
        reply_markup=markup)

    await StateMachine.order_waiting_accept.set()
    log(message)


# Подтверждение заказа
@dp.message_handler(state=StateMachine.order_waiting_accept)
async def order_waiting_accept_handler(message: types.Message, state: FSMContext):
    if message.text == "отменить":
        await state.finish()
        await StateMachine.main.set()
        return
    elif message.text == "подтвердить":
        # Отправить заказ в работу
        async with state.proxy() as data:
            address = data["order_address"]
            count = data["order_count"]
            pizza_id = data["order_pizza_id"]
            price = data["order_price"]
        
        order = OrdersTable.create(
            user_id=UsersTable.get(telegram_id=message.from_user.id).user_id,
            pizza_id=pizza_id,
            pizza_count=count,
            address=address,
            price=price,
            status="in_work"
        )
        async with state.proxy() as data:
            data["order_id"] = order.order_id
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add("Получено")
        await message.answer(get_message("order_in_work", order_number=order.order_id), reply_markup=markup)
        await StateMachine.order_in_work.set()
    log(message)


# Подтверждение получения
@dp.message_handler(state=StateMachine.order_in_work)
async def order_in_work_handler(message: types.Message, state: FSMContext):
    if message.text == "Получено":
        # Заказ доставлен клиенту
        async with state.proxy() as data:
            order_id = data["order_id"]
        OrdersTable.set_order_done(order_id)
        await state.finish()
        await StateMachine.main.set()
        await message.answer(get_message("order_done"), reply_markup=main_keyboard)
        return
    else:
        await message.answer(get_message("order_failed"))
    log(message)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
