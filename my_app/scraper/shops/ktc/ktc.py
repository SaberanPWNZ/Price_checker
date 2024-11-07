import os
import django

from scraper.shops.ktc.ktc_locators import KtcLocator

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "price_checker.settings")
django.setup()

from scraper.shops.ktc.ktc_model import KtcStore
from scraper.shops.ktc.ktc_info import KTC_ARTICLES
from items.models import Item


def start_ktc_wacom():
    ktc = KtcStore(url=KtcLocator.WACOM_PAGE_URL)
    ktc.load_items(container_locator=KtcLocator.CATALOG_GOODS, item_locator=KtcLocator.ITEM_LOOP)
    items = ktc.generate_info(
        price_locator=KtcLocator.ITEM_PRICE,
        status_locator=KtcLocator.ITEM_STATUS,
        title_locator=KtcLocator.ITEM_TITLE
    )
    result = ktc.compare_data(items)
    return result


def start_ktc_xp_pen():
    ktc = KtcStore(url=KtcLocator.XP_PEN_PAGE_URL)
    ktc.load_items(container_locator=KtcLocator.CATALOG_GOODS, item_locator=KtcLocator.ITEM_LOOP)
    items = ktc.generate_info_xp_pen()
    result = ktc.compare_data_xp_pen(partner_items_list=items,
                                     article_dict=KTC_ARTICLES,
                                     model=Item)

    return result


# if __name__ == "__main__":
#
#   print(start_ktc_wacom())
#   print(start_ktc_xp_pen())
