import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope='function', autouse=True)
def new_page(request):
    browser_name = request.param
    with sync_playwright() as p:
        browser_type = getattr(p, browser_name)
        browser = browser_type.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        yield page
        page.close()