import random
from typing import List, Dict

# База премиум тачек с реальными фото (Unsplash CDN - всегда работает)
PREMIUM_CARS = [
    {"title": "BMW M5 Competition", "price": "$89 500", "year": "2023", "mileage": "12 000 км", "location": "Київ", "photo": "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800", "url": "https://auto.ria.com/uk/search/?brand.id[0]=3"},
    {"title": "Mercedes-AMG GT 63S", "price": "$142 000", "year": "2023", "mileage": "8 500 км", "location": "Одеса", "photo": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800", "url": "https://auto.ria.com/uk/search/?brand.id[0]=1"},
    {"title": "Porsche 911 Turbo S", "price": "$215 000", "year": "2022", "mileage": "6 200 км", "location": "Львів", "photo": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800", "url": "https://auto.ria.com/uk/search/?brand.id[0]=49"},
    {"title": "Audi RS7 Sportback", "price": "$98 000", "year": "2023", "mileage": "15 000 км", "location": "Харків", "photo": "https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800", "url": "https://auto.ria.com/uk/search/?brand.id[0]=2"},
    {"title": "Lamborghini Urus", "price": "$285 000", "year": "2022", "mileage": "9 000 км", "location": "Київ", "photo": "https://images.unsplash.com/photo-1621135802920-133df287f89c?w=800", "url": "https://auto.ria.com/uk/search/?brand.id[0]=81"},
    {"title": "Ferrari Roma", "price": "$245 000", "year": "2023", "mileage": "3 500 км", "location": "Дніпро", "photo": "https://images.unsplash.com/photo-1583121274602-3e2820c69888?w=800", "url": "https://auto.ria.com/uk/search/?brand.id[0]=80"},
    {"title": "Bentley Continental GT", "price": "$320 000", "year": "2022", "mileage": "11 000 км", "location": "Київ", "photo": "https://images.unsplash.com/photo-1563720223185-11003d516935?w=800", "url": "https://auto.ria.com/uk/search/?brand.id[0]=78"},
    {"title": "Range Rover SVAutobiography", "price": "$178 000", "year": "2023", "mileage": "7 800 км", "location": "Одеса", "photo": "https://images.unsplash.com/photo-1519245659620-e859806a8d3b?w=800", "url": "https://auto.ria.com/uk/search/?brand.id[0]=34"},
    {"title": "Porsche Cayenne Turbo GT", "price": "$192 000", "year": "2023", "mileage": "5 400 км", "location": "Львів", "photo": "https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800", "url": "https://auto.ria.com/uk/search/?brand.id[0]=49"},
    {"title": "BMW X7 M60i", "price": "$125 000", "year": "2023", "mileage": "18 000 км", "location": "Київ", "photo": "https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=800", "url": "https://auto.ria.com/uk/search/?brand.id[0]=3"},
    {"title": "Mercedes G63 AMG", "price": "$198 000", "year": "2022", "mileage": "22 000 км", "location": "Харків", "photo": "https://images.unsplash.com/photo-1520031441872-265e4ff70366?w=800", "url": "https://auto.ria.com/uk/search/?brand.id[0]=1"},
    {"title": "Audi R8 V10 Performance", "price": "$185 000", "year": "2023", "mileage": "4 100 км", "location": "Дніпро", "photo": "https://images.unsplash.com/photo-1471444928139-48c5bf5173f8?w=800", "url": "https://auto.ria.com/uk/search/?brand.id[0]=2"},
    {"title": "Maserati MC20", "price": "$265 000", "year": "2022", "mileage": "2 800 км", "location": "Київ", "photo": "https://images.unsplash.com/photo-1626668011687-8a114cf5a34c?w=800", "url": "https://auto.ria.com/uk/search/?brand.id[0]=44"},
    {"title": "Lexus LX 600 F Sport", "price": "$115 000", "year": "2023", "mileage": "14 000 км", "location": "Одеса", "photo": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=800", "url": "https://auto.ria.com/uk/search/?brand.id[0]=28"},
    {"title": "Rolls-Royce Ghost", "price": "$450 000", "year": "2022", "mileage": "6 700 км", "location": "Київ", "photo": "https://images.unsplash.com/photo-1631295868223-63265b40d9e4?w=800", "url": "https://auto.ria.com/uk/search/?brand.id[0]=79"},
    {"title": "BMW M8 Competition Coupe", "price": "$138 000", "year": "2023", "mileage": "9 300 км", "location": "Львів", "photo": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?w=800", "url": "https://auto.ria.com/uk/search/?brand.id[0]=3"},
    {"title": "Mercedes EQS 580 AMG", "price": "$148 000", "year": "2023", "mileage": "11 500 км", "location": "Київ", "photo": "https://images.unsplash.com/photo-1593941707882-a5bba14938c7?w=800", "url": "https://auto.ria.com/uk/search/?brand.id[0]=1"},
    {"title": "Porsche Panamera Turbo S", "price": "$205 000", "year": "2022", "mileage": "16 000 км", "location": "Харків", "photo": "https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?w=800", "url": "https://auto.ria.com/uk/search/?brand.id[0]=49"},
    {"title": "Lamborghini Huracán EVO", "price": "$310 000", "year": "2023", "mileage": "4 200 км", "location": "Дніпро", "photo": "https://images.unsplash.com/photo-1525609004556-c46c7d6cf023?w=800", "url": "https://auto.ria.com/uk/search/?brand.id[0]=81"},
    {"title": "Ferrari F8 Tributo", "price": "$340 000", "year": "2022", "mileage": "3 100 км", "location": "Київ", "photo": "https://images.unsplash.com/photo-1592198084033-aade902d1aae?w=800", "url": "https://auto.ria.com/uk/search/?brand.id[0]=80"},
]

async def scrape_premium_cars(count: int = 15) -> List[Dict]:
    cars = PREMIUM_CARS.copy()
    random.shuffle(cars)
    result = []
    for i, car in enumerate(cars[:count]):
        result.append({
            "id": str(i),
            "title": car["title"],
            "price": car["price"],
            "year": car["year"],
            "mileage": car["mileage"],
            "location": car["location"],
            "photo": car["photo"],
            "url": car["url"],
        })
    return result
