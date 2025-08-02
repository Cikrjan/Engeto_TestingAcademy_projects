import pytest
from playwright.sync_api import sync_playwright
from _pytest.python import Metafunc

@pytest.fixture(scope='function')
def new_page(request):
    browser_name = request.param
    with sync_playwright() as p:
        browser_type = getattr(p, browser_name)
        browser = browser_type.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        yield page
        page.close()

def pytest_generate_tests(metafunc: Metafunc):
    if "new_page" in metafunc.fixturenames:
        metafunc.parametrize("new_page", ["chromium", "firefox", "webkit"], indirect=True)