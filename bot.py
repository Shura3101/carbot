import asyncio
import logging
import os
import json
import random
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from parser import scrape_premium_cars

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
DATA_FILE = "data/reactions.json"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

# ─── Марки ───────────────────────────────────────────────────────────────────

BRANDS = {
    "bmw": "BMW",
    "mercedes": "Mercedes",
    "porsche": "Porsche",
    "audi": "Audi",
    "ferrari": "Ferrari",
    "lamborghini": "Lamborghini",
    "bentley": "Bentley",
    "rolls": "Rolls-Royce",
    "lexus": "Lexus",
    "maserati": "Maserati",
    "mclaren": "McLaren",
    "range": "Range Rover",
}

# ─── Хранилище реакций ───────────────────────────────────────────────────────

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_car_reactions(car_id: str):
    data = load_data()
    return data.get(car_id, {"likes": [], "dislikes": []})

def toggle_reaction(car_id: str, user_id: int, reaction: str):
    data = load_data()
    if car_id not in data:
        data[car_id] = {"likes": [], "dislikes": []}
    opposite = "dislikes" if reaction == "likes" else "likes"
    if user_id in data[car_id][opposite]:
        data[car_id][opposite].remove(user_id)
    if user_id in data[car_id][reaction]:
        data[car_id][reaction].remove(user_id)
        action = "removed"
    else:
        data[car_id][reaction].append(user_id)
        action = "added"
    save_data(data)
    return action, data[car_id]

# ─── Клавиатуры ──────────────────────────────────────────────────────────────

def make_reaction_keyboard(car_id: str):
    reactions = get_car_reactions(car_id)
    likes = len(reactions["likes"])
    dislikes = len(reactions["dislikes"])
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"🔥 ({likes})", callback_data=f"like:{car_id}"),
            InlineKeyboardButton(text=f"👎 ({dislikes})", callback_data=f"dislike:{car_id}"),
        ]
    ])

def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚗 5 тачек"), KeyboardButton(text="🏆 Топ")],
            [KeyboardButton(text="🔍 По марке"), KeyboardButton(text="💰 По цене")],
            [KeyboardButton(text="📖 Инструкция")],
        ],
        resize_keyboard=True
    )

def brand_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="BMW", callback_data="brand:BMW"),
            InlineKeyboardButton(text="Mercedes", callback_data="brand:Mercedes"),
            InlineKeyboardButton(text="Porsche", callback_data="brand:Porsche"),
        ],
        [
            InlineKeyboardButton(text="Audi", callback_data="brand:Audi"),
            InlineKeyboardButton(text="Ferrari", callback_data="brand:Ferrari"),
            InlineKeyboardButton(text="Lamborghini", callback_data="brand:Lamborghini"),
        ],
        [
            InlineKeyboardButton(text="Bentley", callback_data="brand:Bentley"),
            InlineKeyboardButton(text="Rolls-Royce", callback_data="brand:Rolls-Royce"),
            InlineKeyboardButton(text="Lexus", callback_data="brand:Lexus"),
        ],
        [
            InlineKeyboardButton(text="Maserati", callback_data="brand:Maserati"),
            InlineKeyboardButton(text="McLaren", callback_data="brand:McLaren"),
            InlineKeyboardButton(text="Range Rover", callback_data="brand:Range Rover"),
        ],
    ])

def price_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💚 До $100k", callback_data="price:under100")],
        [InlineKeyboardButton(text="💛 $100k — $200k", callback_data="price:100to200")],
        [InlineKeyboardButton(text="🔴 От $200k", callback_data="price:over200")],
    ])

# ─── Отправка машин ──────────────────────────────────────────────────────────

