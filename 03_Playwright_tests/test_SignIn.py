import pytest
from playwright.sync_api import sync_playwright, Page

@pytest.fixture(scope='function', autouse=True)
def new_page(request):
    browser_name = request.param
    with sync_playwright() as p:
        browser_type = getattr(p, browser_name)
        browser = browser_type.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        yield page
        page.close()


@pytest.mark.parametrize("new_page", ["chromium", "firefox", "webkit"], indirect=True)
def test_SignIn_Positive(new_page):
    new_page.goto("https://the-internet.herokuapp.com/")

    login_page = new_page.locator("[href='/login']")
    login_page.click()

    user_name = new_page.locator("input#username").fill("tomsmith")
    password = new_page.locator("input#password").fill("SuperSecretPassword!")

    login_button = new_page.locator(".radius")
    login_button.click()

    assert new_page.url == "https://the-internet.herokuapp.com/secure"

