import json
import pytest
from playwright.sync_api import sync_playwright, Page
from page.login.login_page import LoginPage
from utils.helpers import json_reader


@pytest.fixture(scope="function")
def set_up():
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=False)
        context=browser.new_context(base_url="https://rahulshettyacademy.com/client/")
        page=context.new_page()
        page.goto("https://rahulshettyacademy.com/client/")
        page.wait_for_load_state("networkidle")
        yield page
        browser.close()
        page.close()


@pytest.fixture(scope="function")
def json_data(json_path=None):
    return  json_reader



@pytest.fixture(scope="session")
def persistent_login(set_up:set_up, json_data):
    page:Page=set_up
    login = LoginPage(page, json_data("src/page/login/login_locators.json"))
    data = json_reader("src/date/user.json")
    login.login(data["user"], data["password"])

    storage=page.evaluate("()=> JSON.stringify(sessionStorage)")
    with open("src/date/session.json") as f:
        f.write(storage)
        yield page.context
        page.context.close()


@pytest.fixture()
def logged_in_page(persistent_login:persistent_login):
    page=persistent_login.new_page()
    try:
        with open("src/date/session.json") as f:
            storage=json.load(f)
            page.evaluate(f"()=>Object.assign(sessionStorage),{storage}")
    except FileExistsError:
        print(FileExistsError)
    yield page
    page.close()