from src.test.conftest import login,json_data
from src.page.dashboard.dashboard_page import Dashboard
from playwright.sync_api import Page


def test_add_item_cart(login, json_data):
        page:Page=login
        dashboard=Dashboard(page, json_data("page/dashboard/dashboard_locators.json"))
        dashboard.get_all_products("ZARA COAT 3")
        assert dashboard.cart_quantity.text_content() == "1"






