import asyncio
import logging
import random
import json
import urllib.request
from typing import List, Dict

logger = logging.getLogger(__name__)

PREMIUM_BRANDS = {
    "bmw": "3",
    "mercedes": "1",
    "porsche": "49",
    "audi": "2",
    "lexus": "28",
    "land-rover": "34",
    "maserati": "44",
    "bentley": "78",
    "ferrari": "80",
    "lamborghini": "81",
}

def fetch_url(url: str) -> dict | None:
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
        })
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        logger.error(f"Ошибка запроса {url}: {e}")
        return None

def fetch_car_ids(brand_id: str, page: int = 0) -> List[int]:
    url = (
        f"https://auto.ria.com/api/search/auto"
        f"?brand.id[0]={brand_id}"
        f"&price.gte=30000"
        f"&category_id=1"
        f"&page={page}"
        f"&countpage=20"
        f"&with_photo=1"
    )
    data = fetch_url(url)
    if not data:
        return []
    return data.get("result", {}).get("search_result", {}).get("ids", [])

def fetch_car_details(car_id: int) -> Dict | None:
    url = f"https://auto.ria.com/api/info/car?langId=4&auto_id={car_id}"
    data = fetch_url(url)
    if not data:
        return None
    try:
        price_usd = data.get("USD", 0)
        price = f"${price_usd:,}".replace(",", " ") if price_usd else "Цена не указана"
        mileage_raw = data.get("raceInt", 0)
        mileage = f"{mileage_raw:,} км".replace(",", " ") if mileage_raw else "—"
        photo_url = data.get("photoData", {}).get("seoLinkF", None)
        city = data.get("locationCityName", "")
        region = data.get("regionName", "")
        location = ", ".join(filter(None, [city, region])) or "Украина"
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
        logger.error(f"Ошибка обработки car_id={car_id}: {e}")
        return None

async def scrape_premium_cars(count: int = 15) -> List[Dict]:
    cars = []
    brand_ids = list(PREMIUM_BRANDS.values())
    random.shuffle(brand_ids)

    all_ids = []
    for brand_id in brand_ids:
        if len(all_ids) >= count * 3:
            break
        page = random.randint(0, 3)
        ids = await asyncio.to_thread(fetch_car_ids, brand_id, page)
        all_ids.extend(ids)
        await asyncio.sleep(0.3)

    if not all_ids:
        logger.warning("Не удалось получить ID машин")
        return []

    random.shuffle(all_ids)
    selected_ids = all_ids[:count * 2]

    for car_id in selected_ids:
        result = await asyncio.to_thread(fetch_car_details, car_id)
        if result:
            cars.append(result)
        if len(cars) >= count:
            break
        await asyncio.sleep(0.5)

    logger.info(f"Найдено {len(cars)} тачек")
    return cars[:count]
