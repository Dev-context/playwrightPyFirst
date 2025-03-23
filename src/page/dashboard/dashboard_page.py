import time

from playwright.sync_api import Page, expect
from utils.helpers import json_reader


class Dashboard:
    def __init__(self, page:Page, json_reader: json_reader):
        self.page = page
        self.product_name_selector = page.locator("h5 b")
        self.add_to_cart_button_selector = page.locator("button:has-text('Add To Cart')")
        self.product_list = page.locator(".row .card")
        self.cart_quantity = page.locator("button:has-text('Cart') label")


    def get_all_products(self, product_name):
     self.page.wait_for_selector("h5 b")
     for elements in self.product_list.all():
         if product_name == elements.locator(self.product_name_selector).text_content():
            with self.page.expect_response("https://rahulshettyacademy.com/api/ecom/user/get-cart-count/**") as res:
                assert res.value.status == 200
                elements.locator(self.add_to_cart_button_selector).click()
            break




