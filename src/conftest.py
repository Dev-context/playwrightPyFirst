import pytest
from playwright.sync_api import sync_playwright, Page, Playwright, expect
from page.login.login_page import LoginPage
from utils.helpers import json_reader

@pytest.fixture(scope="session")
def browser_instance(request):
    with sync_playwright() as playwright:
        browser_name = request.config.getoption("--browser_name")
        is_headed = request.config.getoption("--headed").lower() == "true"  # Convert to boolean

        if browser_name == "chrome":
            browser = playwright.chromium.launch(headless=not is_headed)
        elif browser_name == "firefox":
            browser = playwright.firefox.launch(headless=not is_headed)
        elif browser_name == "webkit":
            browser = playwright.webkit.launch(headless=not is_headed)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        context = browser.new_context()  # Create a new browser context
        yield context
        context.close()
        browser.close()

@pytest.fixture()
def set_up(browser_instance):
    page = browser_instance.new_page()
    page.goto("https://rahulshettyacademy.com/client/")
    page.wait_for_load_state("networkidle")
    yield page  # Provide the page for test execution
    page.close()

@pytest.fixture(scope="function")
def json_data():
    return json_reader  # Return the function so it can be used dynamically

@pytest.fixture()
def login(set_up: Page, json_data):
    page = set_up
    login_page = LoginPage(page, json_data("src/page/login/login_locators.json"))
    user_data = json_data("src/date/user.json")
    login_page.login(user_data["user"], user_data["password"])
    expect(page.get_by_role("button", name="Sign Out")).to_be_visible()
    yield page  # Yield logged-in page for further tests

def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chrome")
    parser.addoption("--headed", action="store", default="True")
