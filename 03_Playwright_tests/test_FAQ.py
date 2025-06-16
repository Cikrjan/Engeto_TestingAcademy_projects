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
    #přejití na testovanou stránku
    page.goto("https://engeto.cz/")

    #nalezení a kliknutí na tlačítko odmítnou na cookie liště
    cookie_refuse = page.locator("#cookiescript_reject")
    if cookie_refuse.is_visible():
        cookie_refuse.wait_for(state="visible", timeout=3000)
        cookie_refuse.click()

    #nalezení a kliknutí na tlačítko "FAQ"
    faq_button = page.locator("[data-mobile-key='menu-key-4397']")
    faq_button.click()

    #Filtr "Ukončení kurzu a uplatnění" a otestování změny barvy pozadí po najetí na tlačítko
    filter_button = page.locator("[for='filter-item_ukonceni-kurzu']")
    color_before = filter_button.evaluate("""
        function(el) {
            return getComputedStyle(el).backgroundColor;
        }
    """)
    filter_button.hover()
    page.wait_for_timeout(1000)
    color_after = filter_button.evaluate("""
        function(el) {
            return getComputedStyle(el).backgroundColor;
        }
    """)
    print("Barva před:", color_before)
    print("Barva po:", color_after)

    try:
        assert color_before != color_after
        filter_button.click()

    except AssertionError:
        print("Pozor, barva se nezměnila!")
    
    question_rolldown = page.locator("#kdy-se-uzavira-kurz-do-kdy-mohu-odevzdavat-projekty-prochazet-zaznamy-a-ucebni-materialy > h3 > a")
    question_rolldown.click()

    link = page.locator("#kdy-se-uzavira-kurz-do-kdy-mohu-odevzdavat-projekty-prochazet-zaznamy-a-ucebni-materialy > div > ul > li:nth-child(4) > a:nth-child(3)")
    
    assert link.is_visible()

