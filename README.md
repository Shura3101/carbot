# 🏎 CarBot — премиум тачки в Telegram

Бот парсит премиум машины (BMW, Mercedes, Porsche и др.) с auto.ria.com
и присылает их в групповой чат 3 раза в день.

---

## ⚡ Быстрый старт

### Шаг 1 — Создай бота в Telegram

1. Открой [@BotFather](https://t.me/BotFather)
2. Напиши `/newbot`
3. Придумай имя и username (например `@MyCarFinderBot`)
4. Скопируй **токен** (выглядит как `7123456789:AAF...`)

---

### Шаг 2 — Добавь бота в групповой чат

1. Создай группу (или используй существующую)
2. Добавь туда своего бота как участника
3. Дай боту права администратора (чтобы мог слать фото)
4. Узнай ID чата:
   - Добавь [@userinfobot](https://t.me/userinfobot) в чат
   - Он пришлёт ID чата (выглядит как `-1001234567890`)

---

### Шаг 3 — Деплой на Railway (бесплатно)

1. Зарегистрируйся на [railway.app](https://railway.app) через GitHub
2. Нажми **New Project → Deploy from GitHub repo**
3. Загрузи файлы проекта в GitHub репо (или используй Railway CLI)
4. В Railway добавь переменные окружения:

```
BOT_TOKEN = твой_токен_от_botfather
CHAT_ID   = id_твоего_чата (например -1001234567890)
```

5. Railway автоматически запустит `Procfile` → `python bot.py`

---

## 📋 Команды бота

| Команда | Что делает |
|---------|-----------|
| `/start` | Приветствие и инфо |
| `/cars` | Получить тачки прямо сейчас |
| `/top` | Топ тачек по лайкам |

---

## ⏰ Расписание

Бот сам присылает **10–20 тачек** в:
- 🌅 **09:00** — утренняя порция
- ☀️ **14:00** — дневная
- 🌙 **20:00** — вечерняя

---

## 🚗 Марки (премиум/люкс)

BMW, Mercedes-Benz, Porsche, Audi, Lexus,
Land Rover, Maserati, Bentley, Ferrari, Lamborghini, Rolls-Royce

---

## 🗂 Структура проекта

```
carbot/
├── bot.py          # Основной бот (aiogram 3)
├── parser.py       # Парсер auto.ria.com API
├── requirements.txt
├── Procfile        # Для Railway
├── README.md
└── data/
    └── reactions.json  # Лайки/дизлайки (создаётся автоматически)
```
