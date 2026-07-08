import aiohttp
import asyncio
import logging
import re
import random
from typing import List, Dict

logger = logging.getLogger(__name__)

# Только премиум/люкс марки
PREMIUM_BRANDS = {
    "bmw": "3",
    "mercedes": "1",       # Mercedes-Benz
    "porsche": "49",
    "audi": "2",
    "lexus": "28",
    "land-rover": "34",
    "maserati": "44",
    "bentley": "78",
    "ferrari": "80",
    "lamborghini": "81",
    "rolls-royce": "79",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "uk-UA,uk;q=0.9,ru;q=0.8",
}

async def fetch_cars_from_api(session: aiohttp.ClientSession, brand_id: str, page: int = 0) -> List[Dict]:
    """Получаем машины через auto.ria.com API"""
    url = "https://auto.ria.com/api/search/auto"
    params = {
        "brand.id[0]": brand_id,
        "price.currency": 1,          # USD
        "price.gte": 30000,           # от $30k — премиум
        "category_id": 1,             # легковые
        "page": page,
        "countpage": 20,
        "with_photo": 1,
        "lang_id": 4,                 # украинский интерфейс
    }

    try:
        async with session.get(url, params=params, headers=HEADERS, timeout=aiohttp.ClientTimeout(total=15)) as resp:
            if resp.status != 200:
                logger.warning(f"API вернул {resp.status} для brand_id={brand_id}")
                return []
            data = await resp.json(content_type=None)
            return data.get("result", {}).get("search_result", {}).get("ids", [])
    except Exception as e:
        logger.error(f"Ошибка запроса к API: {e}")
        return []

async def fetch_car_details(session: aiohttp.ClientSession, car_id: int) -> Dict | None:
    """Детали одного авто"""
    url = f"https://auto.ria.com/api/info/car?langId=4&auto_id={car_id}"
    try:
        async with session.get(url, headers=HEADERS, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            if resp.status != 200:
                return None
            data = await resp.json(content_type=None)

            # Цена
            price_usd = data.get("USD", 0)
            if price_usd:
                price = f"${price_usd:,}".replace(",", " ")
            else:
                price = "Цена не указана"

            # Пробег
            mileage_raw = data.get("raceInt", 0)
            mileage = f"{mileage_raw:,} км".replace(",", " ") if mileage_raw else "—"

            # Фото
            photos = data.get("photoData", {}).get("seoLinkF", "")
            photo_url = photos if photos else None

            # Локация
            city = data.get("locationCityName", "")
            region = data.get("regionName", "")
            location = ", ".join(filter(None, [city, region])) or "Украина"

            # Название
            brand = data.get("markName", "")
            model = data.get("modelName", "")
            year = data.get("year", "")
            title = f"{brand} {model} {year}".strip()

            return {
                "id": str(car_id),
                "title": title or f"Авто #{car_id}",
                "price": price,
                "year": str(year) if year else "—",
                "mileage": mileage,
                "location": location,
                "photo": photo_url,
                "url": f"https://auto.ria.com/auto_{car_id}.html",
            }

    except Exception as e:
        logger.error(f"Ошибка деталей car_id={car_id}: {e}")
        return None

async def scrape_premium_cars(count: int = 15) -> List[Dict]:
    """Главная функция: парсим премиум тачки"""
    cars = []
    brand_ids = list(PREMIUM_BRANDS.values())
    random.shuffle(brand_ids)  # каждый раз разные марки первыми

    async with aiohttp.ClientSession() as session:
        # Собираем ID машин из нескольких брендов
        all_ids = []
        for brand_id in brand_ids:
            if len(all_ids) >= count * 3:
                break
            page = random.randint(0, 3)  # разные страницы для разнообразия
            ids = await fetch_cars_from_api(session, brand_id, page)
            all_ids.extend(ids)
            await asyncio.sleep(0.5)

        if not all_ids:
            logger.warning("Не удалось получить ID машин")
            return []

        # Перемешиваем и берём нужное количество
        random.shuffle(all_ids)
        selected_ids = all_ids[:count * 2]  # берём с запасом на случай ошибок

        # Получаем детали параллельно (батчами по 5)
        for i in range(0, len(selected_ids), 5):
            batch = selected_ids[i:i+5]
            tasks = [fetch_car_details(session, car_id) for car_id in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, dict) and result:
                    cars.append(result)
                if len(cars) >= count:
                    break

            if len(cars) >= count:
                break

            await asyncio.sleep(1)

    logger.info(f"Найдено {len(cars)} тачек")
    return cars[:count]
