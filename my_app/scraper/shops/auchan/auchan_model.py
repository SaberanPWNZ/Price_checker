import json

from scraper.models import BaseStore, Scraper
from scraper.shops.auchan.auchan_info import AUCHAN_HEADERS
from scraper.shops.auchan.auchan_locators import AuchanLocator
from utillities.utillities import get_article_from_title, clean_price


class AuchanStore(BaseStore):
    def __init__(self, url):
        super().__init__(shop_url=url)
        self.scraper = Scraper()

    def generate_info(self, title_locator=None, price_locator=None, status_locator=None):
        response = self.scraper.get(self.url)
        item_list = []

        try:
            data = json.loads(response.text)
            item_list = []

            for product in data['data']['search']['products']:

                name = product.get('name', '').strip()

                price = product['price']['regularPrice']['amount']['value']
                if product.get('special_price') is not None:
                    price = product['special_price']

                status = product.get('stock_status', '')

                card_item = {
                    'name': name,
                    'price': price,
                    'status': status,
                }

                item_list.append(card_item)

        except Exception as e:
            print(f"Ошибка при обработке данных: {e}")

        return item_list
