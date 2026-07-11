import asyncio
import logging
import random
import json
import urllib.request
import re
from typing import List, Dict

logger = logging.getLogger(__name__)

BASE_URL = "https://auto.ria.com"

SEARCH_URLS = [
    "https://auto.ria.com/uk/search/?category_id=1&brand.id[0]=3&price.USD.gte=30000&page={page}&size=20",   # BMW
    "https://auto.ria.com/uk/search/?category_id=1&brand.id[0]=1&price.USD.gte=30000&page={page}&size=20",   # Mercedes
    "https://auto.ria.com/uk/search/?category_id=1&brand.id[0]=49&price.USD.gte=30000&page={page}&size=20",  # Porsche
    "https://auto.ria.com/uk/search/?category_id=1&brand.id[0]=2&price.USD.gte=30000&page={page}&size=20",   # Audi
    "https://auto.ria.com/uk/search/?category_id=1&brand.id[0]=28&price.USD.gte=30000&page={page}&size=20",  # Lexus
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "uk-UA,uk;q=0.9",
}

def fetch_html(url: str) -> str | None:
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        logger.error(f"Ошибка запроса {url}: {e}")
        return None

def fetch_car_from_page(url: str) -> Dict | None:
    html = fetch_html(url)
    if not html:
        return None
    try:
        # JSON-LD
        jsonld_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
        if jsonld_match:
            data = json.loads(jsonld_match.group(1))
            if isinstance(data, list):
                data = data[0]

            title = data.get("name", "")
            offers = data.get("offers", {})
            price_raw = offers.get("price", 0)
            price = f"${int(float(price_raw)):,}".replace(",", " ") if price_raw else "Цена не указана"

            image = data.get("image", None)
            if isinstance(image, list):
                image = image[0] if image else None

            year_match = re.search(r'"productionDate"\s*:\s*"?(\d{4})"?', html)
            year = year_match.group(1) if year_match else "—"

            mileage_match = re.search(r'"mileageFromOdometer"[^}]*"value"\s*:\s*"?(\d+)"?', html, re.DOTALL)
            mileage = f"{int(mileage_match.group(1)):,} км".replace(",", " ") if mileage_match else "—"

            location_match = re.search(r'"addressLocality"\s*:\s*"([^"]+)"', html)
            location = location_match.group(1) if location_match else "Україна"

            id_match = re.search(r'_(\d+)\.html', url)
            car_id = id_match.group(1) if id_match else url[-10:]

            if not title:
                return None

            return {
                "id": car_id,
                "title": title,
                "price": price,
                "year": year,
                "mileage": mileage,
                "location": location,
                "photo": image,
                "url": url,
            }
    except Exception as e:
        logger.error(f"Ошибка парсинга {url}: {e}")
    return None

async def scrape_premium_cars(count: int = 15) -> List[Dict]:
    cars = []
    urls = SEARCH_URLS.copy()
    random.shuffle(urls)

    all_links = []
    for url_template in urls[:3]:
        page = random.randint(0, 5)
        url = url_template.format(page=page)
        html = await asyncio.to_thread(fetch_html, url)
        if html:
            links = re.findall(r'href="(/uk/auto[^"]+\.html)"', html)
            links = list(set(links))
            full_links = [BASE_URL + l for l in links]
            all_links.extend(full_links)
            logger.info(f"Найдено {len(links)} ссылок")
        await asyncio.sleep(1)

    if not all_links:
        logger.warning("Ссылки не найдены")
        return []

    random.shuffle(all_links)

    for link in all_links[:count * 2]:
        result = await asyncio.to_thread(fetch_car_from_page, link)
        if result:
            cars.append(result)
            logger.info(f"✅ {result['title']} — {result['price']}")
        if len(cars) >= count:
            break
        await asyncio.sleep(1)

    logger.info(f"Итого: {len(cars)} тачек")
    return cars[:count]
