# Запускатор бота
from aiogram_test_bot.bot import run_bot
# Модель
from model import get_intent

# Запуск бота
run_bot(get_intent)