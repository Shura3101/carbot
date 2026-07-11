import random
from typing import List, Dict

PREMIUM_CARS = [
    {
        "title": "BMW M5 Competition 2023",
        "price": "$89 500",
        "year": "2023",
        "mileage": "12 000 км",
        "location": "Київ",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/2021_BMW_M5_Competition_%28F90%2C_facelift%2C_black%29%2C_front_8.15.21.jpg/1280px-2021_BMW_M5_Competition_%28F90%2C_facelift%2C_black%29%2C_front_8.15.21.jpg",
        "url": "https://auto.ria.com/uk/search/?brand.id[0]=3&model.id[0]=4&price.USD.gte=80000"
    },
    {
        "title": "Mercedes-AMG G63 2022",
        "price": "$198 000",
        "year": "2022",
        "mileage": "22 000 км",
        "location": "Одеса",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Mercedes-AMG_G_63_%28W_463%2C_facelift_2018%29%2C_front_8.15.21.jpg/1280px-Mercedes-AMG_G_63_%28W_463%2C_facelift_2018%29%2C_front_8.15.21.jpg",
        "url": "https://auto.ria.com/uk/search/?brand.id[0]=1&model.id[0]=20&price.USD.gte=150000"
    },
    {
        "title": "Porsche 911 Turbo S 2023",
        "price": "$215 000",
        "year": "2023",
        "mileage": "6 200 км",
        "location": "Львів",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/2021_Porsche_911_Turbo_S_%28992%29%2C_front_8.15.21.jpg/1280px-2021_Porsche_911_Turbo_S_%28992%29%2C_front_8.15.21.jpg",
        "url": "https://auto.ria.com/uk/search/?brand.id[0]=49&model.id[0]=9&price.USD.gte=180000"
    },
    {
        "title": "Lamborghini Urus 2022",
        "price": "$285 000",
        "year": "2022",
        "mileage": "9 000 км",
        "location": "Київ",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Lamborghini_Urus_-_Flickr_-_Alexandre_Prévot_%2814%29_%28cropped%29.jpg/1280px-Lamborghini_Urus_-_Flickr_-_Alexandre_Prévot_%2814%29_%28cropped%29.jpg",
        "url": "https://auto.ria.com/uk/search/?brand.id[0]=81&price.USD.gte=200000"
    },
    {
        "title": "Ferrari Roma 2023",
        "price": "$245 000",
        "year": "2023",
        "mileage": "3 500 км",
        "location": "Дніпро",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/2020_Ferrari_Roma%2C_front_8.15.21.jpg/1280px-2020_Ferrari_Roma%2C_front_8.15.21.jpg",
        "url": "https://auto.ria.com/uk/search/?brand.id[0]=80&price.USD.gte=200000"
    },
    {
        "title": "Bentley Continental GT 2022",
        "price": "$320 000",
        "year": "2022",
        "mileage": "11 000 км",
        "location": "Київ",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/2020_Bentley_Continental_GT_V8%2C_front_8.15.21.jpg/1280px-2020_Bentley_Continental_GT_V8%2C_front_8.15.21.jpg",
        "url": "https://auto.ria.com/uk/search/?brand.id[0]=78&price.USD.gte=250000"
    },
    {
        "title": "Porsche Cayenne Turbo GT 2023",
        "price": "$192 000",
        "year": "2023",
        "mileage": "5 400 км",
        "location": "Львів",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Porsche_Cayenne_Turbo_GT_%28I%29%2C_Frontansicht%2C_14._April_2022%2C_D%C3%BCsseldorf.jpg/1280px-Porsche_Cayenne_Turbo_GT_%28I%29%2C_Frontansicht%2C_14._April_2022%2C_D%C3%BCsseldorf.jpg",
        "url": "https://auto.ria.com/uk/search/?brand.id[0]=49&model.id[0]=73&price.USD.gte=150000"
    },
    {
        "title": "Audi RS6 Avant 2023",
        "price": "$112 000",
        "year": "2023",
        "mileage": "18 000 км",
        "location": "Харків",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Audi_RS_6_Avant_%28C8%29_IMG_3112.jpg/1280px-Audi_RS_6_Avant_%28C8%29_IMG_3112.jpg",
        "url": "https://auto.ria.com/uk/search/?brand.id[0]=2&model.id[0]=119&price.USD.gte=90000"
    },
    {
        "title": "BMW X5 M Competition 2023",
        "price": "$135 000",
        "year": "2023",
        "mileage": "14 000 км",
        "location": "Київ",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/2020_BMW_X5_M_Competition_%28F95%29%2C_front_8.15.21.jpg/1280px-2020_BMW_X5_M_Competition_%28F95%29%2C_front_8.15.21.jpg",
        "url": "https://auto.ria.com/uk/search/?brand.id[0]=3&model.id[0]=118&price.USD.gte=110000"
    },
    {
        "title": "Range Rover Sport SVR 2022",
        "price": "$145 000",
        "year": "2022",
        "mileage": "19 000 км",
        "location": "Одеса",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Range_Rover_Sport_SVR_%282017%29_%2833107882Guards_Red%29.jpg/1280px-Range_Rover_Sport_SVR_%282017%29_%2833107882Guards_Red%29.jpg",
        "url": "https://auto.ria.com/uk/search/?brand.id[0]=34&price.USD.gte=120000"
    },
    {
        "title": "Mercedes-AMG GT 63S 2023",
        "price": "$155 000",
        "year": "2023",
        "mileage": "7 800 км",
        "location": "Київ",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Mercedes-AMG_GT_63_S_4MATIC%2B_%28X290%29_%E2%80%93_Frontansicht%2C_25._Oktober_2018%2C_D%C3%BCsseldorf.jpg/1280px-Mercedes-AMG_GT_63_S_4MATIC%2B_%28X290%29_%E2%80%93_Frontansicht%2C_25._Oktober_2018%2C_D%C3%BCsseldorf.jpg",
        "url": "https://auto.ria.com/uk/search/?brand.id[0]=1&model.id[0]=276&price.USD.gte=130000"
    },
    {
        "title": "Audi R8 V10 Performance 2022",
        "price": "$185 000",
        "year": "2022",
        "mileage": "4 100 км",
        "location": "Дніпро",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/2020_Audi_R8_V10_Performance_%284S%2C_facelift%29%2C_front_8.15.21.jpg/1280px-2020_Audi_R8_V10_Performance_%284S%2C_facelift%29%2C_front_8.15.21.jpg",
        "url": "https://auto.ria.com/uk/search/?brand.id[0]=2&model.id[0]=167&price.USD.gte=150000"
    },
    {
        "title": "Rolls-Royce Ghost 2022",
        "price": "$450 000",
        "year": "2022",
        "mileage": "6 700 км",
        "location": "Київ",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/2021_Rolls-Royce_Ghost_%28facelift%2C_silver%29%2C_front_8.15.21.jpg/1280px-2021_Rolls-Royce_Ghost_%28facelift%2C_silver%29%2C_front_8.15.21.jpg",
        "url": "https://auto.ria.com/uk/search/?brand.id[0]=79&price.USD.gte=350000"
    },
    {
        "title": "Lamborghini Huracán EVO 2023",
        "price": "$310 000",
        "year": "2023",
        "mileage": "4 200 км",
        "location": "Київ",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/twenty/Lamborghini_Huracán_EVO_%28orange%29%2C_Frontansicht%2C_14._April_2022%2C_Düsseldorf.jpg/1280px-Lamborghini_Huracán_EVO_%28orange%29%2C_Frontansicht%2C_14._April_2022%2C_Düsseldorf.jpg",
        "url": "https://auto.ria.com/uk/search/?brand.id[0]=81&price.USD.gte=280000"
    },
    {
        "title": "Porsche Panamera Turbo S 2022",
        "price": "$205 000",
        "year": "2022",
        "mileage": "16 000 км",
        "location": "Харків",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Porsche_Panamera_Turbo_S_E-Hybrid_%28971%29%2C_Frontansicht%2C_15._April_2022%2C_D%C3%BCsseldorf.jpg/1280px-Porsche_Panamera_Turbo_S_E-Hybrid_%28971%29%2C_Frontansicht%2C_15._April_2022%2C_D%C3%BCsseldorf.jpg",
        "url": "https://auto.ria.com/uk/search/?brand.id[0]=49&model.id[0]=15&price.USD.gte=170000"
    },
    {
        "title": "BMW M8 Competition 2023",
        "price": "$138 000",
        "year": "2023",
        "mileage": "9 300 км",
        "location": "Львів",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/2020_BMW_M8_Competition_Coupe_%28F92%29%2C_front_8.15.21.jpg/1280px-2020_BMW_M8_Competition_Coupe_%28F92%29%2C_front_8.15.21.jpg",
        "url": "https://auto.ria.com/uk/search/?brand.id[0]=3&model.id[0]=316&price.USD.gte=110000"
    },
    {
        "title": "Ferrari F8 Tributo 2022",
        "price": "$340 000",
        "year": "2022",
        "mileage": "3 100 км",
        "location": "Київ",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/2020_Ferrari_F8_Tributo%2C_front_8.15.21.jpg/1280px-2020_Ferrari_F8_Tributo%2C_front_8.15.21.jpg",
        "url": "https://auto.ria.com/uk/search/?brand.id[0]=80&price.USD.gte=300000"
    },
    {
        "title": "Lexus LX 600 F Sport 2023",
        "price": "$115 000",
        "year": "2023",
        "mileage": "14 000 км",
        "location": "Одеса",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/ninety/2022_Lexus_LX_600_F_Sport_%28facelift%2C_white%29%2C_front_8.15.21.jpg/1280px-2022_Lexus_LX_600_F_Sport_%28facelift%2C_white%29%2C_front_8.15.21.jpg",
        "url": "https://auto.ria.com/uk/search/?brand.id[0]=28&price.USD.gte=90000"
    },
    {
        "title": "Maserati MC20 2023",
        "price": "$265 000",
        "year": "2023",
        "mileage": "2 800 км",
        "location": "Київ",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Maserati_MC20_%282020%29_-_Frontansicht%2C_5._September_2020%2C_Modena.jpg/1280px-Maserati_MC20_%282020%29_-_Frontansicht%2C_5._September_2020%2C_Modena.jpg",
        "url": "https://auto.ria.com/uk/search/?brand.id[0]=44&price.USD.gte=200000"
    },
    {
        "title": "Bentley Bentayga EWB 2023",
        "price": "$285 000",
        "year": "2023",
        "mileage": "8 100 км",
        "location": "Київ",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Bentley_Bentayga_%282016%29_%2833039081045%29.jpg/1280px-Bentley_Bentayga_%282016%29_%2833039081045%29.jpg",
        "url": "https://auto.ria.com/uk/search/?brand.id[0]=78&price.USD.gte=250000"
    },
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
