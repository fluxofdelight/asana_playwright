import json
import pytest

from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture(scope="session")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="session", autouse=True)
def login_to_asana(page):
    with open("../data/login_data.json", "r") as f:
        login_data = json.load(f)

    page.goto(login_data["url"])
    page.fill('input[type="email"]', login_data["email"])
    page.click('form.LoginEmailForm > div[role="button"]')
    page.wait_for_load_state()
    page.is_visible('div.MessageBanner-contents')
    page.fill('input[type="password"]', login_data["password"])
    page.click('form.LoginPasswordForm > div[role="button"]')
    page.wait_for_load_state()
