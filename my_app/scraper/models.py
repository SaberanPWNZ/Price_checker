import os
import django
from typing import List
import requests
from bs4 import BeautifulSoup
from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "price_checker.settings")


if not settings.configured:
    django.setup()

from items.models import Item

class BaseStore:
    def __init__(self, shop_url, headers=None, cookies=None):
        self.item_list = []
        self.url = shop_url
        self.headers = headers
        self.cookies = cookies
        self.all_items = []

    def get(self, shop_url):
        response = requests.get(url=shop_url, headers=self.headers)
        return response

    def compare_data(self, partner_items_list: List[dict]):
        missing_items = []
        for elem in partner_items_list:
            try:
                article = elem.get('article', '').upper()
                if not article:
                    raise ValueError(f'Article is missing or empty in element: {elem}')
                price_partner = int(elem['price'])

                item = Item.objects.filter(article=article).first()

                if item:
                    item_price = int(item.rrp_price)
                    if price_partner == item_price:
                        missing_items.append(f'✅ {article} - Ціна партнера: {price_partner} грн, РРЦ: {item_price} грн')
                    elif price_partner < item_price:
                        missing_items.append(f'🛑 {article} - Ціна нижча за РРЦ: {price_partner} грн, РРЦ: {item_price} грн')
                    else:
                        missing_items.append(f'⚠️ {article} - Ціна вища за РРЦ: {price_partner} грн, РРЦ: {item_price} грн')
                else:
                    missing_items.append(f'🔍 {article} не знайдено в базі данних')

            except KeyError as e:
                missing_items.append(f'❌ Помилка: Невірний формат данних {elem}, {e}')

            except ValueError as e:
                missing_items.append(f'❌ Помилка: {e}')

            except Exception as e:
                missing_items.append(f'❌ Помилка: розпізнавання данних {article}')

        sorted_items = sorted(missing_items, key=lambda x: (not x.startswith('🛑'), x))
        return sorted_items


class Soup:
    def __init__(self, response):
        self.soup = BeautifulSoup(response.text, 'lxml')

    def find_element(self, **kwargs):
        return self.soup.find(**kwargs)

    def find_all_next(self, **kwargs):
        return self.soup.find_all_next(**kwargs)

    def find_all_elements(self, **kwargs):
        return self.soup.find_all(**kwargs)

    def find_next_element(self, **kwargs):
        return self.soup.find_next(**kwargs)



if __name__ == "__main__":
    store = BaseStore(shop_url='https://ktc.ua/search/?mobile=0&q=wacom&t=df497d188f6e6a5b97c412a28d48fd2b')
    partner_items = [{'article': 'CTL-4100K-N', 'price': 1111}]
    result = store.compare_data(partner_items_list=partner_items)
    print(result)