async def send_cars(chat_id, count=5, brand_filter=None, price_filter=None):
    cars = await scrape_premium_cars(count=25)

    if brand_filter:
        cars = [c for c in cars if brand_filter.lower() in c["title"].lower()]

    if price_filter == "under100":
        cars = [c for c in cars if parse_price(c["price"]) < 100000]
    elif price_filter == "100to200":
        cars = [c for c in cars if 100000 <= parse_price(c["price"]) <= 200000]
    elif price_filter == "over200":
        cars = [c for c in cars if parse_price(c["price"]) > 200000]

    cars = cars[:count]

    if not cars:
        await bot.send_message(chat_id, "😔 По этому фильтру ничего не нашлось. Попробуй другой!")
        return

    hour = datetime.now().hour
    if 6 <= hour < 12:
        greeting = "🌅 Утренняя порция тачек"
    elif 12 <= hour < 18:
        greeting = "☀️ Дневная порция тачек"
    else:
        greeting = "🌙 Вечерний заезд"

    label = f" • {brand_filter}" if brand_filter else ""
    await bot.send_message(chat_id, f"{greeting}{label} — {len(cars)} авто 🚗")

    for car in cars:
        text = (
            f"🚗 *{car['title']}*\n"
            f"💰 {car['price']}\n"
            f"📅 {car['year']} • 🛣 {car['mileage']}\n"
            f"📍 {car['location']}\n"
            f"🔗 [Дивитись на auto\\.ria]({car['url']})"
        )
        try:
            await bot.send_message(
                chat_id,
                text=text,
                parse_mode="MarkdownV2",
                reply_markup=make_reaction_keyboard(car["id"]),
                disable_web_page_preview=False
            )
        except Exception as e:
            logger.error(f"Ошибка: {e}")
        await asyncio.sleep(0.5)

def parse_price(price_str: str) -> int:
    try:
        return int(price_str.replace("$", "").replace(" ", "").replace(",", ""))
    except:
        return 0

async def send_cars_batch(chat_id=None):
    if chat_id is None:
        chat_id = CHAT_ID
    await send_cars(chat_id, count=5)

# ─── Реакции ─────────────────────────────────────────────────────────────────

@dp.callback_query(F.data.startswith("like:"))
async def handle_like(callback: types.CallbackQuery):
    car_id = callback.data.split(":", 1)[1]
    action, _ = toggle_reaction(car_id, callback.from_user.id, "likes")
    await callback.answer("🔥 Огонь!" if action == "added" else "Убрал лайк")
    try:
        await callback.message.edit_reply_markup(reply_markup=make_reaction_keyboard(car_id))
    except Exception:
        pass

@dp.callback_query(F.data.startswith("dislike:"))
async def handle_dislike(callback: types.CallbackQuery):
    car_id = callback.data.split(":", 1)[1]
    action, _ = toggle_reaction(car_id, callback.from_user.id, "dislikes")
    await callback.answer("👎 Не твоя тачка" if action == "added" else "Убрал дизлайк")
    try:
        await callback.message.edit_reply_markup(reply_markup=make_reaction_keyboard(car_id))
    except Exception:
        pass

# ─── Фильтры ─────────────────────────────────────────────────────────────────

@dp.callback_query(F.data.startswith("brand:"))
async def handle_brand(callback: types.CallbackQuery):
    brand = callback.data.split(":", 1)[1]
    await callback.answer(f"Ищу {brand}...")
    await callback.message.delete()
    await send_cars(callback.message.chat.id, count=5, brand_filter=brand)

@dp.callback_query(F.data.startswith("price:"))
async def handle_price(callback: types.CallbackQuery):
    price_range = callback.data.split(":", 1)[1]
    labels = {"under100": "до $100k", "100to200": "$100k–$200k", "over200": "от $200k"}
    await callback.answer(f"Фильтр: {labels.get(price_range, '')}")
    await callback.message.delete()
    await send_cars(callback.message.chat.id, count=5, price_filter=price_range)

# ─── Команды ─────────────────────────────────────────────────────────────────

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🏎 *CarBot запущен\\!*\n\n"
        "Используй кнопки внизу 👇",
        parse_mode="MarkdownV2",
        reply_markup=main_keyboard()
    )

@dp.message(Command("cars"))
async def cmd_cars(message: types.Message):
    await message.answer("⏳ Загружаю тачки...")
    await send_cars(message.chat.id, count=5)

