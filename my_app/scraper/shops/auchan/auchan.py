import os
import django


from scraper.shops.auchan.auchan_info import AUCHAN_ARTICLES
from scraper.shops.auchan.auchan_locators import AuchanLocator
from scraper.shops.auchan.auchan_model import AuchanStore

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "price_checker.settings")
django.setup()
from items.models import Item


def start_auchan_wacom():
    auchan = AuchanStore(url=AuchanLocator.WACOM_PAGE_URL)

    items = auchan.generate_info()
    result = auchan.compare_data_xp_pen(partner_items_list=items,
                                        article_dict=AUCHAN_ARTICLES,
                                        model=Item)

    return result


if __name__ == "__main__":
    print(start_auchan_wacom())
