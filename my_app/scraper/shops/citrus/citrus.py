import os
import django


from scraper.shops.citrus.citrus_info import CITRUS_ITEMS
from scraper.shops.citrus.citrus_locators import CitrusLocator
from scraper.shops.citrus.citrus_model import CitrusStore

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "price_checker.settings")
django.setup()
from items.models import Item

def start_citrus_wacom():
    citrus = CitrusStore(url=CitrusLocator.WACOM_PAGE_URL)
    items = citrus.generate_info()
    result = citrus.compare_data_xp_pen(
        partner_items_list=items,
        article_dict=CITRUS_ITEMS,
        model=Item
    )
    return result



if __name__ == "__main__":
    print(start_citrus_wacom())