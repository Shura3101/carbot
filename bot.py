import asyncio
import logging
import os
import json
import random
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from parser import scrape_premium_cars

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")  # ID группового чата
DATA_FILE = "data/reactions.json"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

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

# ─── Клавиатура реакций ──────────────────────────────────────────────────────

def make_reaction_keyboard(car_id: str):
    reactions = get_car_reactions(car_id)
    likes = len(reactions["likes"])
    dislikes = len(reactions["dislikes"])

    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"🔥 Огонь! ({likes})",
                callback_data=f"like:{car_id}"
            ),
            InlineKeyboardButton(
                text=f"👎 Не то ({dislikes})",
                callback_data=f"dislike:{car_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="💬 Обсудить",
                callback_data=f"discuss:{car_id}"
            )
        ]
    ])

# ─── Отправка пачки машин ────────────────────────────────────────────────────

async def send_cars_batch():
    logger.info("Парсим тачки с auto.ria.com...")
    try:
        cars = await scrape_premium_cars(count=random.randint(10, 20))
    except Exception as e:
        logger.error(f"Ошибка парсинга: {e}")
        return

    if not cars:
        logger.warning("Машины не найдены")
        return

    hour = datetime.now().hour
    if 6 <= hour < 12:
        greeting = "🌅 Доброе утро, пацаны! Смотрите что нашёл"
    elif 12 <= hour < 18:
        greeting = "☀️ Дневная порция горячих тачек"
    else:
        greeting = "🌙 Вечерний заезд. Выбирайте мечту"

    await bot.send_message(
        CHAT_ID,
        f"{greeting} — {len(cars)} тачек с auto.ria.com 🚗\n\n"
        f"👇 Лайкайте, дизлайкайте, обсуждайте!"
    )

    for car in cars:
        caption = (
            f"🚗 *{car['title']}*\n"
            f"💰 {car['price']}\n"
            f"📅 {car['year']} • 🛣 {car['mileage']}\n"
            f"📍 {car['location']}\n"
            f"🔗 [Смотреть на auto.ria]({car['url']})"
        )

        try:
            if car.get("photo"):
                msg = await bot.send_photo(
                    CHAT_ID,
                    photo=car["photo"],
                    caption=caption,
                    parse_mode="Markdown",
                    reply_markup=make_reaction_keyboard(car["id"])
                )
            else:
                msg = await bot.send_message(
                    CHAT_ID,
                    text=caption,
                    parse_mode="Markdown",
                    reply_markup=make_reaction_keyboard(car["id"]),
                    disable_web_page_preview=False
                )
        except Exception as e:
            logger.error(f"Ошибка отправки {car['title']}: {e}")

        await asyncio.sleep(1.5)  # небольшая задержка между фото

# ─── Обработчики кнопок ──────────────────────────────────────────────────────

@dp.callback_query(F.data.startswith("like:"))
async def handle_like(callback: types.CallbackQuery):
    car_id = callback.data.split(":", 1)[1]
    user_id = callback.from_user.id
    action, reactions = toggle_reaction(car_id, user_id, "likes")

    msg = "🔥 Огонь!" if action == "added" else "Убрал лайк"
    await callback.answer(msg, show_alert=False)

    try:
        await callback.message.edit_reply_markup(
            reply_markup=make_reaction_keyboard(car_id)
        )
    except Exception:
        pass

@dp.callback_query(F.data.startswith("dislike:"))
async def handle_dislike(callback: types.CallbackQuery):
    car_id = callback.data.split(":", 1)[1]
    user_id = callback.from_user.id
    action, reactions = toggle_reaction(car_id, user_id, "dislikes")

    msg = "👎 Не твоя тачка" if action == "added" else "Убрал дизлайк"
    await callback.answer(msg, show_alert=False)

    try:
        await callback.message.edit_reply_markup(
            reply_markup=make_reaction_keyboard(car_id)
        )
    except Exception:
        pass

@dp.callback_query(F.data.startswith("discuss:"))
async def handle_discuss(callback: types.CallbackQuery):
    car_id = callback.data.split(":", 1)[1]
    reactions = get_car_reactions(car_id)
    likes = len(reactions["likes"])
    dislikes = len(reactions["dislikes"])

    await callback.answer(
        f"🔥 {likes} огонь | 👎 {dislikes} не то\nПиши мнение прямо в чат!",
        show_alert=True
    )

# ─── Команды ─────────────────────────────────────────────────────────────────

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🏎 *CarBot запущен!*\n\n"
        "Каждый день в 9:00, 14:00 и 20:00 буду присылать "
        "горячие тачки с auto.ria.com\n\n"
        "Команды:\n"
        "/cars — получить тачки прямо сейчас\n"
        "/top — топ тачек по лайкам",
        parse_mode="Markdown"
    )

@dp.message(Command("cars"))
async def cmd_cars(message: types.Message):
    await message.answer("⏳ Парсю auto.ria.com, подожди секунду...")
    await send_cars_batch()

@dp.message(Command("top"))
async def cmd_top(message: types.Message):
    data = load_data()
    if not data:
        await message.answer("Пока нет лайков. Оцените тачки!")
        return

    sorted_cars = sorted(
        data.items(),
        key=lambda x: len(x[1].get("likes", [])),
        reverse=True
    )[:5]

    text = "🏆 *Топ тачек по лайкам:*\n\n"
    for i, (car_id, reactions) in enumerate(sorted_cars, 1):
        likes = len(reactions.get("likes", []))
        dislikes = len(reactions.get("dislikes", []))
        text += f"{i}. ID: `{car_id[:20]}...`\n   🔥 {likes} | 👎 {dislikes}\n\n"

    await message.answer(text, parse_mode="Markdown")

# ─── Запуск ──────────────────────────────────────────────────────────────────

async def main():
    # Расписание: 9:00, 14:00, 20:00
    scheduler.add_job(send_cars_batch, "cron", hour=9, minute=0)
    scheduler.add_job(send_cars_batch, "cron", hour=14, minute=0)
    scheduler.add_job(send_cars_batch, "cron", hour=20, minute=0)
    scheduler.start()

    logger.info("🚗 CarBot запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
