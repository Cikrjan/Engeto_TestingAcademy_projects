import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope='function', autouse=True)
def new_page(request):
    browser_name = request.param
    with sync_playwright() as p:
        browser_type = getattr(p, browser_name)
        browser = browser_type.launch(headless=False)
        page = browser.new_page()
        yield page
        page.close()


@pytest.mark.parametrize("new_page", ["chromium", "firefox", "webkit"], indirect=True)
def test_hover(new_page):
    page =  new_page
    page.goto("https://engeto.cz/")
    title = "Kurzy programování a dalších IT technologií | ENGETO"

    assert page.title() == title
