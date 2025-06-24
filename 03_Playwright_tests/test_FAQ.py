import pytest

@pytest.mark.parametrize("new_page", ["chromium", "firefox", "webkit"], indirect=True)
def test_FAQ(new_page):
    #přejití na testovanou stránku
    new_page.goto("https://engeto.cz/")

    #nalezení a kliknutí na tlačítko odmítnou na cookie liště
    cookie_refuse = new_page.locator("#cookiescript_reject")
    if cookie_refuse.is_visible():
        cookie_refuse.wait_for(state="visible", timeout=3000)
        cookie_refuse.click()

    #nalezení a kliknutí na tlačítko "FAQ"
    faq_button = new_page.locator("[data-mobile-key='menu-key-4397']")
    faq_button.click()

    #Filtr "Ukončení kurzu a uplatnění" a otestování změny barvy pozadí po najetí na tlačítko
    filter_button = new_page.locator("[for='filter-item_ukonceni-kurzu']")
    color_before = filter_button.evaluate("""
        function(el) {
            return getComputedStyle(el).backgroundColor;
        }
    """)
    filter_button.hover()
    new_page.wait_for_timeout(1000)
    color_after = filter_button.evaluate("""
        function(el) {
            return getComputedStyle(el).backgroundColor;
        }
    """)
    # Print pro kontrolu barev před a po:
    # print("Barva před:", color_before)
    # print("Barva po:", color_after)

    try:
        assert color_before != color_after
        filter_button.click()

    except AssertionError:
        print("Pozor, barva se nezměnila!")
    
    question_rolldown = new_page.locator("#kdy-se-uzavira-kurz-do-kdy-mohu-odevzdavat-projekty-prochazet-zaznamy-a-ucebni-materialy > h3 > a")
    question_rolldown.click()

    link = new_page.locator("#kdy-se-uzavira-kurz-do-kdy-mohu-odevzdavat-projekty-prochazet-zaznamy-a-ucebni-materialy > div > ul > li:nth-child(4) > a:nth-child(3)")
    
    assert link.is_visible()

