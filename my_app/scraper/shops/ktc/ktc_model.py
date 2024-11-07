from items.models import Item
from scraper.models import BaseStore, Scraper
from scraper.shops.ktc.ktc_locators import KtcLocator


class KtcStore(BaseStore):
    def __init__(self, url):
        super().__init__(shop_url=url)
        self.scraper = Scraper()

    def generate_info_xp_pen(self):
        return self.generate_info(
            title_locator=KtcLocator.ITEM_TITLE,
            price_locator=KtcLocator.ITEM_PRICE,
            status_locator=KtcLocator.ITEM_STATUS
        )
