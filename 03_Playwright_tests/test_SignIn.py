import pytest
from playwright.sync_api import sync_playwright, Page

@pytest.fixture(scope='function', autouse=True)
def page(request):
    browser_name = request.param
    with sync_playwright() as p:
        browser_type = getattr(p, browser_name)
        browser = browser_type.launch(headless=True)
        page = browser.new_page()
        yield page
        page.close()


@pytest.mark.parametrize("page", ["chromium", "firefox", "webkit"], indirect=True)
def test_SignIn(page):
    pass