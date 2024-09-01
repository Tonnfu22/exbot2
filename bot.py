import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from dotenv import load_dotenv
import os
import requests

from pycoingecko import CoinGeckoAPI
from promocodes import validate_promo_code
from database import create_order, get_user
from keyboards import main_menu, crypto_menu

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

scheduler = AsyncIOScheduler()

cg = CoinGeckoAPI()
SUPPORTED_COINS = ['bitcoin', 'ethereum', 'ripple']  # Пример списка поддерживаемых монет

async def send_price_updates():
    users = [...]  # Получите пользователей из базы данных
    for user in users:
        for coin in SUPPORTED_COINS:
            price = cg.get_price(ids=coin, vs_currencies='usd')
            await bot.send_message(user.id, f"Текущий курс {coin.upper()} = ${price[coin]['usd']:.2f}")

scheduler.add_job(send_price_updates, IntervalTrigger(hours=1))
scheduler.start()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Добро пожаловать в криптовалютный обменник! Выберите опцию:", reply_markup=main_menu())

@dp.message_handler(commands=['buy'])
async def buy_crypto(message: types.Message):
    try:
        _, coin, amount, price = message.text.split()
        user_id = message.from_user.id
        amount = float(amount)
        price = float(price)
        create_order(user_id, coin, amount, price, 'buy')
        await message.reply(f"Заявка на покупку {amount} {coin.upper()} по цене ${price} размещена.")
    except ValueError:
        await message.reply("Ошибка в формате команды. Используйте /buy <монета> <количество> <цена>")

@dp.message_handler(commands=['sell'])
async def sell_crypto(message: types.Message):
    try:
        _, coin, amount, price = message.text.split()
        user_id = message.from_user.id
        amount = float(amount)
        price = float(price)
        create_order(user_id, coin, amount, price, 'sell')
        await message.reply(f"Заявка на продажу {amount} {coin.upper()} по цене ${price} размещена.")
    except ValueError:
        await message.reply("Ошибка в формате команды. Используйте /sell <монета> <количество> <цена>")

@dp.message_handler(commands=['lang'])
async def change_language(message: types.Message):
    lang = message.text.split()[1].strip()
    if lang in ['en', 'ru']:
        # Сохраните язык пользователя в базе данных
        await message.reply(f"Язык изменен на {lang}")
    else:
        await message.reply("Поддерживаются только языки: en, ru.")

@dp.callback_query_handler(lambda c: c.data.startswith('crypto_'))
async def crypto_handler(callback_query: types.CallbackQuery):
    coin = callback_query.data.split('_')[1]
    price = cg.get_price(ids=coin, vs_currencies='usd')
    if price:
        await bot.send_message(callback_query.from_user.id, f"Текущий курс {coin.upper()} = ${price[coin]['usd']:.2f}")
    else:
        await bot.send_message(callback_query.from_user.id, f"Не удалось получить данные по {coin.upper()}.")

@dp.callback_query_handler(lambda c: c.data == 'promo')
async def promo_handler(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Введите промокод:")

@dp.message_handler(lambda message: message.text.startswith('PROMO'))
async def process_promo_code(message: types.Message):
    promo_code = message.text.split()[0].strip().upper()
    discount = validate_promo_code(promo_code)
    if discount:
        await message.reply(f"Промокод применен! Ваша скидка: {discount * 100:.0f}%.")
    else:
        await message.reply("Неверный промокод.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