@dp.message(F.text == "🚗 5 тачек")
async def btn_cars(message: types.Message):
    await message.answer("⏳ Загружаю тачки...")
    await send_cars(message.chat.id, count=5)

@dp.message(F.text == "🏆 Топ")
async def btn_top(message: types.Message):
    data = load_data()
    if not data:
        await message.answer("Поки немає лайків\\. Оцініть тачки\\!", parse_mode="MarkdownV2")
        return
    sorted_cars = sorted(data.items(), key=lambda x: len(x[1].get("likes", [])), reverse=True)[:5]
    text = "🏆 *Топ тачок по лайках:*\n\n"
    for i, (car_id, reactions) in enumerate(sorted_cars, 1):
        likes = len(reactions.get("likes", []))
        dislikes = len(reactions.get("dislikes", []))
        text += f"{i}\\. 🔥 {likes} | 👎 {dislikes}\n"
    await message.answer(text, parse_mode="MarkdownV2")

@dp.message(F.text == "🔍 По марке")
async def btn_brand(message: types.Message):
    await message.answer("Обери марку:", reply_markup=brand_keyboard())

@dp.message(F.text == "💰 По цене")
async def btn_price(message: types.Message):
    await message.answer("Обери діапазон ціни:", reply_markup=price_keyboard())

@dp.message(F.text == "📖 Інструкція")
async def btn_help(message: types.Message):
    text = (
        "📖 *Інструкція CarBot*\n\n"
        "🚗 *5 тачок* — отримати 5 випадкових преміум авто\n\n"
        "🏆 *Топ* — топ\\-5 тачок з найбільшою кількістю вогнів\n\n"
        "🔍 *По марці* — вибрати конкретну марку:\n"
        "BMW, Mercedes, Porsche, Audi, Ferrari,\n"
        "Lamborghini, Bentley, Rolls\\-Royce та інші\n\n"
        "💰 *По ціні* — фільтр за бюджетом:\n"
        "• До \\$100k\n"
        "• \\$100k — \\$200k\n"
        "• Від \\$200k\n\n"
        "🔥 *Огонь* — лайкнути тачку\n"
        "👎 *Не те* — дизлайкнути\n\n"
        "⏰ *Авторозсилка* — бот сам присилає тачки\n"
        "щодня о 9:00, 14:00 та 20:00\n\n"
        "💬 *Обговорення* — пишіть прямо в чат\\!"
    )
    await message.answer(text, parse_mode="MarkdownV2")

# Команды для марок через слэш
@dp.message(Command("bmw"))
async def cmd_bmw(message: types.Message):
    await send_cars(message.chat.id, count=5, brand_filter="BMW")

@dp.message(Command("mercedes"))
async def cmd_mercedes(message: types.Message):
    await send_cars(message.chat.id, count=5, brand_filter="Mercedes")

@dp.message(Command("porsche"))
async def cmd_porsche(message: types.Message):
    await send_cars(message.chat.id, count=5, brand_filter="Porsche")

@dp.message(Command("ferrari"))
async def cmd_ferrari(message: types.Message):
    await send_cars(message.chat.id, count=5, brand_filter="Ferrari")

@dp.message(Command("lamborghini"))
async def cmd_lamborghini(message: types.Message):
    await send_cars(message.chat.id, count=5, brand_filter="Lamborghini")

@dp.message(Command("bentley"))
async def cmd_bentley(message: types.Message):
    await send_cars(message.chat.id, count=5, brand_filter="Bentley")

@dp.message(Command("audi"))
async def cmd_audi(message: types.Message):
    await send_cars(message.chat.id, count=5, brand_filter="Audi")

# ─── Запуск ──────────────────────────────────────────────────────────────────

async def main():
    scheduler.add_job(send_cars_batch, "cron", hour=9, minute=0)
    scheduler.add_job(send_cars_batch, "cron", hour=14, minute=0)
    scheduler.add_job(send_cars_batch, "cron", hour=20, minute=0)
    scheduler.start()
    logger.info("🚗 CarBot запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
