import pytest
from playwright.sync_api import Page, expect, sync_playwright, Response
from ..utils.helpers import json_reader
from ..page.login.login_page import LoginPage
from conftest import  set_up,json_data



def test_login_success(set_up: set_up,json_data):
    page:Page = set_up
    login = LoginPage(page,json_data("src/page/login/login_locators.json"))
    data=json_reader("src/date/user.json")
    login.login(data["user"], data["password"])
    expect(page.locator("button").filter(has_text="Sign Out")).to_be_visible()

def test_login_unsuccessful(set_up:set_up, json_data):
    page: Page = set_up
    with page.expect_response("**/api/ecom/auth/login") as response:
        login = LoginPage(page,json_data("src/page/login/login_locators.json"))
        login.login("auto_user@mail.com", "@Q123456789")
        res = response.value  # Assigning the response
        assert res.status == 400
        expect(page.locator("div").filter(has_text="Incorrect email or password.").nth(2)).to_be_visible()







