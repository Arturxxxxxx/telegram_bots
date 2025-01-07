import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from datetime import datetime, timedelta
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from data_json import load_user_data, save_user_data
from api_manager import fetch_sales_data
from report_manager import generate_report, split_message
from keyboard_manager import create_shop_keyboard, create_period_keyboard

class StateShop(StatesGroup):
    shop_name = State()
    shop_api_key = State()
    delet_shop = State()
    select_shop = State()
    select_period = State()
    custom_period = State()
    custom_end_date = State()

logging.basicConfig(level=logging.INFO)
bot = Bot(token='7839698649:AAFCws771SSfuDCkZRlXCcEy_NJ2ecqJTs4')  
dp = Dispatcher()

@dp.message(Command('start'))
async def start(message: Message, state: FSMContext):
    await message.answer('Привет, я твой помощник для управления магазинами!')

@dp.message(Command('addshop'))
async def addshop(message: Message, state: FSMContext):
    await message.answer('Введите название магазина:')
    await state.set_state(StateShop.shop_name)

@dp.message(StateShop.shop_name)
async def save_addshop(message: Message, state: FSMContext):
    shop_name = message.text
    await state.update_data(shop_name=shop_name)
    await message.answer('Введите API ключ магазина:')
    await state.set_state(StateShop.shop_api_key)

@dp.message(StateShop.shop_api_key)
async def save_addshop_api_key(message: Message, state: FSMContext):
    shop_api_key = message.text
    user_id = str(message.from_user.id)
    user_data = await state.get_data()
    shop_name = user_data['shop_name']

    data = load_user_data()

    if user_id not in data:
        data[user_id] = []

    data[user_id].append({"name": shop_name, "api_key": shop_api_key})

    save_user_data(data)

    await message.answer(f"Магазин '{shop_name}' успешно добавлен!")
    await state.clear()

@dp.message(Command('shops'))
async def list_shops(message: Message):
    user_id = str(message.from_user.id)
    shops = load_user_data().get(user_id, [])

    if not shops:
        await message.answer("У вас нет добавленных магазинов.")
        return

    shop_names = [shop["name"] for shop in shops]
    await message.answer(f"Ваши магазины: {', '.join(shop_names)}")

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer(
        'Доступные команды:\n'
        '/addshop - добавить магазин\n'
        '/shops - посмотреть магазины\n'
        '/delshop - удалить магазин\n'
        '/report - получить отчет'
    )

@dp.message(Command('delshop'))
async def delshop(message: Message, state: FSMContext):
    await message.answer('Введите название магазина для удаления:')
    await state.set_state(StateShop.delet_shop)

@dp.message(StateShop.delet_shop)
async def delete_shop(message: Message, state: FSMContext):
    shop_name = message.text
    user_id = str(message.from_user.id)

    data = load_user_data()

    if user_id in data:
        data[user_id] = [shop for shop in data[user_id] if shop['name'] != shop_name]
        save_user_data(data)
        await message.answer(f"Магазин '{shop_name}' успешно удален.")
    else:
        await message.answer(f"Магазин '{shop_name}' не найден.")

@dp.message(Command('report'))
async def report(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)

    shops = load_user_data().get(user_id, [])
    if not shops:
        await message.answer("У вас нет магазинов.")
        return

    keyboard = create_shop_keyboard(shops)
    await message.answer("Выберите магазин для получения отчета:", reply_markup=keyboard.as_markup())

@dp.callback_query(lambda call: call.data.startswith("shop_"))
async def select_shop(call: CallbackQuery, state: FSMContext):
    shop_name = call.data.split("_")[1]
    await state.update_data(selected_shop=shop_name)
    await call.message.answer("Выберите период для отчета:", reply_markup=create_period_keyboard())
    await state.set_state('select_period')

@dp.callback_query(lambda call: call.data.startswith("period_"))
async def select_period(call: CallbackQuery, state: FSMContext):
    period = call.data.split("_")[1]
    now = datetime.now()
    user_data = await state.get_data()
    selected_shop = user_data['selected_shop']
    shop = next((s for s in load_user_data().get(str(call.from_user.id), []) if s['name'] == selected_shop), None)

    if not shop or not shop.get("api_key"):
        await call.message.answer("Магазин не найден или отсутствует API-ключ.")
        return

    api_key = shop["api_key"]
    
    if period == "today":
        start_date = end_date = now.strftime("%Y-%m-%d")
    elif period == "yesterday":
        start_date = end_date = (now - timedelta(days=1)).strftime("%Y-%m-%d")
    elif period == "last7":
        start_date = (now - timedelta(days=7)).strftime("%Y-%m-%d")
        end_date = now.strftime("%Y-%m-%d")
    else:
        await call.message.answer("Некорректный выбор периода.")
        return

    sales_data = fetch_sales_data(api_key, start_date, end_date)
    if sales_data:
        report = generate_report(sales_data)
        for chunk in split_message(report):
            await call.message.answer(chunk, parse_mode='Markdown')
    else:
        await call.message.answer("Не удалось получить данные.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
