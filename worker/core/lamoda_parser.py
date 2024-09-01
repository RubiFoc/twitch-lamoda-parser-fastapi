import httpx
from bs4 import BeautifulSoup

from core.mongo import MongoService
from models.lamoda import Product


async def fetch_page(client, category_url, page_number):
    response = await client.get(f"{category_url}?page={page_number}")
    if response.status_code == 200:
        return response.text
    else:
        print(f"Ошибка: Код ответа {response.status_code}")
        return None


async def get_category(category_url: str):
    category = category_url.split('/')
    if len(category[-1]) == 0:
        return category[-2]
    else:
        return category[-1]


async def parse_products(page_content, category):
    mongo_service = MongoService()
    bs = BeautifulSoup(page_content, 'html.parser')
    products = bs.find_all('div', class_='x-product-card__card')
    if not products:
        return False  # Вернуть False, если нет продуктов на странице

    for product in products:
        link = product.find(
            'a', class_='x-product-card__link'
        ).get('href')
        full_link = f"https://www.lamoda.by{link}"
        brand = product.find(
            'div', class_='x-product-card-description__brand-name'
        ).get_text(strip=True)
        product_name = product.find(
            'div', class_='x-product-card-description__product-name'
        ).get_text(strip=True)
        try:
            price = float(product.find(
                'span', class_='x-product-card-description__price-single'
            ).text.replace(' ', '').replace('р.', '').strip())
        except AttributeError:
            price = float(product.find(
                'span', class_='x-product-card-description__price-new'
            ).text.replace(' ', '').replace('р.', '').strip())

        product = Product(name=product_name, brand=brand, link=full_link, price=price)
        mongo_service.insert_document(f'lamoda_{category}', product.dict())

    return True


async def parse_lamoda(category_url):
    category = await get_category(category_url)
    async with httpx.AsyncClient() as client:
        page_number = 1
        while True:
            print(f'Страница {page_number}')
            page_content = await fetch_page(client, category_url, page_number)
            if page_content:
                products_found = await parse_products(page_content, category)
                if not products_found:
                    break
                page_number += 1
            else:
                break
