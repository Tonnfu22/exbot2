from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Курсы криптовалют", callback_data="crypto_menu"))
    markup.add(InlineKeyboardButton("Промокоды", callback_data="promo"))
    return markup

def crypto_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("BTC", callback_data="crypto_bitcoin"))
    markup.add(InlineKeyboardButton("LTC", callback_data="crypto_litecoin"))
    markup.add(InlineKeyboardButton("ETH", callback_data="crypto_ethereum"))
    markup.add(InlineKeyboardButton("XMR", callback_data="crypto_monero"))
    markup.add(InlineKeyboardButton("USDT", callback_data="crypto_tether"))
    return markup