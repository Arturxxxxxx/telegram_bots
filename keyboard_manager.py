from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def create_shop_keyboard(shops):
    keyboard = InlineKeyboardBuilder()
    for shop in shops:
        keyboard.button(text=shop["name"], callback_data=f"shop_{shop['name']}")
    return keyboard.adjust(1)

def create_period_keyboard():
    markup = [
        [InlineKeyboardButton(text="Сегодня", callback_data="period_today")],
        [InlineKeyboardButton(text="Вчера", callback_data="period_yesterday")],
        [InlineKeyboardButton(text="Последние 7 дней", callback_data="period_last7")],
        [InlineKeyboardButton(text="Произвольный период", callback_data="period_custom")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=markup)
