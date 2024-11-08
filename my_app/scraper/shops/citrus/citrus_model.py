import re

import requests
from bs4 import BeautifulSoup

from scraper.models import BaseStore, Scraper


class CitrusStore(BaseStore):
    def __init__(self, url):
        super().__init__(shop_url=url)
        self.scraper = Scraper()

    def generate_info(self):
        item_list = []
        for i in range(1, 4):
            response = requests.get(f'https://www.ctrs.com.ua/search/?page={i}&query=wacom')
            soup = BeautifulSoup(response.text, 'lxml')

            all_items = soup.find(class_='catalog-facet')

            for elem in all_items:
                name_elem = elem.find_next(class_='line-clamp-2 break-word MainProductCard-module__title___3fVuF')
                price_elem = elem.find_next(class_='medium MainProductCard-module__price___34KIa')
                status = elem.find_next(class_='df aic pt8 pb8 MainProductCard-module__cashback___wq57O')

                name = name_elem.text.strip() if name_elem else None
                price = price_elem.text.strip('₴').replace(' ', '').strip() if price_elem else None

                if price:
                    price = re.sub(r'\s+', '', price)
                else:
                    continue

                if status:
                    status = 'in_stock'
                else:
                    status = 'not_in_stock'
                card_item = {
                    'name': name,
                    'price': price,
                    'status': status
                }
                item_list.append(card_item)

        return item_list

