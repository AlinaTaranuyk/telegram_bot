import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

API_TOKEN = os.environ.get("BOT_TOKEN")  # беремо токен з Render Environment Variable
MANAGER_ID = 123456789  # Telegram ID менеджера

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def create_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=5)
    keyboard.add(InlineKeyboardButton(text="Связаться с менеджером", callback_data="contact_manager"))
    hours = [f"{hour:02d}:00" for hour in range(9, 23)]
    for i in range(0, len(hours), 5):
        keyboard.row(*[InlineKeyboardButton(text=h, callback_data=h) for h in hours[i:i+5]])
    keyboard.add(InlineKeyboardButton(text="Толко ночь", callback_data="only_night"))
    return keyboard

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Отмечаемся со скольки в работке ⏰💲📆", reply_markup=create_keyboard())

@dp.callback_query_handler(lambda c: c.data)
async def process_callback(callback_query: types.CallbackQuery):
    data = callback_query.data
    user_name = callback_query.from_user.full_name
    if data == "contact_manager":
        await bot.send_message(MANAGER_ID, f"{user_name} хочет связаться с менеджером")
        await callback_query.answer("Менеджер получил сообщение")
    elif data == "only_night":
        await bot.send_message(MANAGER_ID, f"{user_name} отмечается только на ночную смену")
        await callback_query.answer("Вы отметили ночную смену")
    else:
        await bot.send_message(MANAGER_ID, f"{user_name} отмечается с {data}")
        await callback_query.answer(f"Вы отметили время: {data}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
