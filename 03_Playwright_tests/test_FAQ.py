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
def test_FAQ(page):
    #odkliknutí cookie consentu
    page.goto("https://engeto.cz/")

    #nalezení a kliknutí na tlačítko odmítnou na cookie liště
    cookie_refuse = page.locator("#cookiescript_reject")
    if cookie_refuse.is_visible():
        cookie_refuse.wait_for(state="visible", timeout=3000)
        cookie_refuse.click()

    #nalezení a kliknutí na tlačítko "FAQ"
    faq_button = page.locator("[data-mobile-key='menu-key-4397']")
    faq_button.click()

    filter_button = page.locator("[for='filter-item_ukonceni-kurzu']")
    color_before = filter_button.evaluate("""
        function(el) {
            return getComputedStyle(el).backgroundColor;
        }
    """)
    filter_button.hover()
    page.wait_for_timeout(300)
    color_after = filter_button.evaluate("""
        function(el) {
            return getComputedStyle(el).backgroundColor;
        }
    """)
    if color_before == color_after:
        filter_button.click()
    
    filter_subtitle = page.locator("#h-pristup-a-dokonceni-kurzu")

    assert filter_subtitle.is_visible()
